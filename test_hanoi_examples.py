"""测试汉诺塔完整版"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from yanlv.lexer import create_lexer
from yanlv.interpreter import create_interpreter

lexer = create_lexer("yanlv_nospace")

print("=" * 80)
print("测试汉诺塔完整版")
print("=" * 80)

# 原始的汉诺塔完整版（有问题）
print("\n1. 原始的汉诺塔完整版:")
print("-" * 80)

code1 = '''函数汉诺塔参数n from to aux
如果n等于1则
    输出"移动盘子"
    输出from
    输出"到"
    输出to
    否则
        调用汉诺塔参数n-1 from aux to
        输出"移动盘子"
        输出from
        输出"到"
        输出to
        调用汉诺塔参数n-1 aux to from
输出"汉诺塔算法已定义"'''

print("代码:")
print(code1)

try:
tokens = lexer.tokenize(code1)
interpreter = create_interpreter()
output = interpreter.execute(tokens)
print("\n执行结果:")
for line in output:
print(line)
except Exception as e:
print(f"\n错误: {e}")

# 修正的汉诺塔完整版（使用嵌套条件）
print("\n\n2. 修正的汉诺塔完整版（使用嵌套条件）:")
print("-" * 80)

code2 = '''函数汉诺塔参数n from to aux
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

print("代码:")
print(code2)

try:
tokens = lexer.tokenize(code2)
interpreter = create_interpreter()
output = interpreter.execute(tokens)
print("\n执行结果:")
for line in output:
print(line)

# 统计移动次数
move_count = str(output).count("移动盘子")
print(f"\n移动次数: {move_count}")
if move_count == 7:
print("✅ 正确！汉诺塔(3)应该移动7次")
else:
print(f"❌ 错误！汉诺塔(3)应该移动7次，实际移动{move_count}次")
except Exception as e:
print(f"\n错误: {e}")

# 测试"否则"关键字是否支持
print("\n\n3. 测试'否则'关键字:")
print("-" * 80)

code3 = '''定义变量x为10
如果x大于5则
    输出"x大于5"
    否则
        输出"x不大于5"
        结束'''

        print("代码:")
        print(code3)

        try:
        tokens = lexer.tokenize(code3)
        print("\n词元分析:")
        for i, token in enumerate(tokens):
        print(f"{i:3d}: {token.type.name:20s} = {token.value}")

        interpreter = create_interpreter()
        output = interpreter.execute(tokens)
        print("\n执行结果:")
        for line in output:
        print(line)
        except Exception as e:
        print(f"\n错误: {e}")
