"""深入分析汉诺塔问题"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from yanlv.lexer import create_lexer
from yanlv.interpreter import create_interpreter

lexer = create_lexer("yanlv_nospace")

print("=" * 70)
print("汉诺塔问题深入分析")
print("=" * 70)

# 标准汉诺塔算法（Python）
print("\n1. 标准汉诺塔算法（Python参考）:")
print("-" * 70)

def hanoi_python(n, from_rod='A', to_rod='C', aux_rod='B'):
    """标准汉诺塔递归实现"""
    if n > 0:
        hanoi_python(n-1, from_rod, aux_rod, to_rod)
        print(f"移动盘子 {n} 从 {from_rod} 到 {to_rod}")
        hanoi_python(n-1, aux_rod, to_rod, from_rod)

print("Python汉诺塔(3):")
hanoi_python(3)

# 言律语言汉诺塔
print("\n\n2. 言律语言汉诺塔:")
print("-" * 70)

hanoi_yanlv = '''函数汉诺塔参数n
如果n大于0则
输出"移动盘子"
输出n
调用汉诺塔参数n-1
结束
结束
输出"汉诺塔算法已定义"
调用汉诺塔参数3'''

print("言律语言代码:")
print(hanoi_yanlv)

tokens = lexer.tokenize(hanoi_yanlv)
interpreter = create_interpreter()
output = interpreter.execute(tokens)

print("\n执行结果:")
for line in output:
    print(line)

print("\n\n3. 问题分析:")
print("-" * 70)
print("[X] 问题1: 言律语言汉诺塔只输出了3次移动")
print("    标准汉诺塔(3)应该输出7次移动")
print()
print("[X] 问题2: 言律语言汉诺塔缺少柱子信息")
print("    标准汉诺塔需要三个柱子: from, to, aux")
print()
print("[X] 问题3: 言律语言汉诺塔的递归逻辑不完整")
print("    标准汉诺塔需要两次递归调用:")
print("    - hanoi(n-1, from, aux, to)  # 移动n-1个盘子到辅助柱")
print("    - hanoi(n-1, aux, to, from)  # 从辅助柱移到目标柱")
print()
print("[X] 问题4: 言律语言缺少多参数函数支持")
print("    当前只支持单参数函数")

print("\n\n4. 正确的言律语言汉诺塔应该是:")
print("-" * 70)
correct_hanoi = '''函数汉诺塔参数n from to aux
如果n大于0则
调用汉诺塔参数n-1 from aux to
输出"移动盘子"
输出n
输出"从"
输出from
输出"到"
输出to
调用汉诺塔参数n-1 aux to from
结束
结束
输出"汉诺塔算法已定义"
调用汉诺塔参数3 A C B'''
print(correct_hanoi)

print("\n\n5. 言律语言语法问题总结:")
print("-" * 70)
problems = [
    "1. 多参数函数支持不完整",
    "2. 函数调用时参数顺序处理有问题",
    "3. 字符串参数传递有问题",
    "4. 递归调用的参数求值不完整",
    "5. 缺少完整的表达式系统",
    "6. 条件语句只支持简单的比较",
    "7. 缺少循环变量支持",
    "8. 缺少数组/列表支持",
    "9. 缺少赋值语句支持",
    "10. 缺少运算符优先级处理"
]

for problem in problems:
    print(f"[X] {problem}")
