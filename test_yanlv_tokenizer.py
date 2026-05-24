"""测试言律语言专用分词器"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from yanlv.lexer.yanlv_tokenizer import create_yanlv_tokenizer

tokenizer = create_yanlv_tokenizer()

test_cases = [
    '输出"你好"',
    '定义变量x为10',
    '定义变量x为10输出x',
    '输出"开始"定义变量x为10输出x输出"结束"',
    '如果条件成立则输出"真"否则输出"假"',
    '循环5次执行输出"循环"结束',
]

print("=" * 60)
print("言律语言专用分词器测试")
print("=" * 60)

for code in test_cases:
    print(f"\n代码: {code}")
    print("-" * 40)

    segments = tokenizer.segment(code)
    print(f"分词结果: {segments}")
    print(f"词元数: {len(segments)}")

print("\n" + "=" * 60)
