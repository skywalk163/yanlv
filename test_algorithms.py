"""测试汉诺塔和冒泡排序算法"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from yanlv.lexer import create_lexer

lexer = create_lexer("yanlv_nospace")

# 汉诺塔算法
hanoi_code = '''函数汉诺塔参数n from to aux
如果n等于1则
    输出"移动盘子"
    输出from
    输出"到"
    输出to
    否则
        调用汉诺塔参数n-1 from aux to
        输出"移动盘子"
        输出from
        输出"到"
        输出to
        调用汉诺塔参数n-1 aux to from
输出"汉诺塔算法已定义"'''

# 冒泡排序算法
bubble_sort_code = '''函数冒泡排序参数arr n
定义变量i为0
循环n次执行
    定义变量j为0
    循环n-i-1次执行
        如果arr[j]大于arr[j+1]则
            定义变量temp为arr[j]
            赋值arr[j]为arr[j+1]
            赋值arr[j+1]为temp
返回arr
输出"冒泡排序算法已定义"'''

# 简化版汉诺塔
hanoi_simple = '''函数汉诺塔参数n
如果n大于0则
    输出"移动盘子"
    输出n
    调用汉诺塔参数n-1
输出"汉诺塔算法已定义"
调用汉诺塔参数3'''

# 简化版冒泡排序
bubble_simple = '''函数冒泡排序参数n
定义变量i为0
循环n次执行
    定义变量j为0
    循环n次执行
        输出"比较元素"
        输出j
输出"排序完成"
调用冒泡排序参数5'''

test_cases = [
('汉诺塔算法（完整版）', hanoi_code),
('冒泡排序算法（完整版）', bubble_sort_code),
('汉诺塔算法（简化版）', hanoi_simple),
('冒泡排序算法（简化版）', bubble_simple),
]

print("=" * 60)
print("言律语言经典算法测试")
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
