"""
言律语言增强解释器测试

测试修复后的解释器功能
"""

import unittest
import sys
import os

# 添加src目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from yanlv.lexer import create_lexer
from yanlv.interpreter_enhanced import create_enhanced_interpreter


class TestEnhancedInterpreter(unittest.TestCase):
"""测试增强解释器"""

def setUp(self):
"""测试前准备"""
self.lexer = create_lexer('yanlv_nospace')
self.interpreter = create_enhanced_interpreter()

def test_output_number(self):
"""测试数字输出"""
code = '输出10'
tokens = self.lexer.tokenize(code)
output = self.interpreter.execute(tokens)
self.assertEqual(len(output), 1)
self.assertEqual(output[0], '10')

def test_output_string(self):
"""测试字符串输出"""
code = '输出"你好"'
tokens = self.lexer.tokenize(code)
output = self.interpreter.execute(tokens)
self.assertEqual(len(output), 1)
self.assertEqual(output[0], '你好')

def test_variable_definition_and_output(self):
"""测试变量定义和输出"""
code = '''
定义变量x为10
输出x
'''
tokens = self.lexer.tokenize(code)
output = self.interpreter.execute(tokens)
self.assertGreater(len(output), 0)
self.assertEqual(output[0], '10.0')

def test_arithmetic_addition(self):
"""测试加法运算"""
code = '''
定义变量a为10
定义变量b为20
输出a+b
'''
tokens = self.lexer.tokenize(code)
output = self.interpreter.execute(tokens)
self.assertGreater(len(output), 0)
self.assertEqual(output[0], '30.0')

def test_arithmetic_subtraction(self):
"""测试减法运算"""
code = '''
定义变量a为30
定义变量b为10
输出a-b
'''
tokens = self.lexer.tokenize(code)
output = self.interpreter.execute(tokens)
self.assertGreater(len(output), 0)
self.assertEqual(output[0], '20.0')

def test_arithmetic_multiplication(self):
"""测试乘法运算"""
code = '''
定义变量a为5
定义变量b为6
输出a*b
'''
tokens = self.lexer.tokenize(code)
output = self.interpreter.execute(tokens)
self.assertGreater(len(output), 0)
self.assertEqual(output[0], '30.0')

def test_arithmetic_division(self):
"""测试除法运算"""
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
# 2 + 3 * 4 = 14
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
# (2 + 3) * 4 = 20
self.assertEqual(output[0], '20.0')

def test_array_definition(self):
"""测试数组定义"""
code = '定义变量arr为[1,2,3,4,5]'
tokens = self.lexer.tokenize(code)
output = self.interpreter.execute(tokens)
# 数组定义不应该产生输出
self.assertEqual(len(output), 0)

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
"""测试前准备"""
self.lexer = create_lexer('yanlv_nospace')
self.interpreter = create_enhanced_interpreter()

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
# 条件为假，不应该输出
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
    # 应该输出3次
    self.assertEqual(len(output), 3)


    if __name__ == '__main__':
    unittest.main()
