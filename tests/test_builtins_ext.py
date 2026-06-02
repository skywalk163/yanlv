"""
测试言律语言内置函数扩展模块
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from yanlv.builtins_ext import (
    # 数学运算函数
    绝对值, 除法余数, 最大值, 最小值, 幂运算, 四舍五入, 求和,
    # 类型转换函数
    布尔值, 整数, 浮点数, 复数, 字符串, 列表, 元组, 集合,
    不可变集合, 字典, 字节串, 字节数组, 内存视图, 字符转数字, 数字转字符,
    # 序列操作函数
    长度, 范围, 切片对象, 排序, 反转, 枚举, 拉链, 映射, 过滤,
    存在真值, 全部真值,
    # 输入输出函数
    格式化, 对象表示,
    # 类型检查函数
    类型, 是实例, 是子类, 可调用, 有属性,
    # 其他函数
    二进制, 八进制, 十六进制,
)


def test_数学运算函数():
    """测试数学运算函数"""
    # 绝对值
    assert 绝对值(-5) == 5
    assert 绝对值(-3.14) == 3.14
    assert 绝对值(complex(3, 4)) == 5.0
    
    # 除法余数
    assert 除法余数(10, 3) == (3, 1)
    assert 除法余数(-10, 3) == (-4, 2)
    
    # 最大值
    assert 最大值(1, 2, 3) == 3
    assert 最大值([1, 2, 3]) == 3
    assert 最大值([], 默认值=0) == 0
    
    # 最小值
    assert 最小值(1, 2, 3) == 1
    assert 最小值([1, 2, 3]) == 1
    assert 最小值([], 默认值=0) == 0
    
    # 幂运算
    assert 幂运算(2, 10) == 1024
    assert 幂运算(2, 10, 100) == 24
    
    # 四舍五入
    assert 四舍五入(3.14159, 2) == 3.14
    assert 四舍五入(3.5) == 4
    
    # 求和
    assert 求和([1, 2, 3, 4]) == 10
    assert 求和([1, 2, 3], 10) == 16
    
    print("[OK] 数学运算函数测试通过")


def test_类型转换函数():
    """测试类型转换函数"""
    # 布尔值
    assert 布尔值(1) == True
    assert 布尔值(0) == False
    assert 布尔值("") == False
    
    # 整数
    assert 整数('123') == 123
    assert 整数('1010', 进制=2) == 10
    assert 整数(3.14) == 3
    
    # 浮点数
    assert 浮点数('3.14') == 3.14
    assert 浮点数(10) == 10.0
    
    # 复数
    assert 复数(3, 4) == complex(3, 4)
    assert 复数('3+4j') == complex(3, 4)
    
    # 字符串
    assert 字符串(123) == '123'
    assert 字符串([1, 2, 3]) == '[1, 2, 3]'
    
    # 列表
    assert 列表((1, 2, 3)) == [1, 2, 3]
    assert 列表('abc') == ['a', 'b', 'c']
    
    # 元组
    assert 元组([1, 2, 3]) == (1, 2, 3)
    assert 元组('abc') == ('a', 'b', 'c')
    
    # 集合
    assert 集合([1, 2, 2, 3]) == {1, 2, 3}
    
    # 不可变集合
    assert 不可变集合([1, 2, 3]) == frozenset({1, 2, 3})
    
    # 字典
    assert 字典([('a', 1), ('b', 2)]) == {'a': 1, 'b': 2}
    assert 字典(a=1, b=2) == {'a': 1, 'b': 2}
    
    # 字符转数字
    assert 字符转数字('A') == 65
    assert 字符转数字('中') == 20013
    
    # 数字转字符
    assert 数字转字符(65) == 'A'
    assert 数字转字符(20013) == '中'
    
    print("[OK] 类型转换函数测试通过")


def test_序列操作函数():
    """测试序列操作函数"""
    # 长度
    assert 长度([1, 2, 3]) == 3
    assert 长度('hello') == 5
    
    # 范围
    assert 列表(范围(5)) == [0, 1, 2, 3, 4]
    assert 列表(范围(1, 5)) == [1, 2, 3, 4]
    assert 列表(范围(0, 10, 2)) == [0, 2, 4, 6, 8]
    
    # 切片对象
    assert [0, 1, 2, 3, 4, 5][切片对象(1, 4)] == [1, 2, 3]
    
    # 排序
    assert 排序([3, 1, 2]) == [1, 2, 3]
    assert 排序(['abc', 'a', 'abcd'], 键函数=len) == ['a', 'abc', 'abcd']
    
    # 反转
    assert 列表(反转([1, 2, 3])) == [3, 2, 1]
    
    # 枚举
    assert 列表(枚举(['a', 'b', 'c'])) == [(0, 'a'), (1, 'b'), (2, 'c')]
    
    # 拉链
    assert 列表(拉链([1, 2, 3], ['a', 'b', 'c'])) == [(1, 'a'), (2, 'b'), (3, 'c')]
    
    # 映射
    assert 列表(映射(lambda x: x**2, [1, 2, 3])) == [1, 4, 9]
    
    # 过滤
    assert 列表(过滤(lambda x: x > 0, [-1, 0, 1, 2])) == [1, 2]
    assert 列表(过滤(None, [0, 1, '', 'a'])) == [1, 'a']
    
    # 存在真值
    assert 存在真值([0, 0, 1]) == True
    assert 存在真值([0, 0, 0]) == False
    
    # 全部真值
    assert 全部真值([1, 1, 1]) == True
    assert 全部真值([1, 0, 1]) == False
    
    print("[OK] 序列操作函数测试通过")


def test_输入输出函数():
    """测试输入输出函数"""
    # 格式化
    assert 格式化(3.14159, '.2f') == '3.14'
    assert 格式化(255, 'x') == 'ff'
    
    # 对象表示
    assert 对象表示([1, 2, 3]) == '[1, 2, 3]'
    assert 对象表示('hello') == "'hello'"
    
    print("[OK] 输入输出函数测试通过")


def test_类型检查函数():
    """测试类型检查函数"""
    # 类型
    assert 类型(123) == int
    assert 类型('hello') == str
    
    # 是实例
    assert 是实例(123, int) == True
    assert 是实例(123, (int, str)) == True
    
    # 是子类
    assert 是子类(int, object) == True
    
    # 可调用
    assert 可调用(len) == True
    assert 可调用(123) == False
    
    # 有属性
    assert 有属性([1, 2, 3], 'append') == True
    
    print("[OK] 类型检查函数测试通过")


def test_其他函数():
    """测试其他函数"""
    # 二进制
    assert 二进制(10) == '0b1010'
    
    # 八进制
    assert 八进制(10) == '0o12'
    
    # 十六进制
    assert 十六进制(255) == '0xff'
    
    print("[OK] 其他函数测试通过")


if __name__ == '__main__':
    test_数学运算函数()
    test_类型转换函数()
    test_序列操作函数()
    test_输入输出函数()
    test_类型检查函数()
    test_其他函数()
    print("\n[SUCCESS] 所有测试通过！")
