"""测试比较运算符"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from yanlv.lexer import create_lexer
from yanlv.interpreter import create_interpreter

lexer = create_lexer("yanlv_nospace")

code = '''定义变量z为5
定义变量y为10
如果z小于等于y则
    输出"z小于等于y"
    结束'''

    print("代码:")
    print(code)
    print("\n词元分析:")
    tokens = lexer.tokenize(code)
    for i, token in enumerate(tokens):
    print(f"{i:3d}: {token.type.name:20s} = {token.value}")

    print("\n执行结果:")
    interpreter = create_interpreter()
    output = interpreter.execute(tokens)
    for line in output:
    print(line)
