"""
言律语言词法分析器 - 上下文管理器

管理词法分析过程中的上下文信息
"""

from typing import List, Optional, Dict, Any, Set
from dataclasses import dataclass, field
from enum import Enum
from lexer_token import Token, TokenType
from utils import Position, Range, ErrorInfo
from error_handler import ErrorHandler, ErrorSeverity


class ContextType(Enum):
    """上下文类型"""
    GLOBAL = "global"
    FUNCTION = "function"
    LOOP = "loop"
    CONDITIONAL = "conditional"
    BLOCK = "block"
    STRING = "string"
    COMMENT = "comment"


@dataclass
class Context:
    """上下文信息"""
    type: ContextType
    start_position: Position
    end_position: Optional[Position] = None
    parent: Optional['Context'] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    tokens: List[Token] = field(default_factory=list)
    
    def __str__(self) -> str:
        """返回上下文字符串表示"""
        return f"Context(type={self.type.value}, start={self.start_position}, end={self.end_position})"
    
    def is_open(self) -> bool:
        """检查上下文是否已打开（未结束）"""
        return self.end_position is None
    
    def close(self, end_position: Position):
        """关闭上下文"""
        self.end_position = end_position
    
    def add_token(self, token: Token):
        """添加词元到上下文"""
        self.tokens.append(token)
    
    def get_tokens(self) -> List[Token]:
        """获取上下文中的词元"""
        return self.tokens.copy()
    
    def get_token_count(self) -> int:
        """获取词元数量"""
        return len(self.tokens)
    
    def get_metadata(self, key: str, default: Any = None) -> Any:
        """获取元数据"""
        return self.metadata.get(key, default)
    
    def set_metadata(self, key: str, value: Any):
        """设置元数据"""
        self.metadata[key] = value
    
    def has_metadata(self, key: str) -> bool:
        """检查是否有指定元数据"""
        return key in self.metadata


