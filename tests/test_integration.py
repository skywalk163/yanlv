#!/usr/bin/env python3
"""
言律语言集成测试

测试所有模块的集成和协同工作
"""

import sys
import os
import unittest
from typing import List

# 添加src目录到Python路径
src_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src')
sys.path.insert(0, src_path)

# 导入所有模块
from yanlv.lexer import create_lexer, tokenize, TokenType
from yanlv.semantic import AmbiguityResolver, SemanticContextTracker, TypeInferenceSystem
from yanlv.feedback import FeedbackCollector, FeedbackEnabledCompiler, LearningEngine


class TestLexerIntegration(unittest.TestCase):
    """测试词法分析器集成"""
    
    def test_lexer_basic_functionality(self):
        """测试词法分析器基本功能"""
        lexer = create_lexer("jieba")
        
        # 测试简单代码
        source = "如果 条件 成立 则 输出 'Hello'"
        tokens = lexer.tokenize(source)
        
        self.assertGreater(len(tokens), 0)
        self.assertEqual(tokens[-1].type, TokenType.EOF)
    
    def test_lexer_with_different_segmenters(self):
        """测试不同分词器"""
        # jieba分词器
        lexer_jieba = create_lexer("jieba")
        tokens_jieba = lexer_jieba.tokenize("这是一个测试")
        
        self.assertGreater(len(tokens_jieba), 0)
    
    def test_lexer_performance_stats(self):
        """测试性能统计"""
        lexer = create_lexer("jieba")
        tokens = lexer.tokenize("这是一个测试")
        
        stats = lexer.get_performance_stats()
        self.assertIn('tokens_processed', stats)
        self.assertGreater(stats['tokens_processed'], 0)
    
    def test_lexer_error_handling(self):
        """测试错误处理"""
        lexer = create_lexer("jieba")
        tokens = lexer.tokenize("")
        
        # 空输入应该只返回EOF
        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0].type, TokenType.EOF)


class TestSemanticIntegration(unittest.TestCase):
    """测试语义分析集成"""
    
    def test_semantic_context_tracker(self):
        """测试语义上下文跟踪"""
        tracker = SemanticContextTracker()
        
        # 测试上下文管理
        tracker.add_context("function")
        # 验证上下文已添加
        self.assertIsNotNone(tracker.get_recent_context())
    
    def test_type_inference(self):
        """测试类型推断"""
        tracker = SemanticContextTracker()
        inference = TypeInferenceSystem(tracker)
        
        # 测试基本类型推断
        from yanlv.lexer.utils import Position
        pos = Position(line=1, column=1, offset=0)
        type1 = inference.infer_type("123", pos)
        
        self.assertIsNotNone(type1)
    
    def test_ambiguity_resolver(self):
        """测试歧义消解器"""
        tracker = SemanticContextTracker()
        inference = TypeInferenceSystem(tracker)
        resolver = AmbiguityResolver(tracker, inference)
        
        # 验证消解器已创建
        self.assertIsNotNone(resolver)


class TestFeedbackIntegration(unittest.TestCase):
    """测试反馈系统集成"""
    
    def test_feedback_collector_basic(self):
        """测试反馈收集器基本功能"""
        collector = FeedbackCollector()
        
        # 收集歧义反馈
        feedback_id = collector.collect_ambiguity_feedback(
            source_text="这是一个测试",
            ambiguous_segment="测试",
            system_interpretation="名词",
            user_correction="动词",
            context=["这是", "一个"],
            confidence=0.8
        )
        
        self.assertIsNotNone(feedback_id)
        self.assertEqual(collector.stats['ambiguity_feedbacks'], 1)
    
    def test_feedback_enabled_compiler(self):
        """测试支持反馈的编译器"""
        compiler = FeedbackEnabledCompiler()
        
        # 报告歧义
        compiler.report_ambiguity(
            source_text="这是一个测试",
            ambiguous_segment="测试",
            system_interpretation="名词",
            user_correction="动词",
            context=["这是", "一个"]
        )
        
        summary = compiler.get_feedback_summary()
        self.assertGreater(summary['ambiguity_feedbacks'], 0)
    
    def test_learning_engine(self):
        """测试学习引擎"""
        from yanlv.feedback import FeedbackDataModel, AmbiguityPattern
        
        model = FeedbackDataModel()
        
        # 添加模式
        pattern = AmbiguityPattern(
            pattern_id="test-001",
            pattern_text="测试",
            frequency=10,
            common_interpretations=["名词", "动词"],
            user_preferences={"动词": 8, "名词": 2},
            confidence=0.7
        )
        model.add_pattern(pattern)
        
        # 学习
        engine = LearningEngine(model)
        results = engine.learn_from_feedbacks()
        
        self.assertEqual(results['patterns_analyzed'], 1)


