"""
言律语言集成测试 - 示例文件测试
"""

import unittest
import sys
import os
import glob

# 添加src目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from yanlv.compiler import YanLuCompiler


class TestExampleFiles(unittest.TestCase):
    """示例文件测试"""
    
    def setUp(self):
        """测试前准备"""
        self.compiler = YanLuCompiler(use_advanced=True)
        self.examples_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'examples')
    
    def test_simple_test(self):
        """测试简单测试文件"""
        file_path = os.path.join(self.examples_dir, 'simple_test.yan')
        if not os.path.exists(file_path):
            self.skipTest(f"文件不存在: {file_path}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            code = f.read()
        
        # 执行代码，不应该抛出异常
        try:
            result = self.compiler.run(code)
            self.assertIsInstance(result, list)
        except Exception as e:
            self.fail(f"执行失败: {e}")
    
    def test_conditions_and_loops(self):
        """测试条件和循环示例"""
        file_path = os.path.join(self.examples_dir, '条件和循环.yan')
        if not os.path.exists(file_path):
            self.skipTest(f"文件不存在: {file_path}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            code = f.read()
        
        try:
            result = self.compiler.run(code)
            self.assertIsInstance(result, list)
            # 应该有输出
            self.assertGreater(len(result), 0)
        except Exception as e:
            self.fail(f"执行失败: {e}")
    
    def test_string_processing(self):
        """测试字符串处理示例"""
        file_path = os.path.join(self.examples_dir, '字符串处理.yan')
        if not os.path.exists(file_path):
            self.skipTest(f"文件不存在: {file_path}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            code = f.read()
        
        try:
            result = self.compiler.run(code)
            self.assertIsInstance(result, list)
        except Exception as e:
            self.fail(f"执行失败: {e}")
    
    def test_math_calculation(self):
        """测试数学计算示例"""
        file_path = os.path.join(self.examples_dir, '数学计算.yan')
        if not os.path.exists(file_path):
            self.skipTest(f"文件不存在: {file_path}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            code = f.read()
        
        try:
            result = self.compiler.run(code)
            self.assertIsInstance(result, list)
        except Exception as e:
            self.fail(f"执行失败: {e}")
    
    def test_simple_causal(self):
        """测试简单因果链"""
        file_path = os.path.join(self.examples_dir, '..', 'test_simple_causal.yan')
        if not os.path.exists(file_path):
            self.skipTest(f"文件不存在: {file_path}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            code = f.read()
        
        try:
            result = self.compiler.run(code)
            self.assertIsInstance(result, list)
            self.assertGreater(len(result), 0)
            # 应该输出"开启空调制冷"
            self.assertTrue(any('开启空调制冷' in r for r in result))
        except Exception as e:
            self.fail(f"执行失败: {e}")


class TestPlaygroundExamples(unittest.TestCase):
    """Playground示例测试"""
    
    def setUp(self):
        """测试前准备"""
        self.compiler = YanLuCompiler(use_advanced=False)
    
    def test_hello_world(self):
        """测试Hello World示例"""
        code = '输出"你好，言律语言！"'
        result = self.compiler.run(code)
        
        self.assertEqual(len(result), 1)
        self.assertIn('你好，言律语言！', result[0])
    
    def test_variable_definition(self):
        """测试变量定义示例"""
        code = '''定义变量x为10
输出x'''
        result = self.compiler.run(code)
        
        self.assertGreater(len(result), 0)
        self.assertTrue(any('10' in r for r in result))
    
    def test_condition_block(self):
        """测试条件程序块示例"""
        code = '''如果条件成立则
    输出"条件为真"
    输出"执行完成"'''
        result = self.compiler.run(code)
        
        self.assertGreater(len(result), 0)
    
    def test_loop_block(self):
        """测试循环程序块示例"""
        code = '''循环5次执行
    定义变量x为10
    输出x
    输出"循环一次"'''
        result = self.compiler.run(code)
        
        self.assertGreater(len(result), 0)
    
    def test_function_block(self):
        """测试函数程序块示例"""
        code = '''函数计算平方参数n
    定义变量result为0
    返回result
输出"函数已定义"'''
        result = self.compiler.run(code)
        
        self.assertGreater(len(result), 0)
    
    def test_hanoi(self):
        """测试汉诺塔示例"""
        code = '''函数汉诺塔参数n from to aux
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
输出"汉诺塔算法已定义"
调用汉诺塔参数3 A C B'''
        result = self.compiler.run(code)
        
        self.assertGreater(len(result), 0)
    
    def test_array_operations(self):
        """测试数组操作示例"""
        code = '''定义变量arr为[5,3,8,1,2]
输出"原始数组:"
输出arr
输出"访问元素:"
输出arr[0]
输出arr[1]
输出arr[2]
输出arr[3]
输出arr[4]'''
        result = self.compiler.run(code)
        
        self.assertGreater(len(result), 0)


if __name__ == '__main__':
    unittest.main()
