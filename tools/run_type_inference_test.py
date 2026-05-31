#!/usr/bin/env python3
"""
直接运行类型推断系统测试
"""

import sys
import os

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 直接执行type_inference.py中的测试函数
with open(os.path.join("src", "yanlv", "semantic", "type_inference.py"), "r", encoding="utf-8") as f:
    code = f.read()
    
# 修改导入语句
code = code.replace("from .context_tracker import", "from src.yanlv.semantic.context_tracker import")

# 执行代码
exec(code)

# 运行测试函数
if __name__ == "__main__":
    test_type_inference_system()