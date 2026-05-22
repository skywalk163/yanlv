#!/usr/bin/env python3
"""
言律语言错误处理系统 - 测试
"""

import sys
import os
import unittest

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

from yanlv.error_handling import (
    ErrorCategory, ErrorSeverity, RecoveryStrategy,
    ErrorContext, ErrorSuggestion, EnhancedError,
    ErrorRecoverySystem, ErrorSuggestionEngine, EnhancedErrorHandler,
    create_error_context, create_enhanced_error_handler
)


class TestErrorContext(unittest.TestCase):
    """测试错误上下文"""
    
    def test_error_context_creation(self):
        """测试错误上下文创建"""
        context = ErrorContext(
            source_code="这是一个测试",
            line_number=1,
            column_number=5,
            offset=10,
            surrounding_lines=["这是一个测试"],
            current_token="测试",
            expected_tokens=["标识符"],
            call_stack=[]
        )
        
        self.assertEqual(context.line_number, 1)
        self.assertEqual(context.column_number, 5)
        self.assertEqual(context.current_token, "测试")
    
    def test_error_context_to_dict(self):
        """测试错误上下文转换为字典"""
        context = ErrorContext(
            source_code="这是一个测试",
            line_number=1,
            column_number=5,
            offset=10,
            surrounding_lines=["这是一个测试"],
            current_token="测试",
            expected_tokens=["标识符"],
            call_stack=[]
        )
        
        context_dict = context.to_dict()
        self.assertEqual(context_dict['line_number'], 1)
        self.assertEqual(context_dict['current_token'], "测试")
    
    def test_get_context_snippet(self):
        """测试获取上下文片段"""
        source = "第一行\n第二行\n第三行\n第四行\n第五行"
        context = ErrorContext(
            source_code=source,
            line_number=3,
            column_number=1,
            offset=0,
            surrounding_lines=[],
            current_token=None,
            expected_tokens=[],
            call_stack=[]
        )
        
        snippet = context.get_context_snippet(context_size=1)
        self.assertIn("第三行", snippet)


class TestErrorSuggestion(unittest.TestCase):
    """测试错误建议"""
    
    def test_error_suggestion_creation(self):
        """测试错误建议创建"""
        suggestion = ErrorSuggestion(
            suggestion_id="sug-001",
            description="检查语法",
            fix_code="修复代码",
            confidence=0.8,
            category="syntax",
            priority=8
        )
        
        self.assertEqual(suggestion.suggestion_id, "sug-001")
        self.assertEqual(suggestion.confidence, 0.8)
    
    def test_error_suggestion_to_dict(self):
        """测试错误建议转换为字典"""
        suggestion = ErrorSuggestion(
            suggestion_id="sug-001",
            description="检查语法",
            fix_code="修复代码",
            confidence=0.8,
            category="syntax",
            priority=8
        )
        
        sug_dict = suggestion.to_dict()
        self.assertEqual(sug_dict['description'], "检查语法")
        self.assertEqual(sug_dict['confidence'], 0.8)


class TestEnhancedError(unittest.TestCase):
    """测试增强错误"""
    
    def test_enhanced_error_creation(self):
        """测试增强错误创建"""
        context = ErrorContext(
            source_code="测试",
            line_number=1,
            column_number=1,
            offset=0,
            surrounding_lines=[],
            current_token=None,
            expected_tokens=[],
            call_stack=[]
        )
        
        error = EnhancedError(
            error_id="err-001",
            error_code="LEX001",
            category=ErrorCategory.LEXICAL,
            severity=ErrorSeverity.ERROR,
            message="无效字符",
            context=context,
            suggestions=[],
            recovery_strategy=RecoveryStrategy.SKIP
        )
        
        self.assertEqual(error.error_code, "LEX001")
        self.assertEqual(error.category, ErrorCategory.LEXICAL)
        self.assertFalse(error.handled)
        self.assertFalse(error.recovered)
    
    def test_enhanced_error_format(self):
        """测试增强错误格式化"""
        context = ErrorContext(
            source_code="测试",
            line_number=1,
            column_number=1,
            offset=0,
            surrounding_lines=["测试"],
            current_token="测试",
            expected_tokens=[],
            call_stack=[]
        )
        
        suggestion = ErrorSuggestion(
            suggestion_id="sug-001",
            description="检查语法",
            fix_code="修复",
            confidence=0.8,
            category="syntax",
            priority=8
        )
        
        error = EnhancedError(
            error_id="err-001",
            error_code="LEX001",
            category=ErrorCategory.LEXICAL,
            severity=ErrorSeverity.ERROR,
            message="无效字符",
            context=context,
            suggestions=[suggestion],
            recovery_strategy=RecoveryStrategy.SKIP
        )
        
        formatted = error.format_error()
        self.assertIn("LEX001", formatted)
        self.assertIn("无效字符", formatted)


