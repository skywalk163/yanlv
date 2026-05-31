"""
言律语言单元测试 - 解释器测试
"""

import unittest
import sys
import os

# 添加src目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from yanlv.compiler import YanLuCompiler


class TestInterpreter(unittest.TestCase):
    """解释器测试"""
    
    def setUp(self):
        """测试前准备"""
        self.compiler = YanLuCompiler(use_advanced=False)
    
    def test_simple_output(self):
        """测试简单输出"""
        code = '输出"你好"'
        result = self.compiler.run(code)
        
        self.assertEqual(len(result), 1)
        self.assertIn('你好', result[0])
    
    def test_variable_definition(self):
        """测试变量定义"""
        code = '''定义变量x为10
输出x'''
        result = self.compiler.run(code)
        
        self.assertGreater(len(result), 0)
        self.assertIn('10', result[-1])
    
    def test_arithmetic(self):
        """测试算术运算"""
        code = '''定义变量a为10
定义变量b为5
定义变量c为a加b
输出c'''
        result = self.compiler.run(code)
        
        self.assertGreater(len(result), 0)
        # 检查结果包含15
        self.assertTrue(any('15' in r for r in result))
    
    def test_if_statement(self):
        """测试条件语句"""
        code = '''定义变量x为10
如果x大于5则
    输出"大于5"
否则
    输出"小于等于5"'''
        result = self.compiler.run(code)
        
        self.assertGreater(len(result), 0)
        self.assertTrue(any('大于5' in r for r in result))
    
    def test_loop(self):
        """测试循环"""
        code = '''循环3次执行
    输出"循环"'''
        result = self.compiler.run(code)
        
        # 应该输出3次
        loop_count = sum(1 for r in result if '循环' in r)
        self.assertEqual(loop_count, 3)
    
    def test_array(self):
        """测试数组"""
        code = '''定义变量arr为[5,3,8,1,2]
输出arr[0]'''
        result = self.compiler.run(code)
        
        self.assertGreater(len(result), 0)
        self.assertTrue(any('5' in r for r in result))


class TestAdvancedInterpreter(unittest.TestCase):
    """高级解释器测试"""
    
    def setUp(self):
        """测试前准备"""
        self.compiler = YanLuCompiler(use_advanced=True)
    
    def test_causal_chain(self):
        """测试因果链"""
        code = '''定温度是30。
温度大于28，印"开启空调制冷"。'''
        result = self.compiler.run(code)
        
        self.assertGreater(len(result), 0)
        self.assertTrue(any('开启空调制冷' in r for r in result))
    
    def test_advanced_define(self):
        """测试高级定义"""
        code = '定温度是30。'
        result = self.compiler.run(code)
        
        # 定义语句不应该有输出
        self.assertEqual(len(result), 0)
    
    def test_condition_with_and(self):
        """测试组合条件（且）"""
        code = '''定温度是25。
定湿度是80。
温度大于20且湿度大于70，印"温度适宜且潮湿"。'''
        result = self.compiler.run(code)
        
        self.assertGreater(len(result), 0)
        self.assertTrue(any('温度适宜且潮湿' in r for r in result))
    
    def test_range_condition(self):
        """测试范围条件"""
        code = '''定温度是25。
温度在20到30之间，印"温度正常"。'''
        result = self.compiler.run(code)
        
        self.assertGreater(len(result), 0)
        self.assertTrue(any('温度正常' in r for r in result))


if __name__ == '__main__':
    unittest.main()
