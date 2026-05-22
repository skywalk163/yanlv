#!/usr/bin/env python3
"""
言律语言用户反馈系统 - 测试
"""

import sys
import os
import unittest

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 使用绝对导入
import feedback_model
import feedback_collector
import pattern_analyzer

from feedback_model import (
    FeedbackType, FeedbackSeverity, FeedbackStatus,
    UserFeedback, AmbiguityFeedback, AmbiguityPattern, LearningRule,
    FeedbackDataModel
)
from feedback_collector import FeedbackCollector, FeedbackEnabledCompiler
from pattern_analyzer import PatternAnalyzer, LearningEngine, DynamicRuleAdjuster


class TestFeedbackModel(unittest.TestCase):
    """测试反馈数据模型"""
    
    def test_ambiguity_feedback_creation(self):
        """测试歧义反馈创建"""
        feedback = AmbiguityFeedback(
            source_text="这是一个测试",
            ambiguous_segment="测试",
            system_interpretation="名词",
            user_correction="动词",
            context=["这是", "一个"],
            confidence=0.8
        )
        
        self.assertEqual(feedback.ambiguous_segment, "测试")
        self.assertEqual(feedback.system_interpretation, "名词")
        self.assertEqual(feedback.user_correction, "动词")
        self.assertEqual(feedback.confidence, 0.8)
    
    def test_user_feedback_creation(self):
        """测试用户反馈创建"""
        feedback = UserFeedback(
            feedback_id="test-001",
            feedback_type=FeedbackType.AMBIGUITY_RESOLUTION,
            severity=FeedbackSeverity.MEDIUM,
            status=FeedbackStatus.PENDING,
            content="测试反馈"
        )
        
        self.assertEqual(feedback.feedback_id, "test-001")
        self.assertEqual(feedback.feedback_type, FeedbackType.AMBIGUITY_RESOLUTION)
        self.assertEqual(feedback.status, FeedbackStatus.PENDING)
    
    def test_ambiguity_pattern(self):
        """测试歧义模式"""
        pattern = AmbiguityPattern(
            pattern_id="pattern-001",
            pattern_text="测试",
            frequency=10,
            common_interpretations=["名词", "动词"],
            user_preferences={"动词": 7, "名词": 3},
            confidence=0.7
        )
        
        # 测试更新偏好
        pattern.update_preference("动词")
        self.assertEqual(pattern.frequency, 11)
        self.assertEqual(pattern.user_preferences["动词"], 8)
        
        # 测试获取偏好解释
        preferred = pattern.get_preferred_interpretation()
        self.assertEqual(preferred, "动词")
    
    def test_learning_rule(self):
        """测试学习规则"""
        rule = LearningRule(
            rule_id="rule-001",
            condition="测试",
            action="动词",
            priority=50,
            confidence=0.8,
            source="user_feedback"
        )
        
        # 测试更新使用统计
        rule.update_usage(success=True)
        self.assertEqual(rule.usage_count, 1)
        self.assertEqual(rule.success_count, 1)
        
        # 测试成功率
        success_rate = rule.get_success_rate()
        self.assertEqual(success_rate, 1.0)
    
    def test_feedback_data_model(self):
        """测试反馈数据模型"""
        model = FeedbackDataModel()
        
        # 添加反馈
        feedback = UserFeedback(
            feedback_id="test-001",
            feedback_type=FeedbackType.SUGGESTION,
            severity=FeedbackSeverity.LOW,
            status=FeedbackStatus.PENDING,
            content="测试建议"
        )
        
        feedback_id = model.add_feedback(feedback)
        self.assertEqual(feedback_id, "test-001")
        self.assertEqual(model.stats['total_feedbacks'], 1)
        
        # 获取反馈
        retrieved = model.get_feedback("test-001")
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.content, "测试建议")


class TestFeedbackCollector(unittest.TestCase):
    """测试反馈收集器"""
    
    def test_collector_creation(self):
        """测试收集器创建"""
        collector = FeedbackCollector()
        self.assertIsNotNone(collector)
        self.assertIsNotNone(collector.data_model)
    
    def test_collect_ambiguity_feedback(self):
        """测试收集歧义反馈"""
        collector = FeedbackCollector()
        
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
    
    def test_collect_error_correction(self):
        """测试收集错误纠正"""
        collector = FeedbackCollector()
        
        feedback_id = collector.collect_error_correction(
            error_type="语法错误",
            error_message="缺少分号",
            correction="添加分号"
        )
        
        self.assertIsNotNone(feedback_id)
        self.assertEqual(collector.stats['feedbacks_collected'], 1)
    
    def test_collect_suggestion(self):
        """测试收集建议"""
        collector = FeedbackCollector()
        
        feedback_id = collector.collect_suggestion(
            suggestion="建议增加自动补全功能",
            category="功能建议",
            priority=2
        )
        
        self.assertIsNotNone(feedback_id)
    
    def test_collect_rating(self):
        """测试收集评分"""
        collector = FeedbackCollector()
        
        feedback_id = collector.collect_rating(
            item_id="feature-001",
            rating=4,
            comment="很好用"
        )
        
        self.assertIsNotNone(feedback_id)
    
    def test_process_feedback(self):
        """测试处理反馈"""
        collector = FeedbackCollector()
        
        # 收集反馈
        feedback_id = collector.collect_ambiguity_feedback(
            source_text="这是一个测试",
            ambiguous_segment="测试",
            system_interpretation="名词",
            user_correction="动词",
            context=["这是", "一个"],
            confidence=0.8
        )
        
        # 获取待处理反馈
        pending = collector.get_pending_feedbacks()
        self.assertGreater(len(pending), 0)
        
        # 处理反馈
        success = collector.process_feedback(pending[0].feedback_id)
        self.assertTrue(success)


