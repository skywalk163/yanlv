"""
言律语言JavaScript代码生成器测试
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from yanlv.js_generator import JavaScriptCodeGenerator, generate_javascript
from yanlv.ast_nodes import (
    Program, VariableDeclaration, FunctionDeclaration,
    IfStatement, WhileStatement, BinaryExpression, Identifier, Literal
)


class TestJavaScriptCodeGenerator(unittest.TestCase):
    """测试JavaScript代码生成器"""
    
    def setUp(self):
        self.generator = JavaScriptCodeGenerator()
    
    def test_generate_literal_number(self):
        """测试数字字面量"""
        lit = Literal(42, 'number')
        code = self.generator.generate(lit)
        
        self.assertEqual(code, '42')
    
    def test_generate_literal_string(self):
        """测试字符串字面量"""
        lit = Literal('hello', 'string')
        code = self.generator.generate(lit)
        
        self.assertEqual(code, '"hello"')
    
    def test_generate_literal_boolean(self):
        """测试布尔字面量"""
        lit_true = Literal(True, 'boolean')
        code_true = self.generator.generate(lit_true)
        self.assertEqual(code_true, 'true')
        
        lit_false = Literal(False, 'boolean')
        code_false = self.generator.generate(lit_false)
        self.assertEqual(code_false, 'false')
    
    def test_generate_identifier(self):
        """测试标识符"""
        ident = Identifier('x')
        code = self.generator.generate(ident)
        
        self.assertEqual(code, 'x')
    
    def test_generate_binary_expression(self):
        """测试二元表达式"""
        expr = BinaryExpression(
            '+',
            Literal(10, 'number'),
            Literal(20, 'number')
        )
        code = self.generator.generate(expr)
        
        self.assertEqual(code, '(10 + 20)')
    
    def test_generate_variable_declaration(self):
        """测试变量声明"""
        var_decl = VariableDeclaration(
            'x',
            Literal(10, 'number')
        )
        code = self.generator.generate(var_decl)
        
        self.assertEqual(code, 'let x = 10;')
    
    def test_generate_function_declaration(self):
        """测试函数声明"""
        func_decl = FunctionDeclaration(
            'add',
            ['a', 'b'],
            [
                ReturnStatement(
                    BinaryExpression(
                        '+',
                        Identifier('a'),
                        Identifier('b')
                    )
                )
            ]
        )
        code = self.generator.generate(func_decl)
        
        self.assertIn('function add(a, b)', code)
        self.assertIn('return', code)
    
    def test_generate_if_statement(self):
        """测试条件语句"""
        if_stmt = IfStatement(
            BinaryExpression(
                '>',
                Identifier('x'),
                Literal(10, 'number')
            ),
            [
                VariableDeclaration('y', Literal(1, 'number'))
            ],
            [
                VariableDeclaration('y', Literal(0, 'number'))
            ]
        )
        code = self.generator.generate(if_stmt)
        
        self.assertIn('if', code)
        self.assertIn('else', code)
    
    def test_generate_while_statement(self):
        """测试While循环"""
        while_stmt = WhileStatement(
            BinaryExpression(
                '<',
                Identifier('i'),
                Literal(10, 'number')
            ),
            [
                VariableDeclaration('i', Literal(0, 'number'))
            ]
        )
        code = self.generator.generate(while_stmt)
        
        self.assertIn('while', code)
    
    def test_generate_program(self):
        """测试程序"""
        program = Program([
            VariableDeclaration('x', Literal(10, 'number')),
            VariableDeclaration('y', Literal(20, 'number'))
        ])
        code = self.generator.generate(program)
        
        self.assertIn('let x = 10;', code)
        self.assertIn('let y = 20;', code)


class TestOperatorConversion(unittest.TestCase):
    """测试运算符转换"""
    
    def setUp(self):
        self.generator = JavaScriptCodeGenerator()
    
    def test_arithmetic_operators(self):
        """测试算术运算符"""
        self.assertEqual(self.generator._convert_operator('+'), '+')
        self.assertEqual(self.generator._convert_operator('-'), '-')
        self.assertEqual(self.generator._convert_operator('*'), '*')
        self.assertEqual(self.generator._convert_operator('/'), '/')
        self.assertEqual(self.generator._convert_operator('%'), '%')
    
    def test_comparison_operators(self):
        """测试比较运算符"""
        self.assertEqual(self.generator._convert_operator('=='), '===')
        self.assertEqual(self.generator._convert_operator('!='), '!==')
        self.assertEqual(self.generator._convert_operator('<'), '<')
        self.assertEqual(self.generator._convert_operator('>'), '>')
    
    def test_logical_operators(self):
        """测试逻辑运算符"""
        self.assertEqual(self.generator._convert_operator('且'), '&&')
        self.assertEqual(self.generator._convert_operator('或'), '||')
        self.assertEqual(self.generator._convert_operator('非'), '!')


class TestComplexExpressions(unittest.TestCase):
    """测试复杂表达式"""
    
    def setUp(self):
        self.generator = JavaScriptCodeGenerator()
    
    def test_nested_binary_expression(self):
        """测试嵌套二元表达式"""
        expr = BinaryExpression(
            '+',
            BinaryExpression(
                '*',
                Literal(2, 'number'),
                Literal(3, 'number')
            ),
            Literal(4, 'number')
        )
        code = self.generator.generate(expr)
        
        self.assertEqual(code, '((2 * 3) + 4)')
    
    def test_function_call(self):
        """测试函数调用"""
        call = CallExpression(
            'add',
            [Literal(10, 'number'), Literal(20, 'number')]
        )
        code = self.generator.generate(call)
        
        self.assertEqual(code, 'add(10, 20)')


# 需要导入ReturnStatement和CallExpression
from yanlv.ast_nodes import ReturnStatement, CallExpression


if __name__ == '__main__':
    unittest.main()
