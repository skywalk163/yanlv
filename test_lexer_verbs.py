#!/usr/bin/env python3
"""
测试词法分析器动词识别
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from yanlv.lexer import YanLuLexer
from yanlv.lexer.token import TokenType

# 创建词法分析器
lexer = YanLuLexer()

# 测试代码
source_code = """
温度变为30度。
风扇开启。
计算总和。
移动物体。
创建文件。
删除缓存。
查询用户。
修改设置。
发送消息。
比较大小。
转换格式。
"""

print("词法分析器动词识别测试")
print("=" * 60)

# 进行词法分析
tokens = lexer.tokenize(source_code)

# 打印所有词法单元
print("所有词法单元:")
print("-" * 80)
print(f"{'行':<4} {'列':<4} {'类型':<20} {'值':<20} {'词素':<20}")
print("-" * 80)

for token in tokens:
    if token.type == TokenType.EOF:
        continue
        
    value_str = str(token.value)
    if len(value_str) > 18:
        value_str = value_str[:15] + "..."
    
    lexeme_str = token.lexeme
    if len(lexeme_str) > 18:
        lexeme_str = lexeme_str[:15] + "..."
    
    print(f"{token.line:<4} {token.column:<4} {token.type.value:<20} {value_str:<20} {lexeme_str:<20}")

print("-" * 80)

# 检查动词词法单元
verb_tokens = [t for t in tokens if t.type.name.startswith('VERB_')]
print(f"\n动词词法单元数量: {len(verb_tokens)}")

if verb_tokens:
    print("\n识别的动词:")
    for token in verb_tokens:
        print(f"  - {token.lexeme} (类型: {token.type.value})")
else:
    print("\n未识别到动词词法单元")
    
    # 调试：检查所有词法单元类型
    print("\n所有词法单元类型:")
    type_counts = {}
    for token in tokens:
        if token.type != TokenType.EOF:
            type_name = token.type.value
            type_counts[type_name] = type_counts.get(type_name, 0) + 1
    
    for type_name, count in sorted(type_counts.items()):
        print(f"  {type_name}: {count}")

# 测试单个动词识别
print("\n" + "=" * 60)
print("单个动词识别测试:")

test_verbs = ["变为", "开启", "计算", "移动", "创建", "删除", "查询", "修改", "发送", "比较", "转换"]

for verb in test_verbs:
    test_code = f"{verb}测试。"
    tokens = lexer.tokenize(test_code)
    
    verb_found = False
    for token in tokens:
        if token.type.name.startswith('VERB_') and token.lexeme == verb:
            verb_found = True
            print(f"  {verb}: 识别为 {token.type.value}")
            break
    
    if not verb_found:
        print(f"  {verb}: 未识别为动词")
        # 打印所有词法单元用于调试
        for token in tokens:
            if token.type != TokenType.EOF:
                print(f"    - {token.lexeme}: {token.type.value}")

# 测试动词在句子中的识别
print("\n" + "=" * 60)
print("动词在句子中的识别测试:")

test_sentences = [
    "温度变为30度。",
    "风扇开启。",
    "计算总和。",
    "移动物体。",
    "创建文件。",
]

for sentence in test_sentences:
    print(f"\n句子: {sentence}")
    tokens = lexer.tokenize(sentence)
    
    verbs = []
    for token in tokens:
        if token.type.name.startswith('VERB_'):
            verbs.append((token.lexeme, token.type.value))
    
    if verbs:
        print(f"  识别到的动词: {verbs}")
    else:
        print(f"  未识别到动词")
        # 打印所有词法单元
        for token in tokens:
            if token.type != TokenType.EOF:
                print(f"    {token.lexeme}: {token.type.value}")