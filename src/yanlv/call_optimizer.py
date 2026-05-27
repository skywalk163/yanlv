"""
言律语言函数调用优化器

实现优化的函数调用机制,包括内联缓存、分发表优化和记忆化
"""

from typing import Dict, Any, Optional, Callable, List, Tuple
from dataclasses import dataclass, field
import time
import hashlib


@dataclass
class CallStats:
    """函数调用统计信息"""
    total_calls: int = 0           # 总调用次数
    cache_hits: int = 0            # 缓存命中次数
    cache_misses: int = 0          # 缓存未命中次数
    total_time: float = 0.0        # 总调用时间(毫秒)
    memoized_calls: int = 0        # 记忆化调用次数
    
    @property
    def cache_hit_rate(self) -> float:
        """缓存命中率"""
        total = self.cache_hits + self.cache_misses
        return self.cache_hits / total if total > 0 else 0.0
    
    @property
    def average_time(self) -> float:
        """平均调用时间(微秒)"""
        return (self.total_time * 1000) / self.total_calls if self.total_calls > 0 else 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'total_calls': self.total_calls,
            'cache_hits': self.cache_hits,
            'cache_misses': self.cache_misses,
            'cache_hit_rate': f"{self.cache_hit_rate:.2%}",
            'memoized_calls': self.memoized_calls,
            'average_time_us': f"{self.average_time:.2f}μs"
        }


@dataclass
class FunctionInfo:
    """函数信息"""
    name: str                      # 函数名
    params: List[str]              # 参数列表
    body: Any                      # 函数体
    is_pure: bool = False          # 是否为纯函数
    call_count: int = 0            # 调用次数
    total_time: float = 0.0        # 总执行时间


