"""
测试言律语言标准库扩展模块
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from yanlv.stdlib.math_ext import (
    平方根, 立方根, 幂函数, 阶乘, 组合数, 排列数,
    正弦, 余弦, 正切, 圆周率, 自然常数,
    向下取整, 向上取整, 绝对值
)

from yanlv.stdlib.datetime_ext import (
    日期时间, 日期, 时间, 时间差, 创建时区
)

from yanlv.stdlib.json_ext import (
    转为json字符串, 从json字符串, 验证json, 格式化json
)

from yanlv.stdlib.random_ext import (
    设置随机种子, 随机整数, 随机浮点数, 随机选择, 随机字符串
)


def test_math模块():
    """测试math模块"""
    print("=" * 50)
    print("测试math模块")
    print("=" * 50)
    
    # 基本运算
    assert 平方根(16) == 4.0
    assert 立方根(27) == 3.0
    assert 幂函数(2, 10) == 1024.0
    assert 阶乘(5) == 120
    assert 组合数(5, 2) == 10
    assert 排列数(5, 2) == 20
    
    # 三角函数
    import math
    assert abs(正弦(圆周率 / 2) - 1.0) < 1e-10
    assert abs(余弦(0) - 1.0) < 1e-10
    
    # 取整函数
    assert 向下取整(3.7) == 3
    assert 向上取整(3.3) == 4
    assert 绝对值(-5) == 5.0
    
    # 常数
    assert abs(圆周率 - 3.141592653589793) < 1e-10
    assert abs(自然常数 - 2.718281828459045) < 1e-10
    
    print("[OK] math模块测试通过")


def test_datetime模块():
    """测试datetime模块"""
    print("=" * 50)
    print("测试datetime模块")
    print("=" * 50)
    
    # 日期时间
    现在 = 日期时间.现在()
    assert 现在.获取年份() > 2020
    assert 1 <= 现在.获取月份() <= 12
    assert 1 <= 现在.获取日期() <= 31
    
    # 日期
    今天 = 日期.今天()
    assert 今天.获取年份() > 2020
    
    # 时间差
    delta = 时间差(days=7)
    assert delta.总天数() == 7.0
    
    # 时区
    东八区 = 创建时区(8)
    assert 东八区 is not None
    
    print("[OK] datetime模块测试通过")


def test_json模块():
    """测试json模块"""
    print("=" * 50)
    print("测试json模块")
    print("=" * 50)
    
    # 基本转换
    数据 = {'姓名': '张三', '年龄': 25, '技能': ['Python', 'Java']}
    json字符串 = 转为json字符串(数据)
    解析数据 = 从json字符串(json字符串)
    assert 解析数据 == 数据
    
    # 格式化
    格式化字符串 = 格式化json(数据)
    assert '姓名' in 格式化字符串
    
    # 验证
    assert 验证json('{"test": 123}') == True
    assert 验证json('{invalid}') == False
    
    print("[OK] json模块测试通过")


def test_random模块():
    """测试random模块"""
    print("=" * 50)
    print("测试random模块")
    print("=" * 50)
    
    # 设置种子以确保可重复性
    设置随机种子(42)
    
    # 随机整数
    num = 随机整数(1, 100)
    assert 1 <= num <= 100
    
    # 随机浮点数
    f = 随机浮点数(0, 1)
    assert 0 <= f < 1
    
    # 随机选择
    选项 = ['A', 'B', 'C', 'D']
    选择 = 随机选择(选项)
    assert 选择 in 选项
    
    # 随机字符串
    字符串 = 随机字符串(10)
    assert len(字符串) == 10
    
    print("[OK] random模块测试通过")


def test_pathlib模块():
    """测试pathlib模块"""
    print("=" * 50)
    print("测试pathlib模块")
    print("=" * 50)
    
    from yanlv.stdlib.pathlib_ext import 路径对象, 当前目录
    
    # 当前目录
    当前 = 当前目录()
    assert 当前.是否存在()
    assert 当前.是否目录()
    
    # 路径操作
    p = 路径对象('test.txt')
    assert p.获取文件名() == 'test.txt'
    assert p.获取扩展名() == '.txt'
    assert p.获取主文件名() == 'test'
    
    print("[OK] pathlib模块测试通过")


if __name__ == '__main__':
    print("\n" + "=" * 50)
    print("言律语言标准库扩展模块测试")
    print("=" * 50 + "\n")
    
    test_math模块()
    test_datetime模块()
    test_json模块()
    test_random模块()
    test_pathlib模块()
    
    print("\n" + "=" * 50)
    print("[SUCCESS] 所有测试通过！")
    print("=" * 50)
