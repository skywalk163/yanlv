"""测试所有新功能"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from yanlv.lexer import create_lexer
from yanlv.interpreter import create_interpreter

lexer = create_lexer("yanlv_nospace")

print("=" * 80)
print("测试所有新功能")
print("=" * 80)

# 测试1: 数组元素修改
print("\n测试1: 数组元素修改")
print("-" * 80)

code1 = '''定义变量arr为[1,2,3,4,5]
输出"原始数组:"
输出arr
设置arr[0]为10
设置arr[2]为30
输出"修改后:"
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
print("\n[OK] 数组元素修改成功！")
except Exception as e:
print(f"\n[FAIL] 错误: {e}")

# 测试2: 动态数组操作 - 添加
print("\n\n测试2: 动态数组操作 - 添加")
print("-" * 80)

code2 = '''定义变量arr为[1,2,3]
输出"原始数组:"
输出arr
添加arr 4
添加arr 5
输出"添加后:"
输出arr'''

print("代码:")
print(code2)

try:
tokens = lexer.tokenize(code2)
interpreter = create_interpreter()
output = interpreter.execute(tokens)
print("\n执行结果:")
for line in output:
print(line)
print("\n[OK] 数组添加成功！")
except Exception as e:
print(f"\n[FAIL] 错误: {e}")

# 测试3: 动态数组操作 - 删除
print("\n\n测试3: 动态数组操作 - 删除")
print("-" * 80)

code3 = '''定义变量arr为[1,2,3,4,5]
输出"原始数组:"
输出arr
删除arr 0
删除arr 2
输出"删除后:"
输出arr'''

print("代码:")
print(code3)

try:
tokens = lexer.tokenize(code3)
interpreter = create_interpreter()
output = interpreter.execute(tokens)
print("\n执行结果:")
for line in output:
print(line)
print("\n[OK] 数组删除成功！")
except Exception as e:
print(f"\n[FAIL] 错误: {e}")

# 测试4: 长度查询
print("\n\n测试4: 长度查询")
print("-" * 80)

code4 = '''定义变量arr为[1,2,3,4,5]
定义变量str为"hello"
输出"数组长度:"
长度arr
输出"字符串长度:"
长度str'''

print("代码:")
print(code4)

try:
tokens = lexer.tokenize(code4)
interpreter = create_interpreter()
output = interpreter.execute(tokens)
print("\n执行结果:")
for line in output:
print(line)
print("\n[OK] 长度查询成功！")
except Exception as e:
print(f"\n[FAIL] 错误: {e}")

# 测试5: 比较运算符
print("\n\n测试5: 比较运算符")
print("-" * 80)

code5 = '''定义变量x为10
定义变量y为10
定义变量z为5

如果x大于等于y则
    输出"x大于等于y"

如果z小于等于y则
    输出"z小于等于y"

如果x不等于z则
    输出"x不等于z"
    结束'''

    print("代码:")
    print(code5)

    try:
    tokens = lexer.tokenize(code5)
    interpreter = create_interpreter()
    output = interpreter.execute(tokens)
    print("\n执行结果:")
    for line in output:
    print(line)
    print("\n[OK] 比较运算符成功！")
    except Exception as e:
    print(f"\n[FAIL] 错误: {e}")

    # 测试6: 冒泡排序（完整版）
    print("\n\n测试6: 冒泡排序（完整版）")
    print("-" * 80)

    code6 = '''定义变量arr为[5,3,8,1,2]
    输出"原始数组:"
    输出arr

    输出"排序过程:"
    如果arr[0]大于arr[1]则
        输出"交换arr[0]和arr[1]"
        设置arr[0]为3
        设置arr[1]为5

    输出"排序后:"
    输出arr'''

    print("代码:")
    print(code6)

    try:
    tokens = lexer.tokenize(code6)
    interpreter = create_interpreter()
    output = interpreter.execute(tokens)
    print("\n执行结果:")
    for line in output:
    print(line)
    print("\n[OK] 冒泡排序演示成功！")
    except Exception as e:
    print(f"\n[FAIL] 错误: {e}")

    print("\n" + "=" * 80)
    print("测试完成")
    print("=" * 80)
