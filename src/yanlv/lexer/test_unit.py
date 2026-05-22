#!/usr/bin/env python3
"""
言律语言词法分析器 - 单元测试

测试所有核心模块的功能
"""

import sys
import os
import unittest
from typing import List

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 导入模块
from lexer_token import Token, TokenType
from tokenizer import YanLuTokenizer, JiebaTokenizer
from matcher import TokenMatcher, create_token_matcher
from error_handler import ErrorHandler, ErrorCode, ErrorSeverity
from context_manager import ContextManager, ContextType
from pattern_manager import PatternManager, PatternType
from performance_optimizer import PerformanceOptimizer, OptimizationConfig, OptimizationLevel
from utils import Position, Range, ErrorInfo, PerformanceStats, Cache
from lexer_modular import ModularYanLuLexer, create_lexer


class TestLexerToken(unittest.TestCase):
    """测试词元定义"""
    
    def test_token_creation(self):
        """测试词元创建"""
        token = Token(TokenType.IDENTIFIER, "变量", 1, 1, "变量")
        self.assertEqual(token.type, TokenType.IDENTIFIER)
        self.assertEqual(token.value, "变量")
        self.assertEqual(token.line, 1)
        self.assertEqual(token.column, 1)
    
    def test_token_type_count(self):
        """测试词元类型数量"""
        self.assertEqual(len(TokenType), 59)
    
    def test_token_is_type(self):
        """测试词元类型检查"""
        token = Token(TokenType.NUMBER, "123", 1, 1, "123")
        self.assertTrue(token.is_number())
        self.assertFalse(token.is_identifier())
        self.assertFalse(token.is_string())
    
    def test_token_to_dict(self):
        """测试词元转换为字典"""
        token = Token(TokenType.IDENTIFIER, "变量", 1, 1, "变量")
        token_dict = token.to_dict()
        self.assertEqual(token_dict['type'], 'IDENTIFIER')
        self.assertEqual(token_dict['value'], '变量')
        self.assertEqual(token_dict['line'], 1)
        self.assertEqual(token_dict['column'], 1)


class TestTokenizer(unittest.TestCase):
    """测试分词器"""
    
    def test_jieba_tokenizer_creation(self):
        """测试jieba分词器创建"""
        tokenizer = JiebaTokenizer()
        self.assertEqual(tokenizer.get_segmenter_type(), "jieba")
    
    def test_tokenizer_segment(self):
        """测试分词功能"""
        tokenizer = JiebaTokenizer()
        segments = tokenizer.segment("这是一个测试")
        self.assertIsInstance(segments, list)
        self.assertTrue(len(segments) > 0)
    
    def test_tokenizer_factory(self):
        """测试分词器工厂"""
        tokenizer = YanLuTokenizer.create("jieba")
        self.assertEqual(tokenizer.get_segmenter_type(), "jieba")
    
    def test_available_tokenizers(self):
        """测试可用分词器列表"""
        tokenizers = YanLuTokenizer.get_available_tokenizers()
        self.assertIn("jieba", tokenizers)


class TestMatcher(unittest.TestCase):
    """测试词元匹配器"""
    
    def test_matcher_creation(self):
        """测试匹配器创建"""
        matcher = TokenMatcher()
        self.assertIsNotNone(matcher)
    
    def test_match_number(self):
        """测试数字匹配"""
        matcher = TokenMatcher()
        token = matcher.match_token("123", 0, 1, 1)
        self.assertIsNotNone(token)
        self.assertEqual(token.type, TokenType.NUMBER)
    
    def test_match_identifier(self):
        """测试标识符匹配"""
        matcher = TokenMatcher()
        token = matcher.match_token("变量", 0, 1, 1)
        self.assertIsNotNone(token)
        self.assertEqual(token.type, TokenType.IDENTIFIER)
    
    def test_match_chinese_punctuation(self):
        """测试中文标点匹配"""
        matcher = TokenMatcher()
        token = matcher.match_token("。", 0, 1, 1)
        self.assertIsNotNone(token)
        self.assertEqual(token.type, TokenType.PERIOD)


