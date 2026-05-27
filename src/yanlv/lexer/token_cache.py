"""
言律语言词法分析器 - Token缓存管理器

实现基于LRU策略的Token缓存机制,避免重复分词,提升编译速度
"""

from collections import OrderedDict
from typing import List, Optional, Dict, Any
from dataclasses import dataclass
import hashlib
import time
from .lexer_token import Token


@dataclass
class CacheStats:
    """缓存统计信息"""
    hits: int = 0              # 缓存命中次数
    misses: int = 0            # 缓存未命中次数
    size: int = 0              # 当前缓存大小
    max_size: int = 1000       # 最大缓存大小
    evictions: int = 0         # 淘汰次数
    total_time_saved: float = 0.0  # 节省的总时间(毫秒)
    
    @property
    def hit_rate(self) -> float:
        """计算缓存命中率"""
        total = self.hits + self.misses
        return self.hits / total if total > 0 else 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'hits': self.hits,
            'misses': self.misses,
            'size': self.size,
            'max_size': self.max_size,
            'evictions': self.evictions,
            'hit_rate': f"{self.hit_rate:.2%}",
            'total_time_saved_ms': f"{self.total_time_saved:.2f}"
        }


class TokenCache:
    """
    Token缓存管理器
    
    使用LRU(Least Recently Used)策略管理Token缓存,
    避免对相同代码的重复分词,提升编译速度。
    
    Attributes:
        cache: 有序字典,实现LRU缓存
        max_size: 最大缓存大小
        stats: 缓存统计信息
    """
    
    def __init__(self, max_size: int = 1000):
        """
        初始化Token缓存
        
        Args:
            max_size: 最大缓存大小,默认1000
        """
        self.cache: OrderedDict[str, List[Token]] = OrderedDict()
        self.max_size = max_size
        self.stats = CacheStats(max_size=max_size)
        self._enabled = True
    
    def _compute_hash(self, code: str) -> str:
        """
        计算代码内容的哈希值
        
        Args:
            code: 源代码字符串
            
        Returns:
            哈希值字符串
        """
        return hashlib.md5(code.encode('utf-8')).hexdigest()
    
    def get(self, code: str) -> Optional[List[Token]]:
        """
        从缓存获取Token列表
        
        Args:
            code: 源代码字符串
            
        Returns:
            Token列表(如果缓存命中),否则返回None
        """
        if not self._enabled:
            return None
        
        code_hash = self._compute_hash(code)
        
        if code_hash in self.cache:
            # 缓存命中
            self.stats.hits += 1
            # 将访问的项移到末尾(LRU策略)
            self.cache.move_to_end(code_hash)
            return self.cache[code_hash]
        
        # 缓存未命中
        self.stats.misses += 1
        return None
    
    def put(self, code: str, tokens: List[Token], time_saved: float = 0.0) -> None:
        """
        将Token列表添加到缓存
        
        Args:
            code: 源代码字符串
            tokens: Token列表
            time_saved: 节省的时间(毫秒)
        """
        if not self._enabled:
            return
        
        code_hash = self._compute_hash(code)
        
        # 如果缓存已满,删除最旧的项
        if len(self.cache) >= self.max_size:
            self.cache.popitem(last=False)  # 删除最早的项
            self.stats.evictions += 1
        
        # 添加新项
        self.cache[code_hash] = tokens
        self.stats.size = len(self.cache)
        self.stats.total_time_saved += time_saved
    
    def clear(self) -> None:
        """清空缓存"""
        self.cache.clear()
        self.stats.size = 0
    
    def get_stats(self) -> CacheStats:
        """
        获取缓存统计信息
        
        Returns:
            缓存统计信息对象
        """
        self.stats.size = len(self.cache)
        return self.stats
    
    def enable(self) -> None:
        """启用缓存"""
        self._enabled = True
    
    def disable(self) -> None:
        """禁用缓存"""
        self._enabled = False
    
    def is_enabled(self) -> bool:
        """
        检查缓存是否启用
        
        Returns:
            是否启用
        """
        return self._enabled
    
    def resize(self, new_size: int) -> None:
        """
        调整缓存大小
        
        Args:
            new_size: 新的最大缓存大小
        """
        self.max_size = new_size
        self.stats.max_size = new_size
        
        # 如果当前缓存超过新大小,删除多余的项
        while len(self.cache) > new_size:
            self.cache.popitem(last=False)
            self.stats.evictions += 1
        
        self.stats.size = len(self.cache)
    
    def get_memory_usage(self) -> int:
        """
        估算缓存内存占用(字节)
        
        Returns:
            估算的内存占用
        """
        # 粗略估算:每个Token约100字节
        total_tokens = sum(len(tokens) for tokens in self.cache.values())
        return total_tokens * 100
    
    def warmup(self, code_samples: List[str], tokenizer_func) -> None:
        """
        预热缓存
        
        Args:
            code_samples: 代码样本列表
            tokenizer_func: 分词函数
        """
        for code in code_samples:
            if code not in self.cache:
                tokens = tokenizer_func(code)
                self.put(code, tokens)
    
    def __len__(self) -> int:
        """获取缓存大小"""
        return len(self.cache)
    
    def __contains__(self, code: str) -> bool:
        """检查代码是否在缓存中"""
        code_hash = self._compute_hash(code)
        return code_hash in self.cache
    
    def __bool__(self) -> bool:
        """缓存是否启用且可用"""
        return self._enabled
    
    def __repr__(self) -> str:
        """返回缓存的字符串表示"""
        return (
            f"TokenCache(size={len(self.cache)}/{self.max_size}, "
            f"hit_rate={self.stats.hit_rate:.2%}, "
            f"enabled={self._enabled})"
        )


