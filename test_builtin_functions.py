"""测试内置函数和字符串操作"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from yanlv.lexer import create_lexer
from yanlv.interpreter import create_interpreter

lexer = create_lexer("jieba")
interpreter = create_interpreter()

def run_test(name, code):
    """运行测试"""
    print("=" * 60)
    print(f"测试: {name}")
    print("=" * 60)
    tokens = lexer.tokenize(code)
    output = interpreter.execute(tokens)
    print(f"代码:\n{code}")
    print(f"输出: {output}")
    print()
    return output

# 测试1: 字符串连接
run_test("字符串连接", '''
定义变量s1为"hello"
定义变量s2为"world"
定义变量s3为s1+s2
输出s3
''')

# 测试2: 字符串字面量连接
run_test("字符串字面量连接", '''
定义变量s为"hello"+" "+"world"
输出s
''')

# 测试3: 绝对值函数
run_test("绝对值函数", '''
定义变量x为-10
绝对值x
绝对值-5
''')

# 测试4: 平方根函数
run_test("平方根函数", '''
平方根16
平方根25
平方根2
''')

# 测试5: 幂函数
run_test("幂函数", '''
幂2 10
幂3 3
幂5 2
''')

# 测试6: 取整函数
run_test("取整函数", '''
取整3.7
取整-2.3
取整5.0
''')

# 测试7: 随机数函数
run_test("随机数函数", '''
随机数
随机数1 10
''')

# 测试8: 数组排序
run_test("数组排序", '''
定义变量arr为[3,1,4,1,5,9,2,6]
排序arr
输出arr
''')

# 测试9: 数组反转
run_test("数组反转", '''
定义变量arr为[1,2,3,4,5]
反转arr
输出arr
''')

# 测试10: 数组最大值
run_test("数组最大值", '''
定义变量arr为[3,1,4,1,5,9,2,6]
最大值arr
''')

# 测试11: 数组最小值
run_test("数组最小值", '''
定义变量arr为[3,1,4,1,5,9,2,6]
最小值arr
''')

# 测试12: 数组求和
run_test("数组求和", '''
定义变量arr为[1,2,3,4,5]
求和arr
''')

# 测试13: 综合测试
run_test("综合测试", '''
定义变量a为-25
定义变量b为绝对值a
输出b
平方根b
定义变量nums为[5,2,8,1,9]
排序nums
输出nums
求和nums
''')

print("=" * 60)
print("所有测试完成！")
print("=" * 60)
