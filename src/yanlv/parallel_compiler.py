"""
言律语言并行编译支持

实现多文件并行编译,提升大规模项目编译速度
"""

from typing import List, Dict, Any, Optional, Callable
from dataclasses import dataclass, field
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, Future
import threading
import time
import os


@dataclass
class CompilationTask:
    """编译任务"""
    file_path: str                 # 文件路径
    content: str                   # 文件内容
    priority: int = 0              # 优先级(数字越小优先级越高)
    dependencies: List[str] = field(default_factory=list)  # 依赖文件列表


@dataclass
class CompilationResult:
    """编译结果"""
    file_path: str                 # 文件路径
    success: bool                  # 是否成功
    output: Any = None             # 编译输出
    error: Optional[str] = None    # 错误信息
    time: float = 0.0              # 编译时间(毫秒)


@dataclass
class ParallelStats:
    """并行编译统计信息"""
    total_tasks: int = 0           # 总任务数
    completed_tasks: int = 0       # 已完成任务数
    failed_tasks: int = 0          # 失败任务数
    total_time: float = 0.0        # 总编译时间(毫秒)
    parallel_time: float = 0.0     # 并行编译时间(毫秒)
    
    @property
    def speedup(self) -> float:
        """加速比"""
        return self.total_time / self.parallel_time if self.parallel_time > 0 else 1.0
    
    @property
    def success_rate(self) -> float:
        """成功率"""
        return self.completed_tasks / self.total_tasks if self.total_tasks > 0 else 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'total_tasks': self.total_tasks,
            'completed_tasks': self.completed_tasks,
            'failed_tasks': self.failed_tasks,
            'success_rate': f"{self.success_rate:.2%}",
            'total_time_ms': f"{self.total_time:.2f}",
            'parallel_time_ms': f"{self.parallel_time:.2f}",
            'speedup': f"{self.speedup:.2f}x"
        }


class DependencyGraph:
    """
    依赖图
    
    管理文件之间的依赖关系,支持拓扑排序
    """
    
    def __init__(self):
        """初始化依赖图"""
        self.graph: Dict[str, List[str]] = {}  # 文件 -> 依赖列表
        self.reverse_graph: Dict[str, List[str]] = {}  # 文件 -> 被依赖列表
    
    def add_file(self, file_path: str, dependencies: List[str] = None) -> None:
        """
        添加文件及其依赖
        
        Args:
            file_path: 文件路径
            dependencies: 依赖文件列表
        """
        self.graph[file_path] = dependencies or []
        
        # 更新反向图
        for dep in (dependencies or []):
            if dep not in self.reverse_graph:
                self.reverse_graph[dep] = []
            self.reverse_graph[dep].append(file_path)
    
    def topological_sort(self) -> List[str]:
        """
        拓扑排序
        
        Returns:
            排序后的文件列表(依赖优先)
        """
        visited = set()
        result = []
        
        def visit(file_path: str):
            if file_path in visited:
                return
            visited.add(file_path)
            
            # 先访问依赖
            for dep in self.graph.get(file_path, []):
                visit(dep)
            
            result.append(file_path)
        
        # 访问所有文件
        for file_path in self.graph:
            visit(file_path)
        
        return result
    
    def get_compilation_order(self) -> List[List[str]]:
        """
        获取编译顺序(分层)
        
        Returns:
            分层的文件列表,每层可以并行编译
        """
        # 计算入度
        in_degree = {file: 0 for file in self.graph}
        for file, deps in self.graph.items():
            for dep in deps:
                if dep in in_degree:
                    in_degree[file] += 1
        
        layers = []
        remaining = set(self.graph.keys())
        
        while remaining:
            # 找出入度为0的文件
            layer = [f for f in remaining if in_degree[f] == 0]
            
            if not layer:
                # 存在循环依赖
                raise ValueError("检测到循环依赖")
            
            layers.append(layer)
            
            # 移除当前层,更新入度
            for file in layer:
                remaining.remove(file)
                for dependent in self.reverse_graph.get(file, []):
                    if dependent in in_degree:
                        in_degree[dependent] -= 1
        
        return layers


