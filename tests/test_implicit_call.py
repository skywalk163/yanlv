"""
言律语言意合式函数调用测试
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from yanlv.implicit_call import (
    ImplicitCallResolver, ChainCallBuilder, CallContext,
    ParameterType, create_implicit_call_resolver, create_chain_builder
)


class TestImplicitCallResolver(unittest.TestCase):
    """测试意合式调用解析器"""
    
    def setUp(self):
        self.resolver = create_implicit_call_resolver()
    
    def test_infer_parameters_exact_match(self):
        """测试参数数量匹配"""
        args = self.resolver.infer_parameters('加', [10, 20], CallContext())
        self.assertEqual(len(args), 2)
        self.assertEqual(args[0], 10)
        self.assertEqual(args[1], 20)
    
    def test_infer_parameters_from_context(self):
        """测试从上下文推断参数"""
        context = CallContext()
        context.recent_values = [5]
        
        args = self.resolver.infer_parameters('加', [10], context)
        self.assertEqual(len(args), 2)
        self.assertEqual(args[0], 10)
        self.assertEqual(args[1], 5)
    
    def test_parse_implicit_call(self):
        """测试解析意合式调用"""
        func_name, args = self.resolver.parse_implicit_call('加 10 20')
        
        self.assertEqual(func_name, '加')
        self.assertEqual(len(args), 2)
        self.assertEqual(args[0], 10.0)
        self.assertEqual(args[1], 20.0)
    
    def test_execute_function(self):
        """测试执行函数"""
        result = self.resolver._execute_function('加', [10, 20])
        self.assertEqual(result, 30)
        
        result = self.resolver._execute_function('减', [30, 10])
        self.assertEqual(result, 20)
        
        result = self.resolver._execute_function('乘', [5, 6])
        self.assertEqual(result, 30)
        
        result = self.resolver._execute_function('除', [20, 4])
        self.assertEqual(result, 5.0)


class TestChainCallBuilder(unittest.TestCase):
    """测试链式调用构建器"""
    
    def setUp(self):
        self.resolver = create_implicit_call_resolver()
        self.builder = create_chain_builder(self.resolver)
    
    def test_single_call(self):
        """测试单次调用"""
        result = (self.builder
                 .with_value(10)
                 .then('加', 5)
                 .execute())
        
        self.assertEqual(result, 15)
    
    def test_chain_calls(self):
        """测试链式调用"""
        result = (self.builder
                 .with_value(10)
                 .then('加', 5)
                 .then('乘', 2)
                 .execute())
        
        # (10 + 5) * 2 = 30
        self.assertEqual(result, 30)
    
    def test_complex_chain(self):
        """测试复杂链式调用"""
        result = (self.builder
                 .with_value(100)
                 .then('减', 20)
                 .then('除', 2)
                 .then('加', 5)
                 .execute())
        
        # ((100 - 20) / 2) + 5 = 45
        self.assertEqual(result, 45.0)


class TestCallContext(unittest.TestCase):
    """测试调用上下文"""
    
    def test_context_with_variables(self):
        """测试带变量的上下文"""
        context = CallContext()
        context.available_variables = {
            'x': 10,
            'y': 20,
            'name': 'test'
        }
        
        self.assertIn('x', context.available_variables)
        self.assertEqual(context.available_variables['x'], 10)
    
    def test_context_with_recent_values(self):
        """测试带最近值的上下文"""
        context = CallContext()
        context.recent_values = [1, 2, 3, 4, 5]
        
        self.assertEqual(len(context.recent_values), 5)
        self.assertEqual(context.recent_values[-1], 5)


class TestFunctionSignatures(unittest.TestCase):
    """测试函数签名"""
    
    def setUp(self):
        self.resolver = create_implicit_call_resolver()
    
    def test_builtin_function_signatures(self):
        """测试内置函数签名"""
        self.assertIn('加', self.resolver.function_signatures)
        self.assertIn('减', self.resolver.function_signatures)
        self.assertIn('乘', self.resolver.function_signatures)
        self.assertIn('除', self.resolver.function_signatures)
        self.assertIn('映射', self.resolver.function_signatures)
        self.assertIn('过滤', self.resolver.function_signatures)
    
    def test_function_signature_structure(self):
        """测试函数签名结构"""
        sig = self.resolver.function_signatures['加']
        
        self.assertEqual(sig.name, '加')
        self.assertEqual(len(sig.parameters), 2)
        self.assertEqual(sig.parameters[0].name, 'a')
        self.assertEqual(sig.parameters[1].name, 'b')


if __name__ == '__main__':
    unittest.main()
