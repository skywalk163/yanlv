"""
言律语言性能优化模块

提供词法分析、语法分析和代码生成的性能优化
"""

import time
import functools
from typing import List, Dict, Any, Callable, Optional
from dataclasses import dataclass, field


@dataclass
class PerformanceMetrics:
    """性能指标"""
    operation: str
    duration: float
    input_size: int
    throughput: float = 0.0
    
    def __post_init__(self):
        if self.input_size > 0 and self.duration > 0:
            self.throughput = self.input_size / self.duration


class PerformanceMonitor:
    """性能监控器"""
    
    def __init__(self):
        """初始化监控器"""
        self.metrics: List[PerformanceMetrics] = []
        self.enabled = True
    
    def measure(self, operation: str) -> 'PerformanceContext':
        """创建性能测量上下文"""
        return PerformanceContext(self, operation)
    
    def record(self, metric: PerformanceMetrics):
        """记录性能指标"""
        if self.enabled:
            self.metrics.append(metric)
    
    def get_summary(self) -> Dict[str, Any]:
        """获取性能摘要"""
        if not self.metrics:
            return {}
        
        summary = {}
        for metric in self.metrics:
            op = metric.operation
            if op not in summary:
                summary[op] = {
                    'count': 0,
                    'total_time': 0.0,
                    'avg_time': 0.0,
                    'total_size': 0,
                    'avg_throughput': 0.0
                }
            
            summary[op]['count'] += 1
            summary[op]['total_time'] += metric.duration
            summary[op]['total_size'] += metric.input_size
        
        # 计算平均值
        for op in summary:
            count = summary[op]['count']
            summary[op]['avg_time'] = summary[op]['total_time'] / count
            if summary[op]['total_time'] > 0:
                summary[op]['avg_throughput'] = summary[op]['total_size'] / summary[op]['total_time']
        
        return summary


class PerformanceContext:
    """性能测量上下文"""
    
    def __init__(self, monitor: PerformanceMonitor, operation: str):
        """初始化上下文"""
        self.monitor = monitor
        self.operation = operation
        self.start_time = 0.0
        self.input_size = 0
    
    def __enter__(self):
        """进入上下文"""
        self.start_time = time.time()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """退出上下文"""
        duration = time.time() - self.start_time
        metric = PerformanceMetrics(
            operation=self.operation,
            duration=duration,
            input_size=self.input_size
        )
        self.monitor.record(metric)
        return False
    
    def set_input_size(self, size: int):
        """设置输入大小"""
        self.input_size = size


# ============================================================================
# 缓存装饰器
# ============================================================================

def cached(maxsize: int = 128):
    """
    缓存装饰器
    
    Args:
        maxsize: 最大缓存数量
    """
    return functools.lru_cache(maxsize=maxsize)


def memoize(func: Callable) -> Callable:
    """
    记忆化装饰器
    
    Args:
        func: 要优化的函数
        
    Returns:
        优化后的函数
    """
    cache = {}
    
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # 创建缓存键
        key = (args, frozenset(kwargs.items()))
        
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        
        return cache[key]
    
    return wrapper


# ============================================================================
# 词法分析优化
# ============================================================================

class OptimizedLexer:
    """优化的词法分析器"""
    
    def __init__(self):
        """初始化优化词法分析器"""
        # 预编译正则表达式
        self._keyword_cache = {}
        self._token_cache = {}
    
    @cached(maxsize=256)
    def _is_keyword(self, word: str) -> bool:
        """
        检查是否是关键字（带缓存）
        
        Args:
            word: 要检查的单词
            
        Returns:
            是否是关键字
        """
        keywords = {
            '定义', '变量', '数组', '函数', '参数', '调用', '返回',
            '如果', '否则', '当', '循环', '执行', '结束',
            '输出', '设置', '添加', '删除', '长度',
            '尝试', '捕获', '抛出', '异常', '最终',
            '模块', '导入', '导出', '从', '为'
        }
        return word in keywords
    
    def tokenize_optimized(self, source: str) -> List[Any]:
        """
        优化的词法分析
        
        Args:
            source: 源代码
            
        Returns:
            Token列表
        """
        # 使用缓存
        if source in self._token_cache:
            return self._token_cache[source]
        
        # 执行词法分析
        tokens = self._tokenize_fast(source)
        
        # 缓存结果
        if len(source) < 10000:  # 只缓存小文件
            self._token_cache[source] = tokens
        
        return tokens
    
    def _tokenize_fast(self, source: str) -> List[Any]:
        """快速词法分析"""
        tokens = []
        lines = source.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            # 快速处理每行
            words = line.split()
            for col_num, word in enumerate(words, 1):
                # 简化的token创建
                tokens.append({
                    'value': word,
                    'line': line_num,
                    'column': col_num,
                    'is_keyword': self._is_keyword(word)
                })
        
        return tokens


# ============================================================================
# 语法分析优化
# ============================================================================

