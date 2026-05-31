from yanlv.lexer.lexer_modular import tokenize

code = '''定义变量问候为 "你好，世界！"
输出 问候'''

tokens = tokenize(code)

print("Tokens:")
for t in tokens:
    print(f"  {t.type}: '{t.value}'")
