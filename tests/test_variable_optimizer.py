"""
变量查找优化器测试

测试OptimizedVariableManager和Scope的功能
"""

import pytest
import time
from yanlv.variable_optimizer import (
    Scope, 
    OptimizedVariableManager, 
    VariableStats,
    get_global_variable_manager
)


class TestScope:
    """Scope测试类"""
    
    def test_scope_initialization(self):
        """测试作用域初始化"""
        scope = Scope("test")
        assert scope.name == "test"
        assert scope.parent is None
        assert len(scope.variables) == 0
    
    def test_scope_get_set(self):
        """测试作用域变量存取"""
        scope = Scope("test")
        
        # 设置变量
        scope.set("x", 10)
        assert scope.get("x") == 10
        
        # 更新变量
        scope.set("x", 20)
        assert scope.get("x") == 20
    
    def test_scope_chain(self):
        """测试作用域链"""
        parent = Scope("parent")
        parent.set("x", 10)
        parent.set("y", 20)
        
        child = Scope("child", parent)
        child.set("z", 30)
        
        # 子作用域可以访问父作用域的变量
        assert child.get("x") == 10
        assert child.get("y") == 20
        assert child.get("z") == 30
        
        # 父作用域不能访问子作用域的变量
        with pytest.raises(NameError):
            parent.get("z")
    
    def test_scope_shadowing(self):
        """测试变量遮蔽"""
        parent = Scope("parent")
        parent.set("x", 10)
        
        child = Scope("child", parent)
        child.set("x", 20)  # 遮蔽父作用域的x
        
        assert child.get("x") == 20
        assert parent.get("x") == 10  # 父作用域的x不变
    
    def test_scope_delete(self):
        """测试变量删除"""
        scope = Scope("test")
        scope.set("x", 10)
        
        assert scope.delete("x") == True
        with pytest.raises(NameError):
            scope.get("x")
        
        assert scope.delete("y") == False  # 不存在的变量
    
    def test_scope_cache(self):
        """测试作用域缓存"""
        scope = Scope("test")
        
        # 设置变量
        scope.set("x", 10)
        
        # 第一次获取(未命中缓存)
        stats = VariableStats()
        value1 = scope.get("x", stats)
        assert value1 == 10
        assert stats.total_lookups == 1
        assert stats.cache_hits == 0  # 第一次未命中
        
        # 第二次获取(命中缓存)
        value2 = scope.get("x", stats)
        assert value2 == 10
        assert stats.total_lookups == 2
        assert stats.cache_hits == 1  # 第二次命中
    
    def test_scope_contains(self):
        """测试变量存在检查"""
        scope = Scope("test")
        scope.set("x", 10)
        
        assert "x" in scope
        assert "y" not in scope


class TestOptimizedVariableManager:
    """OptimizedVariableManager测试类"""
    
    def test_manager_initialization(self):
        """测试管理器初始化"""
        manager = OptimizedVariableManager()
        assert manager.get_scope_depth() == 1
        assert manager.current_scope.name == "global"
    
    def test_manager_scope_operations(self):
        """测试作用域操作"""
        manager = OptimizedVariableManager()
        
        # 设置全局变量
        manager.set_global("x", 10)
        assert manager.get("x") == 10
        
        # 进入新作用域
        manager.enter_scope("function1")
        assert manager.get_scope_depth() == 2
        
        # 设置局部变量
        manager.set("y", 20, local=True)
        assert manager.get("y") == 20
        
        # 可以访问全局变量
        assert manager.get("x") == 10
        
        # 退出作用域
        exited = manager.exit_scope()
        assert exited is not None
        assert manager.get_scope_depth() == 1
        
        # 不能访问局部变量
        with pytest.raises(NameError):
            manager.get("y")
    
    def test_manager_variable_shadowing(self):
        """测试变量遮蔽"""
        manager = OptimizedVariableManager()
        
        # 设置全局变量
        manager.set("x", 10)
        
        # 进入新作用域并遮蔽
        manager.enter_scope("function1")
        manager.set("x", 20, local=True)
        
        assert manager.get("x") == 20
        
        # 退出作用域
        manager.exit_scope()
        
        # 全局变量不变
        assert manager.get("x") == 10
    
    def test_manager_stats(self):
        """测试统计信息"""
        manager = OptimizedVariableManager()
        
        # 设置变量
        manager.set("x", 10)
        manager.set("y", 20)
        
        # 多次访问
        for _ in range(10):
            manager.get("x")
        
        stats = manager.get_stats()
        assert stats.total_lookups == 10
        assert stats.cache_hits >= 9  # 第一次未命中,后续命中
    
    def test_manager_cache_control(self):
        """测试缓存控制"""
        manager = OptimizedVariableManager()
        
        # 设置变量
        manager.set("x", 10)
        
        # 禁用缓存
        manager.disable_cache()
        manager.set("y", 20)
        
        # 启用缓存
        manager.enable_cache()
        manager.set("z", 30)
        
        # 验证变量都存在
        assert manager.get("x") == 10
        assert manager.get("y") == 20
        assert manager.get("z") == 30
    
    def test_manager_nested_scopes(self):
        """测试嵌套作用域"""
        manager = OptimizedVariableManager()
        
        # 全局作用域
        manager.set("a", 1)
        
        # 第一层嵌套
        manager.enter_scope("level1")
        manager.set("b", 2, local=True)
        
        # 第二层嵌套
        manager.enter_scope("level2")
        manager.set("c", 3, local=True)
        
        # 可以访问所有外层变量
        assert manager.get("a") == 1
        assert manager.get("b") == 2
        assert manager.get("c") == 3
        
        # 退出到第一层
        manager.exit_scope()
        assert manager.get("a") == 1
        assert manager.get("b") == 2
        with pytest.raises(NameError):
            manager.get("c")
        
        # 退出到全局
        manager.exit_scope()
        assert manager.get("a") == 1
        with pytest.raises(NameError):
            manager.get("b")


