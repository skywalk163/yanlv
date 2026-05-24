"""测试条件判断"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from yanlv.lexer import create_lexer
from yanlv.interpreter import create_interpreter

lexer = create_lexer("yanlv_nospace")

# 测试条件
code = '''定义变量n为3
如果n大于0则
输出"条件为真"
结束
输出"完成"'''

print("=" * 60)
print("条件判断测试")
print("=" * 60)
print("代码:")
print(code)

tokens = lexer.tokenize(code)
print("\n词元分析:")
for i, token in enumerate(tokens):
    print(f"{i:2d}: {token.type.name:15s} = \"{token.value}\"")

print("\n执行结果:")
interpreter = create_interpreter()
output = interpreter.execute(tokens)
for line in output:
    print(line)
