"""测试无空格词法分析器"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from yanlv.lexer import create_lexer

# 使用言律语言无空格分词器
lexer = create_lexer("yanlv_nospace")

test_cases = [
    ('无空格输出', '输出"你好"'),
    ('无空格变量', '定义变量x为10'),
    ('无空格多语句', '定义变量x为10输出x'),
    ('复杂示例', '输出"开始"定义变量x为10输出x输出"结束"'),
]

print("=" * 60)
print("无空格言律语言词法分析测试")
print("=" * 60)

for name, code in test_cases:
    print(f"\n[{name}]")
    print(f"代码: {code}")
    print("-" * 40)

    tokens = lexer.tokenize(code)

    print(f"词元数: {len(tokens)}")
    for i, token in enumerate(tokens):
        print(f"  {i}: {token.type.name:15s} = \"{token.value}\"")

print("\n" + "=" * 60)
print("测试完成！")
print("=" * 60)
