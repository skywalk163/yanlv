"""
并行编译器测试

测试ParallelCompiler的功能
"""

import pytest
import time
from yanlv.parallel_compiler import (
    DependencyGraph, 
    ParallelCompiler,
    CompilationTask,
    CompilationResult,
    get_global_parallel_compiler
)


class TestDependencyGraph:
    """DependencyGraph测试类"""
    
    def test_graph_initialization(self):
        """测试依赖图初始化"""
        graph = DependencyGraph()
        assert len(graph.graph) == 0
    
    def test_graph_add_file(self):
        """测试添加文件"""
        graph = DependencyGraph()
        
        graph.add_file("a.yanlv", [])
        graph.add_file("b.yanlv", ["a.yanlv"])
        
        assert "a.yanlv" in graph.graph
        assert "b.yanlv" in graph.graph
        assert graph.graph["b.yanlv"] == ["a.yanlv"]
    
    def test_graph_topological_sort(self):
        """测试拓扑排序"""
        graph = DependencyGraph()
        
        # a -> b -> c
        graph.add_file("a.yanlv", [])
        graph.add_file("b.yanlv", ["a.yanlv"])
        graph.add_file("c.yanlv", ["b.yanlv"])
        
        order = graph.topological_sort()
        
        # a应该在b之前,b应该在c之前
        assert order.index("a.yanlv") < order.index("b.yanlv")
        assert order.index("b.yanlv") < order.index("c.yanlv")
    
    def test_graph_compilation_order(self):
        """测试编译顺序(分层)"""
        graph = DependencyGraph()
        
        # a, b 无依赖
        # c 依赖 a, b
        graph.add_file("a.yanlv", [])
        graph.add_file("b.yanlv", [])
        graph.add_file("c.yanlv", ["a.yanlv", "b.yanlv"])
        
        layers = graph.get_compilation_order()
        
        # 第一层应该包含a和b
        assert "a.yanlv" in layers[0] or "b.yanlv" in layers[0]
        # 第二层应该包含c
        assert "c.yanlv" in layers[1]
    
    def test_graph_circular_dependency(self):
        """测试循环依赖检测"""
        graph = DependencyGraph()
        
        # a -> b -> a (循环)
        graph.add_file("a.yanlv", ["b.yanlv"])
        graph.add_file("b.yanlv", ["a.yanlv"])
        
        with pytest.raises(ValueError, match="循环依赖"):
            graph.get_compilation_order()


