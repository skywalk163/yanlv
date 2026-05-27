"""
言律语言语法分析器测试
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from yanlv.parser import Parser, parse_tokens
from yanlv.lexer.lexer_token import Token, TokenType
from yanlv.ast_nodes import (
Program, VariableDeclaration, FunctionDeclaration,
IfStatement, WhileStatement, BinaryExpression, Identifier, Literal
)


class TestParser(unittest.TestCase):
"""测试语法分析器"""

def test_parse_empty_program(self):
"""测试空程序"""
tokens = []
program = parse_tokens(tokens)

self.assertIsInstance(program, Program)
self.assertEqual(len(program.statements), 0)

def test_parse_number_literal(self):
"""测试数字字面量"""
tokens = [Token(TokenType.NUMBER, 42, 1, 1, '42')]
program = parse_tokens(tokens)

self.assertEqual(len(program.statements), 0)

def test_parse_variable_declaration(self):
"""测试变量声明"""
tokens = [
Token(TokenType.DEFINE, '定义', 1, 1, '定义'),
Token(TokenType.VARIABLE, '变量', 1, 3, '变量'),
Token(TokenType.IDENTIFIER, 'x', 1, 5, 'x'),
Token(TokenType.IS, '为', 1, 7, '为'),
Token(TokenType.NUMBER, 10, 1, 9, '10'),
]

program = parse_tokens(tokens)

self.assertEqual(len(program.statements), 1)
self.assertIsInstance(program.statements[0], VariableDeclaration)
self.assertEqual(program.statements[0].name, 'x')

def test_parse_binary_expression(self):
"""测试二元表达式"""
tokens = [
Token(TokenType.NUMBER, 10, 1, 1, '10'),
Token(TokenType.PLUS, '+', 1, 3, '+'),
Token(TokenType.NUMBER, 20, 1, 5, '20'),
]

parser = Parser(tokens)
expr = parser._parse_expression()

self.assertIsInstance(expr, BinaryExpression)
self.assertEqual(expr.operator, '+')

def test_parse_identifier(self):
"""测试标识符"""
tokens = [Token(TokenType.IDENTIFIER, 'x', 1, 1, 'x')]

parser = Parser(tokens)
expr = parser._parse_expression()

self.assertIsInstance(expr, Identifier)
self.assertEqual(expr.name, 'x')

def test_parse_function_declaration(self):
"""测试函数声明"""
tokens = [
Token(TokenType.FUNCTION, '函数', 1, 1, '函数'),
Token(TokenType.IDENTIFIER, 'add', 1, 3, 'add'),
Token(TokenType.PARAMETER, '参数', 1, 5, '参数'),
Token(TokenType.IDENTIFIER, 'a', 1, 7, 'a'),
Token(TokenType.IDENTIFIER, 'b', 1, 9, 'b'),
Token(TokenType.END, '结束', 2, 1, '结束'),
]

program = parse_tokens(tokens)

self.assertEqual(len(program.statements), 1)
self.assertIsInstance(program.statements[0], FunctionDeclaration)
self.assertEqual(program.statements[0].name, 'add')
self.assertEqual(len(program.statements[0].parameters), 2)

def test_parse_if_statement(self):
"""测试条件语句"""
tokens = [
Token(TokenType.IF, '如果', 1, 1, '如果'),
Token(TokenType.IDENTIFIER, 'x', 1, 3, 'x'),
Token(TokenType.GREATER, '大于', 1, 5, '大于'),
Token(TokenType.NUMBER, 10, 1, 7, '10'),
Token(TokenType.THEN, '则', 1, 9, '则'),
Token(TokenType.END, '结束', 2, 1, '结束'),
]

program = parse_tokens(tokens)

self.assertEqual(len(program.statements), 1)
self.assertIsInstance(program.statements[0], IfStatement)

def test_parse_while_statement(self):
"""测试While循环"""
tokens = [
Token(TokenType.WHILE, '当', 1, 1, '当'),
Token(TokenType.IDENTIFIER, 'x', 1, 3, 'x'),
Token(TokenType.LESS, '小于', 1, 5, '小于'),
Token(TokenType.NUMBER, 10, 1, 7, '10'),
Token(TokenType.END, '结束', 2, 1, '结束'),
]

program = parse_tokens(tokens)

self.assertEqual(len(program.statements), 1)
self.assertIsInstance(program.statements[0], WhileStatement)


class TestExpressionParsing(unittest.TestCase):
"""测试表达式解析"""

def test_addition(self):
"""测试加法"""
tokens = [
Token(TokenType.NUMBER, 10, 1, 1, '10'),
Token(TokenType.PLUS, '+', 1, 3, '+'),
Token(TokenType.NUMBER, 20, 1, 5, '20'),
]

parser = Parser(tokens)
expr = parser._parse_expression()

self.assertIsInstance(expr, BinaryExpression)
self.assertEqual(expr.operator, '+')

def test_subtraction(self):
"""测试减法"""
tokens = [
Token(TokenType.NUMBER, 30, 1, 1, '30'),
Token(TokenType.MINUS, '-', 1, 3, '-'),
Token(TokenType.NUMBER, 10, 1, 5, '10'),
]

parser = Parser(tokens)
expr = parser._parse_expression()

self.assertIsInstance(expr, BinaryExpression)
self.assertEqual(expr.operator, '-')

def test_multiplication(self):
"""测试乘法"""
tokens = [
Token(TokenType.NUMBER, 5, 1, 1, '5'),
Token(TokenType.MULTIPLY, '*', 1, 3, '*'),
Token(TokenType.NUMBER, 6, 1, 5, '6'),
]

parser = Parser(tokens)
expr = parser._parse_expression()

self.assertIsInstance(expr, BinaryExpression)
self.assertEqual(expr.operator, '*')

def test_division(self):
"""测试除法"""
tokens = [
Token(TokenType.NUMBER, 20, 1, 1, '20'),
Token(TokenType.DIVIDE, '/', 1, 3, '/'),
Token(TokenType.NUMBER, 4, 1, 5, '4'),
]

parser = Parser(tokens)
expr = parser._parse_expression()

self.assertIsInstance(expr, BinaryExpression)
self.assertEqual(expr.operator, '/')

def test_operator_precedence(self):
"""测试运算符优先级"""
tokens = [
Token(TokenType.NUMBER, 2, 1, 1, '2'),
Token(TokenType.PLUS, '+', 1, 3, '+'),
Token(TokenType.NUMBER, 3, 1, 5, '3'),
Token(TokenType.MULTIPLY, '*', 1, 7, '*'),
Token(TokenType.NUMBER, 4, 1, 9, '4'),
]

parser = Parser(tokens)
expr = parser._parse_expression()

# 应该解析为 2 + (3 * 4)
self.assertIsInstance(expr, BinaryExpression)
self.assertEqual(expr.operator, '+')
self.assertIsInstance(expr.right, BinaryExpression)
self.assertEqual(expr.right.operator, '*')


if __name__ == '__main__':
unittest.main()
