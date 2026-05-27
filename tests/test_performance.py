"""
言律语言性能优化测试
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from yanlv.performance import (
    PerformanceMonitor, OptimizedLexer, OptimizedParser,
    OptimizedCodeGenerator, BatchProcessor, cached, memoize,
    create_performance_monitor
)


class TestPerformanceMonitor(unittest.TestCase):
    """测试性能监控器"""
    
    def setUp(self):
        self.monitor = create_performance_monitor()
    
    def test_measure_operation(self):
        """测试操作测量"""
        with self.monitor.measure('test_op') as ctx:
            ctx.set_input_size(100)
            # 模拟操作
            pass
        
        summary = self.monitor.get_summary()
        self.assertIn('test_op', summary)
        self.assertEqual(summary['test_op']['count'], 1)
    
    def test_multiple_operations(self):
        """测试多次操作"""
        for i in range(5):
            with self.monitor.measure('multi_op') as ctx:
                ctx.set_input_size(100 * (i + 1))
        
        summary = self.monitor.get_summary()
        self.assertEqual(summary['multi_op']['count'], 5)


class TestOptimizedLexer(unittest.TestCase):
    """测试优化词法分析器"""
    
    def setUp(self):
        self.lexer = OptimizedLexer()
    
    def test_tokenize_simple(self):
        """测试简单词法分析"""
        source = "定义变量x为10"
        tokens = self.lexer.tokenize_optimized(source)
        
        self.assertGreater(len(tokens), 0)
    
    def test_tokenize_multiline(self):
        """测试多行词法分析"""
        source = """
定义变量x为10
定义变量y为20
输出x加y
"""
        tokens = self.lexer.tokenize_optimized(source)
        
        self.assertGreater(len(tokens), 0)
    
    def test_keyword_detection(self):
        """测试关键字检测"""
        self.assertTrue(self.lexer._is_keyword('定义'))
        self.assertTrue(self.lexer._is_keyword('变量'))
        self.assertFalse(self.lexer._is_keyword('xyz'))
    
    def test_caching(self):
        """测试缓存"""
        source = "定义变量x为10"
        
        # 第一次调用
        tokens1 = self.lexer.tokenize_optimized(source)
        
        # 第二次调用（应该从缓存获取）
        tokens2 = self.lexer.tokenize_optimized(source)
        
        self.assertEqual(len(tokens1), len(tokens2))


class TestOptimizedParser(unittest.TestCase):
    """测试优化语法分析器"""
    
    def setUp(self):
        self.parser = OptimizedParser()
    
    def test_parse_simple(self):
        """测试简单语法分析"""
        tokens = [
            {'value': '定义', 'line': 1, 'column': 1},
            {'value': '变量', 'line': 1, 'column': 3},
            {'value': 'x', 'line': 1, 'column': 5},
        ]
        ast = self.parser.parse_optimized(tokens)
        
        self.assertIsNotNone(ast)
        self.assertEqual(ast['type'], 'Program')
    
    def test_precedence(self):
        """测试优先级"""
        self.assertEqual(self.parser._get_precedence('+'), 5)
        self.assertEqual(self.parser._get_precedence('*'), 6)
        self.assertGreater(self.parser._get_precedence('*'), 
                          self.parser._get_precedence('+'))


class TestOptimizedCodeGenerator(unittest.TestCase):
    """测试优化代码生成器"""
    
    def setUp(self):
        self.generator = OptimizedCodeGenerator()
    
    def test_generate_simple(self):
        """测试简单代码生成"""
        ast = {
            'type': 'Program',
            'statements': [
                {'type': 'Expression', 'value': 'x'}
            ]
        }
        code = self.generator.generate_optimized(ast)
        
        self.assertIn('x', code)
    
    def test_template_caching(self):
        """测试模板缓存"""
        template1 = self.generator._get_template('VariableDeclaration')
        template2 = self.generator._get_template('VariableDeclaration')
        
        self.assertEqual(template1, template2)


class TestBatchProcessor(unittest.TestCase):
    """测试批处理器"""
    
    def test_batch_processing(self):
        """测试批处理"""
        processor = BatchProcessor(batch_size=10)
        items = list(range(25))
        
        results = processor.process_batch(items, lambda x: x * 2)
        
        self.assertEqual(len(results), 25)
        self.assertEqual(results[0], 0)
        self.assertEqual(results[24], 48)


class TestDecorators(unittest.TestCase):
    """测试装饰器"""
    
    def test_cached_decorator(self):
        """测试缓存装饰器"""
        call_count = 0
        
        @cached(maxsize=10)
        def expensive_function(x):
            nonlocal call_count
            call_count += 1
            return x * 2
        
        # 第一次调用
        result1 = expensive_function(5)
        self.assertEqual(result1, 10)
        self.assertEqual(call_count, 1)
        
        # 第二次调用（应该从缓存获取）
        result2 = expensive_function(5)
        self.assertEqual(result2, 10)
        self.assertEqual(call_count, 1)  # 没有增加
    
    def test_memoize_decorator(self):
        """测试记忆化装饰器"""
        call_count = 0
        
        @memoize
        def fibonacci(n):
            nonlocal call_count
            call_count += 1
            if n <= 1:
                return n
            return fibonacci(n - 1) + fibonacci(n - 2)
        
        # 计算fibonacci(10)
        result = fibonacci(10)
        self.assertEqual(result, 55)


if __name__ == '__main__':
    unittest.main()