class TokenCacheManager:
    """
    Token缓存管理器
    
    管理多个TokenCache实例,支持不同场景的缓存策略
    """
    
    def __init__(self):
        """初始化缓存管理器"""
        self.caches: Dict[str, TokenCache] = {}
        self.default_cache = TokenCache()
        self.caches['default'] = self.default_cache
    
    def get_cache(self, name: str = 'default') -> TokenCache:
        """
        获取指定名称的缓存
        
        Args:
            name: 缓存名称
            
        Returns:
            TokenCache实例
        """
        if name not in self.caches:
            self.caches[name] = TokenCache()
        return self.caches[name]
    
    def create_cache(self, name: str, max_size: int = 1000) -> TokenCache:
        """
        创建新的缓存
        
        Args:
            name: 缓存名称
            max_size: 最大缓存大小
            
        Returns:
            新创建的TokenCache实例
        """
        cache = TokenCache(max_size=max_size)
        self.caches[name] = cache
        return cache
    
    def clear_all(self) -> None:
        """清空所有缓存"""
        for cache in self.caches.values():
            cache.clear()
    
    def get_total_stats(self) -> Dict[str, Any]:
        """
        获取所有缓存的汇总统计
        
        Returns:
            汇总统计信息
        """
        total_hits = sum(cache.stats.hits for cache in self.caches.values())
        total_misses = sum(cache.stats.misses for cache in self.caches.values())
        total_size = sum(len(cache) for cache in self.caches.values())
        total_evictions = sum(cache.stats.evictions for cache in self.caches.values())
        total_time_saved = sum(
            cache.stats.total_time_saved for cache in self.caches.values()
        )
        
        total = total_hits + total_misses
        hit_rate = total_hits / total if total > 0 else 0.0
        
        return {
            'total_hits': total_hits,
            'total_misses': total_misses,
            'total_size': total_size,
            'total_evictions': total_evictions,
            'hit_rate': f"{hit_rate:.2%}",
            'total_time_saved_ms': f"{total_time_saved:.2f}",
            'cache_count': len(self.caches)
        }
    
    def __repr__(self) -> str:
        """返回管理器的字符串表示"""
        stats = self.get_total_stats()
        return (
            f"TokenCacheManager(caches={stats['cache_count']}, "
            f"total_size={stats['total_size']}, "
            f"hit_rate={stats['hit_rate']})"
        )


# 全局缓存管理器实例
_global_cache_manager: Optional[TokenCacheManager] = None


def get_global_cache_manager() -> TokenCacheManager:
    """
    获取全局缓存管理器实例
    
    Returns:
        全局TokenCacheManager实例
    """
    global _global_cache_manager
    if _global_cache_manager is None:
        _global_cache_manager = TokenCacheManager()
    return _global_cache_manager


def get_global_cache() -> TokenCache:
    """
    获取全局默认缓存
    
    Returns:
        全局默认TokenCache实例
    """
    return get_global_cache_manager().default_cache
