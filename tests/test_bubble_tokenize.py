from yanlv.lexer.lexer_modular import tokenize

code = '''定冒泡排序是函列表：
  定长度是列表，长。'''

tokens = tokenize(code)

print("Tokens:")
for t in tokens:
    print(f"  {t.type}: '{t.value}'")
