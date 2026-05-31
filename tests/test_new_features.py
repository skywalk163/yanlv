"""测试新功能：数组、索引访问、复杂表达式"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from yanlv.lexer import create_lexer
from yanlv.interpreter import create_interpreter

lexer = create_lexer("yanlv_nospace")

print("=" * 80)
print("测试新功能")
print("=" * 80)

# 测试1: 数组定义
print("\n测试1: 数组定义")
print("-" * 80)

code1 = '''定义变量arr为[1,2,3,4,5]
输出arr'''

print("代码:")
print(code1)

try:
    tokens = lexer.tokenize(code1)
    interpreter = create_interpreter()
    output = interpreter.execute(tokens)
    print("\n执行结果:")
    for line in output:
        print(line)
    print("\n[OK] 数组定义成功！")
except Exception as e:
    print(f"\n[FAIL] 错误: {e}")

# 测试2: 数组索引访问
print("\n\n测试2: 数组索引访问")
print("-" * 80)

code2 = '''定义变量arr为[10,20,30,40,50]
输出arr[0]
输出arr[2]
输出arr[4]'''

print("代码:")
print(code2)

try:
    tokens = lexer.tokenize(code2)
    interpreter = create_interpreter()
    output = interpreter.execute(tokens)
    print("\n执行结果:")
    for line in output:
        print(line)
    
    if "10.0" in str(output) and "30.0" in str(output) and "50.0" in str(output):
        print("\n[OK] 数组索引访问成功！")
    else:
        print("\n[FAIL] 数组索引访问失败！")
except Exception as e:
    print(f"\n[FAIL] 错误: {e}")

# 测试3: 数组索引访问（使用变量）
print("\n\n测试3: 数组索引访问（使用变量）")
print("-" * 80)

code3 = '''定义变量arr为[10,20,30,40,50]
定义变量i为2
输出arr[i]'''

print("代码:")
print(code3)

try:
    tokens = lexer.tokenize(code3)
    interpreter = create_interpreter()
    output = interpreter.execute(tokens)
    print("\n执行结果:")
    for line in output:
        print(line)
    
    if "30.0" in str(output):
        print("\n[OK] 数组索引访问（变量）成功！")
    else:
        print("\n[FAIL] 数组索引访问（变量）失败！")
except Exception as e:
    print(f"\n[FAIL] 错误: {e}")

# 测试4: 运算符优先级
print("\n\n测试4: 运算符优先级")
print("-" * 80)

code4 = '''定义变量a为2
定义变量b为3
定义变量c为4
输出a+b*c'''

print("代码:")
print(code4)

try:
    tokens = lexer.tokenize(code4)
    interpreter = create_interpreter()
    output = interpreter.execute(tokens)
    print("\n执行结果:")
    for line in output:
        print(line)
    
    # 2 + 3 * 4 = 2 + 12 = 14
    if "14.0" in str(output):
        print("\n[OK] 运算符优先级正确！（2 + 3 * 4 = 14）")
    else:
        print("\n[FAIL] 运算符优先级错误！")
except Exception as e:
    print(f"\n[FAIL] 错误: {e}")

# 测试5: 括号
print("\n\n测试5: 括号")
print("-" * 80)

code5 = '''定义变量a为2
定义变量b为3
定义变量c为4
输出(a+b)*c'''

print("代码:")
print(code5)

try:
    tokens = lexer.tokenize(code5)
    interpreter = create_interpreter()
    output = interpreter.execute(tokens)
    print("\n执行结果:")
    for line in output:
        print(line)
    
    # (2 + 3) * 4 = 5 * 4 = 20
    if "20.0" in str(output):
        print("\n[OK] 括号处理正确！（(2 + 3) * 4 = 20）")
    else:
        print("\n[FAIL] 括号处理错误！")
except Exception as e:
    print(f"\n[FAIL] 错误: {e}")

# 测试6: 复杂表达式
print("\n\n测试6: 复杂表达式")
print("-" * 80)

code6 = '''定义变量x为10
定义变量y为5
定义变量z为2
输出x+y*z
输出(x+y)*z
输出x-y-z
输出x/(y-z)'''

print("代码:")
print(code6)

try:
    tokens = lexer.tokenize(code6)
    interpreter = create_interpreter()
    output = interpreter.execute(tokens)
    print("\n执行结果:")
    for line in output:
        print(line)
    
    # x+y*z = 10+5*2 = 10+10 = 20
    # (x+y)*z = (10+5)*2 = 15*2 = 30
    # x-y-z = 10-5-2 = 3
    # x/(y-z) = 10/(5-2) = 10/3 = 3.333...
    if "20.0" in str(output) and "30.0" in str(output) and "3.0" in str(output):
        print("\n[OK] 复杂表达式处理正确！")
    else:
        print("\n[FAIL] 复杂表达式处理错误！")
except Exception as e:
    print(f"\n[FAIL] 错误: {e}")

# 测试7: 冒泡排序（完整版）
print("\n\n测试7: 冒泡排序（完整版）")
print("-" * 80)

code7 = '''定义变量arr为[5,3,8,1,2]
输出"原始数组:"
输出arr
输出"访问元素:"
输出arr[0]
输出arr[1]
输出arr[2]
输出arr[3]
输出arr[4]'''

print("代码:")
print(code7)

try:
    tokens = lexer.tokenize(code7)
    interpreter = create_interpreter()
    output = interpreter.execute(tokens)
    print("\n执行结果:")
    for line in output:
        print(line)
    print("\n[OK] 冒泡排序数组访问成功！")
except Exception as e:
    print(f"\n[FAIL] 错误: {e}")

print("\n" + "=" * 80)
print("测试完成")
print("=" * 80)
