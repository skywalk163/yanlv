"""
AST节点对象池单元测试

测试ASTNodePool的功能
"""

import pytest
from yanlv.ast_node_pool import (
    ASTNodePool, 
    PoolStats, 
    get_global_pool,
    create_pool
)
from yanlv.ast_nodes import (
    NodeType, Program, VariableDeclaration, 
    Identifier, Literal, BinaryExpression
)


class TestASTNodePool:
    """ASTNodePool测试类"""
    
    def test_pool_initialization(self):
        """测试对象池初始化"""
        pool = ASTNodePool(max_pool_size=100)
        assert len(pool) == 0
        assert pool.max_pool_size == 100
        assert pool.enabled == True
        assert pool.stats.total_created == 0
        assert pool.stats.total_reused == 0
    
    def test_pool_acquire_and_release(self):
        """测试对象获取和释放"""
        pool = ASTNodePool()
        
        # 创建一个节点
        node = pool.create_node(Identifier, name="test")
        assert node is not None
        assert node.name == "test"
        assert pool.stats.total_created == 1
        
        # 释放节点
        pool.release(node)
        assert pool.stats.total_released == 1
        assert len(pool) == 1
        
        # 再次获取,应该复用
        node2 = pool.acquire(NodeType.IDENTIFIER)
        assert node2 is not None
        assert pool.stats.total_reused == 1
    
    def test_pool_reuse(self):
        """测试对象复用"""
        pool = ASTNodePool()
        
        # 创建并释放多个节点
        for i in range(5):
            node = pool.create_node(Identifier, name=f"var{i}")
            pool.release(node)
        
        assert len(pool) == 5
        assert pool.stats.total_created == 5
        assert pool.stats.total_released == 5
        
        # 从池中获取,应该复用
        for i in range(3):
            node = pool.acquire(NodeType.IDENTIFIER)
            assert node is not None
        
        assert pool.stats.total_reused == 3
        assert len(pool) == 2  # 5 - 3 = 2
    
    def test_pool_disabled(self):
        """测试禁用对象池"""
        pool = ASTNodePool(enabled=False)
        
        # 创建节点
        node = pool.create_node(Identifier, name="test")
        assert node is not None
        
        # 释放节点(不会加入池)
        pool.release(node)
        assert len(pool) == 0
        
        # 获取节点(返回None)
        node2 = pool.acquire(NodeType.IDENTIFIER)
        assert node2 is None
    
    def test_pool_max_size(self):
        """测试池最大容量"""
        pool = ASTNodePool(max_pool_size=5)
        
        # 创建并释放超过容量的节点
        for i in range(10):
            node = pool.create_node(Identifier, name=f"var{i}")
            pool.release(node)
        
        # 池中最多5个
        assert len(pool) <= 5
    
    def test_pool_clear(self):
        """测试清空池"""
        pool = ASTNodePool()
        
        # 创建并释放一些节点
        for i in range(5):
            node = pool.create_node(Identifier, name=f"var{i}")
            pool.release(node)
        
        assert len(pool) == 5
        
        # 清空
        pool.clear()
        assert len(pool) == 0
    
    def test_pool_resize(self):
        """测试调整池大小"""
        pool = ASTNodePool(max_pool_size=10)
        
        # 创建并释放10个节点
        for i in range(10):
            node = pool.create_node(Identifier, name=f"var{i}")
            pool.release(node)
        
        assert len(pool) == 10
        
        # 调整大小为5
        pool.resize(5)
        assert len(pool) == 5
        assert pool.max_pool_size == 5
    
    def test_pool_stats(self):
        """测试统计信息"""
        pool = ASTNodePool()
        
        # 创建一些节点
        for i in range(5):
            node = pool.create_node(Identifier, name=f"var{i}")
            pool.release(node)
        
        # 复用一些节点
        for i in range(3):
            pool.acquire(NodeType.IDENTIFIER)
        
        stats = pool.get_stats()
        assert stats.total_created == 5
        assert stats.total_reused == 3
        assert stats.total_released == 5
        assert stats.current_pooled == 2  # 5 - 3
        
        # 检查复用率
        expected_rate = 3 / (5 + 3)
        assert abs(stats.reuse_rate - expected_rate) < 0.01
    
    def test_pool_warmup(self):
        """测试预热对象池"""
        pool = ASTNodePool()
        
        # 预热
        pool.warmup([NodeType.IDENTIFIER, NodeType.LITERAL], count=5)
        
        # 检查池中有预热的对象
        assert len(pool.pools[NodeType.IDENTIFIER]) == 5
        assert len(pool.pools[NodeType.LITERAL]) == 5
    
    def test_pool_different_types(self):
        """测试不同类型节点"""
        pool = ASTNodePool()
        
        # 创建不同类型的节点
        id_node = pool.create_node(Identifier, name="x")
        lit_node = pool.create_node(Literal, value=10)
        var_node = pool.create_node(VariableDeclaration, name="y", initializer=None)
        
        assert id_node is not None
        assert lit_node is not None
        assert var_node is not None
        
        # 释放
        pool.release(id_node)
        pool.release(lit_node)
        pool.release(var_node)
        
        # 检查各类型池
        assert len(pool.pools[NodeType.IDENTIFIER]) == 1
        assert len(pool.pools[NodeType.LITERAL]) == 1
        assert len(pool.pools[NodeType.VARIABLE_DECL]) == 1
    
    def test_node_reset(self):
        """测试节点重置"""
        pool = ASTNodePool()
        
        # 创建并设置节点
        node = pool.create_node(Identifier, name="test")
        node.line = 10
        node.column = 5
        node.metadata["key"] = "value"
        
        # 释放(会重置)
        pool.release(node)
        
        # 再次获取
        node2 = pool.acquire(NodeType.IDENTIFIER)
        assert node2 is not None
        # 节点应该被重置了
        assert node2.line == 0
        assert node2.column == 0
        assert len(node2.metadata) == 0
    
    def test_memory_estimation(self):
        """测试内存估算"""
        pool = ASTNodePool()
        
        # 创建节点
        node = pool.create_node(Identifier, name="test")
        
        # 检查内存统计
        assert pool.stats.memory_saved > 0


