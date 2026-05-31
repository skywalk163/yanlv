from yanlv.lexer.lexer_modular import tokenize

code = '输出"你好"'
tokens = tokenize(code)

print("Tokens:")
for t in tokens:
    print(f"  {t.type}: '{t.value}'")
