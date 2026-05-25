"""测试词法分析"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from yanlv.lexer import create_lexer

lexer = create_lexer("yanlv_nospace")

code = '''定义变量x为10
输出x
设置x为20
输出x'''

print("代码:")
print(code)
print("\n词元分析:")
tokens = lexer.tokenize(code)
for i, token in enumerate(tokens):
    print(f"{i:3d}: {token.type.name:20s} = {token.value}")