class TestFullPipeline(unittest.TestCase):
    """测试完整流程"""
    
    def test_complete_analysis_pipeline(self):
        """测试完整分析流程"""
        # 1. 创建词法分析器
        lexer = create_lexer("jieba")
        
        # 2. 创建语义分析器
        tracker = SemanticContextTracker()
        inference = TypeInferenceSystem(tracker)
        resolver = AmbiguityResolver(tracker, inference)
        
        # 3. 创建反馈系统
        collector = FeedbackCollector()
        
        # 4. 分析代码
        source = "如果 条件 成立 则 输出 'Hello World'"
        tokens = lexer.tokenize(source)
        
        # 5. 验证结果
        self.assertGreater(len(tokens), 0)
        
        # 6. 获取性能统计
        stats = lexer.get_performance_stats()
        self.assertGreater(stats['tokens_processed'], 0)
    
    def test_feedback_learning_pipeline(self):
        """测试反馈学习流程"""
        # 1. 创建反馈收集器
        collector = FeedbackCollector()
        
        # 2. 收集多个不同的反馈（不同的segment以避免去重）
        for i in range(5):
            collector.collect_ambiguity_feedback(
                source_text=f"测试{i}",
                ambiguous_segment=f"测试{i}",  # 不同的segment
                system_interpretation="名词",
                user_correction="动词",
                context=[],
                confidence=0.8
            )
        
        # 3. 验证统计
        stats = collector.get_statistics()
        self.assertEqual(stats['ambiguity_feedbacks'], 5)
    
    def test_error_recovery_pipeline(self):
        """测试错误恢复流程"""
        lexer = create_lexer("jieba")
        
        # 测试各种输入
        test_cases = [
            "",  # 空输入
            "   ",  # 空白输入
            "如果",  # 单个关键词
            "如果 条件",  # 部分语句
            "如果 条件 成立 则 输出 'Hello'",  # 完整语句
        ]
        
        for source in test_cases:
            tokens = lexer.tokenize(source)
            self.assertIsInstance(tokens, list)
            self.assertGreater(len(tokens), 0)


class TestPerformanceIntegration(unittest.TestCase):
    """测试性能集成"""
    
    def test_large_input_performance(self):
        """测试大输入性能"""
        lexer = create_lexer("jieba")
        
        # 生成大输入
        source = "\n".join([
            "如果 条件 成立 则 输出 '结果'"
            for _ in range(100)
        ])
        
        # 分析
        tokens = lexer.tokenize(source)
        
        # 验证
        self.assertGreater(len(tokens), 100)
        
        # 检查性能
        stats = lexer.get_performance_stats()
        self.assertGreater(stats['tokens_processed'], 100)
    
    def test_repeated_analysis_performance(self):
        """测试重复分析性能"""
        lexer = create_lexer("jieba")
        source = "这是一个测试"
        
        # 重复分析
        for _ in range(10):
            tokens = lexer.tokenize(source)
            self.assertGreater(len(tokens), 0)
        
        # 检查统计
        stats = lexer.get_performance_stats()
        self.assertGreater(stats['tokens_processed'], 0)


class TestModuleInteraction(unittest.TestCase):
    """测试模块交互"""
    
    def test_lexer_to_semantic(self):
        """测试词法分析器到语义分析器"""
        lexer = create_lexer("jieba")
        tracker = SemanticContextTracker()
        
        # 词法分析
        tokens = lexer.tokenize("定义 函数 参数")
        
        # 验证词法分析结果
        self.assertGreater(len(tokens), 0)
        
        # 验证语义跟踪器可用
        self.assertIsNotNone(tracker)
    
    def test_semantic_to_feedback(self):
        """测试语义分析器到反馈系统"""
        tracker = SemanticContextTracker()
        collector = FeedbackCollector()
        
        # 语义分析
        tracker.add_context("function")
        
        # 发现歧义，收集反馈
        collector.collect_ambiguity_feedback(
            source_text="测试",
            ambiguous_segment="测试",
            system_interpretation="名词",
            user_correction="动词",
            context=[],
            confidence=0.7
        )
        
        # 验证
        self.assertEqual(collector.stats['ambiguity_feedbacks'], 1)
    
    def test_feedback_to_lexer(self):
        """测试反馈系统到词法分析器"""
        from yanlv.feedback import FeedbackDataModel, LearningEngine
        
        # 创建反馈系统
        model = FeedbackDataModel()
        engine = LearningEngine(model)
        
        # 学习规则
        from yanlv.feedback import AmbiguityPattern
        pattern = AmbiguityPattern(
            pattern_id="test-001",
            pattern_text="测试",
            frequency=10,
            common_interpretations=["动词"],
            user_preferences={"动词": 10},
            confidence=0.9
        )
        model.add_pattern(pattern)
        
        engine.learn_from_feedbacks()
        
        # 应用到词法分析
        lexer = create_lexer("jieba")
        tokens = lexer.tokenize("这是一个测试")
        
        # 验证
        self.assertGreater(len(tokens), 0)


def run_integration_tests():
    """运行集成测试"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # 添加所有测试
    suite.addTests(loader.loadTestsFromTestCase(TestLexerIntegration))
    suite.addTests(loader.loadTestsFromTestCase(TestSemanticIntegration))
    suite.addTests(loader.loadTestsFromTestCase(TestFeedbackIntegration))
    suite.addTests(loader.loadTestsFromTestCase(TestFullPipeline))
    suite.addTests(loader.loadTestsFromTestCase(TestPerformanceIntegration))
    suite.addTests(loader.loadTestsFromTestCase(TestModuleInteraction))
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_integration_tests()
    sys.exit(0 if success else 1)