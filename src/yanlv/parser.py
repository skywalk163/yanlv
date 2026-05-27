"""
言律语言语法分析器

将Token序列转换为AST
"""

from typing import List, Optional, Tuple
from .lexer.lexer_token import Token, TokenType
from .ast_nodes import (
    Program, VariableDeclaration, FunctionDeclaration,
    IfStatement, WhileStatement, ForStatement, ReturnStatement,
    OutputStatement, BinaryExpression, UnaryExpression, CallExpression,
    MemberExpression, Identifier, Literal, ArrayLiteral, ASTNode
)


class Parser:
    """语法分析器"""
    
    def __init__(self, tokens: List[Token]):
        """初始化解析器"""
        self.tokens = tokens
        self.current = 0
    
    def parse(self) -> Program:
        """
        解析程序
        
        Returns:
            程序AST节点
        """
        statements = []
        
        while not self._is_at_end():
            stmt = self._parse_statement()
            if stmt:
                statements.append(stmt)
        
        return Program(statements)
    
    def _is_at_end(self) -> bool:
        """检查是否到达末尾"""
        return self.current >= len(self.tokens)
    
    def _peek(self) -> Optional[Token]:
        """查看当前token"""
        if self._is_at_end():
            return None
        return self.tokens[self.current]
    
    def _previous(self) -> Optional[Token]:
        """查看前一个token"""
        if self.current == 0:
            return None
        return self.tokens[self.current - 1]
    
    def _advance(self) -> Optional[Token]:
        """前进并返回当前token"""
        if not self._is_at_end():
            self.current += 1
        return self._previous()
    
    def _match(self, *types: TokenType) -> bool:
        """匹配token类型"""
        for token_type in types:
            if self._check(token_type):
                self._advance()
                return True
        return False
    
    def _check(self, token_type: TokenType) -> bool:
        """检查当前token类型"""
        if self._is_at_end():
            return False
        return self._peek().type == token_type
    
    def _parse_statement(self) -> Optional[ASTNode]:
        """解析语句"""
        if self._match(TokenType.DEFINE):
            return self._parse_variable_declaration()
        elif self._match(TokenType.FUNCTION):
            return self._parse_function_declaration()
        elif self._match(TokenType.IF):
            return self._parse_if_statement()
        elif self._match(TokenType.WHILE):
            return self._parse_while_statement()
        elif self._match(TokenType.FOR):
            return self._parse_for_statement()
        elif self._match(TokenType.RETURN):
            return self._parse_return_statement()
        elif self._match(TokenType.OUTPUT):
            return self._parse_output_statement()
        elif self._match(TokenType.NEWLINE):
            return None
        else:
            # 跳过未知token
            self._advance()
            return None
    
    def _parse_variable_declaration(self) -> VariableDeclaration:
        """解析变量声明"""
        # 跳过 VARIABLE 关键字
        self._match(TokenType.VARIABLE)
        
        # 获取变量名
        name = ""
        if self._check(TokenType.IDENTIFIER):
            name = self._advance().value
        
        # 跳过 IS
        self._match(TokenType.IS)
        
        # 解析初始值
        initializer = self._parse_expression()
        
        return VariableDeclaration(name, initializer)
    
    def _parse_function_declaration(self) -> FunctionDeclaration:
        """解析函数声明"""
        # 获取函数名
        name = ""
        if self._check(TokenType.IDENTIFIER):
            name = self._advance().value
        
        # 跳过 PARAMETER
        self._match(TokenType.PARAMETER)
        
        # 获取参数列表
        parameters = []
        while self._check(TokenType.IDENTIFIER):
            parameters.append(self._advance().value)
        
        # 解析函数体
        body = []
        while not self._check(TokenType.END) and not self._is_at_end():
            stmt = self._parse_statement()
            if stmt:
                body.append(stmt)
        
        # 跳过 END
        self._match(TokenType.END)
        
        return FunctionDeclaration(name, parameters, body)
    
    def _parse_if_statement(self) -> IfStatement:
        """解析条件语句"""
        # 解析条件
        condition = self._parse_expression()
        
        # 跳过 THEN
        self._match(TokenType.THEN)
        
        # 解析 consequent
        consequent = []
        while not self._check(TokenType.ELSE) and not self._check(TokenType.END) and not self._is_at_end():
            stmt = self._parse_statement()
            if stmt:
                consequent.append(stmt)
        
        # 解析 alternate
        alternate = []
        if self._match(TokenType.ELSE):
            while not self._check(TokenType.END) and not self._is_at_end():
                stmt = self._parse_statement()
                if stmt:
                    alternate.append(stmt)
        
        # 跳过 END
        self._match(TokenType.END)
        
        return IfStatement(condition, consequent, alternate)
    
    def _parse_while_statement(self) -> WhileStatement:
        """解析While循环"""
        # 解析条件
        condition = self._parse_expression()
        
        # 解析循环体
        body = []
        while not self._check(TokenType.END) and not self._is_at_end():
            stmt = self._parse_statement()
            if stmt:
                body.append(stmt)
        
        # 跳过 END
        self._match(TokenType.END)
        
        return WhileStatement(condition, body)
    
    def _parse_for_statement(self) -> ForStatement:
        """解析For循环"""
        # 简化实现
        init = None
        condition = None
        update = None
        
        # 解析循环体
        body = []
        while not self._check(TokenType.END) and not self._is_at_end():
            stmt = self._parse_statement()
            if stmt:
                body.append(stmt)
        
        # 跳过 END
        self._match(TokenType.END)
        
        return ForStatement(init, condition, update, body)
    
    def _parse_return_statement(self) -> ReturnStatement:
        """解析返回语句"""
        value = None
        if not self._check(TokenType.NEWLINE) and not self._is_at_end():
            value = self._parse_expression()
        
        return ReturnStatement(value)
    
    def _parse_output_statement(self) -> OutputStatement:
        """解析输出语句"""
        value = self._parse_expression()
        return OutputStatement(value)
    
    def _parse_expression(self) -> ASTNode:
        """解析表达式"""
        return self._parse_additive()
    
    def _parse_additive(self) -> ASTNode:
        """解析加减表达式"""
        left = self._parse_multiplicative()
        
        while self._match(TokenType.PLUS, TokenType.MINUS):
            operator = self._previous().value
            right = self._parse_multiplicative()
            left = BinaryExpression(operator, left, right)
        
        return left
    
    def _parse_multiplicative(self) -> ASTNode:
        """解析乘除表达式"""
        left = self._parse_unary()
        
        while self._match(TokenType.MULTIPLY, TokenType.DIVIDE, TokenType.MODULO):
            operator = self._previous().value
            right = self._parse_unary()
            left = BinaryExpression(operator, left, right)
        
        return left
    
    def _parse_unary(self) -> ASTNode:
        """解析一元表达式"""
        if self._match(TokenType.MINUS):
            operator = self._previous().value
            right = self._parse_primary()
            return UnaryExpression(operator, right)
        
        return self._parse_primary()
    
    def _parse_primary(self) -> ASTNode:
        """解析基本表达式"""
        # 数字
        if self._match(TokenType.NUMBER):
            return Literal(self._previous().value, 'number')
        
        # 字符串
        if self._match(TokenType.STRING):
            return Literal(self._previous().value, 'string')
        
        # 布尔值
        if self._match(TokenType.BOOLEAN):
            value = self._previous().value == "真"
            return Literal(value, 'boolean')
        
        # 数组
        if self._match(TokenType.LBRACKET):
            return self._parse_array_literal()
        
        # 括号表达式
        if self._match(TokenType.LPAREN):
            expr = self._parse_expression()
            self._match(TokenType.RPAREN)
            return expr
        
        # 标识符
        if self._match(TokenType.IDENTIFIER):
            name = self._previous().value
            
            # 数组访问
            if self._match(TokenType.LBRACKET):
                index = self._parse_expression()
                self._match(TokenType.RBRACKET)
                return MemberExpression(Identifier(name), index)
            
            # 函数调用
            if self._match(TokenType.PARAMETER):
                return self._parse_call_expression(name)
            
            return Identifier(name)
        
        # 默认返回0
        return Literal(0, 'number')
    
    def _parse_array_literal(self) -> ArrayLiteral:
        """解析数组字面量"""
        elements = []
        
        while not self._check(TokenType.RBRACKET) and not self._is_at_end():
            elements.append(self._parse_expression())
            self._match(TokenType.COMMA)
        
        self._match(TokenType.RBRACKET)
        
        return ArrayLiteral(elements)
    
    def _parse_call_expression(self, name: str) -> CallExpression:
        """解析函数调用"""
        arguments = []
        
        while not self._check(TokenType.NEWLINE) and not self._is_at_end():
            if self._check(TokenType.IDENTIFIER):
                arguments.append(Identifier(self._advance().value))
            elif self._check(TokenType.NUMBER):
                arguments.append(Literal(self._advance().value, 'number'))
            elif self._check(TokenType.STRING):
                arguments.append(Literal(self._advance().value, 'string'))
            else:
                break
        
        return CallExpression(name, arguments)


# ============================================================================
# 辅助函数
# ============================================================================

def parse_tokens(tokens: List[Token]) -> Program:
    """解析token序列"""
    parser = Parser(tokens)
    return parser.parse()


# ============================================================================
# 导出
# ============================================================================

__all__ = [
    'Parser',
    'parse_tokens',
]
