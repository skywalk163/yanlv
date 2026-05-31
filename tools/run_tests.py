#!/usr/bin/env python3
"""
言律语言测试运行脚本
"""

import unittest
import sys
import os

# 添加src目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def run_all_tests():
    """运行所有测试"""
    # 发现所有测试
    loader = unittest.TestLoader()
    
    # 单元测试
    unit_tests = loader.discover('tests/unit', pattern='test_*.py')
    
    # 集成测试
    integration_tests = loader.discover('tests/integration', pattern='test_*.py')
    
    # 创建测试套件
    suite = unittest.TestSuite()
    suite.addTests(unit_tests)
    suite.addTests(integration_tests)
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # 返回退出码
    return 0 if result.wasSuccessful() else 1

def run_unit_tests():
    """只运行单元测试"""
    loader = unittest.TestLoader()
    suite = loader.discover('tests/unit', pattern='test_*.py')
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return 0 if result.wasSuccessful() else 1

def run_integration_tests():
    """只运行集成测试"""
    loader = unittest.TestLoader()
    suite = loader.discover('tests/integration', pattern='test_*.py')
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return 0 if result.wasSuccessful() else 1

if __name__ == '__main__':
    if len(sys.argv) > 1:
        test_type = sys.argv[1]
        if test_type == 'unit':
            sys.exit(run_unit_tests())
        elif test_type == 'integration':
            sys.exit(run_integration_tests())
        else:
            print(f"未知的测试类型: {test_type}")
            print("用法: python run_tests.py [unit|integration]")
            sys.exit(1)
    else:
        sys.exit(run_all_tests())
