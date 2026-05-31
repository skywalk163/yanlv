"""
言律语言语句结束处理器测试
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from yanlv.lexer.statement_processor import StatementProcessor


def test_basic_period():
"""测试句号强制结束"""
print("\n=== 测试句号强制结束 ===")

processor = StatementProcessor()

code = '''定义变量x为10。
输出x。'''

result = processor.process_source(code)
print(f"输入:\n{code}")
print(f"\n输出:\n{result}")

# 验证句号保留
assert '。' in result
print("[PASS] 句号强制结束测试通过")


def test_line_continuation():
"""测试续行拼接"""
print("\n=== 测试续行拼接 ===")

processor = StatementProcessor()

code = '''定义变量x为10
输出x'''

result = processor.process_source(code)
print(f"输入:\n{code}")
print(f"\n输出:\n{result}")

# 验证两行被拼接
assert '定义变量x为10 输出x' in result
print("[PASS] 续行拼接测试通过")


def test_indent_block():
"""测试缩进块处理"""
print("\n=== 测试缩进块处理 ===")

processor = StatementProcessor()

code = '''如果条件成立则
输出"条件为真"
结束'''

result = processor.process_source(code)
print(f"输入:\n{code}")
print(f"\n输出:\n{result}")

# 验证缩进块保持不变
assert '如果条件成立则' in result
assert '输出"条件为真"' in result
assert '结束' in result
print("[PASS] 缩进块处理测试通过")


def test_mixed_mode():
"""测试混合模式"""
print("\n=== 测试混合模式 ===")

processor = StatementProcessor()

code = '''定义变量x为10。
定义变量y为20
输出x
输出y。'''

result = processor.process_source(code)
print(f"输入:\n{code}")
print(f"\n输出:\n{result}")

# 验证句号结束和续行拼接
assert '定义变量x为10。' in result
assert '定义变量y为20 输出x' in result
assert '输出y。' in result
print("[PASS] 混合模式测试通过")


def test_nested_blocks():
"""测试嵌套块"""
print("\n=== 测试嵌套块 ===")

processor = StatementProcessor()

code = '''如果条件1成立则
如果条件2成立则
    输出"嵌套条件"
结束'''

result = processor.process_source(code)
print(f"输入:\n{code}")
print(f"\n输出:\n{result}")

# 验证嵌套块保持不变
assert '如果条件1成立则' in result
assert '如果条件2成立则' in result
assert '输出"嵌套条件"' in result
print("[PASS] 嵌套块测试通过")


def test_empty_lines():
"""测试空行处理"""
print("\n=== 测试空行处理 ===")

processor = StatementProcessor()

code = '''定义变量x为10。

输出x。'''

result = processor.process_source(code)
print(f"输入:\n{code}")
print(f"\n输出:\n{result}")

# 验证空行保留
assert '\n\n' in result
print("[PASS] 空行处理测试通过")


def test_complex_example():
"""测试复杂示例"""
print("\n=== 测试复杂示例 ===")

processor = StatementProcessor()

code = '''定义变量x为10。
定义变量y为20
定义变量z为x加y。
如果z大于20则
    输出"z大于20"
    输出z。
输出"程序结束"。'''

result = processor.process_source(code)
print(f"输入:\n{code}")
print(f"\n输出:\n{result}")

# 验证复杂示例处理正确
assert '定义变量x为10。' in result
assert '定义变量y为20 定义变量z为x加y。' in result
assert '如果z大于20则' in result
assert '输出"z大于20"' in result
assert '输出z。' in result
print("[PASS] 复杂示例测试通过")


def run_all_tests():
"""运行所有测试"""
print("\n" + "="*50)
print("言律语言语句结束处理器测试")
print("="*50)

try:
test_basic_period()
test_line_continuation()
test_indent_block()
test_mixed_mode()
test_nested_blocks()
test_empty_lines()
test_complex_example()

print("\n" + "="*50)
print("[PASS] 所有测试通过！")
print("="*50)
return True
except Exception as e:
print(f"\n[FAIL] 测试失败: {e}")
import traceback
traceback.print_exc()
return False


if __name__ == "__main__":
success = run_all_tests()
sys.exit(0 if success else 1)