class TestErrorRecoverySystem(unittest.TestCase):
    """测试错误恢复系统"""
    
    def test_recovery_system_creation(self):
        """测试恢复系统创建"""
        system = ErrorRecoverySystem()
        self.assertIsNotNone(system)
        self.assertEqual(system.recovery_stats['total_errors'], 0)
    
    def test_recovery_skip(self):
        """测试跳过恢复"""
        system = ErrorRecoverySystem()
        
        context = ErrorContext(
            source_code="测试",
            line_number=1,
            column_number=1,
            offset=0,
            surrounding_lines=[],
            current_token=None,
            expected_tokens=[],
            call_stack=[]
        )
        
        error = EnhancedError(
            error_id="err-001",
            error_code="LEX001",
            category=ErrorCategory.LEXICAL,
            severity=ErrorSeverity.ERROR,
            message="测试错误",
            context=context,
            suggestions=[],
            recovery_strategy=RecoveryStrategy.SKIP
        )
        
        success = system.recover(error)
        self.assertTrue(success)
        self.assertTrue(error.recovered)
    
    def test_recovery_stats(self):
        """测试恢复统计"""
        system = ErrorRecoverySystem()
        
        context = ErrorContext(
            source_code="测试",
            line_number=1,
            column_number=1,
            offset=0,
            surrounding_lines=[],
            current_token=None,
            expected_tokens=[],
            call_stack=[]
        )
        
        error = EnhancedError(
            error_id="err-001",
            error_code="LEX001",
            category=ErrorCategory.LEXICAL,
            severity=ErrorSeverity.ERROR,
            message="测试错误",
            context=context,
            suggestions=[],
            recovery_strategy=RecoveryStrategy.SKIP
        )
        
        system.recover(error)
        stats = system.get_recovery_stats()
        
        self.assertEqual(stats['total_errors'], 1)
        self.assertEqual(stats['recovered_errors'], 1)


class TestErrorSuggestionEngine(unittest.TestCase):
    """测试错误建议引擎"""
    
    def test_suggestion_engine_creation(self):
        """测试建议引擎创建"""
        engine = ErrorSuggestionEngine()
        self.assertIsNotNone(engine)
    
    def test_generate_suggestions(self):
        """测试生成建议"""
        engine = ErrorSuggestionEngine()
        
        context = ErrorContext(
            source_code="测试",
            line_number=1,
            column_number=1,
            offset=0,
            surrounding_lines=[],
            current_token=None,
            expected_tokens=[],
            call_stack=[]
        )
        
        error = EnhancedError(
            error_id="err-001",
            error_code="LEX001",
            category=ErrorCategory.LEXICAL,
            severity=ErrorSeverity.ERROR,
            message="无效字符",
            context=context,
            suggestions=[],
            recovery_strategy=RecoveryStrategy.SKIP
        )
        
        suggestions = engine.generate_suggestions(error)
        self.assertGreater(len(suggestions), 0)


class TestEnhancedErrorHandler(unittest.TestCase):
    """测试增强错误处理器"""
    
    def test_handler_creation(self):
        """测试处理器创建"""
        handler = EnhancedErrorHandler()
        self.assertIsNotNone(handler)
        self.assertEqual(len(handler.errors), 0)
    
    def test_create_error(self):
        """测试创建错误"""
        handler = EnhancedErrorHandler()
        
        context = create_error_context(
            source_code="测试",
            line_number=1,
            column_number=1,
            current_token="测试"
        )
        
        error = handler.create_error(
            error_code="LEX001",
            category=ErrorCategory.LEXICAL,
            severity=ErrorSeverity.ERROR,
            message="无效字符",
            context=context
        )
        
        self.assertEqual(error.error_code, "LEX001")
        self.assertGreater(len(error.suggestions), 0)
    
    def test_handle_error(self):
        """测试处理错误"""
        handler = EnhancedErrorHandler()
        
        context = create_error_context(
            source_code="测试",
            line_number=1,
            column_number=1
        )
        
        error = handler.create_error(
            error_code="LEX001",
            category=ErrorCategory.LEXICAL,
            severity=ErrorSeverity.ERROR,
            message="无效字符",
            context=context
        )
        
        success = handler.handle_error(error)
        self.assertTrue(success)
        self.assertEqual(len(handler.errors), 1)
    
    def test_error_statistics(self):
        """测试错误统计"""
        handler = EnhancedErrorHandler()
        
        context = create_error_context(
            source_code="测试",
            line_number=1,
            column_number=1
        )
        
        error = handler.create_error(
            error_code="LEX001",
            category=ErrorCategory.LEXICAL,
            severity=ErrorSeverity.ERROR,
            message="无效字符",
            context=context
        )
        
        handler.handle_error(error)
        stats = handler.get_statistics()
        
        self.assertEqual(stats['total_errors'], 1)
        self.assertIn('lexical', stats['errors_by_category'])
    
    def test_max_errors_limit(self):
        """测试最大错误数限制"""
        handler = EnhancedErrorHandler(max_errors=2)
        
        context = create_error_context(
            source_code="测试",
            line_number=1,
            column_number=1
        )
        
        # 添加3个错误
        for i in range(3):
            error = handler.create_error(
                error_code=f"LEX00{i}",
                category=ErrorCategory.LEXICAL,
                severity=ErrorSeverity.ERROR,
                message=f"错误{i}",
                context=context
            )
            handler.handle_error(error)
        
        # 只应该有2个错误
        self.assertEqual(len(handler.errors), 2)


def run_tests():
    """运行所有测试"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # 添加所有测试
    suite.addTests(loader.loadTestsFromTestCase(TestErrorContext))
    suite.addTests(loader.loadTestsFromTestCase(TestErrorSuggestion))
    suite.addTests(loader.loadTestsFromTestCase(TestEnhancedError))
    suite.addTests(loader.loadTestsFromTestCase(TestErrorRecoverySystem))
    suite.addTests(loader.loadTestsFromTestCase(TestErrorSuggestionEngine))
    suite.addTests(loader.loadTestsFromTestCase(TestEnhancedErrorHandler))
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)