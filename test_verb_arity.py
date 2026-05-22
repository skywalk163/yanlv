#!/usr/bin/env python3
"""
测试动词元数识别
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from yanlv.lexer.verb_categories import get_verb_arity, VERB_ARITY

# 测试动词
test_verbs = ["变为", "开启", "计算", "移动", "创建", "删除", "查询", "修改", "发送", "比较", "转换"]

print("动词元数测试:")
print("=" * 40)

for verb in test_verbs:
    arity = get_verb_arity(verb)
    in_dict = verb in VERB_ARITY
    print(f"动词: {verb:10} 元数: {arity:2} 在字典中: {in_dict}")

print("\n检查VERB_ARITY字典内容:")
print(f"字典大小: {len(VERB_ARITY)}")
print("前20个动词:")
for i, (verb, arity) in enumerate(list(VERB_ARITY.items())[:20]):
    print(f"  {i+1:2}. {verb:10} -> {arity}")

# 检查特定动词
print("\n检查测试动词是否在字典中:")
for verb in test_verbs:
    if verb in VERB_ARITY:
        print(f"  [OK] {verb} 在字典中，元数: {VERB_ARITY[verb]}")
    else:
        print(f"  [NO] {verb} 不在字典中")

# 检查动词分类
from yanlv.lexer.verb_categories import get_verb_category, VERB_CATEGORIES

print("\n检查动词分类:")
for verb in test_verbs:
    category_name, category_info = get_verb_category(verb)
    if category_info:
        print(f"  {verb:10} -> 类别: {category_name}")
    else:
        print(f"  {verb:10} -> 未找到类别")

# 列出所有动词
print("\n所有动词类别和动词:")
for category_name, category_info in VERB_CATEGORIES.items():
    verbs = category_info["verbs"]
    print(f"{category_name}: {len(verbs)}个动词")
    for verb in verbs[:5]:  # 只显示前5个
        print(f"  - {verb}")
    if len(verbs) > 5:
        print(f"  ... 还有{len(verbs)-5}个")
    print()