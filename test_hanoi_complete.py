"""测试完整的汉诺塔算法"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from yanlv.lexer import create_lexer
from yanlv.interpreter import create_interpreter

lexer = create_lexer("yanlv_nospace")

print("=" * 80)
print("测试完整的汉诺塔算法")
print("=" * 80)

# 标准汉诺塔（Python）
print("\n1. 标准汉诺塔（Python参考）:")
print("-" * 80)

def hanoi_python(n, from_rod='A', to_rod='C', aux_rod='B'):
"""标准汉诺塔递归实现"""
if n > 0:
hanoi_python(n-1, from_rod, aux_rod, to_rod)
print(f"移动盘子 {n} 从 {from_rod} 到 {to_rod}")
hanoi_python(n-1, aux_rod, to_rod, from_rod)

print("Python汉诺塔(3):")
hanoi_python(3)

# 言律语言汉诺塔（完整版）
print("\n\n2. 言律语言汉诺塔（完整版）:")
print("-" * 80)

hanoi_yanlv = '''函数汉诺塔参数n from to aux
如果n大于0则
    调用汉诺塔参数n-1 from aux to
    输出"移动盘子"
    输出n
    输出"从"
    输出from
    输出"到"
    输出to
    调用汉诺塔参数n-1 aux to from
输出"汉诺塔算法已定义"
调用汉诺塔参数3 A C B'''

print("言律语言代码:")
print(hanoi_yanlv)

tokens = lexer.tokenize(hanoi_yanlv)
interpreter = create_interpreter()
output = interpreter.execute(tokens)

print("\n执行结果:")
for line in output:
print(line)

print("\n\n3. 对比分析:")
print("-" * 80)
print("Python汉诺塔输出: 7次移动")
print("言律语言汉诺塔输出: 检查上面的输出")
print()
print("如果言律语言汉诺塔正确输出了7次移动，说明多参数函数和递归调用都已修复！")
