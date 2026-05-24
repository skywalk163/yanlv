"""
言律语言词法分析器 - 词元定义

包含Token类和TokenType枚举
"""

from enum import Enum
from typing import Any, Dict, Optional
from dataclasses import dataclass, asdict


class TokenType(Enum):
    """词元类型枚举"""
    # 标识符
    IDENTIFIER = "IDENTIFIER"
    
    # 字面量
    NUMBER = "NUMBER"
    STRING = "STRING"
    BOOLEAN = "BOOLEAN"
    
    # 关键词
    IF = "IF"
    ELSE = "ELSE"
    ELIF = "ELIF"
    WHEN = "WHEN"
    THEN = "THEN"
    FOR = "FOR"
    IN = "IN"
    WHILE = "WHILE"
    DEF = "DEF"
    SET = "SET"
    IS = "IS"
    RETURN = "RETURN"
    END = "END"
    LOOP = "LOOP"
    FOR_EACH = "FOR_EACH"
    UNTIL = "UNTIL"

    # 言律语言特定关键词
    OUTPUT = "OUTPUT"      # 输出
    DEFINE = "DEFINE"      # 定义
    FUNCTION = "FUNCTION"  # 函数
    VARIABLE = "VARIABLE"  # 变量
    PARAMETER = "PARAMETER"  # 参数
    
    # 运算符
    PLUS = "PLUS"
    MINUS = "MINUS"
    MULTIPLY = "MULTIPLY"
    DIVIDE = "DIVIDE"
    MODULO = "MODULO"
    POWER = "POWER"
    EQUAL = "EQUAL"
    NOT_EQUAL = "NOT_EQUAL"
    LESS = "LESS"
    GREATER = "GREATER"
    LESS_EQUAL = "LESS_EQUAL"
    GREATER_EQUAL = "GREATER_EQUAL"
    AND = "AND"
    OR = "OR"
    NOT = "NOT"
    
    # 分组符号
    LPAREN = "LPAREN"
    RPAREN = "RPAREN"
    LBRACKET = "LBRACKET"
    RBRACKET = "RBRACKET"
    LBRACE = "LBRACE"
    RBRACE = "RBRACE"
    
    # 标点符号
    PERIOD = "PERIOD"
    COMMA = "COMMA"
    SEMICOLON = "SEMICOLON"
    COLON = "COLON"
    ENUMERATION = "ENUMERATION"
    EXCLAMATION = "EXCLAMATION"
    QUESTION = "QUESTION"
    BOOK_TITLE = "BOOK_TITLE"
    ELLIPSIS = "ELLIPSIS"
    DASH = "DASH"
    TILDE = "TILDE"
    MIDDLE_DOT = "MIDDLE_DOT"
    SQUARE_BRACKETS = "SQUARE_BRACKETS"
    
    # 动词
    VERB = "VERB"
    
    # 其他
    NEWLINE = "NEWLINE"
    EOF = "EOF"
    COMMENT = "COMMENT"
    ERROR = "ERROR"


