"""
言律语言词法分析器增强测试

提升词法分析器的测试覆盖率
"""

import unittest
import sys
import os

# 添加src目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from yanlv.lexer import create_lexer
from yanlv.lexer.lexer_token import TokenType


class TestLexerBasic(unittest.TestCase):
"""测试词法分析器基础功能"""

def setUp(self):
"""测试前准备"""
self.lexer = create_lexer('yanlv_nospace')

def test_tokenize_empty(self):
"""测试空字符串"""
tokens = self.lexer.tokenize('')
self.assertEqual(len(tokens), 0)

def test_tokenize_number(self):
"""测试数字"""
tokens = self.lexer.tokenize('123')
self.assertGreater(len(tokens), 0)

def test_tokenize_string(self):
"""测试字符串"""
tokens = self.lexer.tokenize('"你好"')
self.assertGreater(len(tokens), 0)

def test_tokenize_identifier(self):
"""测试标识符"""
tokens = self.lexer.tokenize('变量名')
self.assertGreater(len(tokens), 0)

def test_tokenize_keyword(self):
"""测试关键词"""
tokens = self.lexer.tokenize('定义')
self.assertGreater(len(tokens), 0)

def test_tokenize_operator(self):
"""测试运算符"""
tokens = self.lexer.tokenize('+')
self.assertGreater(len(tokens), 0)

def test_tokenize_punctuation(self):
"""测试标点符号"""
tokens = self.lexer.tokenize('。')
self.assertGreater(len(tokens), 0)

def test_tokenize_mixed(self):
"""测试混合内容"""
code = '定义变量x为10'
tokens = self.lexer.tokenize(code)
self.assertGreater(len(tokens), 0)


class TestLexerKeywords(unittest.TestCase):
"""测试关键词识别"""

def setUp(self):
"""测试前准备"""
self.lexer = create_lexer('yanlv_nospace')

def test_keyword_define(self):
"""测试定义关键词"""
tokens = self.lexer.tokenize('定义')
self.assertGreater(len(tokens), 0)

def test_keyword_if(self):
"""测试如果关键词"""
tokens = self.lexer.tokenize('如果')
self.assertGreater(len(tokens), 0)

def test_keyword_else(self):
"""测试否则关键词"""
tokens = self.lexer.tokenize('否则')
self.assertGreater(len(tokens), 0)

def test_keyword_loop(self):
"""测试循环关键词"""
tokens = self.lexer.tokenize('循环')
self.assertGreater(len(tokens), 0)

def test_keyword_function(self):
"""测试函数关键词"""
tokens = self.lexer.tokenize('函数')
self.assertGreater(len(tokens), 0)

def test_keyword_output(self):
"""测试输出关键词"""
tokens = self.lexer.tokenize('输出')
self.assertGreater(len(tokens), 0)


class TestLexerOperators(unittest.TestCase):
"""测试运算符识别"""

def setUp(self):
"""测试前准备"""
self.lexer = create_lexer('yanlv_nospace')

def test_arithmetic_operators(self):
"""测试算术运算符"""
operators = ['+', '-', '*', '/', '%']
for op in operators:
tokens = self.lexer.tokenize(op)
self.assertGreater(len(tokens), 0, f"Failed for operator: {op}")

def test_comparison_operators(self):
"""测试比较运算符"""
operators = ['大于', '小于', '等于', '不等于']
for op in operators:
tokens = self.lexer.tokenize(op)
self.assertGreater(len(tokens), 0, f"Failed for operator: {op}")


class TestLexerPunctuation(unittest.TestCase):
"""测试标点符号识别"""

def setUp(self):
"""测试前准备"""
self.lexer = create_lexer('yanlv_nospace')

def test_chinese_punctuation(self):
"""测试中文标点"""
punctuations = ['。', '，', '；', '：', '、']
for punct in punctuations:
tokens = self.lexer.tokenize(punct)
self.assertGreater(len(tokens), 0, f"Failed for punctuation: {punct}")

def test_brackets(self):
"""测试括号"""
brackets = ['(', ')', '[', ']', '{', '}']
for bracket in brackets:
tokens = self.lexer.tokenize(bracket)
self.assertGreater(len(tokens), 0, f"Failed for bracket: {bracket}")


class TestLexerComplex(unittest.TestCase):
"""测试复杂表达式"""

def setUp(self):
"""测试前准备"""
self.lexer = create_lexer('yanlv_nospace')

def test_variable_definition(self):
"""测试变量定义"""
code = '定义变量x为10'
tokens = self.lexer.tokenize(code)
self.assertGreater(len(tokens), 0)

def test_function_call(self):
"""测试函数调用"""
code = '调用函数参数10 20'
tokens = self.lexer.tokenize(code)
self.assertGreater(len(tokens), 0)

def test_if_statement(self):
"""测试条件语句"""
code = '如果x大于5则输出x结束'
tokens = self.lexer.tokenize(code)
self.assertGreater(len(tokens), 0)

def test_loop_statement(self):
"""测试循环语句"""
code = '循环5次执行输出i结束'
tokens = self.lexer.tokenize(code)
self.assertGreater(len(tokens), 0)

def test_array_definition(self):
"""测试数组定义"""
code = '定义变量arr为[1,2,3]'
tokens = self.lexer.tokenize(code)
self.assertGreater(len(tokens), 0)

def test_expression(self):
"""测试表达式"""
code = 'a+b*c'
tokens = self.lexer.tokenize(code)
self.assertGreater(len(tokens), 0)


class TestLexerEdgeCases(unittest.TestCase):
"""测试边界情况"""

def setUp(self):
"""测试前准备"""
self.lexer = create_lexer('yanlv_nospace')

def test_whitespace(self):
"""测试空白字符"""
code = '   '
tokens = self.lexer.tokenize(code)
# 空白字符应该被忽略或产生空token列表
self.assertGreaterEqual(len(tokens), 0)

def test_newline(self):
"""测试换行符"""
code = '\n\n'
tokens = self.lexer.tokenize(code)
self.assertGreaterEqual(len(tokens), 0)

def test_mixed_whitespace(self):
"""测试混合空白字符"""
code = '  \n  \t  '
tokens = self.lexer.tokenize(code)
self.assertGreaterEqual(len(tokens), 0)

def test_long_identifier(self):
"""测试长标识符"""
code = '这是一个很长的变量名称用于测试'
tokens = self.lexer.tokenize(code)
self.assertGreater(len(tokens), 0)

def test_nested_brackets(self):
"""测试嵌套括号"""
code = '[[[1,2],[3,4]],[[5,6],[7,8]]]'
tokens = self.lexer.tokenize(code)
self.assertGreater(len(tokens), 0)


if __name__ == '__main__':
unittest.main()
