"""
言律语言AST节点定义

定义抽象语法树的节点类型
"""

from typing import List, Optional, Any, Dict
from dataclasses import dataclass, field
from enum import Enum


class NodeType(Enum):
    """AST节点类型"""
    # 程序
    PROGRAM = "Program"
    
    # 声明
    VARIABLE_DECL = "VariableDeclaration"
    FUNCTION_DECL = "FunctionDeclaration"
    
    # 语句
    EXPRESSION_STMT = "ExpressionStatement"
    IF_STMT = "IfStatement"
    WHILE_STMT = "WhileStatement"
    FOR_STMT = "ForStatement"
    RETURN_STMT = "ReturnStatement"
    OUTPUT_STMT = "OutputStatement"
    
    # 表达式
    BINARY_EXPR = "BinaryExpression"
    UNARY_EXPR = "UnaryExpression"
    CALL_EXPR = "CallExpression"
    MEMBER_EXPR = "MemberExpression"
    IDENTIFIER = "Identifier"
    LITERAL = "Literal"
    ARRAY_LITERAL = "ArrayLiteral"
    
    # 其他
    BLOCK = "Block"
    PARAMETER = "Parameter"


@dataclass
class ASTNode:
    """AST节点基类"""
    node_type: NodeType
    line: int = 0
    column: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __str__(self) -> str:
        return f"{self.node_type.value}"
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "type": self.node_type.value,
            "line": self.line,
            "column": self.column,
            "metadata": self.metadata
        }


@dataclass
class Program(ASTNode):
    """程序节点"""
    statements: List[ASTNode] = field(default_factory=list)
    
    def __init__(self, statements: List[ASTNode] = None):
        super().__init__(NodeType.PROGRAM)
        self.statements = statements or []
    
    def to_dict(self) -> Dict[str, Any]:
        result = super().to_dict()
        result["statements"] = [stmt.to_dict() for stmt in self.statements]
        return result


@dataclass
class VariableDeclaration(ASTNode):
    """变量声明"""
    name: str = ""
    initializer: Optional[ASTNode] = None
    
    def __init__(self, name: str, initializer: ASTNode = None):
        super().__init__(NodeType.VARIABLE_DECL)
        self.name = name
        self.initializer = initializer
    
    def to_dict(self) -> Dict[str, Any]:
        result = super().to_dict()
        result["name"] = self.name
        if self.initializer:
            result["initializer"] = self.initializer.to_dict()
        return result


@dataclass
class FunctionDeclaration(ASTNode):
    """函数声明"""
    name: str = ""
    parameters: List[str] = field(default_factory=list)
    body: List[ASTNode] = field(default_factory=list)
    
    def __init__(self, name: str, parameters: List[str] = None, body: List[ASTNode] = None):
        super().__init__(NodeType.FUNCTION_DECL)
        self.name = name
        self.parameters = parameters or []
        self.body = body or []
    
    def to_dict(self) -> Dict[str, Any]:
        result = super().to_dict()
        result["name"] = self.name
        result["parameters"] = self.parameters
        result["body"] = [stmt.to_dict() for stmt in self.body]
        return result


@dataclass
class IfStatement(ASTNode):
    """条件语句"""
    condition: Optional[ASTNode] = None
    consequent: List[ASTNode] = field(default_factory=list)
    alternate: List[ASTNode] = field(default_factory=list)
    
    def __init__(self, condition: ASTNode, consequent: List[ASTNode] = None, alternate: List[ASTNode] = None):
        super().__init__(NodeType.IF_STMT)
        self.condition = condition
        self.consequent = consequent or []
        self.alternate = alternate or []
    
    def to_dict(self) -> Dict[str, Any]:
        result = super().to_dict()
        if self.condition:
            result["condition"] = self.condition.to_dict()
        result["consequent"] = [stmt.to_dict() for stmt in self.consequent]
        result["alternate"] = [stmt.to_dict() for stmt in self.alternate]
        return result


@dataclass
class WhileStatement(ASTNode):
    """循环语句"""
    condition: Optional[ASTNode] = None
    body: List[ASTNode] = field(default_factory=list)
    
    def __init__(self, condition: ASTNode, body: List[ASTNode] = None):
        super().__init__(NodeType.WHILE_STMT)
        self.condition = condition
        self.body = body or []
    
    def to_dict(self) -> Dict[str, Any]:
        result = super().to_dict()
        if self.condition:
            result["condition"] = self.condition.to_dict()
        result["body"] = [stmt.to_dict() for stmt in self.body]
        return result


@dataclass
class ForStatement(ASTNode):
    """For循环语句"""
    init: Optional[ASTNode] = None
    condition: Optional[ASTNode] = None
    update: Optional[ASTNode] = None
    body: List[ASTNode] = field(default_factory=list)
    
    def __init__(self, init: ASTNode = None, condition: ASTNode = None, 
                 update: ASTNode = None, body: List[ASTNode] = None):
        super().__init__(NodeType.FOR_STMT)
        self.init = init
        self.condition = condition
        self.update = update
        self.body = body or []
    
    def to_dict(self) -> Dict[str, Any]:
        result = super().to_dict()
        if self.init:
            result["init"] = self.init.to_dict()
        if self.condition:
            result["condition"] = self.condition.to_dict()
        if self.update:
            result["update"] = self.update.to_dict()
        result["body"] = [stmt.to_dict() for stmt in self.body]
        return result


