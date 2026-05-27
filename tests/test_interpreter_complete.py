"""
言律语言完整解释器测试

测试所有核心功能
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from yanlv.lexer import create_lexer
from yanlv.interpreter_complete import create_complete_interpreter


class TestCompleteInterpreter(unittest.TestCase):
"""测试完整解释器"""

def setUp(self):
self.lexer = create_lexer('yanlv_nospace')
self.interpreter = create_complete_interpreter()

def test_output_number(self):
"""测试数字输出"""
code = '输出10'
tokens = self.lexer.tokenize(code)
output = self.interpreter.execute(tokens)
self.assertEqual(len(output), 1)
self.assertEqual(output[0], '10')

def test_output_string(self):
"""测试字符串输出"""
code = '输出"你好世界"'
tokens = self.lexer.tokenize(code)
output = self.interpreter.execute(tokens)
self.assertEqual(len(output), 1)
self.assertEqual(output[0], '你好世界')

def test_variable_definition(self):
"""测试变量定义"""
code = '定义变量x为10'
tokens = self.lexer.tokenize(code)
output = self.interpreter.execute(tokens)
self.assertEqual(len(output), 0)
self.assertIn('x', self.interpreter.variables)

def test_variable_output(self):
"""测试变量输出"""
code = '''
定义变量x为20
输出x
'''
tokens = self.lexer.tokenize(code)
output = self.interpreter.execute(tokens)
self.assertGreater(len(output), 0)
self.assertEqual(output[0], '20.0')

def test_addition(self):
"""测试加法"""
code = '''
定义变量a为10
定义变量b为20
输出a+b
'''
tokens = self.lexer.tokenize(code)
output = self.interpreter.execute(tokens)
self.assertGreater(len(output), 0)
self.assertEqual(output[0], '30.0')

def test_subtraction(self):
"""测试减法"""
code = '''
定义变量a为30
定义变量b为10
输出a-b
'''
tokens = self.lexer.tokenize(code)
output = self.interpreter.execute(tokens)
self.assertGreater(len(output), 0)
self.assertEqual(output[0], '20.0')

def test_multiplication(self):
"""测试乘法"""
code = '''
定义变量a为5
定义变量b为6
输出a*b
'''
tokens = self.lexer.tokenize(code)
output = self.interpreter.execute(tokens)
self.assertGreater(len(output), 0)
self.assertEqual(output[0], '30.0')

def test_division(self):
"""测试除法"""
code = '''
定义变量a为20
定义变量b为4
输出a/b
'''
tokens = self.lexer.tokenize(code)
output = self.interpreter.execute(tokens)
self.assertGreater(len(output), 0)
self.assertEqual(output[0], '5.0')

def test_operator_precedence(self):
"""测试运算符优先级"""
code = '''
定义变量a为2
定义变量b为3
定义变量c为4
输出a+b*c
'''
tokens = self.lexer.tokenize(code)
output = self.interpreter.execute(tokens)
self.assertGreater(len(output), 0)
self.assertEqual(output[0], '14.0')

def test_parentheses(self):
"""测试括号"""
code = '''
定义变量a为2
定义变量b为3
定义变量c为4
输出(a+b)*c
'''
tokens = self.lexer.tokenize(code)
output = self.interpreter.execute(tokens)
self.assertGreater(len(output), 0)
self.assertEqual(output[0], '20.0')

def test_array_definition(self):
"""测试数组定义"""
code = '定义变量arr为[1,2,3,4,5]'
tokens = self.lexer.tokenize(code)
output = self.interpreter.execute(tokens)
self.assertEqual(len(output), 0)
self.assertIn('arr', self.interpreter.variables)

def test_array_access(self):
"""测试数组访问"""
code = '''
定义变量arr为[10,20,30]
输出arr[0]
'''
tokens = self.lexer.tokenize(code)
output = self.interpreter.execute(tokens)
self.assertGreater(len(output), 0)
self.assertEqual(output[0], '10.0')

def test_array_length(self):
"""测试数组长度"""
code = '''
定义变量arr为[1,2,3,4,5]
长度arr
'''
tokens = self.lexer.tokenize(code)
output = self.interpreter.execute(tokens)
self.assertGreater(len(output), 0)
self.assertEqual(output[0], '5')


class TestControlStructures(unittest.TestCase):
"""测试控制结构"""

def setUp(self):
self.lexer = create_lexer('yanlv_nospace')
self.interpreter = create_complete_interpreter()

def test_if_true(self):
"""测试条件为真"""
code = '''
定义变量x为10
如果x大于5则
    输出"大于5"
'''
tokens = self.lexer.tokenize(code)
output = self.interpreter.execute(tokens)
self.assertGreater(len(output), 0)
self.assertEqual(output[0], '大于5')

def test_if_false(self):
"""测试条件为假"""
code = '''
定义变量x为3
如果x大于5则
    输出"大于5"
'''
tokens = self.lexer.tokenize(code)
output = self.interpreter.execute(tokens)
self.assertEqual(len(output), 0)

def test_if_else(self):
"""测试if-else"""
code = '''
定义变量x为3
如果x大于5则
    输出"大于5"
    否则
        输出"不大于5"
    '''
    tokens = self.lexer.tokenize(code)
    output = self.interpreter.execute(tokens)
    self.assertGreater(len(output), 0)
    self.assertEqual(output[0], '不大于5')

    def test_loop(self):
    """测试循环"""
    code = '''
    循环3次执行
        输出i
    '''
    tokens = self.lexer.tokenize(code)
    output = self.interpreter.execute(tokens)
    self.assertEqual(len(output), 3)


    class TestFunctions(unittest.TestCase):
    """测试函数"""

    def setUp(self):
    self.lexer = create_lexer('yanlv_nospace')
    self.interpreter = create_complete_interpreter()

    def test_function_definition(self):
    """测试函数定义"""
    code = '''
    函数加法参数a b
        输出a+b
    '''
    tokens = self.lexer.tokenize(code)
    output = self.interpreter.execute(tokens)
    self.assertEqual(len(output), 0)
    self.assertIn('加法', self.interpreter.functions)

    def test_function_call(self):
    """测试函数调用"""
    code = '''
    函数加法参数a b
        输出a+b
    调用加法参数10 20
    '''
    tokens = self.lexer.tokenize(code)
    output = self.interpreter.execute(tokens)
    self.assertGreater(len(output), 0)


    if __name__ == '__main__':
    unittest.main()
