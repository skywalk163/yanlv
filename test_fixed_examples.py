"""测试修复后的playground示例"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from yanlv.lexer import create_lexer
from yanlv.interpreter import create_interpreter

lexer = create_lexer("yanlv_nospace")

print("=" * 80)
print("测试修复后的playground示例")
print("=" * 80)

# 测试1: 汉诺塔完整版
print("\n测试1: 汉诺塔完整版")
print("-" * 80)

code1 = '''函数汉诺塔参数n from to aux
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

print("代码:")
print(code1)

try:
    tokens = lexer.tokenize(code1)
    interpreter = create_interpreter()
    output = interpreter.execute(tokens)
    print("\n执行结果:")
    for line in output:
        print(line)
    
    move_count = str(output).count("移动盘子")
    print(f"\n移动次数: {move_count}")
    if move_count == 7:
        print("[OK] 汉诺塔算法正确！")
    else:
        print(f"[FAIL] 汉诺塔算法错误（应该是7次，实际{move_count}次）")
except Exception as e:
    print(f"\n错误: {e}")

# 测试2: 冒泡排序简化版
print("\n\n测试2: 冒泡排序简化版")
print("-" * 80)

code2 = '''函数冒泡排序参数n
定义变量i为0
循环n次执行
定义变量j为0
循环n次执行
输出"比较元素"
输出j
输出j+1
结束
结束
结束
输出"排序完成"
结束
调用冒泡排序参数5'''

print("代码:")
print(code2)

try:
    tokens = lexer.tokenize(code2)
    interpreter = create_interpreter()
    output = interpreter.execute(tokens)
    print("\n执行结果:")
    for line in output:
        print(line)
    print("\n[OK] 冒泡排序简化版执行成功！")
except Exception as e:
    print(f"\n错误: {e}")

# 测试3: 否则分支
print("\n\n测试3: 否则分支")
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
    interpreter = create_interpreter()
    output = interpreter.execute(tokens)
    print("\n执行结果:")
    for line in output:
        print(line)
    
    if "x大于5" in str(output) and "x不大于5" not in str(output):
        print("\n[OK] 否则分支正确！")
    else:
        print("\n[FAIL] 否则分支错误！")
except Exception as e:
    print(f"\n错误: {e}")

# 测试4: 否则分支（条件为假）
print("\n\n测试4: 否则分支（条件为假）")
print("-" * 80)

code4 = '''定义变量x为3
如果x大于5则
输出"x大于5"
否则
输出"x不大于5"
结束'''

print("代码:")
print(code4)

try:
    tokens = lexer.tokenize(code4)
    interpreter = create_interpreter()
    output = interpreter.execute(tokens)
    print("\n执行结果:")
    for line in output:
        print(line)
    
    if "x不大于5" in str(output) and "x大于5" not in str(output):
        print("\n[OK] 否则分支正确！")
    else:
        print("\n[FAIL] 否则分支错误！")
except Exception as e:
    print(f"\n错误: {e}")

print("\n" + "=" * 80)
print("测试完成")
print("=" * 80)
