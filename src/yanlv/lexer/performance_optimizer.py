"""
言律语言词法分析器 - 性能优化器

包含性能优化、缓存和监控功能
"""

import time
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass
from enum import Enum
from .utils import Cache, PerformanceMonitor, Logger


class OptimizationLevel(Enum):
    """优化级别"""
    NONE = "none"
    BASIC = "basic"
    ADVANCED = "advanced"
    AGGRESSIVE = "aggressive"


@dataclass
class OptimizationConfig:
    """优化配置"""
    level: OptimizationLevel = OptimizationLevel.BASIC
    enable_cache: bool = True
    cache_size: int = 1000
    enable_profiling: bool = False
    enable_memory_monitoring: bool = False
    enable_threading: bool = False
    max_workers: int = 4
    batch_size: int = 100
    timeout_seconds: float = 30.0


class PerformanceOptimizer:
    """性能优化器"""
    
    def __init__(self, config: Optional[OptimizationConfig] = None):
        """初始化性能优化器"""
        self.config = config or OptimizationConfig()
        self.monitor = PerformanceMonitor()
        self.logger = Logger("performance")
        
        # 缓存
        self.caches: Dict[str, Cache] = {}
        self._init_caches()
        
        # 性能数据
        self.performance_data: Dict[str, Any] = {
            'total_operations': 0,
            'total_time': 0.0,
            'average_time': 0.0,
            'peak_memory_mb': 0.0,
            'cache_hit_rates': {},
            'optimizations_applied': []
        }
    
    def _init_caches(self):
        """初始化缓存"""
        if self.config.enable_cache:
            # 分词缓存
            self.caches['tokenization'] = Cache(max_size=self.config.cache_size)
            
            # 词元匹配缓存
            self.caches['matching'] = Cache(max_size=self.config.cache_size)
            
            # 模式匹配缓存
            self.caches['pattern_matching'] = Cache(max_size=self.config.cache_size)
    
    def optimize_tokenization(self, text: str) -> List[str]:
        """优化分词"""
        cache_key = f"tokenization:{hash(text)}"
        
        # 检查缓存
        if self.config.enable_cache:
            cached_result = self.caches['tokenization'].get(cache_key)
            if cached_result is not None:
                self.performance_data['cache_hit_rates']['tokenization'] = \
                    self.performance_data['cache_hit_rates'].get('tokenization', 0) + 1
                return cached_result
        
        # 执行分词
        with self.monitor:
            # 这里应该调用实际的分词函数
            # 为了演示，我们使用简单的空格分词
            result = text.split()
        
        # 更新缓存
        if self.config.enable_cache:
            self.caches['tokenization'].set(cache_key, result)
        
        # 更新性能数据
        self._update_performance_data('tokenization', len(text))
        
        return result
    
    def optimize_matching(self, segment: str, matcher_func: Callable[[str], Any]) -> Any:
        """优化词元匹配"""
        cache_key = f"matching:{hash(segment)}"
        
        # 检查缓存
        if self.config.enable_cache:
            cached_result = self.caches['matching'].get(cache_key)
            if cached_result is not None:
                self.performance_data['cache_hit_rates']['matching'] = \
                    self.performance_data['cache_hit_rates'].get('matching', 0) + 1
                return cached_result
        
        # 执行匹配
        with self.monitor:
            result = matcher_func(segment)
        
        # 更新缓存
        if self.config.enable_cache:
            self.caches['matching'].set(cache_key, result)
        
        # 更新性能数据
        self._update_performance_data('matching', 1)
        
        return result
    
    def _update_performance_data(self, operation: str, size: int):
        """更新性能数据"""
        self.performance_data['total_operations'] += 1
        self.performance_data['total_time'] += self.monitor.stats.total_time
        
        # 计算平均时间
        if self.performance_data['total_operations'] > 0:
            self.performance_data['average_time'] = \
                self.performance_data['total_time'] / self.performance_data['total_operations']
        
        # 记录优化应用
        if operation not in self.performance_data['optimizations_applied']:
            self.performance_data['optimizations_applied'].append(operation)
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """获取缓存统计信息"""
        stats = {}
        for name, cache in self.caches.items():
            stats[name] = {
                'size': cache.size(),
                'max_size': cache.max_size
            }
        return stats
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """获取性能统计信息"""
        stats = self.performance_data.copy()
        stats.update(self.monitor.get_stats().to_dict())
        
        # 计算缓存命中率
        for cache_name in self.caches:
            hits = self.performance_data['cache_hit_rates'].get(cache_name, 0)
            total = self.performance_data['total_operations']
            if total > 0:
                stats[f'{cache_name}_hit_rate'] = hits / total
            else:
                stats[f'{cache_name}_hit_rate'] = 0.0
        
        return stats
    
    def clear_caches(self):
        """清空所有缓存"""
        for cache in self.caches.values():
            cache.clear()
        
        self.performance_data['cache_hit_rates'].clear()
    
    def reset_performance_data(self):
        """重置性能数据"""
        self.performance_data = {
            'total_operations': 0,
            'total_time': 0.0,
            'average_time': 0.0,
            'peak_memory_mb': 0.0,
            'cache_hit_rates': {},
            'optimizations_applied': []
        }
        self.monitor.reset()
    
    def update_config(self, **kwargs):
        """更新配置"""
        for key, value in kwargs.items():
            if hasattr(self.config, key):
                setattr(self.config, key, value)
        
        # 重新初始化缓存
        if 'cache_size' in kwargs or 'enable_cache' in kwargs:
            self._init_caches()


# 工厂函数
def create_performance_optimizer(config: Optional[OptimizationConfig] = None) -> PerformanceOptimizer:
    """创建性能优化器"""
    return PerformanceOptimizer(config)


def get_default_optimizer() -> PerformanceOptimizer:
    """获取默认性能优化器"""
    return PerformanceOptimizer()


def optimize_with_level(level: OptimizationLevel) -> OptimizationConfig:
    """根据优化级别获取配置"""
    if level == OptimizationLevel.NONE:
        return OptimizationConfig(
            level=level,
            enable_cache=False,
            enable_profiling=False,
            enable_memory_monitoring=False,
            enable_threading=False
        )
    elif level == OptimizationLevel.BASIC:
        return OptimizationConfig(
            level=level,
            enable_cache=True,
            cache_size=500,
            enable_profiling=False,
            enable_memory_monitoring=False,
            enable_threading=False
        )
    elif level == OptimizationLevel.ADVANCED:
        return OptimizationConfig(
            level=level,
            enable_cache=True,
            cache_size=1000,
            enable_profiling=True,
            enable_memory_monitoring=True,
            enable_threading=True,
            max_workers=2
        )
    elif level == OptimizationLevel.AGGRESSIVE:
        return OptimizationConfig(
            level=level,
            enable_cache=True,
            cache_size=5000,
            enable_profiling=True,
            enable_memory_monitoring=True,
            enable_threading=True,
            max_workers=4,
            batch_size=50,
            timeout_seconds=60.0
        )
    else:
        return OptimizationConfig()