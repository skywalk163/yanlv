#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""测试解释器"""

import sys
import os
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from yanlv.lexer.lexer_modular import tokenize
from yanlv.advanced_interpreter import AdvancedInterpreter

code = """定 年龄 是 25
输出 年龄"""

tokens = tokenize(code)
print("词元：")
for i, token in enumerate(tokens):
    print(f"{i:3d} | {token.type.name:20s} | {token.value}")

print("\n执行：")
interpreter = AdvancedInterpreter()
output = interpreter.execute(tokens)
print("输出：", output)
print("变量：", interpreter.variables)