class ContextManager:
    """上下文管理器"""
    
    def __init__(self):
        """初始化上下文管理器"""
        self._context_stack: List[Context] = []
        self._global_context = Context(ContextType.GLOBAL, Position(line=1, column=1, offset=0))
        self._current_context = self._global_context
        
        # 上下文统计
        self._context_count = 0
        self._max_depth = 0
        
        # 符号表
        self._symbol_table: Dict[str, Any] = {}
        
        # 错误处理器
        self._error_handler: Optional[ErrorHandler] = None
    
    def push_context(self, context_type: ContextType, start_position: Position, 
                     metadata: Optional[Dict[str, Any]] = None) -> Context:
        """
        推入新上下文
        
        Args:
            context_type: 上下文类型
            start_position: 开始位置
            metadata: 元数据
            
        Returns:
            新创建的上下文
        """
        context = Context(
            type=context_type,
            start_position=start_position,
            parent=self._current_context,
            metadata=metadata or {}
        )
        
        self._context_stack.append(context)
        self._current_context = context
        self._context_count += 1
        self._max_depth = max(self._max_depth, len(self._context_stack))
        
        return context
    
    def pop_context(self, end_position: Position) -> Optional[Context]:
        """
        弹出当前上下文
        
        Args:
            end_position: 结束位置
            
        Returns:
            弹出的上下文，如果栈为空则返回None
        """
        if not self._context_stack:
            return None
        
        context = self._context_stack.pop()
        context.close(end_position)
        
        # 更新当前上下文
        if self._context_stack:
            self._current_context = self._context_stack[-1]
        else:
            self._current_context = self._global_context
        
        return context
    
    def get_current_context(self) -> Context:
        """获取当前上下文"""
        return self._current_context
    
    def get_context_stack(self) -> List[Context]:
        """获取上下文栈"""
        return self._context_stack.copy()
    
    def get_context_depth(self) -> int:
        """获取上下文深度"""
        return len(self._context_stack)
    
    def get_global_context(self) -> Context:
        """获取全局上下文"""
        return self._global_context
    
    def add_token_to_current_context(self, token: Token):
        """添加词元到当前上下文"""
        self._current_context.add_token(token)
    
    def add_token_to_context(self, token: Token, context_type: Optional[ContextType] = None):
        """
        添加词元到指定类型的上下文
        
        Args:
            token: 词元
            context_type: 上下文类型，如果为None则添加到当前上下文
        """
        if context_type is None:
            self._current_context.add_token(token)
        else:
            # 查找指定类型的上下文
            for context in reversed(self._context_stack):
                if context.type == context_type:
                    context.add_token(token)
                    return
            
            # 如果未找到，添加到全局上下文
            self._global_context.add_token(token)
    
    def get_tokens_in_context(self, context_type: ContextType) -> List[Token]:
        """
        获取指定类型上下文中的词元
        
        Args:
            context_type: 上下文类型
            
        Returns:
            词元列表
        """
        tokens = []
        for context in self._context_stack:
            if context.type == context_type:
                tokens.extend(context.get_tokens())
        
        return tokens
    
    def get_all_tokens(self) -> List[Token]:
        """获取所有词元（包括全局上下文）"""
        all_tokens = self._global_context.get_tokens().copy()
        for context in self._context_stack:
            all_tokens.extend(context.get_tokens())
        return all_tokens
    
    def clear_contexts(self):
        """清除所有上下文（除了全局上下文）"""
        self._context_stack.clear()
        self._current_context = self._global_context
        self._global_context.tokens.clear()
        self._global_context.metadata.clear()
    
    def set_error_handler(self, error_handler: ErrorHandler):
        """设置错误处理器"""
        self._error_handler = error_handler
    
    def get_error_handler(self) -> Optional[ErrorHandler]:
        """获取错误处理器"""
        return self._error_handler
    
    # 符号表管理
    def add_symbol(self, name: str, value: Any, symbol_type: str = "variable"):
        """
        添加符号到符号表
        
        Args:
            name: 符号名称
            value: 符号值
            symbol_type: 符号类型
        """
        self._symbol_table[name] = {
            'value': value,
            'type': symbol_type,
            'context': self._current_context.type.value,
            'position': self._current_context.start_position
        }
    
    def get_symbol(self, name: str) -> Optional[Any]:
        """
        从符号表获取符号
        
        Args:
            name: 符号名称
            
        Returns:
            符号值，如果不存在则返回None
        """
        symbol_info = self._symbol_table.get(name)
        return symbol_info['value'] if symbol_info else None
    
    def has_symbol(self, name: str) -> bool:
        """
        检查符号是否存在
        
        Args:
            name: 符号名称
            
        Returns:
            是否存在
        """
        return name in self._symbol_table
    
    def remove_symbol(self, name: str) -> bool:
        """
        从符号表移除符号
        
        Args:
            name: 符号名称
            
        Returns:
            是否成功移除
        """
        if name in self._symbol_table:
            del self._symbol_table[name]
            return True
        return False
    
    def get_symbol_table(self) -> Dict[str, Any]:
        """获取符号表"""
        return self._symbol_table.copy()
    
    def clear_symbol_table(self):
        """清空符号表"""
        self._symbol_table.clear()
    
    # 上下文验证
    def validate_context(self, expected_type: Optional[ContextType] = None) -> bool:
        """
        验证当前上下文
        
        Args:
            expected_type: 期望的上下文类型
            
        Returns:
            是否有效
        """
        if expected_type and self._current_context.type != expected_type:
            if self._error_handler:
                self._error_handler.add_error(
                    code="CONTEXT001",
                    message=f"无效的上下文: 期望 {expected_type.value}, 实际 {self._current_context.type.value}",
                    position=self._current_context.start_position,
                    severity=ErrorSeverity.ERROR,
                    suggestion=f"请确保在 {expected_type.value} 上下文中执行此操作"
                )
            return False
        return True
    
    def ensure_context(self, context_type: ContextType, position: Position) -> bool:
        """
        确保指定类型的上下文存在
        
        Args:
            context_type: 上下文类型
            position: 位置
            
        Returns:
            是否成功
        """
        # 检查当前上下文栈中是否有指定类型的上下文
        for context in self._context_stack:
            if context.type == context_type:
                return True
        
        # 如果没有，创建新的上下文
        self.push_context(context_type, position)
        return True
    
    # 统计信息
    def get_statistics(self) -> Dict[str, Any]:
        """获取统计信息"""
        return {
            'total_contexts': self._context_count,
            'current_depth': len(self._context_stack),
            'max_depth': self._max_depth,
            'symbol_count': len(self._symbol_table),
            'global_token_count': self._global_context.get_token_count(),
            'context_token_counts': {
                context.type.value: context.get_token_count()
                for context in self._context_stack
            }
        }
    
    def reset_statistics(self):
        """重置统计信息"""
        self._context_count = 0
        self._max_depth = 0
    
    # 上下文查找
    def find_context_by_type(self, context_type: ContextType) -> Optional[Context]:
        """
        按类型查找上下文
        
        Args:
            context_type: 上下文类型
            
        Returns:
            上下文，如果未找到则返回None
        """
        for context in reversed(self._context_stack):
            if context.type == context_type:
                return context
        return None
    
    def find_context_by_position(self, position: Position) -> Optional[Context]:
        """
        按位置查找上下文
        
        Args:
            position: 位置
            
        Returns:
            上下文，如果未找到则返回None
        """
        for context in reversed(self._context_stack):
            if context.end_position is None:
                # 未关闭的上下文
                if (position.line >= context.start_position.line and 
                    position.column >= context.start_position.column):
                    return context
            else:
                # 已关闭的上下文
                if (position.line >= context.start_position.line and 
                    position.column >= context.start_position.column and
                    position.line <= context.end_position.line and 
                    position.column <= context.end_position.column):
                    return context
        
        return self._global_context
    
    # 上下文操作
    def enter_function(self, name: str, position: Position, 
                       parameters: Optional[List[str]] = None) -> Context:
        """
        进入函数上下文
        
        Args:
            name: 函数名称
            position: 开始位置
            parameters: 参数列表
            
        Returns:
            函数上下文
        """
        metadata = {
            'name': name,
            'parameters': parameters or [],
            'return_type': None,
            'local_variables': set()
        }
        return self.push_context(ContextType.FUNCTION, position, metadata)
    
    def enter_loop(self, loop_type: str, position: Position) -> Context:
        """
        进入循环上下文
        
        Args:
            loop_type: 循环类型 ('for', 'while', 'foreach')
            position: 开始位置
            
        Returns:
            循环上下文
        """
        metadata = {
            'loop_type': loop_type,
            'break_count': 0,
            'continue_count': 0
        }
        return self.push_context(ContextType.LOOP, position, metadata)
    
    def enter_conditional(self, condition: str, position: Position) -> Context:
        """
        进入条件上下文
        
        Args:
            condition: 条件表达式
            position: 开始位置
            
        Returns:
            条件上下文
        """
        metadata = {
            'condition': condition,
            'has_else': False
        }
        return self.push_context(ContextType.CONDITIONAL, position, metadata)
    
    def enter_block(self, block_type: str, position: Position) -> Context:
        """
        进入块上下文
        
        Args:
            block_type: 块类型
            position: 开始位置
            
        Returns:
            块上下文
        """
        metadata = {
            'block_type': block_type
        }
        return self.push_context(ContextType.BLOCK, position, metadata)
    
    def __str__(self) -> str:
        """返回上下文管理器描述"""
        stats = self.get_statistics()
        return (
            f"ContextManager("
            f"depth={stats['current_depth']}, "
            f"contexts={stats['total_contexts']}, "
            f"symbols={stats['symbol_count']}"
            f")"
        )
    
    def __repr__(self) -> str:
        """返回上下文管理器表示"""
        return self.__str__()


# 工厂函数
def create_context_manager() -> ContextManager:
    """创建上下文管理器"""
    return ContextManager()


def get_default_context_manager() -> ContextManager:
    """获取默认上下文管理器"""
    return ContextManager()