class TestErrorHandler(unittest.TestCase):
    """测试错误处理器"""
    
    def test_error_handler_creation(self):
        """测试错误处理器创建"""
        handler = ErrorHandler()
        self.assertIsNotNone(handler)
    
    def test_add_error(self):
        """测试添加错误"""
        handler = ErrorHandler()
        position = Position(line=1, column=1, offset=0)
        handler.add_error(ErrorCode.LEXER_INVALID_CHAR, "测试错误", position)
        self.assertEqual(handler.get_error_count(), 1)
    
    def test_add_warning(self):
        """测试添加警告"""
        handler = ErrorHandler()
        position = Position(line=1, column=1, offset=0)
        handler.add_warning(ErrorCode.LEXER_INVALID_CHAR, "测试警告", position)
        self.assertEqual(handler.get_warning_count(), 1)
    
    def test_has_errors(self):
        """测试错误检查"""
        handler = ErrorHandler()
        self.assertFalse(handler.has_errors())
        
        position = Position(line=1, column=1, offset=0)
        handler.add_error(ErrorCode.LEXER_INVALID_CHAR, "测试错误", position)
        self.assertTrue(handler.has_errors())


class TestContextManager(unittest.TestCase):
    """测试上下文管理器"""
    
    def test_context_manager_creation(self):
        """测试上下文管理器创建"""
        manager = ContextManager()
        self.assertIsNotNone(manager)
    
    def test_push_context(self):
        """测试推入上下文"""
        manager = ContextManager()
        position = Position(line=1, column=1, offset=0)
        context = manager.push_context(ContextType.FUNCTION, position)
        self.assertEqual(context.type, ContextType.FUNCTION)
        self.assertEqual(manager.get_context_depth(), 1)
    
    def test_pop_context(self):
        """测试弹出上下文"""
        manager = ContextManager()
        position = Position(line=1, column=1, offset=0)
        manager.push_context(ContextType.FUNCTION, position)
        
        end_position = Position(line=10, column=1, offset=100)
        context = manager.pop_context(end_position)
        self.assertEqual(manager.get_context_depth(), 0)
    
    def test_symbol_table(self):
        """测试符号表"""
        manager = ContextManager()
        manager.add_symbol("变量", 123, "variable")
        
        self.assertTrue(manager.has_symbol("变量"))
        self.assertEqual(manager.get_symbol("变量"), 123)


class TestPatternManager(unittest.TestCase):
    """测试模式管理器"""
    
    def test_pattern_manager_creation(self):
        """测试模式管理器创建"""
        manager = PatternManager()
        self.assertIsNotNone(manager)
    
    def test_builtin_patterns(self):
        """测试内置模式"""
        manager = PatternManager()
        self.assertGreater(manager.get_pattern_count(), 0)
    
    def test_add_pattern(self):
        """测试添加模式"""
        manager = PatternManager()
        success = manager.add_pattern(
            name="test_pattern",
            pattern=r"^test$",
            token_type=TokenType.IDENTIFIER,
            priority=100
        )
        self.assertTrue(success)
        self.assertTrue(manager.has_pattern("test_pattern"))
    
    def test_match_pattern(self):
        """测试模式匹配"""
        manager = PatternManager()
        result = manager.match("123")
        self.assertIsNotNone(result)
        self.assertEqual(result[0], TokenType.NUMBER)


class TestPerformanceOptimizer(unittest.TestCase):
    """测试性能优化器"""
    
    def test_optimizer_creation(self):
        """测试优化器创建"""
        optimizer = PerformanceOptimizer()
        self.assertIsNotNone(optimizer)
    
    def test_optimization_config(self):
        """测试优化配置"""
        config = OptimizationConfig(
            level=OptimizationLevel.ADVANCED,
            enable_cache=True,
            cache_size=2000
        )
        optimizer = PerformanceOptimizer(config)
        self.assertEqual(optimizer.config.level, OptimizationLevel.ADVANCED)
    
    def test_cache_stats(self):
        """测试缓存统计"""
        optimizer = PerformanceOptimizer()
        stats = optimizer.get_cache_stats()
        self.assertIsInstance(stats, dict)
    
    def test_performance_stats(self):
        """测试性能统计"""
        optimizer = PerformanceOptimizer()
        stats = optimizer.get_performance_stats()
        self.assertIsInstance(stats, dict)
        self.assertIn('total_operations', stats)


