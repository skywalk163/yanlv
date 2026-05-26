"""
言律语言编译器架构测试

测试AST节点和代码生成器
"""

import unittest
import sys
import os

# 添加src目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from yanlv.ast_nodes import (
    Program, VariableDeclaration, FunctionDeclaration,
    IfStatement, WhileStatement, ReturnStatement, OutputStatement,
    BinaryExpression, CallExpression, Identifier, Literal, ArrayLiteral
)
from yanlv.code_generator import generate_python_code


class TestASTNodes(unittest.TestCase):
    """测试AST节点"""
    
    def test_literal_number(self):
        """测试数字字面量"""
        lit = Literal(42, 'number')
        self.assertEqual(lit.value, 42)
        self.assertEqual(lit.literal_type, 'number')
    
    def test_literal_string(self):
        """测试字符串字面量"""
        lit = Literal("你好", 'string')
        self.assertEqual(lit.value, "你好")
        self.assertEqual(lit.literal_type, 'string')
    
    def test_literal_boolean(self):
        """测试布尔字面量"""
        lit = Literal(True, 'boolean')
        self.assertEqual(lit.value, True)
        self.assertEqual(lit.literal_type, 'boolean')
    
    def test_identifier(self):
        """测试标识符"""
        ident = Identifier("x")
        self.assertEqual(ident.name, "x")
    
    def test_binary_expression(self):
        """测试二元表达式"""
        left = Identifier("a")
        right = Identifier("b")
        expr = BinaryExpression("+", left, right)
        self.assertEqual(expr.operator, "+")
        self.assertEqual(expr.left.name, "a")
        self.assertEqual(expr.right.name, "b")
    
    def test_array_literal(self):
        """测试数组字面量"""
        elements = [Literal(1, 'number'), Literal(2, 'number'), Literal(3, 'number')]
        arr = ArrayLiteral(elements)
        self.assertEqual(len(arr.elements), 3)
    
    def test_variable_declaration(self):
        """测试变量声明"""
        init = Literal(10, 'number')
        decl = VariableDeclaration("x", init)
        self.assertEqual(decl.name, "x")
        self.assertEqual(decl.initializer.value, 10)
    
    def test_function_declaration(self):
        """测试函数声明"""
        body = [ReturnStatement(Literal(42, 'number'))]
        func = FunctionDeclaration("test", ["x", "y"], body)
        self.assertEqual(func.name, "test")
        self.assertEqual(len(func.parameters), 2)
        self.assertEqual(len(func.body), 1)
    
    def test_if_statement(self):
        """测试条件语句"""
        condition = BinaryExpression(">", Identifier("x"), Literal(0, 'number'))
        consequent = [OutputStatement(Literal("positive", 'string'))]
        if_stmt = IfStatement(condition, consequent)
        self.assertIsNotNone(if_stmt.condition)
        self.assertEqual(len(if_stmt.consequent), 1)
    
    def test_program(self):
        """测试程序"""
        stmts = [
            VariableDeclaration("x", Literal(10, 'number')),
            OutputStatement(Identifier("x"))
        ]
        program = Program(stmts)
        self.assertEqual(len(program.statements), 2)