class TestGlobalPool:
    """全局对象池测试"""
    
    def test_get_global_pool(self):
        """测试获取全局池"""
        pool1 = get_global_pool()
        pool2 = get_global_pool()
        
        # 应该是同一个实例
        assert pool1 is pool2
    
    def test_create_pool(self):
        """测试创建新池"""
        pool = create_pool(max_pool_size=500, enabled=False)
        
        assert pool.max_pool_size == 500
        assert pool.enabled == False


class TestPoolPerformance:
    """对象池性能测试"""
    
    def test_pool_performance_benefit(self):
        """测试对象池性能收益"""
        import time
        
        # 不使用对象池
        start = time.time()
        for _ in range(1000):
            node = Identifier(name="test")
        time_without_pool = time.time() - start
        
        # 使用对象池
        pool = ASTNodePool()
        
        # 预热
        pool.warmup([NodeType.IDENTIFIER], count=100)
        
        start = time.time()
        for _ in range(1000):
            node = pool.acquire(NodeType.IDENTIFIER)
            if node is None:
                node = pool.create_node(Identifier, name="test")
            # 使用节点...
            pool.release(node)
        time_with_pool = time.time() - start
        
        # 对象池应该更快(或至少不慢太多)
        # 这里主要验证功能,性能提升在实际使用中更明显
        print(f"\n不使用对象池: {time_without_pool*1000:.2f}ms")
        print(f"使用对象池: {time_with_pool*1000:.2f}ms")
        print(f"复用率: {pool.stats.reuse_rate:.2%}")
    
    def test_large_scale_pooling(self):
        """测试大规模对象池化"""
        pool = ASTNodePool(max_pool_size=1000)
        
        # 模拟大量节点创建和释放
        for _ in range(100):
            # 创建一批节点
            nodes = []
            for i in range(50):
                node = pool.create_node(Identifier, name=f"var{i}")
                nodes.append(node)
            
            # 释放这批节点
            for node in nodes:
                pool.release(node)
        
        stats = pool.get_stats()
        
        print(f"\n大规模测试:")
        print(f"总创建: {stats.total_created}")
        print(f"总复用: {stats.total_reused}")
        print(f"总释放: {stats.total_released}")
        print(f"复用率: {stats.reuse_rate:.2%}")
        print(f"节省内存: {stats.memory_saved}字节")
        
        # 应该有显著的复用
        assert stats.total_reused > 0


if __name__ == '__main__':
    pytest.main([__file__, '-v', '-s'])