class TestPatternAnalyzer(unittest.TestCase):
    """测试模式分析器"""
    
    def test_analyzer_creation(self):
        """测试分析器创建"""
        model = FeedbackDataModel()
        analyzer = PatternAnalyzer(model)
        self.assertIsNotNone(analyzer)
    
    def test_analyze_patterns(self):
        """测试分析模式"""
        model = FeedbackDataModel()
        
        # 添加一些模式
        for i in range(5):
            pattern = AmbiguityPattern(
                pattern_id=f"pattern-{i}",
                pattern_text=f"测试{i}",
                frequency=i * 2,
                common_interpretations=["名词", "动词"],
                user_preferences={"动词": i},
                confidence=0.5 + i * 0.1
            )
            model.add_pattern(pattern)
        
        analyzer = PatternAnalyzer(model)
        results = analyzer.analyze_patterns()
        
        self.assertEqual(results['total_patterns'], 5)
    
    def test_find_similar_patterns(self):
        """测试查找相似模式"""
        model = FeedbackDataModel()
        
        # 添加模式
        pattern = AmbiguityPattern(
            pattern_id="pattern-001",
            pattern_text="测试文本",
            frequency=10,
            common_interpretations=["名词"],
            user_preferences={"名词": 10},
            confidence=0.8
        )
        model.add_pattern(pattern)
        
        analyzer = PatternAnalyzer(model)
        similar = analyzer.find_similar_patterns("测试文本")
        
        self.assertGreater(len(similar), 0)


class TestLearningEngine(unittest.TestCase):
    """测试学习引擎"""
    
    def test_engine_creation(self):
        """测试引擎创建"""
        model = FeedbackDataModel()
        engine = LearningEngine(model)
        self.assertIsNotNone(engine)
    
    def test_learn_from_feedbacks(self):
        """测试从反馈学习"""
        model = FeedbackDataModel()
        
        # 添加高频模式
        pattern = AmbiguityPattern(
            pattern_id="pattern-001",
            pattern_text="测试",
            frequency=10,
            common_interpretations=["名词", "动词"],
            user_preferences={"动词": 8, "名词": 2},
            confidence=0.6
        )
        model.add_pattern(pattern)
        
        engine = LearningEngine(model)
        results = engine.learn_from_feedbacks()
        
        self.assertEqual(results['patterns_analyzed'], 1)
        self.assertGreater(results['rules_created'], 0)
    
    def test_apply_learned_rules(self):
        """测试应用学习规则"""
        model = FeedbackDataModel()
        
        # 添加规则
        rule = LearningRule(
            rule_id="rule-001",
            condition="测试",
            action="动词",
            priority=50,
            confidence=0.8,
            source="user_feedback"
        )
        model.add_rule(rule)
        
        engine = LearningEngine(model)
        result = engine.apply_learned_rules("这是一个测试")
        
        self.assertEqual(result, "动词")


class TestDynamicRuleAdjuster(unittest.TestCase):
    """测试动态规则调整器"""
    
    def test_adjuster_creation(self):
        """测试调整器创建"""
        model = FeedbackDataModel()
        adjuster = DynamicRuleAdjuster(model)
        self.assertIsNotNone(adjuster)
    
    def test_adjust_rules(self):
        """测试调整规则"""
        model = FeedbackDataModel()
        
        # 添加模式
        pattern = AmbiguityPattern(
            pattern_id="pattern-001",
            pattern_text="测试",
            frequency=10,
            common_interpretations=["动词"],
            user_preferences={"动词": 10},
            confidence=0.8
        )
        model.add_pattern(pattern)
        
        adjuster = DynamicRuleAdjuster(model)
        results = adjuster.adjust_rules()
        
        self.assertIn('learning_results', results)


class TestFeedbackEnabledCompiler(unittest.TestCase):
    """测试支持反馈的编译器"""
    
    def test_compiler_creation(self):
        """测试编译器创建"""
        compiler = FeedbackEnabledCompiler()
        self.assertIsNotNone(compiler)
        self.assertTrue(compiler.auto_collect)
    
    def test_report_ambiguity(self):
        """测试报告歧义"""
        compiler = FeedbackEnabledCompiler()
        
        compiler.report_ambiguity(
            source_text="这是一个测试",
            ambiguous_segment="测试",
            system_interpretation="名词",
            user_correction="动词",
            context=["这是", "一个"]
        )
        
        summary = compiler.get_feedback_summary()
        self.assertGreater(summary['ambiguity_feedbacks'], 0)
    
    def test_enable_disable_feedback(self):
        """测试启用/禁用反馈"""
        compiler = FeedbackEnabledCompiler()
        
        compiler.disable_feedback()
        self.assertFalse(compiler.auto_collect)
        
        compiler.enable_feedback()
        self.assertTrue(compiler.auto_collect)


def run_tests():
    """运行所有测试"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # 添加测试
    suite.addTests(loader.loadTestsFromTestCase(TestFeedbackModel))
    suite.addTests(loader.loadTestsFromTestCase(TestFeedbackCollector))
    suite.addTests(loader.loadTestsFromTestCase(TestPatternAnalyzer))
    suite.addTests(loader.loadTestsFromTestCase(TestLearningEngine))
    suite.addTests(loader.loadTestsFromTestCase(TestDynamicRuleAdjuster))
    suite.addTests(loader.loadTestsFromTestCase(TestFeedbackEnabledCompiler))
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)