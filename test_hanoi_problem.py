"""分析汉诺塔执行问题"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from yanlv.lexer import create_lexer
from yanlv.interpreter import create_interpreter

lexer = create_lexer("yanlv_nospace")

# 汉诺塔代码
hanoi_code = '''函数汉诺塔参数n
如果n大于0则
输出"移动盘子"
输出n
调用汉诺塔参数n-1
结束
结束
输出"汉诺塔算法已定义"
调用汉诺塔参数3'''

print("=" * 60)
print("汉诺塔代码分析")
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

print("\n" + "=" * 60)
print("问题分析:")
print("=" * 60)
print("1. 函数定义正确识别")
print("2. 函数调用正确识别")
print("3. 但是递归调用时参数传递有问题")
print("4. n-1 这样的表达式没有被正确计算")
print("5. 需要支持表达式求值")
