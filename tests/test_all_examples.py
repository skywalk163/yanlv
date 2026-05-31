"""测试所有示例代码"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from yanlv.lexer import Lexer

lexer = Lexer()

examples = [
('Hello World', '输出 "你好，言律语言！"\n输出 "这是一个中文编程语言"'),
('变量定义', '定义 变量 x 为 10\n定义 变量 y 为 20\n输出 x\n输出 y'),
('字符串输出', '输出 "言律语言"\n输出 "支持中文编程"\n输出 "让编程更简单"'),
('数字运算', '定义 变量 a 为 10\n定义 变量 b 为 20\n输出 a\n输出 b\n输出 "计算完成"'),
('条件语句', '如果 条件 成立 则\n  输出 "条件为真"\n否则\n  输出 "条件为假"'),
('循环语句', '循环 5 次 执行\n  输出 "这是循环"\n结束'),
('函数定义', '函数 加法 参数 a b\n  返回 a + b\n结束\n输出 "函数已定义"'),
('多行输出', '输出 "第一行"\n输出 "第二行"\n输出 "第三行"\n输出 "完成"'),
]

print("=" * 60)
print("言律语言示例代码测试")
print("=" * 60)

for name, code in examples:
print(f"\n[{name}]")
print("-" * 40)

tokens = lexer.tokenize(code)

# 统计词元类型
token_types = {}
for token in tokens:
token_type = token.type.name
token_types[token_type] = token_types.get(token_type, 0) + 1

print(f"总词元数: {len(tokens)}")
print(f"词元类型分布:")
for token_type, count in sorted(token_types.items()):
print(f"  {token_type:15s}: {count}")

# 显示前5个词元
print(f"前5个词元:")
for i, token in enumerate(tokens[:5]):
print(f"  {i}: {token.type.name:15s} = \"{token.value}\"")

print("\n" + "=" * 60)
print("所有示例测试完成！")
print("=" * 60)
