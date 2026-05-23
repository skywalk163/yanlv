"""
言律(Yán Lǜ) - 中文原生编程语言

基于中文深层认知特性的编程语言，融合了：
1. 因果链语法 - 直接映射"事件-响应"关系
2. 语境省略语法 - 利用上下文省略重复元素
3. 状态流语法 - 自然语言描述状态变化
4. 意合式函数调用 - 通过语义关联传递参数
5. 多轨制设计 - 中文+数学+多语言融合
6. 元数驱动解析 - 实现无空格分词
7. 百家姓变量命名
"""

__version__ = "2.0.0"
__author__ = "言律语言项目组"
__email__ = "yanlv@example.com"

# 导入主要模块
from . import lexer
from . import semantic
from . import feedback
from . import error_handling

# 导出常用类和函数
from .lexer import (
    create_lexer,
    tokenize,
    Token,
    TokenType,
    YanLuTokenizer,
)

from .semantic import (
    SemanticContextTracker,
    TypeInferenceSystem,
    AmbiguityResolver,
)

from .feedback import (
    FeedbackCollector,
    FeedbackEnabledCompiler,
    LearningEngine,
)

from .error_handling import (
    EnhancedErrorHandler,
    ErrorCategory,
    ErrorSeverity,
    create_error_context,
)


__all__ = [
    # 版本信息
    '__version__',
    '__author__',
    '__email__',
    
    # 模块
    'lexer',
    'semantic',
    'feedback',
    'error_handling',
    
    # 词法分析
    'create_lexer',
    'tokenize',
    'Token',
    'TokenType',
    'YanLuTokenizer',
    
    # 语义分析
    'SemanticContextTracker',
    'TypeInferenceSystem',
    'AmbiguityResolver',
    
    # 反馈系统
    'FeedbackCollector',
    'FeedbackEnabledCompiler',
    'LearningEngine',
    
    # 错误处理
    'EnhancedErrorHandler',
    'ErrorCategory',
    'ErrorSeverity',
    'create_error_context',
]