#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""测试词法分析"""

import sys
import os
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from yanlv.lexer.lexer_modular import tokenize

code = """定 年龄 是 25
输出 年龄"""

tokens = tokenize(code)

print("词元列表：")
print("-" * 60)
for i, token in enumerate(tokens):
    print(f"{i:3d} | {token.type.name:20s} | {token.value}")
