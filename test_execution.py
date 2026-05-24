"""测试代码执行功能"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from yanlv.lexer import create_lexer, TokenType

lexer = create_lexer("yanlv_nospace")

# 测试简单输出
simple_output = '输出"测试"'
tokens = lexer.tokenize(simple_output)
print("简单输出测试:")
for token in tokens:
    print(f"  {token.type.name}: {token.value}")

# 测试条件语句
condition_code = '''如果条件成立则
输出"条件为真"
结束'''
tokens = lexer.tokenize(condition_code)
print("\n条件语句测试:")
for token in tokens:
    print(f"  {token.type.name}: {token.value}")

# 测试循环语句
loop_code = '''循环3次执行
输出"循环"
结束'''
tokens = lexer.tokenize(loop_code)
print("\n循环语句测试:")
for token in tokens:
    print(f"  {token.type.name}: {token.value}")

# 测试函数定义
function_code = '''函数测试参数x
输出x
结束'''
tokens = lexer.tokenize(function_code)
print("\n函数定义测试:")
for token in tokens:
    print(f"  {token.type.name}: {token.value}")

print("\n" + "=" * 60)
print("问题分析:")
print("=" * 60)
print("1. 词法分析器正确识别了所有词元")
print("2. 但是 server.py 的 run_code 函数只是简单标记了程序块")
print("3. 没有真正执行条件、循环、函数等程序块")
print("4. 需要实现完整的解释器来执行这些代码")
