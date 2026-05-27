"""
言律语言AST节点对象池

实现AST节点对象池,减少节点创建和销毁的开销,降低内存占用
"""

from typing import Dict, List, Any, Optional, Type, TypeVar
from dataclasses import dataclass, field
import time
from .ast_nodes import (
    ASTNode, NodeType, Program, VariableDeclaration, 
    FunctionDeclaration, IfStatement,
    WhileStatement, ForStatement, ReturnStatement, OutputStatement,
    BinaryExpression, UnaryExpression, CallExpression, MemberExpression,
    Identifier, Literal, ArrayLiteral
)


T = TypeVar('T', bound=ASTNode)


@dataclass
class PoolStats:
    """对象池统计信息"""
    total_created: int = 0       # 总创建次数
    total_reused: int = 0        # 总复用次数
    total_released: int = 0      # 总释放次数
    current_pooled: int = 0      # 当前池中数量
    max_pooled: int = 1000       # 最大池容量
    memory_saved: int = 0        # 节省的内存(字节)
    
    @property
    def reuse_rate(self) -> float:
        """复用率"""
        total = self.total_created + self.total_reused
        return self.total_reused / total if total > 0 else 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'total_created': self.total_created,
            'total_reused': self.total_reused,
            'total_released': self.total_released,
            'current_pooled': self.current_pooled,
            'max_pooled': self.max_pooled,
            'reuse_rate': f"{self.reuse_rate:.2%}",
            'memory_saved_bytes': self.memory_saved
        }


