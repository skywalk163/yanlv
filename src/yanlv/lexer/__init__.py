"""
言律语言词法分析器模块

提供模块化的词法分析功能
"""

# 导出主要类和函数
from .lexer_token import Token, TokenType
from .tokenizer import YanLuTokenizer, JiebaTokenizer, ThulacTokenizer, YanLuNoSpaceTokenizer
from .matcher import TokenMatcher, create_token_matcher
from .error_handler import ErrorHandler, create_error_handler
from .context_manager import ContextManager, create_context_manager
from .pattern_manager import PatternManager, create_pattern_manager
from .performance_optimizer import PerformanceOptimizer, OptimizationConfig, OptimizationLevel
from .lexer_modular import ModularYanLuLexer, create_lexer, tokenize, tokenize_with_stats

# 为了向后兼容，提供Lexer别名
Lexer = ModularYanLuLexer


__all__ = [
    # 词元
    'Token',
    'TokenType',
    
    # 分词器
    'YanLuTokenizer',
    'JiebaTokenizer',
    'ThulacTokenizer',
    
    # 匹配器
    'TokenMatcher',
    'create_token_matcher',
    
    # 错误处理
    'ErrorHandler',
    'create_error_handler',
    
    # 上下文管理
    'ContextManager',
    'create_context_manager',
    
    # 模式管理
    'PatternManager',
    'create_pattern_manager',
    
    # 性能优化
    'PerformanceOptimizer',
    'OptimizationConfig',
    'OptimizationLevel',
    
    # 主lexer类
    'Lexer',  # 向后兼容别名
    'ModularYanLuLexer',
    'create_lexer',
    'tokenize',
    'tokenize_with_stats',
]


__version__ = '2.0.0'
__author__ = '言律语言项目组'
__description__ = '模块化词法分析器'