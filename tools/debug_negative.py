"""
调试负数处理
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from yanlv.lexer import create_lexer
from yanlv.interpreter import create_interpreter

lexer = create_lexer("yanlv_nospace")
interpreter = create_interpreter()

code = '''
定义变量数字为-5
绝对值 数字
'''

tokens = lexer.tokenize(code)

print("词元列表:")
for i, token in enumerate(tokens):
    print(f"{i}: {token.type.value:20s} = '{token.value}'")

print("\n执行结果:")
output = interpreter.execute(tokens)
print(output)