class TestVariablePerformance:
    """变量查找性能测试"""
    
    def test_lookup_performance(self):
        """测试查找性能"""
        manager = OptimizedVariableManager()
        
        # 设置大量变量
        for i in range(100):
            manager.set(f"var{i}", i)
        
        # 测试查找性能
        start = time.time()
        for _ in range(1000):
            for i in range(100):
                manager.get(f"var{i}")
        elapsed = time.time() - start
        
        stats = manager.get_stats()
        
        print(f"\n查找性能测试:")
        print(f"总查找次数: {stats.total_lookups}")
        print(f"缓存命中率: {stats.cache_hit_rate:.2%}")
        print(f"平均查找时间: {stats.average_time:.2f}μs")
        print(f"总耗时: {elapsed*1000:.2f}ms")
        
        # 验证缓存命中率很高
        assert stats.cache_hit_rate > 0.9
    
    def test_scope_chain_performance(self):
        """测试作用域链性能"""
        manager = OptimizedVariableManager()
        
        # 创建深层作用域链
        manager.set("global_var", 100)
        
        for i in range(10):
            manager.enter_scope(f"level{i}")
            manager.set(f"local_var{i}", i, local=True)
        
        # 测试作用域链查找性能
        start = time.time()
        for _ in range(1000):
            manager.get("global_var")  # 需要遍历作用域链
        elapsed = time.time() - start
        
        stats = manager.get_stats()
        
        print(f"\n作用域链性能测试:")
        print(f"作用域深度: {manager.get_scope_depth()}")
        print(f"总查找次数: {stats.total_lookups}")
        print(f"作用域链搜索次数: {stats.scope_searches}")
        print(f"缓存命中率: {stats.cache_hit_rate:.2%}")
        print(f"总耗时: {elapsed*1000:.2f}ms")
        
        # 验证缓存有效
        assert stats.cache_hit_rate > 0.9
    
    def test_comparison_with_dict(self):
        """与普通字典对比性能"""
        # 使用普通字典
        simple_dict = {}
        for i in range(100):
            simple_dict[f"var{i}"] = i
        
        start = time.time()
        for _ in range(10000):
            for i in range(100):
                _ = simple_dict[f"var{i}"]
        dict_time = time.time() - start
        
        # 使用优化的变量管理器
        manager = OptimizedVariableManager()
        for i in range(100):
            manager.set(f"var{i}", i)
        
        start = time.time()
        for _ in range(10000):
            for i in range(100):
                manager.get(f"var{i}")
        manager_time = time.time() - start
        
        print(f"\n性能对比:")
        print(f"普通字典: {dict_time*1000:.2f}ms")
        print(f"优化管理器: {manager_time*1000:.2f}ms")
        print(f"缓存命中率: {manager.get_stats().cache_hit_rate:.2%}")
        
        # 优化后的性能应该接近或优于普通字典
        # (由于缓存,性能应该相当)


class TestGlobalManager:
    """全局管理器测试"""
    
    def test_get_global_manager(self):
        """测试获取全局管理器"""
        manager1 = get_global_variable_manager()
        manager2 = get_global_variable_manager()
        
        # 应该是同一个实例
        assert manager1 is manager2


if __name__ == '__main__':
    pytest.main([__file__, '-v', '-s'])