class ASTNodePool:
    """
    AST节点对象池
    
    通过对象复用减少内存分配和垃圾回收开销
    
    Attributes:
        pools: 各类型节点的对象池
        stats: 统计信息
        enabled: 是否启用对象池
    """
    
    def __init__(self, max_pool_size: int = 1000, enabled: bool = True):
        """
        初始化对象池
        
        Args:
            max_pool_size: 每种类型节点的最大池容量
            enabled: 是否启用对象池
        """
        self.pools: Dict[NodeType, List[ASTNode]] = {}
        self.max_pool_size = max_pool_size
        self.enabled = enabled
        self.stats = PoolStats(max_pooled=max_pool_size)
        
        # 初始化各类型节点的池
        self._init_pools()
    
    def _init_pools(self):
        """初始化所有节点类型的池"""
        node_types = [
            NodeType.PROGRAM,
            NodeType.VARIABLE_DECL,
            NodeType.FUNCTION_DECL,
            NodeType.IF_STMT,
            NodeType.WHILE_STMT,
            NodeType.FOR_STMT,
            NodeType.RETURN_STMT,
            NodeType.OUTPUT_STMT,
            NodeType.BINARY_EXPR,
            NodeType.UNARY_EXPR,
            NodeType.CALL_EXPR,
            NodeType.MEMBER_EXPR,
            NodeType.IDENTIFIER,
            NodeType.LITERAL,
            NodeType.ARRAY_LITERAL,
        ]
        
        for node_type in node_types:
            self.pools[node_type] = []
    
    def acquire(self, node_type: NodeType) -> Optional[ASTNode]:
        """
        从池中获取节点对象
        
        Args:
            node_type: 节点类型
            
        Returns:
            节点对象(如果池中有),否则返回None
        """
        if not self.enabled:
            return None
        
        pool = self.pools.get(node_type)
        if pool and len(pool) > 0:
            node = pool.pop()
            self.stats.total_reused += 1
            self.stats.current_pooled = sum(len(p) for p in self.pools.values())
            return node
        
        return None
    
    def release(self, node: ASTNode) -> None:
        """
        将节点对象释放回池中
        
        Args:
            node: 要释放的节点对象
        """
        if not self.enabled:
            return
        
        node_type = node.node_type
        pool = self.pools.get(node_type)
        
        if pool is not None and len(pool) < self.max_pool_size:
            # 重置节点状态
            self._reset_node(node)
            pool.append(node)
            self.stats.total_released += 1
            self.stats.current_pooled = sum(len(p) for p in self.pools.values())
    
    def _reset_node(self, node: ASTNode) -> None:
        """
        重置节点状态
        
        Args:
            node: 要重置的节点
        """
        node.line = 0
        node.column = 0
        node.metadata.clear()
        
        # 根据节点类型重置特定字段
        if isinstance(node, Program):
            node.statements = []
        elif isinstance(node, VariableDeclaration):
            node.name = ""
            node.initializer = None
        elif isinstance(node, FunctionDeclaration):
            node.name = ""
            node.params = []
            node.body = None
        elif isinstance(node, ExpressionStatement):
            node.expression = None
        elif isinstance(node, IfStatement):
            node.condition = None
            node.then_branch = None
            node.else_branch = None
        elif isinstance(node, WhileStatement):
            node.condition = None
            node.body = None
        elif isinstance(node, ForStatement):
            node.init = None
            node.condition = None
            node.update = None
            node.body = None
        elif isinstance(node, ReturnStatement):
            node.value = None
        elif isinstance(node, OutputStatement):
            node.expression = None
        elif isinstance(node, BinaryExpression):
            node.left = None
            node.operator = ""
            node.right = None
        elif isinstance(node, UnaryExpression):
            node.operator = ""
            node.operand = None
        elif isinstance(node, CallExpression):
            node.callee = None
            node.arguments = []
        elif isinstance(node, MemberExpression):
            node.object = None
            node.property = None
        elif isinstance(node, Identifier):
            node.name = ""
        elif isinstance(node, Literal):
            node.value = None
        elif isinstance(node, ArrayLiteral):
            node.elements = []
        elif isinstance(node, Block):
            node.statements = []
        elif isinstance(node, Parameter):
            node.name = ""
            node.default_value = None
    
    def create_node(self, node_class: Type[T], *args, **kwargs) -> T:
        """
        创建或复用节点对象
        
        Args:
            node_class: 节点类
            *args: 位置参数
            **kwargs: 关键字参数
            
        Returns:
            节点对象
        """
        # 尝试从池中获取
        node_type = self._get_node_type(node_class)
        node = self.acquire(node_type)
        
        if node is not None:
            # 复用节点,设置新属性
            self._set_node_attrs(node, *args, **kwargs)
            return node
        
        # 创建新节点
        node = node_class(*args, **kwargs)
        self.stats.total_created += 1
        self.stats.memory_saved += self._estimate_node_size(node)
        
        return node
    
    def _get_node_type(self, node_class: Type[T]) -> NodeType:
        """获取节点类型"""
        type_mapping = {
            Program: NodeType.PROGRAM,
            VariableDeclaration: NodeType.VARIABLE_DECL,
            FunctionDeclaration: NodeType.FUNCTION_DECL,
            IfStatement: NodeType.IF_STMT,
            WhileStatement: NodeType.WHILE_STMT,
            ForStatement: NodeType.FOR_STMT,
            ReturnStatement: NodeType.RETURN_STMT,
            OutputStatement: NodeType.OUTPUT_STMT,
            BinaryExpression: NodeType.BINARY_EXPR,
            UnaryExpression: NodeType.UNARY_EXPR,
            CallExpression: NodeType.CALL_EXPR,
            MemberExpression: NodeType.MEMBER_EXPR,
            Identifier: NodeType.IDENTIFIER,
            Literal: NodeType.LITERAL,
            ArrayLiteral: NodeType.ARRAY_LITERAL,
        }
        return type_mapping.get(node_class, NodeType.PROGRAM)
    
    def _set_node_attrs(self, node: T, *args, **kwargs) -> None:
        """设置节点属性"""
        # 这里简化处理,实际使用时需要根据具体节点类型设置属性
        for key, value in kwargs.items():
            if hasattr(node, key):
                setattr(node, key, value)
    
    def _estimate_node_size(self, node: ASTNode) -> int:
        """
        估算节点内存大小
        
        Args:
            node: 节点对象
            
        Returns:
            估算的字节数
        """
        # 基础大小: 64字节
        base_size = 64
        
        # 根据节点类型估算
        if isinstance(node, Program):
            # 包含语句列表
            return base_size + len(getattr(node, 'statements', [])) * 8
        elif isinstance(node, FunctionDeclaration):
            # 包含参数和函数体
            return base_size + len(getattr(node, 'params', [])) * 8 + 64
        elif isinstance(node, CallExpression):
            # 包含参数列表
            return base_size + len(getattr(node, 'arguments', [])) * 8
        elif isinstance(node, ArrayLiteral):
            # 包含元素列表
            return base_size + len(getattr(node, 'elements', [])) * 8
        else:
            return base_size
    
    def clear(self) -> None:
        """清空所有池"""
        for pool in self.pools.values():
            pool.clear()
        self.stats.current_pooled = 0
    
    def get_stats(self) -> PoolStats:
        """获取统计信息"""
        self.stats.current_pooled = sum(len(p) for p in self.pools.values())
        return self.stats
    
    def enable(self) -> None:
        """启用对象池"""
        self.enabled = True
    
    def disable(self) -> None:
        """禁用对象池"""
        self.enabled = False
    
    def resize(self, new_size: int) -> None:
        """
        调整池大小
        
        Args:
            new_size: 新的最大池容量
        """
        self.max_pool_size = new_size
        self.stats.max_pooled = new_size
        
        # 如果当前池超过新大小,删除多余的
        for node_type, pool in self.pools.items():
            while len(pool) > new_size:
                pool.pop()
        
        self.stats.current_pooled = sum(len(p) for p in self.pools.values())
    
    def warmup(self, node_types: List[NodeType], count: int = 10) -> None:
        """
        预热对象池
        
        Args:
            node_types: 要预热的节点类型列表
            count: 每种类型预创建的数量
        """
        for node_type in node_types:
            pool = self.pools.get(node_type)
            if pool is not None:
                for _ in range(count):
                    node = self._create_default_node(node_type)
                    if node is not None:
                        pool.append(node)
        
        self.stats.current_pooled = sum(len(p) for p in self.pools.values())
    
    def _create_default_node(self, node_type: NodeType) -> Optional[ASTNode]:
        """创建默认节点"""
        try:
            if node_type == NodeType.PROGRAM:
                return Program()
            elif node_type == NodeType.VARIABLE_DECL:
                return VariableDeclaration("", None)
            elif node_type == NodeType.IDENTIFIER:
                return Identifier("")
            elif node_type == NodeType.LITERAL:
                return Literal(None)
            # 其他类型可以按需添加
            return None
        except:
            return None
    
    def __len__(self) -> int:
        """获取池中总对象数"""
        return sum(len(pool) for pool in self.pools.values())
    
    def __repr__(self) -> str:
        """字符串表示"""
        return (
            f"ASTNodePool(pooled={len(self)}, "
            f"reuse_rate={self.stats.reuse_rate:.2%}, "
            f"enabled={self.enabled})"
        )


# 全局对象池实例
_global_pool: Optional[ASTNodePool] = None


def get_global_pool() -> ASTNodePool:
    """获取全局对象池"""
    global _global_pool
    if _global_pool is None:
        _global_pool = ASTNodePool()
    return _global_pool


def create_pool(max_pool_size: int = 1000, enabled: bool = True) -> ASTNodePool:
    """创建新的对象池"""
    return ASTNodePool(max_pool_size, enabled)
