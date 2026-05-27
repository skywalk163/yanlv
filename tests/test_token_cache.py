"""
Token缓存管理器单元测试

测试TokenCache和TokenCacheManager的功能
"""

import pytest
import time
from yanlv.lexer.token_cache import (
    TokenCache, 
    TokenCacheManager, 
    CacheStats,
    get_global_cache,
    get_global_cache_manager
)
from yanlv.lexer.lexer_token import Token, TokenType, create_token


class TestTokenCache:
    """TokenCache测试类"""
    
    def test_cache_initialization(self):
        """测试缓存初始化"""
        cache = TokenCache(max_size=100)
        assert len(cache) == 0
        assert cache.max_size == 100
        assert cache.is_enabled() == True
        assert cache.stats.hits == 0
        assert cache.stats.misses == 0
    
    def test_cache_put_and_get(self):
        """测试缓存存取"""
        cache = TokenCache()
        code = "定义 变量 甲 为 10"
        tokens = [
            create_token(TokenType.DEFINE, "定义", 1, 1),
            create_token(TokenType.VARIABLE, "变量", 1, 3),
            create_token(TokenType.IDENTIFIER, "甲", 1, 6),
            create_token(TokenType.IS, "为", 1, 8),
            create_token(TokenType.NUMBER, "10", 1, 10),
        ]
        
        # 存入缓存
        cache.put(code, tokens)
        assert len(cache) == 1
        
        # 从缓存获取
        cached_tokens = cache.get(code)
        assert cached_tokens is not None
        assert len(cached_tokens) == len(tokens)
        assert cache.stats.hits == 1
    
    def test_cache_miss(self):
        """测试缓存未命中"""
        cache = TokenCache()
        code = "定义 变量 甲 为 10"
        
        # 未存入缓存,直接获取
        cached_tokens = cache.get(code)
        assert cached_tokens is None
        assert cache.stats.misses == 1
    
    def test_lru_eviction(self):
        """测试LRU淘汰机制"""
        cache = TokenCache(max_size=3)
        
        # 存入3个项
        for i in range(3):
            code = f"代码{i}"
            tokens = [create_token(TokenType.NUMBER, str(i), 1, 1)]
            cache.put(code, tokens)
        
        assert len(cache) == 3
        
        # 存入第4个项,应该淘汰第1个
        code4 = "代码4"
        tokens4 = [create_token(TokenType.NUMBER, "4", 1, 1)]
        cache.put(code4, tokens4)
        
        assert len(cache) == 3
        assert cache.stats.evictions == 1
        
        # 第1个项应该被淘汰
        cached = cache.get("代码0")
        assert cached is None
    
    def test_lru_access_order(self):
        """测试LRU访问顺序"""
        cache = TokenCache(max_size=3)
        
        # 存入3个项
        for i in range(3):
            code = f"代码{i}"
            tokens = [create_token(TokenType.NUMBER, str(i), 1, 1)]
            cache.put(code, tokens)
        
        # 访问第1个项,使其移到末尾
        cache.get("代码0")
        
        # 存入第4个项,应该淘汰第2个(因为第1个刚被访问过)
        code4 = "代码4"
        tokens4 = [create_token(TokenType.NUMBER, "4", 1, 1)]
        cache.put(code4, tokens4)
        
        # 第1个项应该还在
        cached = cache.get("代码0")
        assert cached is not None
        
        # 第2个项应该被淘汰
        cached = cache.get("代码1")
        assert cached is None
    
    def test_cache_clear(self):
        """测试缓存清空"""
        cache = TokenCache()
        
        # 存入一些项
        for i in range(5):
            code = f"代码{i}"
            tokens = [create_token(TokenType.NUMBER, str(i), 1, 1)]
            cache.put(code, tokens)
        
        assert len(cache) == 5
        
        # 清空缓存
        cache.clear()
        assert len(cache) == 0
        assert cache.stats.size == 0
    
    def test_cache_enable_disable(self):
        """测试缓存启用/禁用"""
        cache = TokenCache()
        code = "测试代码"
        tokens = [create_token(TokenType.NUMBER, "1", 1, 1)]
        
        # 禁用缓存
        cache.disable()
        assert cache.is_enabled() == False
        
        # 禁用状态下,put不起作用
        cache.put(code, tokens)
        assert len(cache) == 0
        
        # 禁用状态下,get返回None
        cached = cache.get(code)
        assert cached is None
        
        # 启用缓存
        cache.enable()
        assert cache.is_enabled() == True
        
        # 启用后正常工作
        cache.put(code, tokens)
        assert len(cache) == 1
        cached = cache.get(code)
        assert cached is not None
    
    def test_cache_resize(self):
        """测试缓存大小调整"""
        cache = TokenCache(max_size=5)
        
        # 存入5个项
        for i in range(5):
            code = f"代码{i}"
            tokens = [create_token(TokenType.NUMBER, str(i), 1, 1)]
            cache.put(code, tokens)
        
        assert len(cache) == 5
        
        # 调整大小为3,应该淘汰2个项
        cache.resize(3)
        assert len(cache) == 3
        assert cache.max_size == 3
        assert cache.stats.evictions >= 2
    
    def test_cache_hit_rate(self):
        """测试缓存命中率计算"""
        cache = TokenCache()
        code = "测试代码"
        tokens = [create_token(TokenType.NUMBER, "1", 1, 1)]
        
        # 存入缓存
        cache.put(code, tokens)
        
        # 命中3次
        for _ in range(3):
            cache.get(code)
        
        # 未命中2次
        for i in range(2):
            cache.get(f"不存在的代码{i}")
        
        stats = cache.get_stats()
        assert stats.hits == 3
        assert stats.misses == 2
        # 命中率 = 3 / (3 + 2) = 0.6
        assert abs(stats.hit_rate - 0.6) < 0.01
    
    def test_cache_contains(self):
        """测试缓存包含检查"""
        cache = TokenCache()
        code = "测试代码"
        tokens = [create_token(TokenType.NUMBER, "1", 1, 1)]
        
        assert code not in cache
        
        cache.put(code, tokens)
        assert code in cache
    
    def test_cache_time_saved(self):
        """测试节省时间统计"""
        cache = TokenCache()
        code = "测试代码"
        tokens = [create_token(TokenType.NUMBER, "1", 1, 1)]
        
        # 存入缓存,记录节省的时间
        cache.put(code, tokens, time_saved=50.0)
        
        stats = cache.get_stats()
        assert stats.total_time_saved == 50.0
    
    def test_cache_memory_usage(self):
        """测试内存占用估算"""
        cache = TokenCache()
        
        # 存入一些Token
        for i in range(10):
            code = f"代码{i}"
            tokens = [create_token(TokenType.NUMBER, str(j), 1, 1) for j in range(5)]
            cache.put(code, tokens)
        
        memory = cache.get_memory_usage()
        # 10个代码 * 5个Token * 100字节 = 5000字节
        assert memory == 5000


