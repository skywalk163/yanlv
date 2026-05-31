"""测试输出语句的词法分析"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from yanlv.lexer import Lexer

lexer = Lexer()
code = '输出 "测试"'
tokens = lexer.tokenize(code)

print('词元分析结果:')
for i, token in enumerate(tokens):
    print(f'{i}: {token.type.name:15s} = "{token.value}"')