class OptimizedParser:
    """优化的语法分析器"""
    
    def __init__(self):
        """初始化优化语法分析器"""
        self._ast_cache = {}
    
    @memoize
    def _get_precedence(self, operator: str) -> int:
        """
        获取运算符优先级（带记忆化）
        
        Args:
            operator: 运算符
            
        Returns:
            优先级
        """
        precedence = {
            '或': 1,
            '且': 2,
            '==': 3, '!=': 3, '等于': 3, '不等于': 3,
            '<': 4, '>': 4, '<=': 4, '>=': 4,
            '小于': 4, '大于': 4, '小于等于': 4, '大于等于': 4,
            '+': 5, '-': 5, '加': 5, '减': 5,
            '*': 6, '/': 6, '%': 6, '乘': 6, '除': 6, '取余': 6,
            '^': 7, '幂': 7,
        }
        return precedence.get(operator, 0)
    
    def parse_optimized(self, tokens: List[Any]) -> Any:
        """
        优化的语法分析
        
        Args:
            tokens: Token列表
            
        Returns:
            AST
        """
        # 使用缓存
        cache_key = tuple(t['value'] for t in tokens)
        if cache_key in self._ast_cache:
            return self._ast_cache[cache_key]
        
        # 执行语法分析
        ast = self._parse_fast(tokens)
        
        # 缓存结果
        if len(tokens) < 1000:  # 只缓存小规模
            self._ast_cache[cache_key] = ast
        
        return ast
    
    def _parse_fast(self, tokens: List[Any]) -> Any:
        """快速语法分析"""
        # 简化的AST构建
        return {
            'type': 'Program',
            'statements': [
                {'type': 'Expression', 'value': t['value']}
                for t in tokens
            ]
        }


# ============================================================================
# 代码生成优化
# ============================================================================

class OptimizedCodeGenerator:
    """优化的代码生成器"""
    
    def __init__(self):
        """初始化优化代码生成器"""
        self._code_cache = {}
        self._template_cache = {}
    
    @cached(maxsize=64)
    def _get_template(self, node_type: str) -> str:
        """
        获取代码模板（带缓存）
        
        Args:
            node_type: 节点类型
            
        Returns:
            代码模板
        """
        templates = {
            'VariableDeclaration': 'let {name} = {value};',
            'FunctionDeclaration': 'function {name}({params}) {{\n{body}\n}}',
            'IfStatement': 'if ({condition}) {{\n{consequent}\n}}',
            'WhileStatement': 'while ({condition}) {{\n{body}\n}}',
            'OutputStatement': 'console.log({value});',
            'BinaryExpression': '({left} {operator} {right})',
        }
        return templates.get(node_type, '{value}')
    
    def generate_optimized(self, ast: Any) -> str:
        """
        优化的代码生成
        
        Args:
            ast: AST
            
        Returns:
            生成的代码
        """
        # 使用缓存
        cache_key = str(ast)
        if cache_key in self._code_cache:
            return self._code_cache[cache_key]
        
        # 执行代码生成
        code = self._generate_fast(ast)
        
        # 缓存结果
        if len(code) < 10000:  # 只缓存小规模
            self._code_cache[cache_key] = code
        
        return code
    
    def _generate_fast(self, ast: Any) -> str:
        """快速代码生成"""
        # 简化的代码生成
        if isinstance(ast, dict):
            if ast.get('type') == 'Program':
                return '\n'.join(
                    self._generate_fast(stmt)
                    for stmt in ast.get('statements', [])
                )
            else:
                return str(ast.get('value', ''))
        
        return str(ast)


# ============================================================================
# 批处理优化
# ============================================================================

class BatchProcessor:
    """批处理器"""
    
    def __init__(self, batch_size: int = 100):
        """
        初始化批处理器
        
        Args:
            batch_size: 批处理大小
        """
        self.batch_size = batch_size
    
    def process_batch(self, items: List[Any], 
                     processor: Callable[[Any], Any]) -> List[Any]:
        """
        批处理
        
        Args:
            items: 要处理的项
            processor: 处理函数
            
        Returns:
            处理结果列表
        """
        results = []
        
        for i in range(0, len(items), self.batch_size):
            batch = items[i:i + self.batch_size]
            batch_results = [processor(item) for item in batch]
            results.extend(batch_results)
        
        return results


# ============================================================================
# 辅助函数
# ============================================================================

def create_performance_monitor() -> PerformanceMonitor:
    """创建性能监控器"""
    return PerformanceMonitor()


def create_optimized_lexer() -> OptimizedLexer:
    """创建优化词法分析器"""
    return OptimizedLexer()


def create_optimized_parser() -> OptimizedParser:
    """创建优化语法分析器"""
    return OptimizedParser()


def create_optimized_generator() -> OptimizedCodeGenerator:
    """创建优化代码生成器"""
    return OptimizedCodeGenerator()


# ============================================================================
# 导出
# ============================================================================

__all__ = [
    'PerformanceMetrics',
    'PerformanceMonitor',
    'PerformanceContext',
    'cached',
    'memoize',
    'OptimizedLexer',
    'OptimizedParser',
    'OptimizedCodeGenerator',
    'BatchProcessor',
    'create_performance_monitor',
    'create_optimized_lexer',
    'create_optimized_parser',
    'create_optimized_generator',
]
