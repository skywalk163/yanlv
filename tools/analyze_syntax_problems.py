"""详细分析言律语言语法问题"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from yanlv.lexer import create_lexer
from yanlv.interpreter import create_interpreter

lexer = create_lexer("yanlv_nospace")

print("=" * 80)
print("言律语言语法问题详细分析")
print("=" * 80)

# 问题1: 多参数函数
print("\n问题1: 多参数函数支持")
print("-" * 80)

code1 = '''函数测试参数a b c
输出a
输出b
输出c
结束
调用测试参数1 2 3'''

print("代码:")
print(code1)
print("\n执行结果:")
tokens = lexer.tokenize(code1)
interpreter = create_interpreter()
output = interpreter.execute(tokens)
for line in output:
    print(line)

print("\n预期结果: 应该输出 1, 2, 3")
print("实际结果: 只输出了第一个参数")

# 问题2: 字符串参数
print("\n\n问题2: 字符串参数传递")
print("-" * 80)

code2 = '''函数问候参数名字
输出"你好"
输出名字
结束
调用问候参数"张三"'''

print("代码:")
print(code2)
print("\n执行结果:")
tokens = lexer.tokenize(code2)
interpreter = create_interpreter()
output = interpreter.execute(tokens)
for line in output:
    print(line)

print("\n预期结果: 应该输出 '你好' 和 '张三'")
print("实际结果: 字符串参数可能无法正确传递")

# 问题3: 表达式求值
print("\n\n问题3: 表达式求值")
print("-" * 80)

code3 = '''定义变量x为10
定义变量y为5
输出x+y
输出x-y
输出x*2'''

print("代码:")
print(code3)
print("\n执行结果:")
tokens = lexer.tokenize(code3)
interpreter = create_interpreter()
output = interpreter.execute(tokens)
for line in output:
    print(line)

print("\n预期结果: 应该输出 15, 5, 20")
print("实际结果: 表达式求值可能不完整")

# 问题4: 嵌套条件
print("\n\n问题4: 嵌套条件语句")
print("-" * 80)

code4 = '''定义变量x为10
如果x大于5则
输出"x大于5"
如果x大于8则
输出"x也大于8"
结束
结束'''

print("代码:")
print(code4)
print("\n执行结果:")
tokens = lexer.tokenize(code4)
interpreter = create_interpreter()
output = interpreter.execute(tokens)
for line in output:
    print(line)

print("\n预期结果: 应该输出两条消息")

# 问题5: 循环变量
print("\n\n问题5: 循环变量支持")
print("-" * 80)

code5 = '''循环5次执行
输出"第"
输出i
输出"次"
结束'''

print("代码:")
print(code5)
print("\n执行结果:")
tokens = lexer.tokenize(code5)
interpreter = create_interpreter()
output = interpreter.execute(tokens)
for line in output:
    print(line)

print("\n预期结果: 应该输出第1次到第5次")
print("实际结果: 循环变量i未定义")

# 问题6: 数组支持
print("\n\n问题6: 数组/列表支持")
print("-" * 80)

code6 = '''定义数组arr为[1,2,3,4,5]
输出arr[0]
输出arr[2]'''

print("代码:")
print(code6)
print("\n执行结果:")
tokens = lexer.tokenize(code6)
interpreter = create_interpreter()
output = interpreter.execute(tokens)
for line in output:
    print(line)

print("\n预期结果: 应该支持数组定义和访问")
print("实际结果: 不支持数组")

# 问题7: 赋值语句
print("\n\n问题7: 赋值语句")
print("-" * 80)

code7 = '''定义变量x为10
设置x为20
输出x'''

print("代码:")
print(code7)
print("\n执行结果:")
tokens = lexer.tokenize(code7)
interpreter = create_interpreter()
output = interpreter.execute(tokens)
for line in output:
    print(line)

print("\n预期结果: 应该输出20")
print("实际结果: 不支持赋值语句")

# 问题8: 函数返回值
print("\n\n问题8: 函数返回值")
print("-" * 80)

code8 = '''函数加法参数a b
返回a+b
结束
定义变量结果为调用加法参数3 5
输出结果'''

print("代码:")
print(code8)
print("\n执行结果:")
tokens = lexer.tokenize(code8)
interpreter = create_interpreter()
output = interpreter.execute(tokens)
for line in output:
    print(line)

print("\n预期结果: 应该输出8")
print("实际结果: 返回值处理不完整")

print("\n\n" + "=" * 80)
print("总结: 言律语言语法实现的主要问题")
print("=" * 80)

problems = [
    ("多参数函数", "函数定义和调用只支持单参数，多参数解析不完整"),
    ("字符串参数", "字符串作为函数参数传递时处理有问题"),
    ("表达式系统", "缺少完整的表达式求值系统，只支持简单的加减"),
    ("嵌套结构", "嵌套的条件和循环可能存在作用域问题"),
    ("循环变量", "循环语句没有提供循环变量（如i）"),
    ("数组支持", "不支持数组和列表类型"),
    ("赋值语句", "缺少变量赋值语句（设置x为...）"),
    ("返回值", "函数返回值处理不完整，无法赋值给变量"),
    ("运算符", "缺少乘除、取模等运算符"),
    ("比较运算", "条件比较只支持简单的大于小于等于"),
]

for i, (name, desc) in enumerate(problems, 1):
    print(f"\n{i}. {name}")
    print(f"   问题: {desc}")
