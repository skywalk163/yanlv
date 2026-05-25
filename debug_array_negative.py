"""
调试数组中的负数
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from yanlv.lexer import create_lexer
from yanlv.interpreter import create_interpreter

lexer = create_lexer("yanlv_nospace")
interpreter = create_interpreter()

code = '''
定义变量负数数组为[-5, -2, -8, -1]
输出 负数数组
'''

tokens = lexer.tokenize(code)

print("词元列表:")
for i, token in enumerate(tokens):
    print(f"{i}: {token.type.value:20s} = '{token.value}'")

print("\n执行结果:")
output = interpreter.execute(tokens)
print(output)