class TestTokenCacheManager:
    """TokenCacheManager测试类"""
    
    def test_manager_initialization(self):
        """测试管理器初始化"""
        manager = TokenCacheManager()
        assert len(manager.caches) == 1
        assert 'default' in manager.caches
    
    def test_get_cache(self):
        """测试获取缓存"""
        manager = TokenCacheManager()
        
        # 获取默认缓存
        cache1 = manager.get_cache('default')
        assert cache1 is not None
        
        # 获取不存在的缓存,应该自动创建
        cache2 = manager.get_cache('test')
        assert cache2 is not None
        assert 'test' in manager.caches
    
    def test_create_cache(self):
        """测试创建缓存"""
        manager = TokenCacheManager()
        
        # 创建新缓存
        cache = manager.create_cache('custom', max_size=500)
        assert cache is not None
        assert cache.max_size == 500
        assert 'custom' in manager.caches
    
    def test_clear_all(self):
        """测试清空所有缓存"""
        manager = TokenCacheManager()
        
        # 在多个缓存中存入数据
        for name in ['cache1', 'cache2', 'cache3']:
            cache = manager.get_cache(name)
            code = f"代码{name}"
            tokens = [create_token(TokenType.NUMBER, "1", 1, 1)]
            cache.put(code, tokens)
        
        # 清空所有缓存
        manager.clear_all()
        
        # 检查所有缓存都已清空
        for cache in manager.caches.values():
            assert len(cache) == 0
    
    def test_total_stats(self):
        """测试汇总统计"""
        manager = TokenCacheManager()
        
        # 在多个缓存中操作
        for i in range(3):
            cache = manager.get_cache(f'cache{i}')
            code = f"代码{i}"
            tokens = [create_token(TokenType.NUMBER, str(i), 1, 1)]
            cache.put(code, tokens)
            cache.get(code)  # 命中
            cache.get("不存在的代码")  # 未命中
        
        stats = manager.get_total_stats()
        assert stats['total_hits'] == 3
        assert stats['total_misses'] == 3
        assert stats['cache_count'] == 4  # default + 3个新缓存


class TestGlobalCache:
    """全局缓存测试类"""
    
    def test_get_global_cache_manager(self):
        """测试获取全局缓存管理器"""
        manager1 = get_global_cache_manager()
        manager2 = get_global_cache_manager()
        
        # 应该返回同一个实例
        assert manager1 is manager2
    
    def test_get_global_cache(self):
        """测试获取全局缓存"""
        cache1 = get_global_cache()
        cache2 = get_global_cache()
        
        # 应该返回同一个实例
        assert cache1 is cache2


class TestCachePerformance:
    """缓存性能测试"""
    
    def test_cache_speedup(self):
        """测试缓存加速效果"""
        cache = TokenCache()
        
        # 模拟分词函数
        def tokenize(code):
            # 模拟耗时操作
            time.sleep(0.001)
            return [create_token(TokenType.NUMBER, "1", 1, 1)]
        
        code = "测试代码" * 100
        
        # 第一次编译(未命中)
        start = time.time()
        tokens1 = tokenize(code)
        time1 = time.time() - start
        cache.put(code, tokens1, time_saved=time1 * 1000)
        
        # 第二次编译(命中)
        start = time.time()
        tokens2 = cache.get(code)
        time2 = time.time() - start
        
        # 缓存命中应该快得多
        assert tokens2 is not None
        assert time2 < time1
    
    def test_cache_warmup(self):
        """测试缓存预热"""
        cache = TokenCache()
        
        # 准备代码样本
        code_samples = [f"代码{i}" for i in range(10)]
        
        # 模拟分词函数
        def tokenize(code):
            return [create_token(TokenType.NUMBER, "1", 1, 1)]
        
        # 预热缓存
        cache.warmup(code_samples, tokenize)
        
        # 检查所有样本都已缓存
        assert len(cache) == 10
        for code in code_samples:
            assert code in cache


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
