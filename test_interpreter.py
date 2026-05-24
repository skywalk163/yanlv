"""测试解释器"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from yanlv.lexer import create_lexer
from yanlv.interpreter import create_interpreter

lexer = create_lexer("yanlv_nospace")
interpreter = create_interpreter()

# 测试1: 简单输出
print("=" * 60)
print("测试1: 简单输出")
print("=" * 60)
code = '输出"你好"'
tokens = lexer.tokenize(code)
output = interpreter.execute(tokens)
print(f"代码: {code}")
print(f"输出: {output}")

# 测试2: 变量定义和输出
print("\n" + "=" * 60)
print("测试2: 变量定义和输出")
print("=" * 60)
code = '定义变量x为10\n输出x'
tokens = lexer.tokenize(code)
output = interpreter.execute(tokens)
print(f"代码: {code}")
print(f"输出: {output}")

# 测试3: 循环语句
print("\n" + "=" * 60)
print("测试3: 循环语句")
print("=" * 60)
code = '循环3次执行\n输出"循环"\n结束'
tokens = lexer.tokenize(code)
output = interpreter.execute(tokens)
print(f"代码: {code}")
print(f"输出: {output}")

# 测试4: 条件语句
print("\n" + "=" * 60)
print("测试4: 条件语句")
print("=" * 60)
code = '如果条件成立则\n输出"条件为真"\n结束'
tokens = lexer.tokenize(code)
output = interpreter.execute(tokens)
print(f"代码: {code}")
print(f"输出: {output}")

# 测试5: 函数定义
print("\n" + "=" * 60)
print("测试5: 函数定义")
print("=" * 60)
code = '函数测试参数x\n输出x\n结束\n输出"函数已定义"'
tokens = lexer.tokenize(code)
output = interpreter.execute(tokens)
print(f"代码: {code}")
print(f"输出: {output}")

# 测试6: 复杂程序
print("\n" + "=" * 60)
print("测试6: 复杂程序")
print("=" * 60)
code = '定义变量count为0\n循环3次执行\n输出"循环"\n结束\n输出"完成"'
tokens = lexer.tokenize(code)
output = interpreter.execute(tokens)
print(f"代码: {code}")
print(f"输出: {output}")

print("\n" + "=" * 60)
print("所有测试完成！")
print("=" * 60)
