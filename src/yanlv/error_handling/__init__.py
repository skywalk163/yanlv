"""
言律语言错误处理模块

提供增强的错误处理、恢复和建议功能
"""

from .enhanced_error_handler import (
    ErrorCategory,
    ErrorSeverity,
    RecoveryStrategy,
    ErrorContext,
    ErrorSuggestion,
    EnhancedError,
    ErrorRecoverySystem,
    ErrorSuggestionEngine,
    EnhancedErrorHandler,
    create_error_context,
    create_enhanced_error_handler
)


__all__ = [
    'ErrorCategory',
    'ErrorSeverity',
    'RecoveryStrategy',
    'ErrorContext',
    'ErrorSuggestion',
    'EnhancedError',
    'ErrorRecoverySystem',
    'ErrorSuggestionEngine',
    'EnhancedErrorHandler',
    'create_error_context',
    'create_enhanced_error_handler'
]


__version__ = '1.0.0'
__author__ = '言律语言项目组'
__description__ = '增强错误处理系统'