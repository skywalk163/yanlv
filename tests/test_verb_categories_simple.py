#!/usr/bin/env python3
"""
简单测试动词分类词典
"""

import sys
import os

# 直接导入模块
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, 'src')
sys.path.insert(0, src_dir)

# 手动导入
import importlib.util

spec = importlib.util.spec_from_file_location(
    "verb_categories", 
    os.path.join(src_dir, "yanlv", "lexer", "verb_categories.py")
)
verb_categories = importlib.util.module_from_spec(spec)
spec.loader.exec_module(verb_categories)

# 运行测试
verb_categories.test_verb_categories()