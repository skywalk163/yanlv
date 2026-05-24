"""测试言律语言的程序块支持"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from yanlv.lexer import create_lexer

lexer = create_lexer("yanlv_nospace")

# 测试程序块
test_cases = [
    ('简单程序块', '''如果条件成立则
输出"条件为真"
输出"执行完成"
结束'''),

    ('嵌套程序块', '''如果条件1成立则
如果条件2成立则
输出"两个条件都成立"
结束
输出"第一个条件成立"
结束'''),

    ('循环程序块', '''循环5次执行
定义变量x为10
输出x
输出"循环一次"
结束'''),

    ('函数程序块', '''函数计算平方参数n
定义变量result为0
返回result
结束
输出"函数已定义"'''),

    ('复杂程序', '''定义变量count为0
循环3次执行
定义变量temp为10
输出temp
如果条件成立则
输出"条件满足"
结束
结束
输出"程序结束"'''),
]

print("=" * 60)
print("言律语言程序块支持测试")
print("=" * 60)

for name, code in test_cases:
    print(f"\n[{name}]")
    print("-" * 40)
    print("代码:")
    print(code)
    print("\n词元分析:")

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

print("\n" + "=" * 60)
print("测试完成！")
print("=" * 60)
