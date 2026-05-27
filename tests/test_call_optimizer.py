"""
函数调用优化器测试

测试OptimizedCallOptimizer的功能
"""

import pytest
import time
from yanlv.call_optimizer import (
    InlineCache, 
    DispatchTable, 
    OptimizedCallOptimizer,
    CallStats,
    get_global_call_optimizer
)


class TestInlineCache:
    """InlineCache测试类"""
    
    def test_cache_initialization(self):
        """测试缓存初始化"""
        cache = InlineCache(max_size=100)
        assert len(cache.cache) == 0
        assert cache.max_size == 100
    
    def test_cache_put_get(self):
        """测试缓存存取"""
        cache = InlineCache()
        
        # 存入缓存
        cache.put("func1", (1, 2), {}, 3)
        
        # 获取缓存
        result = cache.get("func1", (1, 2), {})
        assert result == 3
        assert cache.hits == 1
    
    def test_cache_miss(self):
        """测试缓存未命中"""
        cache = InlineCache()
        
        result = cache.get("func1", (1, 2), {})
        assert result is None
        assert cache.misses == 1
    
    def test_cache_with_kwargs(self):
        """测试带关键字参数的缓存"""
        cache = InlineCache()
        
        # 存入缓存
        cache.put("func1", (1,), {"b": 2}, 3)
        
        # 获取缓存
        result = cache.get("func1", (1,), {"b": 2})
        assert result == 3
        
        # 不同参数,未命中
        result2 = cache.get("func1", (1,), {"b": 3})
        assert result2 is None
    
    def test_cache_max_size(self):
        """测试缓存最大大小"""
        cache = InlineCache(max_size=5)
        
        # 存入超过容量的缓存
        for i in range(10):
            cache.put(f"func{i}", (i,), {}, i)
        
        # 缓存大小应该不超过最大值
        assert len(cache.cache) <= 5
    
    def test_cache_clear(self):
        """测试清空缓存"""
        cache = InlineCache()
        
        # 存入缓存
        cache.put("func1", (1,), {}, 1)
        cache.put("func2", (2,), {}, 2)
        
        # 清空
        cache.clear()
        assert len(cache.cache) == 0
        assert cache.hits == 0
        assert cache.misses == 0


class TestDispatchTable:
    """DispatchTable测试类"""
    
    def test_table_initialization(self):
        """测试分发表初始化"""
        table = DispatchTable()
        assert len(table.table) == 0
    
    def test_table_register_lookup(self):
        """测试函数注册和查找"""
        table = DispatchTable()
        
        # 注册函数
        table.register("add", ["a", "b"], lambda a, b: a + b)
        
        # 查找函数
        func_info = table.lookup("add")
        assert func_info is not None
        assert func_info.name == "add"
        assert func_info.params == ["a", "b"]
    
    def test_table_lookup_nonexistent(self):
        """测试查找不存在的函数"""
        table = DispatchTable()
        
        func_info = table.lookup("nonexistent")
        assert func_info is None
    
    def test_table_update_stats(self):
        """测试统计信息更新"""
        table = DispatchTable()
        
        # 注册函数
        table.register("func", [], None)
        
        # 更新统计
        table.update_stats("func", 10.0)
        table.update_stats("func", 20.0)
        
        func_info = table.lookup("func")
        assert func_info.call_count == 2
        assert func_info.total_time == 30.0
    
    def test_table_hot_functions(self):
        """测试热点函数识别"""
        table = DispatchTable()
        
        # 注册多个函数
        table.register("hot_func", [], None)
        table.register("cold_func", [], None)
        
        # 更新统计
        for _ in range(15):
            table.update_stats("hot_func", 1.0)
        table.update_stats("cold_func", 1.0)
        
        # 获取热点函数
        hot_funcs = table.get_hot_functions(threshold=10)
        assert "hot_func" in hot_funcs
        assert "cold_func" not in hot_funcs


