#!/usr/bin/env python3
"""
测试动词分类词典
"""

import sys
import os

# 添加src目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# 直接导入模块
sys.path.insert(0, os.path.dirname(__file__))

from src.yanlv.lexer.verb_categories import test_verb_categories

if __name__ == "__main__":
    test_verb_categories()