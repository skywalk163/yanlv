#!/usr/bin/env python3
"""
测试类型推断系统
"""

import sys
import os

# 添加src目录到Python路径
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, 'src')
sys.path.insert(0, src_dir)

# 直接导入模块
import importlib.util

# 导入context_tracker
context_tracker_path = os.path.join(src_dir, "yanlv", "semantic", "context_tracker.py")
spec1 = importlib.util.spec_from_file_location("context_tracker", context_tracker_path)
context_tracker_module = importlib.util.module_from_spec(spec1)
sys.modules["context_tracker"] = context_tracker_module
spec1.loader.exec_module(context_tracker_module)

# 导入type_inference
type_inference_path = os.path.join(src_dir, "yanlv", "semantic", "type_inference.py")
spec2 = importlib.util.spec_from_file_location("type_inference", type_inference_path)
type_inference_module = importlib.util.module_from_spec(spec2)
sys.modules["type_inference"] = type_inference_module
spec2.loader.exec_module(type_inference_module)

# 运行测试
if __name__ == "__main__":
    type_inference_module.test_type_inference_system()