@dataclass
class Token:
    """词元类"""
    type: TokenType
    value: str
    line: int
    column: int
    literal: str
    
    def __str__(self) -> str:
        """返回词元的字符串表示"""
        return f"Token({self.type.value}, '{self.value}', line={self.line}, col={self.column})"
    
    def __repr__(self) -> str:
        """返回词元的表示"""
        return self.__str__()
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'type': self.type.value,
            'value': self.value,
            'line': self.line,
            'column': self.column,
            'literal': self.literal
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Token':
        """从字典创建"""
        return cls(
            type=TokenType(data['type']),
            value=data['value'],
            line=data['line'],
            column=data['column'],
            literal=data['literal']
        )
    
    def is_type(self, token_type: TokenType) -> bool:
        """检查词元类型"""
        return self.type == token_type
    
    def is_identifier(self) -> bool:
        """检查是否为标识符"""
        return self.type == TokenType.IDENTIFIER
    
    def is_number(self) -> bool:
        """检查是否为数字"""
        return self.type == TokenType.NUMBER
    
    def is_string(self) -> bool:
        """检查是否为字符串"""
        return self.type == TokenType.STRING
    
    def is_boolean(self) -> bool:
        """检查是否为布尔值"""
        return self.type == TokenType.BOOLEAN
    
    def is_keyword(self) -> bool:
        """检查是否为关键词"""
        return self.type in [
            TokenType.IF, TokenType.ELSE, TokenType.ELIF, TokenType.WHEN,
            TokenType.THEN, TokenType.FOR, TokenType.IN, TokenType.WHILE,
            TokenType.DEF, TokenType.SET, TokenType.IS, TokenType.RETURN,
            TokenType.END, TokenType.LOOP, TokenType.FOR_EACH, TokenType.UNTIL
        ]
    
    def is_operator(self) -> bool:
        """检查是否为运算符"""
        return self.type in [
            TokenType.PLUS, TokenType.MINUS, TokenType.MULTIPLY, TokenType.DIVIDE,
            TokenType.MODULO, TokenType.POWER, TokenType.EQUAL, TokenType.NOT_EQUAL,
            TokenType.LESS, TokenType.GREATER, TokenType.LESS_EQUAL, TokenType.GREATER_EQUAL,
            TokenType.AND, TokenType.OR, TokenType.NOT
        ]
    
    def is_punctuation(self) -> bool:
        """检查是否为标点符号"""
        return self.type in [
            TokenType.PERIOD, TokenType.COMMA, TokenType.SEMICOLON, TokenType.COLON,
            TokenType.ENUMERATION, TokenType.EXCLAMATION, TokenType.QUESTION,
            TokenType.BOOK_TITLE, TokenType.ELLIPSIS, TokenType.DASH,
            TokenType.TILDE, TokenType.MIDDLE_DOT, TokenType.SQUARE_BRACKETS
        ]
    
    def is_grouping_symbol(self) -> bool:
        """检查是否为分组符号"""
        return self.type in [
            TokenType.LPAREN, TokenType.RPAREN, TokenType.LBRACKET,
            TokenType.RBRACKET, TokenType.LBRACE, TokenType.RBRACE
        ]
    
    def is_verb(self) -> bool:
        """检查是否为动词"""
        return self.type == TokenType.VERB
    
    def is_comment(self) -> bool:
        """检查是否为注释"""
        return self.type == TokenType.COMMENT
    
    def is_error(self) -> bool:
        """检查是否为错误"""
        return self.type == TokenType.ERROR
    
    def is_eof(self) -> bool:
        """检查是否为文件结束符"""
        return self.type == TokenType.EOF
    
    def is_newline(self) -> bool:
        """检查是否为换行符"""
        return self.type == TokenType.NEWLINE
    
    def get_position(self) -> str:
        """获取位置字符串"""
        return f"line {self.line}, column {self.column}"
    
    def clone(self) -> 'Token':
        """克隆词元"""
        return Token(
            type=self.type,
            value=self.value,
            line=self.line,
            column=self.column,
            literal=self.literal
        )


# 工具函数
def create_token(token_type: TokenType, value: str, line: int, column: int) -> Token:
    """
    创建词元
    
    Args:
        token_type: 词元类型
        value: 词元值
        line: 行号
        column: 列号
        
    Returns:
        词元对象
    """
    return Token(
        type=token_type,
        value=value,
        line=line,
        column=column,
        literal=value
    )


def create_eof_token(line: int, column: int) -> Token:
    """
    创建EOF词元
    
    Args:
        line: 行号
        column: 列号
        
    Returns:
        EOF词元
    """
    return create_token(TokenType.EOF, "", line, column)


def create_newline_token(line: int, column: int) -> Token:
    """
    创建换行词元
    
    Args:
        line: 行号
        column: 列号
        
    Returns:
        换行词元
    """
    return create_token(TokenType.NEWLINE, "\n", line, column)


def create_error_token(value: str, line: int, column: int) -> Token:
    """
    创建错误词元
    
    Args:
        value: 错误值
        line: 行号
        column: 列号
        
    Returns:
        错误词元
    """
    return create_token(TokenType.ERROR, value, line, column)


def token_list_to_dict(tokens: list[Token]) -> list[Dict[str, Any]]:
    """
    将词元列表转换为字典列表
    
    Args:
        tokens: 词元列表
        
    Returns:
        字典列表
    """
    return [token.to_dict() for token in tokens]


def dict_list_to_tokens(token_dicts: list[Dict[str, Any]]) -> list[Token]:
    """
    将字典列表转换为词元列表
    
    Args:
        token_dicts: 字典列表
        
    Returns:
        词元列表
    """
    return [Token.from_dict(token_dict) for token_dict in token_dicts]