@dataclass
class ReturnStatement(ASTNode):
    """返回语句"""
    value: Optional[ASTNode] = None
    
    def __init__(self, value: ASTNode = None):
        super().__init__(NodeType.RETURN_STMT)
        self.value = value
    
    def to_dict(self) -> Dict[str, Any]:
        result = super().to_dict()
        if self.value:
            result["value"] = self.value.to_dict()
        return result


@dataclass
class OutputStatement(ASTNode):
    """输出语句"""
    value: Optional[ASTNode] = None
    
    def __init__(self, value: ASTNode = None):
        super().__init__(NodeType.OUTPUT_STMT)
        self.value = value
    
    def to_dict(self) -> Dict[str, Any]:
        result = super().to_dict()
        if self.value:
            result["value"] = self.value.to_dict()
        return result


@dataclass
class BinaryExpression(ASTNode):
    """二元表达式"""
    operator: str = ""
    left: Optional[ASTNode] = None
    right: Optional[ASTNode] = None
    
    def __init__(self, operator: str, left: ASTNode, right: ASTNode):
        super().__init__(NodeType.BINARY_EXPR)
        self.operator = operator
        self.left = left
        self.right = right
    
    def to_dict(self) -> Dict[str, Any]:
        result = super().to_dict()
        result["operator"] = self.operator
        if self.left:
            result["left"] = self.left.to_dict()
        if self.right:
            result["right"] = self.right.to_dict()
        return result


@dataclass
class UnaryExpression(ASTNode):
    """一元表达式"""
    operator: str = ""
    operand: Optional[ASTNode] = None
    
    def __init__(self, operator: str, operand: ASTNode):
        super().__init__(NodeType.UNARY_EXPR)
        self.operator = operator
        self.operand = operand
    
    def to_dict(self) -> Dict[str, Any]:
        result = super().to_dict()
        result["operator"] = self.operator
        if self.operand:
            result["operand"] = self.operand.to_dict()
        return result


@dataclass
class CallExpression(ASTNode):
    """函数调用表达式"""
    callee: str = ""
    arguments: List[ASTNode] = field(default_factory=list)
    
    def __init__(self, callee: str, arguments: List[ASTNode] = None):
        super().__init__(NodeType.CALL_EXPR)
        self.callee = callee
        self.arguments = arguments or []
    
    def to_dict(self) -> Dict[str, Any]:
        result = super().to_dict()
        result["callee"] = self.callee
        result["arguments"] = [arg.to_dict() for arg in self.arguments]
        return result


@dataclass
class MemberExpression(ASTNode):
    """成员访问表达式"""
    obj: Optional[ASTNode] = None
    prop: Optional[ASTNode] = None
    
    def __init__(self, obj: ASTNode, prop: ASTNode):
        super().__init__(NodeType.MEMBER_EXPR)
        self.obj = obj
        self.prop = prop
    
    def to_dict(self) -> Dict[str, Any]:
        result = super().to_dict()
        if self.obj:
            result["object"] = self.obj.to_dict()
        if self.prop:
            result["property"] = self.prop.to_dict()
        return result


@dataclass
class Identifier(ASTNode):
    """标识符"""
    name: str = ""
    
    def __init__(self, name: str):
        super().__init__(NodeType.IDENTIFIER)
        self.name = name
    
    def to_dict(self) -> Dict[str, Any]:
        result = super().to_dict()
        result["name"] = self.name
        return result


@dataclass
class Literal(ASTNode):
    """字面量"""
    value: Any = None
    literal_type: str = ""  # 'number', 'string', 'boolean'
    
    def __init__(self, value: Any, literal_type: str):
        super().__init__(NodeType.LITERAL)
        self.value = value
        self.literal_type = literal_type
    
    def to_dict(self) -> Dict[str, Any]:
        result = super().to_dict()
        result["value"] = self.value
        result["literalType"] = self.literal_type
        return result


@dataclass
class ArrayLiteral(ASTNode):
    """数组字面量"""
    elements: List[ASTNode] = field(default_factory=list)
    
    def __init__(self, elements: List[ASTNode] = None):
        super().__init__(NodeType.ARRAY_LITERAL)
        self.elements = elements or []
    
    def to_dict(self) -> Dict[str, Any]:
        result = super().to_dict()
        result["elements"] = [elem.to_dict() for elem in self.elements]
        return result


# ============================================================================
# 导出
# ============================================================================

__all__ = [
    'NodeType',
    'ASTNode',
    'Program',
    'VariableDeclaration',
    'FunctionDeclaration',
    'IfStatement',
    'WhileStatement',
    'ForStatement',
    'ReturnStatement',
    'OutputStatement',
    'BinaryExpression',
    'UnaryExpression',
    'CallExpression',
    'MemberExpression',
    'Identifier',
    'Literal',
    'ArrayLiteral',
]
