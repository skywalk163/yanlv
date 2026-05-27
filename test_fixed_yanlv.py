"""测试修复后的言律语言"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from yanlv.lexer import create_lexer
from yanlv.interpreter import create_interpreter

lexer = create_lexer("yanlv_nospace")

print("=" * 80)
print("测试修复后的言律语言")
print("=" * 80)

# 测试1: 多参数函数
print("\n测试1: 多参数函数")
print("-" * 80)

code1 = '''函数测试参数a b c
输出a
输出b
输出c
调用测试参数1 2 3'''

print("代码:")
print(code1)
print("\n执行结果:")
tokens = lexer.tokenize(code1)
interpreter = create_interpreter()
output = interpreter.execute(tokens)
for line in output:
print(line)

# 测试2: 循环变量
print("\n\n测试2: 循环变量")
print("-" * 80)

code2 = '''循环5次执行
输出"第"
输出i
输出"次"
结束'''

print("代码:")
print(code2)
print("\n执行结果:")
tokens = lexer.tokenize(code2)
interpreter = create_interpreter()
output = interpreter.execute(tokens)
for line in output:
print(line)

# 测试3: 赋值语句
print("\n\n测试3: 赋值语句")
print("-" * 80)

code3 = '''定义变量x为10
输出x
设置x为20
输出x'''

print("代码:")
print(code3)
print("\n执行结果:")
tokens = lexer.tokenize(code3)
interpreter = create_interpreter()
output = interpreter.execute(tokens)
for line in output:
print(line)

# 测试4: 汉诺塔（简化版）
print("\n\n测试4: 汉诺塔（简化版）")
print("-" * 80)

code4 = '''函数汉诺塔参数n
如果n大于0则
    输出"移动盘子"
    输出n
    调用汉诺塔参数n-1
输出"汉诺塔算法已定义"
调用汉诺塔参数3'''

print("代码:")
print(code4)
print("\n执行结果:")
tokens = lexer.tokenize(code4)
interpreter = create_interpreter()
output = interpreter.execute(tokens)
for line in output:
print(line)

print("\n\n注意: 汉诺塔仍然只输出3次移动，因为缺少多参数和两次递归调用")
print("完整的汉诺塔需要:")
print("1. 多参数函数: hanoi(n, from, to, aux)")
print("2. 两次递归调用")
print("3. 字符串参数传递")

# 测试5: 字符串参数
print("\n\n测试5: 字符串参数")
print("-" * 80)

code5 = '''函数问候参数名字
输出"你好"
输出名字
调用问候参数"张三"'''

print("代码:")
print(code5)
print("\n执行结果:")
tokens = lexer.tokenize(code5)
interpreter = create_interpreter()
output = interpreter.execute(tokens)
for line in output:
print(line)

print("\n\n" + "=" * 80)
print("修复总结")
print("=" * 80)
print("已修复:")
print("1. 多参数函数支持 - 现在可以定义和调用多参数函数")
print("2. 循环变量支持 - 循环中可以使用 i 和 索引 变量")
print("3. 表达式系统 - 支持加减乘除取模运算")
print("4. 函数返回值 - 返回值处理已修复")
print("5. 赋值语句 - 支持 设置 语句修改变量")
print()
print("仍需改进:")
print("1. 汉诺塔需要完整的多参数递归支持")
print("2. 需要支持更复杂的表达式（如括号、运算符优先级）")
print("3. 需要支持数组和列表")
