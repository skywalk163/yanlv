"""
言律语言标准库测试
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from yanlv.stdlib import (
    加, 减, 乘, 除, 取余, 幂, 开方, 绝对值,
    长度, 添加, 删除, 排序, 反转, 求和, 平均值,
    分割, 替换, 去空格, 转大写, 转小写,
    随机数, 随机选择,
    当前时间, 当前日期
)


class TestMathFunctions(unittest.TestCase):
    """测试数学函数"""
    
    def test_加法(self):
        self.assertEqual(加(10, 20), 30)
        self.assertEqual(加(1.5, 2.5), 4.0)
    
    def test_减法(self):
        self.assertEqual(减(30, 10), 20)
        self.assertEqual(减(5.5, 2.5), 3.0)
    
    def test_乘法(self):
        self.assertEqual(乘(5, 6), 30)
        self.assertEqual(乘(2.5, 4), 10.0)
    
    def test_除法(self):
        self.assertEqual(除(20, 4), 5.0)
        self.assertEqual(除(10, 2), 5.0)
    
    def test_取余(self):
        self.assertEqual(取余(10, 3), 1)
        self.assertEqual(取余(20, 7), 6)
    
    def test_幂(self):
        self.assertEqual(幂(2, 3), 8)
        self.assertEqual(幂(3, 2), 9)
    
    def test_开方(self):
        self.assertEqual(开方(4), 2.0)
        self.assertEqual(开方(9), 3.0)
    
    def test_绝对值(self):
        self.assertEqual(绝对值(-10), 10)
        self.assertEqual(绝对值(10), 10)


class TestArrayFunctions(unittest.TestCase):
    """测试数组函数"""
    
    def test_长度(self):
        self.assertEqual(长度([1, 2, 3]), 3)
        self.assertEqual(长度("hello"), 5)
    
    def test_添加(self):
        arr = [1, 2, 3]
        result = 添加(arr, 4)
        self.assertEqual(result, [1, 2, 3, 4])
    
    def test_删除(self):
        arr = [1, 2, 3, 2]
        result = 删除(arr, 2)
        self.assertEqual(result, [1, 3, 2])
    
    def test_排序(self):
        arr = [3, 1, 2]
        result = 排序(arr)
        self.assertEqual(result, [1, 2, 3])
    
    def test_反转(self):
        arr = [1, 2, 3]
        result = 反转(arr)
        self.assertEqual(result, [3, 2, 1])
    
    def test_求和(self):
        self.assertEqual(求和([1, 2, 3, 4, 5]), 15)
    
    def test_平均值(self):
        self.assertEqual(平均值([1, 2, 3, 4, 5]), 3.0)


class TestStringFunctions(unittest.TestCase):
    """测试字符串函数"""
    
    def test_分割(self):
        result = 分割("a,b,c", ",")
        self.assertEqual(result, ["a", "b", "c"])
    
    def test_替换(self):
        result = 替换("hello world", "world", "python")
        self.assertEqual(result, "hello python")
    
    def test_去空格(self):
        result = 去空格("  hello  ")
        self.assertEqual(result, "hello")
    
    def test_转大写(self):
        result = 转大写("hello")
        self.assertEqual(result, "HELLO")
    
    def test_转小写(self):
        result = 转小写("HELLO")
        self.assertEqual(result, "hello")


class TestRandomFunctions(unittest.TestCase):
    """测试随机函数"""
    
    def test_随机数(self):
        result = 随机数(1, 10)
        self.assertGreaterEqual(result, 1)
        self.assertLessEqual(result, 10)
    
    def test_随机选择(self):
        arr = [1, 2, 3, 4, 5]
        result = 随机选择(arr)
        self.assertIn(result, arr)


class TestTimeFunctions(unittest.TestCase):
    """测试时间函数"""
    
    def test_当前时间(self):
        result = 当前时间()
        self.assertIsInstance(result, str)
        self.assertIn('-', result)
    
    def test_当前日期(self):
        result = 当前日期()
        self.assertIsInstance(result, str)
        self.assertIn('-', result)


if __name__ == '__main__':
    unittest.main()
