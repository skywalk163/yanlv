#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""测试表达式"""

import sys
import os
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from yanlv.lexer.lexer_modular import tokenize
from yanlv.advanced_interpreter import AdvancedInterpreter

code = """定 a 是 10
定 b 是 3
输出 a 加 b"""

tokens = tokenize(code)
print("词元：")
for i, token in enumerate(tokens):
    print(f"{i:3d} | {token.type.name:20s} | {repr(token.value)}")

print("\n执行：")
interpreter = AdvancedInterpreter()
output = interpreter.execute(tokens)
print("输出：", output)
print("变量：", interpreter.variables)