class TestCodeGenerator(unittest.TestCase):
    """测试代码生成器"""
    
    def test_generate_literal_number(self):
        """测试生成数字字面量"""
        lit = Literal(42, 'number')
        code = generate_python_code(lit)
        self.assertEqual(code, "42")
    
    def test_generate_literal_string(self):
        """测试生成字符串字面量"""
        lit = Literal("你好", 'string')
        code = generate_python_code(lit)
        self.assertEqual(code, '"你好"')
    
    def test_generate_literal_boolean(self):
        """测试生成布尔字面量"""
        lit = Literal(True, 'boolean')
        code = generate_python_code(lit)
        self.assertEqual(code, "True")
    
    def test_generate_identifier(self):
        """测试生成标识符"""
        ident = Identifier("x")
        code = generate_python_code(ident)
        self.assertEqual(code, "x")
    
    def test_generate_binary_expression(self):
        """测试生成二元表达式"""
        left = Identifier("a")
        right = Identifier("b")
        expr = BinaryExpression("+", left, right)
        code = generate_python_code(expr)
        self.assertEqual(code, "(a + b)")
    
    def test_generate_array_literal(self):
        """测试生成数组字面量"""
        elements = [Literal(1, 'number'), Literal(2, 'number'), Literal(3, 'number')]
        arr = ArrayLiteral(elements)
        code = generate_python_code(arr)
        self.assertEqual(code, "[1, 2, 3]")
    
    def test_generate_variable_declaration(self):
        """测试生成变量声明"""
        init = Literal(10, 'number')
        decl = VariableDeclaration("x", init)
        code = generate_python_code(decl)
        self.assertEqual(code, "x = 10")
    
    def test_generate_function_declaration(self):
        """测试生成函数声明"""
        body = [ReturnStatement(Literal(42, 'number'))]
        func = FunctionDeclaration("test", ["x", "y"], body)
        code = generate_python_code(func)
        self.assertIn("def test(x, y):", code)
        self.assertIn("return 42", code)
    
    def test_generate_if_statement(self):
        """测试生成条件语句"""
        condition = BinaryExpression(">", Identifier("x"), Literal(0, 'number'))
        consequent = [OutputStatement(Literal("positive", 'string'))]
        if_stmt = IfStatement(condition, consequent)
        code = generate_python_code(if_stmt)
        self.assertIn("if (x > 0):", code)
        self.assertIn('print("positive")', code)
    
    def test_generate_output_statement(self):
        """测试生成输出语句"""
        output = OutputStatement(Literal("Hello", 'string'))
        code = generate_python_code(output)
        self.assertEqual(code, 'print("Hello")')
    
    def test_generate_call_expression(self):
        """测试生成函数调用"""
        args = [Literal(10, 'number'), Literal(20, 'number')]
        call = CallExpression("add", args)
        code = generate_python_code(call)
        self.assertEqual(code, "add(10, 20)")
    
    def test_generate_program(self):
        """测试生成程序"""
        stmts = [
            VariableDeclaration("x", Literal(10, 'number')),
            OutputStatement(Identifier("x"))
        ]
        program = Program(stmts)
        code = generate_python_code(program)
        self.assertIn("x = 10", code)
        self.assertIn("print(x)", code)


class TestComplexCodeGeneration(unittest.TestCase):
    """测试复杂代码生成"""
    
    def test_factorial_function(self):
        """测试阶乘函数"""
        # 阶乘函数的AST
        func = FunctionDeclaration(
            "factorial",
            ["n"],
            [
                IfStatement(
                    BinaryExpression("<=", Identifier("n"), Literal(1, 'number')),
                    [ReturnStatement(Literal(1, 'number'))],
                    [ReturnStatement(
                        BinaryExpression(
                            "*",
                            Identifier("n"),
                            CallExpression("factorial", [
                                BinaryExpression("-", Identifier("n"), Literal(1, 'number'))
                            ])
                        )
                    )]
                )
            ]
        )
        
        code = generate_python_code(func)
        self.assertIn("def factorial(n):", code)
        self.assertIn("if (n <= 1):", code)
        self.assertIn("return 1", code)
        self.assertIn("return (n * factorial((n - 1)))", code)
    
    def test_fibonacci_function(self):
        """测试斐波那契函数"""
        func = FunctionDeclaration(
            "fibonacci",
            ["n"],
            [
                IfStatement(
                    BinaryExpression("<=", Identifier("n"), Literal(1, 'number')),
                    [ReturnStatement(Identifier("n"))],
                    [ReturnStatement(
                        BinaryExpression(
                            "+",
                            CallExpression("fibonacci", [
                                BinaryExpression("-", Identifier("n"), Literal(1, 'number'))
                            ]),
                            CallExpression("fibonacci", [
                                BinaryExpression("-", Identifier("n"), Literal(2, 'number'))
                            ])
                        )
                    )]
                )
            ]
        )
        
        code = generate_python_code(func)
        self.assertIn("def fibonacci(n):", code)
        self.assertIn("return (fibonacci((n - 1)) + fibonacci((n - 2)))", code)


if __name__ == '__main__':
    unittest.main()
