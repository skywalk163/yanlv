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

# 导入CLI模块（主要入口点）
from . import cli

# 导入编译器
from .compiler import YanLuCompiler

# 导入标准库扩展
from . import stdlib

__all__ = [
    # 版本信息
    '__version__',
    '__author__',
    '__email__',
    
    # 模块
    'cli',
    'stdlib',
    
    # 编译器
    'YanLuCompiler',
]