class InlineCache:
    """
    内联缓存
    
    缓存函数调用的结果,避免重复计算
    """
    
    def __init__(self, max_size: int = 1000):
        """
        初始化内联缓存
        
        Args:
            max_size: 最大缓存大小
        """
        self.cache: Dict[str, Any] = {}
        self.max_size = max_size
        self.hits = 0
        self.misses = 0
    
    def _compute_key(self, func_name: str, args: Tuple, kwargs: Dict) -> str:
        """
        计算缓存键
        
        Args:
            func_name: 函数名
            args: 位置参数
            kwargs: 关键字参数
            
        Returns:
            缓存键
        """
        # 将参数转换为可哈希的字符串
        key_parts = [func_name]
        key_parts.extend(str(arg) for arg in args)
        key_parts.extend(f"{k}={v}" for k, v in sorted(kwargs.items()))
        
        key_str = "|".join(key_parts)
        return hashlib.md5(key_str.encode()).hexdigest()
    
    def get(self, func_name: str, args: Tuple, kwargs: Dict) -> Optional[Any]:
        """
        从缓存获取结果
        
        Args:
            func_name: 函数名
            args: 位置参数
            kwargs: 关键字参数
            
        Returns:
            缓存的结果(如果存在)
        """
        key = self._compute_key(func_name, args, kwargs)
        
        if key in self.cache:
            self.hits += 1
            return self.cache[key]
        
        self.misses += 1
        return None
    
    def put(self, func_name: str, args: Tuple, kwargs: Dict, result: Any) -> None:
        """
        将结果存入缓存
        
        Args:
            func_name: 函数名
            args: 位置参数
            kwargs: 关键字参数
            result: 结果
        """
        if len(self.cache) >= self.max_size:
            # 简单的LRU: 删除一半的缓存
            keys_to_remove = list(self.cache.keys())[:self.max_size // 2]
            for key in keys_to_remove:
                del self.cache[key]
        
        key = self._compute_key(func_name, args, kwargs)
        self.cache[key] = result
    
    def clear(self) -> None:
        """清空缓存"""
        self.cache.clear()
        self.hits = 0
        self.misses = 0
    
    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        total = self.hits + self.misses
        return {
            'size': len(self.cache),
            'max_size': self.max_size,
            'hits': self.hits,
            'misses': self.misses,
            'hit_rate': self.hits / total if total > 0 else 0.0
        }


class DispatchTable:
    """
    分发表
    
    优化函数查找和调度的数据结构
    """
    
    def __init__(self):
        """初始化分发表"""
        self.table: Dict[str, FunctionInfo] = {}
        self._lookup_cache: Dict[str, FunctionInfo] = {}
    
    def register(self, name: str, params: List[str], body: Any, is_pure: bool = False) -> None:
        """
        注册函数
        
        Args:
            name: 函数名
            params: 参数列表
            body: 函数体
            is_pure: 是否为纯函数
        """
        func_info = FunctionInfo(
            name=name,
            params=params,
            body=body,
            is_pure=is_pure
        )
        self.table[name] = func_info
    
    def lookup(self, name: str) -> Optional[FunctionInfo]:
        """
        查找函数
        
        Args:
            name: 函数名
            
        Returns:
            函数信息(如果存在)
        """
        # 先查缓存
        if name in self._lookup_cache:
            return self._lookup_cache[name]
        
        # 查表
        if name in self.table:
            func_info = self.table[name]
            self._lookup_cache[name] = func_info
            return func_info
        
        return None
    
    def update_stats(self, name: str, exec_time: float) -> None:
        """
        更新函数统计信息
        
        Args:
            name: 函数名
            exec_time: 执行时间(毫秒)
        """
        if name in self.table:
            self.table[name].call_count += 1
            self.table[name].total_time += exec_time
    
    def get_hot_functions(self, threshold: int = 10) -> List[str]:
        """
        获取热点函数
        
        Args:
            threshold: 调用次数阈值
            
        Returns:
            热点函数名列表
        """
        return [
            name for name, info in self.table.items()
            if info.call_count >= threshold
        ]
    
    def clear_cache(self) -> None:
        """清空查找缓存"""
        self._lookup_cache.clear()


class OptimizedCallOptimizer:
    """
    优化的函数调用优化器
    
    管理函数调用优化,包括内联缓存、分发表和记忆化
    """
    
    def __init__(self, enable_cache: bool = True, cache_size: int = 1000):
        """
        初始化函数调用优化器
        
        Args:
            enable_cache: 是否启用缓存
            cache_size: 缓存大小
        """
        self.dispatch_table = DispatchTable()
        self.inline_cache = InlineCache(cache_size) if enable_cache else None
        self.stats = CallStats()
        self._enable_cache = enable_cache
        self._memoized_functions: set = set()  # 记忆化函数集合
    
    def register_function(
        self, 
        name: str, 
        params: List[str], 
        body: Any, 
        is_pure: bool = False,
        memoize: bool = False
    ) -> None:
        """
        注册函数
        
        Args:
            name: 函数名
            params: 参数列表
            body: 函数体
            is_pure: 是否为纯函数
            memoize: 是否启用记忆化
        """
        self.dispatch_table.register(name, params, body, is_pure)
        
        if memoize:
            self._memoized_functions.add(name)
    
    def call(
        self, 
        name: str, 
        args: Tuple, 
        kwargs: Dict,
        executor: Callable
    ) -> Any:
        """
        调用函数(带优化)
        
        Args:
            name: 函数名
            args: 位置参数
            kwargs: 关键字参数
            executor: 实际执行函数
            
        Returns:
            函数结果
        """
        start_time = time.time()
        self.stats.total_calls += 1
        
        # 查找函数
        func_info = self.dispatch_table.lookup(name)
        if func_info is None:
            raise NameError(f"未定义的函数: {name}")
        
        # 尝试从缓存获取(仅对纯函数或记忆化函数)
        if self._enable_cache and (func_info.is_pure or name in self._memoized_functions):
            cached_result = self.inline_cache.get(name, args, kwargs)
            if cached_result is not None:
                self.stats.cache_hits += 1
                if name in self._memoized_functions:
                    self.stats.memoized_calls += 1
                return cached_result
        
        self.stats.cache_misses += 1
        
        # 执行函数
        result = executor(func_info, args, kwargs)
        
        # 缓存结果
        if self._enable_cache and (func_info.is_pure or name in self._memoized_functions):
            self.inline_cache.put(name, args, kwargs, result)
        
        # 更新统计
        exec_time = (time.time() - start_time) * 1000
        self.stats.total_time += exec_time
        self.dispatch_table.update_stats(name, exec_time)
        
        return result
    
    def get_stats(self) -> CallStats:
        """获取统计信息"""
        return self.stats
    
    def reset_stats(self) -> None:
        """重置统计信息"""
        self.stats = CallStats()
    
    def clear_cache(self) -> None:
        """清空所有缓存"""
        if self.inline_cache:
            self.inline_cache.clear()
        self.dispatch_table.clear_cache()
    
    def enable_cache(self) -> None:
        """启用缓存"""
        self._enable_cache = True
        if self.inline_cache is None:
            self.inline_cache = InlineCache()
    
    def disable_cache(self) -> None:
        """禁用缓存"""
        self._enable_cache = False
        if self.inline_cache:
            self.inline_cache.clear()
    
    def get_hot_functions(self, threshold: int = 10) -> List[str]:
        """获取热点函数"""
        return self.dispatch_table.get_hot_functions(threshold)
    
    def get_function_info(self, name: str) -> Optional[FunctionInfo]:
        """获取函数信息"""
        return self.dispatch_table.lookup(name)
    
    def __repr__(self) -> str:
        return (
            f"OptimizedCallOptimizer("
            f"functions={len(self.dispatch_table.table)}, "
            f"cache_hit_rate={self.stats.cache_hit_rate:.2%})"
        )


# 全局函数调用优化器实例
_global_optimizer: Optional[OptimizedCallOptimizer] = None


def get_global_call_optimizer() -> OptimizedCallOptimizer:
    """获取全局函数调用优化器"""
    global _global_optimizer
    if _global_optimizer is None:
        _global_optimizer = OptimizedCallOptimizer()
    return _global_optimizer
