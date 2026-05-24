"""测试汉诺塔执行（带调试）"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from yanlv.lexer import create_lexer
from yanlv.interpreter import create_interpreter

lexer = create_lexer("yanlv_nospace")

# 简化的汉诺塔代码
hanoi_code = '''函数汉诺塔参数n
输出"移动盘子"
输出n
结束
输出"汉诺塔算法已定义"
调用汉诺塔参数3'''

print("=" * 60)
print("简化汉诺塔测试")
print("=" * 60)
print("代码:")
print(hanoi_code)

# 词法分析
tokens = lexer.tokenize(hanoi_code)
print("\n词元分析:")
for i, token in enumerate(tokens):
    print(f"{i:2d}: {token.type.name:15s} = \"{token.value}\"")

# 执行
print("\n" + "=" * 60)
print("执行结果:")
print("=" * 60)
interpreter = create_interpreter()
output = interpreter.execute(tokens)
for line in output:
    print(line)

print("\n函数列表:", list(interpreter.functions.keys()))