class ParallelCompiler:
    """
    并行编译器
    
    支持多文件并行编译,自动处理依赖关系
    """
    
    def __init__(
        self, 
        max_workers: int = None,
        use_processes: bool = False
    ):
        """
        初始化并行编译器
        
        Args:
            max_workers: 最大工作线程/进程数
            use_processes: 是否使用进程池(默认使用线程池)
        """
        self.max_workers = max_workers or os.cpu_count() or 4
        self.use_processes = use_processes
        self.stats = ParallelStats()
        self._lock = threading.Lock()
        self._results: Dict[str, CompilationResult] = {}
    
    def compile_single(
        self, 
        task: CompilationTask,
        compiler: Callable[[str, str], Any]
    ) -> CompilationResult:
        """
        编译单个文件
        
        Args:
            task: 编译任务
            compiler: 编译函数
            
        Returns:
            编译结果
        """
        start_time = time.time()
        
        try:
            output = compiler(task.file_path, task.content)
            elapsed = (time.time() - start_time) * 1000
            
            return CompilationResult(
                file_path=task.file_path,
                success=True,
                output=output,
                time=elapsed
            )
        except Exception as e:
            elapsed = (time.time() - start_time) * 1000
            
            return CompilationResult(
                file_path=task.file_path,
                success=False,
                error=str(e),
                time=elapsed
            )
    
    def compile_parallel(
        self,
        tasks: List[CompilationTask],
        compiler: Callable[[str, str], Any]
    ) -> Dict[str, CompilationResult]:
        """
        并行编译多个文件
        
        Args:
            tasks: 编译任务列表
            compiler: 编译函数
            
        Returns:
            文件路径 -> 编译结果的映射
        """
        start_time = time.time()
        
        # 构建依赖图
        dep_graph = DependencyGraph()
        for task in tasks:
            dep_graph.add_file(task.file_path, task.dependencies)
        
        # 获取编译顺序
        try:
            layers = dep_graph.get_compilation_order()
        except ValueError as e:
            # 循环依赖,按顺序编译
            layers = [[task.file_path for task in tasks]]
        
        # 初始化统计
        self.stats = ParallelStats(total_tasks=len(tasks))
        self._results = {}
        
        # 创建执行器
        Executor = ProcessPoolExecutor if self.use_processes else ThreadPoolExecutor
        
        with Executor(max_workers=self.max_workers) as executor:
            # 按层编译
            for layer in layers:
                futures: Dict[str, Future] = {}
                
                # 提交当前层的所有任务
                for file_path in layer:
                    task = next((t for t in tasks if t.file_path == file_path), None)
                    if task:
                        future = executor.submit(
                            self.compile_single, 
                            task, 
                            compiler
                        )
                        futures[file_path] = future
                
                # 等待当前层完成
                for file_path, future in futures.items():
                    result = future.result()
                    
                    with self._lock:
                        self._results[file_path] = result
                        self.stats.completed_tasks += 1
                        
                        if not result.success:
                            self.stats.failed_tasks += 1
                        
                        self.stats.total_time += result.time
        
        # 计算并行时间
        self.stats.parallel_time = (time.time() - start_time) * 1000
        
        return self._results
    
    def compile_batch(
        self,
        file_contents: Dict[str, str],
        compiler: Callable[[str, str], Any],
        dependencies: Dict[str, List[str]] = None
    ) -> Dict[str, CompilationResult]:
        """
        批量编译文件
        
        Args:
            file_contents: 文件路径 -> 内容的映射
            compiler: 编译函数
            dependencies: 文件路径 -> 依赖列表的映射
            
        Returns:
            文件路径 -> 编译结果的映射
        """
        tasks = [
            CompilationTask(
                file_path=file_path,
                content=content,
                dependencies=(dependencies or {}).get(file_path, [])
            )
            for file_path, content in file_contents.items()
        ]
        
        return self.compile_parallel(tasks, compiler)
    
    def get_stats(self) -> ParallelStats:
        """获取统计信息"""
        return self.stats
    
    def get_results(self) -> Dict[str, CompilationResult]:
        """获取编译结果"""
        return self._results
    
    def get_failed_files(self) -> List[str]:
        """获取失败的文件列表"""
        return [
            file_path for file_path, result in self._results.items()
            if not result.success
        ]
    
    def get_successful_files(self) -> List[str]:
        """获取成功的文件列表"""
        return [
            file_path for file_path, result in self._results.items()
            if result.success
        ]


# 全局并行编译器实例
_global_compiler: Optional[ParallelCompiler] = None


def get_global_parallel_compiler() -> ParallelCompiler:
    """获取全局并行编译器"""
    global _global_compiler
    if _global_compiler is None:
        _global_compiler = ParallelCompiler()
    return _global_compiler
