"""
言律语言用户反馈系统

提供完整的用户反馈收集、分析和学习功能
"""

from .feedback_model import (
    FeedbackType,
    FeedbackSeverity,
    FeedbackStatus,
    AmbiguityFeedback,
    UserFeedback,
    AmbiguityPattern,
    LearningRule,
    FeedbackDataModel
)

from .feedback_collector import (
    FeedbackCollector,
    FeedbackEnabledCompiler,
    create_feedback_collector,
    create_feedback_enabled_compiler
)

from .pattern_analyzer import (
    PatternAnalyzer,
    LearningEngine,
    DynamicRuleAdjuster,
    create_pattern_analyzer,
    create_learning_engine,
    create_dynamic_rule_adjuster
)


__all__ = [
    # 反馈模型
    'FeedbackType',
    'FeedbackSeverity',
    'FeedbackStatus',
    'AmbiguityFeedback',
    'UserFeedback',
    'AmbiguityPattern',
    'LearningRule',
    'FeedbackDataModel',
    
    # 反馈收集
    'FeedbackCollector',
    'FeedbackEnabledCompiler',
    'create_feedback_collector',
    'create_feedback_enabled_compiler',
    
    # 模式分析
    'PatternAnalyzer',
    'LearningEngine',
    'DynamicRuleAdjuster',
    'create_pattern_analyzer',
    'create_learning_engine',
    'create_dynamic_rule_adjuster'
]


__version__ = '1.0.0'
__author__ = '言律语言项目组'
__description__ = '用户反馈系统'