class TestOptimizedCallOptimizer:
    """OptimizedCallOptimizer测试类"""
    
    def test_optimizer_initialization(self):
        """测试优化器初始化"""
        optimizer = OptimizedCallOptimizer()
        assert len(optimizer.dispatch_table.table) == 0
    
    def test_optimizer_register_call(self):
        """测试函数注册和调用"""
        optimizer = OptimizedCallOptimizer()
        
        # 注册函数
        def add_impl(func_info, args, kwargs):
            return args[0] + args[1]
        
        optimizer.register_function("add", ["a", "b"], None)
        
        # 调用函数
        result = optimizer.call("add", (1, 2), {}, add_impl)
        assert result == 3
    
    def test_optimizer_pure_function_caching(self):
        """测试纯函数缓存"""
        optimizer = OptimizedCallOptimizer()
        
        call_count = 0
        
        def pure_func_impl(func_info, args, kwargs):
            nonlocal call_count
            call_count += 1
            return args[0] * args[0]
        
        # 注册纯函数
        optimizer.register_function("square", ["x"], None, is_pure=True)
        
        # 第一次调用
        result1 = optimizer.call("square", (5,), {}, pure_func_impl)
        assert result1 == 25
        assert call_count == 1
        
        # 第二次调用(应该从缓存获取)
        result2 = optimizer.call("square", (5,), {}, pure_func_impl)
        assert result2 == 25
        assert call_count == 1  # 没有增加
    
    def test_optimizer_memoization(self):
        """测试记忆化"""
        optimizer = OptimizedCallOptimizer()
        
        call_count = 0
        
        def fib_impl(func_info, args, kwargs):
            nonlocal call_count
            call_count += 1
            n = args[0]
            if n <= 1:
                return n
            # 这里简化,实际应该递归调用
            return n
        
        # 注册记忆化函数
        optimizer.register_function("fib", ["n"], None, memoize=True)
        
        # 调用
        result = optimizer.call("fib", (10,), {}, fib_impl)
        assert result == 10
        assert call_count == 1
        
        # 再次调用(应该从缓存获取)
        result2 = optimizer.call("fib", (10,), {}, fib_impl)
        assert result2 == 10
        assert call_count == 1  # 没有增加
    
    def test_optimizer_stats(self):
        """测试统计信息"""
        optimizer = OptimizedCallOptimizer()
        
        def impl(func_info, args, kwargs):
            return args[0]
        
        optimizer.register_function("func", ["x"], None, is_pure=True)
        
        # 多次调用
        for i in range(10):
            optimizer.call("func", (i,), {}, impl)
        
        stats = optimizer.get_stats()
        assert stats.total_calls == 10
        assert stats.cache_misses == 10  # 每次参数不同,都未命中
    
    def test_optimizer_cache_control(self):
        """测试缓存控制"""
        optimizer = OptimizedCallOptimizer()
        
        def impl(func_info, args, kwargs):
            return args[0]
        
        optimizer.register_function("func", ["x"], None, is_pure=True)
        
        # 启用缓存
        optimizer.enable_cache()
        result1 = optimizer.call("func", (5,), {}, impl)
        
        # 禁用缓存
        optimizer.disable_cache()
        result2 = optimizer.call("func", (5,), {}, impl)
        
        # 启用缓存
        optimizer.enable_cache()
        result3 = optimizer.call("func", (5,), {}, impl)
        
        assert result1 == result2 == result3 == 5
    
    def test_optimizer_nonexistent_function(self):
        """测试调用不存在的函数"""
        optimizer = OptimizedCallOptimizer()
        
        def impl(func_info, args, kwargs):
            return None
        
        with pytest.raises(NameError):
            optimizer.call("nonexistent", (), {}, impl)


class TestCallPerformance:
    """函数调用性能测试"""
    
    def test_caching_performance(self):
        """测试缓存性能"""
        optimizer = OptimizedCallOptimizer()
        
        call_count = 0
        
        def expensive_func(func_info, args, kwargs):
            nonlocal call_count
            call_count += 1
            # 模拟耗时操作
            time.sleep(0.001)
            return args[0] ** 2
        
        optimizer.register_function("expensive", ["x"], None, is_pure=True)
        
        # 不使用缓存(每次参数不同)
        start = time.time()
        for i in range(100):
            optimizer.call("expensive", (i,), {}, expensive_func)
        time_no_cache = time.time() - start
        
        # 使用缓存(相同参数)
        optimizer.reset_stats()
        call_count = 0
        start = time.time()
        for _ in range(100):
            optimizer.call("expensive", (5,), {}, expensive_func)
        time_with_cache = time.time() - start
        
        stats = optimizer.get_stats()
        
        print(f"\n缓存性能测试:")
        print(f"不使用缓存: {time_no_cache*1000:.2f}ms")
        print(f"使用缓存: {time_with_cache*1000:.2f}ms")
        print(f"缓存命中率: {stats.cache_hit_rate:.2%}")
        print(f"实际调用次数: {call_count}")
        
        # 缓存应该显著提升性能
        assert time_with_cache < time_no_cache
        assert stats.cache_hit_rate > 0.9
    
    def test_dispatch_performance(self):
        """测试分发表性能"""
        optimizer = OptimizedCallOptimizer()
        
        # 注册多个函数
        def impl(func_info, args, kwargs):
            return args[0]
        
        for i in range(100):
            optimizer.register_function(f"func{i}", ["x"], None)
        
        # 测试查找性能
        start = time.time()
        for _ in range(10000):
            for i in range(100):
                optimizer.dispatch_table.lookup(f"func{i}")
        elapsed = time.time() - start
        
        print(f"\n分发表性能测试:")
        print(f"查找次数: 1000000")
        print(f"总耗时: {elapsed*1000:.2f}ms")
        print(f"平均查找时间: {elapsed*1000000:.2f}μs")


class TestGlobalOptimizer:
    """全局优化器测试"""
    
    def test_get_global_optimizer(self):
        """测试获取全局优化器"""
        optimizer1 = get_global_call_optimizer()
        optimizer2 = get_global_call_optimizer()
        
        # 应该是同一个实例
        assert optimizer1 is optimizer2


if __name__ == '__main__':
    pytest.main([__file__, '-v', '-s'])
