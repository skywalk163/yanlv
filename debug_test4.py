"""
调试测试 - 使用不带数字的变量名
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from yanlv.lexer import create_lexer
from yanlv.interpreter import create_interpreter

# 测试词法分析器
lexer = create_lexer("yanlv_nospace")
interpreter = create_interpreter()

code = '''
定义变量问候为"你好"
定义变量世界为"世界"
连接 问候 世界
'''

tokens = lexer.tokenize(code)

print("词元列表:")
for i, token in enumerate(tokens):
    print(f"{i}: {token.type.value:20s} = '{token.value}'")

print("\n执行结果:")
output = interpreter.execute(tokens)
print(output)
