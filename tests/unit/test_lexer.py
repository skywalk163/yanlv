"""
言律语言单元测试 - 词法分析器测试
"""

import unittest
import sys
import os

# 添加src目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from yanlv.lexer.lexer_modular import tokenize
from yanlv.lexer.lexer_token import TokenType


class TestLexer(unittest.TestCase):
    """词法分析器测试"""
    
    def test_simple_output(self):
        """测试简单输出语句"""
        code = '输出"你好"'
        tokens = tokenize(code)
        
        # 检查token数量
        self.assertGreater(len(tokens), 0)
        
        # 检查第一个token是OUTPUT
        self.assertEqual(tokens[0].type, TokenType.OUTPUT)
        self.assertEqual(tokens[0].value, '输出')
        
        # 检查第二个token是STRING
        self.assertEqual(tokens[1].type, TokenType.STRING)
        self.assertEqual(tokens[1].value, '"你好"')
    
    def test_variable_definition(self):
        """测试变量定义"""
        code = '定义变量x为10'
        tokens = tokenize(code)
        
        # 检查token类型
        self.assertEqual(tokens[0].type, TokenType.DEFINE)
        self.assertEqual(tokens[1].type, TokenType.VARIABLE)
        self.assertEqual(tokens[2].type, TokenType.IDENTIFIER)
        self.assertEqual(tokens[3].type, TokenType.IS)
        self.assertEqual(tokens[4].type, TokenType.NUMBER)
    
    def test_string_literal(self):
        """测试字符串字面量"""
        code = '定义变量问候为 "你好，世界！"'
        tokens = tokenize(code)
        
        # 查找STRING token
        string_tokens = [t for t in tokens if t.type == TokenType.STRING]
        self.assertEqual(len(string_tokens), 1)
        self.assertEqual(string_tokens[0].value, '"你好，世界！"')
    
    def test_if_statement(self):
        """测试条件语句"""
        code = '如果条件成立则'
        tokens = tokenize(code)
        
        self.assertEqual(tokens[0].type, TokenType.IF)
    
    def test_loop_statement(self):
        """测试循环语句"""
        code = '循环5次执行'
        tokens = tokenize(code)
        
        self.assertEqual(tokens[0].type, TokenType.LOOP)
    
    def test_function_definition(self):
        """测试函数定义"""
        code = '函数计算平方参数n'
        tokens = tokenize(code)
        
        self.assertEqual(tokens[0].type, TokenType.FUNCTION)
    
    def test_array_definition(self):
        """测试数组定义"""
        code = '定义变量arr为[5,3,8,1,2]'
        tokens = tokenize(code)
        
        # 检查包含LBRACKET和RBRACKET
        bracket_tokens = [t for t in tokens if t.type in (TokenType.LBRACKET, TokenType.RBRACKET)]
        self.assertEqual(len(bracket_tokens), 2)
    
    def test_multiline_code(self):
        """测试多行代码"""
        code = '''输出"第一行"
输出"第二行"
输出"第三行"'''
        tokens = tokenize(code)
        
        # 检查包含多个OUTPUT
        output_tokens = [t for t in tokens if t.type == TokenType.OUTPUT]
        self.assertEqual(len(output_tokens), 3)
        
        # 检查包含NEWLINE
        newline_tokens = [t for t in tokens if t.type == TokenType.NEWLINE]
        self.assertGreater(len(newline_tokens), 0)


class TestLexerAdvanced(unittest.TestCase):
    """词法分析器高级测试"""
    
    def test_causal_chain(self):
        """测试因果链语法"""
        code = '温度大于28，开启空调制冷。'
        tokens = tokenize(code)
        
        # 检查包含COMMA和PERIOD
        comma_tokens = [t for t in tokens if t.type == TokenType.COMMA]
        period_tokens = [t for t in tokens if t.type == TokenType.PERIOD]
        
        self.assertEqual(len(comma_tokens), 1)
        self.assertEqual(len(period_tokens), 1)
    
    def test_advanced_define(self):
        """测试高级定义语法"""
        code = '定温度是30。'
        tokens = tokenize(code)
        
        # 检查第一个token是DEF
        self.assertEqual(tokens[0].type, TokenType.DEF)
    
    def test_theme_block(self):
        """测试主题块语法"""
        code = '以张三为主题：'
        tokens = tokenize(code)
        
        # 检查包含COLON
        colon_tokens = [t for t in tokens if t.type == TokenType.COLON]
        self.assertEqual(len(colon_tokens), 1)


if __name__ == '__main__':
    unittest.main()