class TestParallelCompiler:
    """ParallelCompiler测试类"""
    
    def test_compiler_initialization(self):
        """测试编译器初始化"""
        compiler = ParallelCompiler(max_workers=4)
        assert compiler.max_workers == 4
    
    def test_compiler_single_task(self):
        """测试单个编译任务"""
        compiler = ParallelCompiler()
        
        def simple_compiler(file_path: str, content: str):
            return f"compiled: {file_path}"
        
        task = CompilationTask(file_path="test.yanlv", content="测试内容")
        result = compiler.compile_single(task, simple_compiler)
        
        assert result.success
        assert result.output == "compiled: test.yanlv"
    
    def test_compiler_single_task_error(self):
        """测试单个编译任务错误"""
        compiler = ParallelCompiler()
        
        def error_compiler(file_path: str, content: str):
            raise ValueError("编译错误")
        
        task = CompilationTask(file_path="test.yanlv", content="测试内容")
        result = compiler.compile_single(task, error_compiler)
        
        assert not result.success
        assert "编译错误" in result.error
    
    def test_compiler_parallel_no_dependencies(self):
        """测试无依赖的并行编译"""
        compiler = ParallelCompiler(max_workers=4)
        
        call_count = 0
        
        def simple_compiler(file_path: str, content: str):
            nonlocal call_count
            call_count += 1
            time.sleep(0.01)  # 模拟编译时间
            return f"compiled: {file_path}"
        
        tasks = [
            CompilationTask(file_path=f"file{i}.yanlv", content=f"内容{i}")
            for i in range(10)
        ]
        
        results = compiler.compile_parallel(tasks, simple_compiler)
        
        # 所有任务应该成功
        assert len(results) == 10
        assert all(r.success for r in results.values())
        
        stats = compiler.get_stats()
        assert stats.total_tasks == 10
        assert stats.completed_tasks == 10
        assert stats.failed_tasks == 0
    
    def test_compiler_parallel_with_dependencies(self):
        """测试有依赖的并行编译"""
        compiler = ParallelCompiler(max_workers=4)
        
        compile_order = []
        
        def tracking_compiler(file_path: str, content: str):
            compile_order.append(file_path)
            time.sleep(0.01)
            return f"compiled: {file_path}"
        
        tasks = [
            CompilationTask(file_path="a.yanlv", content="a", dependencies=[]),
            CompilationTask(file_path="b.yanlv", content="b", dependencies=["a.yanlv"]),
            CompilationTask(file_path="c.yanlv", content="c", dependencies=["a.yanlv"]),
            CompilationTask(file_path="d.yanlv", content="d", dependencies=["b.yanlv", "c.yanlv"])
        ]
        
        results = compiler.compile_parallel(tasks, tracking_compiler)
        
        # 所有任务应该成功
        assert all(r.success for r in results.values())
        
        # a应该在b和c之前
        assert compile_order.index("a.yanlv") < compile_order.index("b.yanlv")
        assert compile_order.index("a.yanlv") < compile_order.index("c.yanlv")
        
        # b和c应该在d之前
        assert compile_order.index("b.yanlv") < compile_order.index("d.yanlv")
        assert compile_order.index("c.yanlv") < compile_order.index("d.yanlv")
    
    def test_compiler_batch(self):
        """测试批量编译"""
        compiler = ParallelCompiler()
        
        def simple_compiler(file_path: str, content: str):
            return len(content)
        
        file_contents = {
            "file1.yanlv": "内容1",
            "file2.yanlv": "内容22",
            "file3.yanlv": "内容333"
        }
        
        results = compiler.compile_batch(file_contents, simple_compiler)
        
        assert len(results) == 3
        assert results["file1.yanlv"].output == 3
        assert results["file2.yanlv"].output == 4
        assert results["file3.yanlv"].output == 5


class TestParallelPerformance:
    """并行编译性能测试"""
    
    def test_parallel_speedup(self):
        """测试并行加速"""
        # 串行编译
        def slow_compiler(file_path: str, content: str):
            time.sleep(0.1)  # 模拟耗时编译
            return f"compiled: {file_path}"
        
        tasks = [
            CompilationTask(file_path=f"file{i}.yanlv", content=f"内容{i}")
            for i in range(8)
        ]
        
        # 串行
        start = time.time()
        for task in tasks:
            slow_compiler(task.file_path, task.content)
        serial_time = time.time() - start
        
        # 并行
        compiler = ParallelCompiler(max_workers=4)
        start = time.time()
        compiler.compile_parallel(tasks, slow_compiler)
        parallel_time = time.time() - start
        
        stats = compiler.get_stats()
        
        print(f"\n并行编译性能测试:")
        print(f"串行时间: {serial_time*1000:.2f}ms")
        print(f"并行时间: {parallel_time*1000:.2f}ms")
        print(f"加速比: {stats.speedup:.2f}x")
        
        # 并行应该比串行快
        assert parallel_time < serial_time
        assert stats.speedup > 1.0


class TestGlobalCompiler:
    """全局编译器测试"""
    
    def test_get_global_compiler(self):
        """测试获取全局编译器"""
        compiler1 = get_global_parallel_compiler()
        compiler2 = get_global_parallel_compiler()
        
        # 应该是同一个实例
        assert compiler1 is compiler2


if __name__ == '__main__':
    pytest.main([__file__, '-v', '-s'])
