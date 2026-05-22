#!/usr/bin/env python3
"""
测试语义上下文跟踪器
"""

import sys
import os

# 添加src目录到Python路径
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, 'src')
sys.path.insert(0, src_dir)

# 直接导入模块
import importlib.util

spec = importlib.util.spec_from_file_location(
    "context_tracker", 
    os.path.join(src_dir, "yanlv", "semantic", "context_tracker.py")
)
context_tracker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(context_tracker)

# 运行测试
context_tracker.test_semantic_context_tracker()