class TestUtils(unittest.TestCase):
    """测试工具模块"""
    
    def test_position(self):
        """测试位置"""
        position = Position(line=1, column=5, offset=10)
        self.assertEqual(position.line, 1)
        self.assertEqual(position.column, 5)
        self.assertEqual(position.offset, 10)
    
    def test_range(self):
        """测试范围"""
        start = Position(line=1, column=1, offset=0)
        end = Position(line=1, column=10, offset=10)
        range_obj = Range(start=start, end=end)
        self.assertEqual(range_obj.start, start)
        self.assertEqual(range_obj.end, end)
    
    def test_cache(self):
        """测试缓存"""
        cache = Cache(max_size=10)
        cache.set("key1", "value1")
        self.assertEqual(cache.get("key1"), "value1")
        self.assertIsNone(cache.get("key2"))
    
    def test_performance_stats(self):
        """测试性能统计"""
        stats = PerformanceStats()
        stats.total_time = 1.5
        stats.tokens_processed = 100
        self.assertEqual(stats.total_time, 1.5)
        self.assertEqual(stats.tokens_processed, 100)


class TestModularLexer(unittest.TestCase):
    """测试模块化词法分析器"""
    
    def test_lexer_creation(self):
        """测试词法分析器创建"""
        lexer = create_lexer("jieba")
        self.assertIsNotNone(lexer)
        self.assertEqual(lexer.segmenter_type, "jieba")
    
    def test_tokenize_empty(self):
        """测试空文本分词"""
        lexer = create_lexer("jieba")
        tokens = lexer.tokenize("")
        self.assertGreater(len(tokens), 0)  # 至少有EOF
    
    def test_tokenize_simple(self):
        """测试简单文本分词"""
        lexer = create_lexer("jieba")
        tokens = lexer.tokenize("这是一个测试")
        self.assertGreater(len(tokens), 0)
    
    def test_get_config(self):
        """测试获取配置"""
        lexer = create_lexer("jieba", verbose=True)
        config = lexer.get_config()
        self.assertEqual(config['segmenter'], "jieba")
        self.assertTrue(config['verbose'])
    
    def test_performance_stats(self):
        """测试性能统计"""
        lexer = create_lexer("jieba")
        lexer.tokenize("这是一个测试")
        stats = lexer.get_performance_stats()
        self.assertIsInstance(stats, dict)
        self.assertIn('tokens_processed', stats)


class TestIntegration(unittest.TestCase):
    """集成测试"""
    
    def test_full_pipeline(self):
        """测试完整流程"""
        # 创建词法分析器
        lexer = create_lexer("jieba", verbose=False)
        
        # 分析源代码
        source_code = "如果 条件 成立 则 输出 'Hello World'"
        tokens = lexer.tokenize(source_code)
        
        # 验证结果
        self.assertGreater(len(tokens), 0)
        
        # 检查性能统计
        stats = lexer.get_performance_stats()
        self.assertGreater(stats['tokens_processed'], 0)
    
    def test_error_handling(self):
        """测试错误处理"""
        lexer = create_lexer("jieba")
        
        # 分析包含错误的代码
        source_code = "这是一个测试"
        tokens = lexer.tokenize(source_code)
        
        # 验证没有致命错误
        self.assertIsInstance(tokens, list)


def run_tests():
    """运行所有测试"""
    # 创建测试套件
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # 添加测试
    suite.addTests(loader.loadTestsFromTestCase(TestLexerToken))
    suite.addTests(loader.loadTestsFromTestCase(TestTokenizer))
    suite.addTests(loader.loadTestsFromTestCase(TestMatcher))
    suite.addTests(loader.loadTestsFromTestCase(TestErrorHandler))
    suite.addTests(loader.loadTestsFromTestCase(TestContextManager))
    suite.addTests(loader.loadTestsFromTestCase(TestPatternManager))
    suite.addTests(loader.loadTestsFromTestCase(TestPerformanceOptimizer))
    suite.addTests(loader.loadTestsFromTestCase(TestUtils))
    suite.addTests(loader.loadTestsFromTestCase(TestModularLexer))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # 返回测试结果
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)