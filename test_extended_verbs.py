"""
测试扩展后的动词分类词典
"""

import sys
import os

# 添加src目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# 导入扩展后的动词分类词典
exec(open('src/yanlv/lexer/verb_categories_final.py', 'r', encoding='utf-8').read())

def test_extended_verbs():
    """测试扩展后的动词分类词典"""
    print("测试扩展后的动词分类词典")
    print("=" * 60)
    
    # 统计动词数量
    total_verbs = 0
    category_counts = {}
    
    for category_name, category_info in VERB_CATEGORIES.items():
        verb_count = len(category_info["verbs"])
        category_counts[category_name] = verb_count
        total_verbs += verb_count
        print(f"{category_name}: {verb_count}个动词")
    
    print(f"\n总计: {total_verbs}个动词")
    print(f"类别数量: {len(VERB_CATEGORIES)}个")
    
    # 测试新添加的动词
    print("\n测试新添加的动词:")
    
    # 测试数学运算动词
    math_verbs = ["加", "减", "乘", "除", "开方", "对数"]
    for verb in math_verbs:
        category, info = get_verb_category(verb)
        if category != "UNKNOWN":
            print(f"  {verb}: {category} (元数: {get_verb_arity(verb)})")
        else:
            print(f"  {verb}: 未找到")
    
    # 测试逻辑运算动词
    logic_verbs = ["与", "或", "非", "且", "异或"]
    print("\n逻辑运算动词:")
    for verb in logic_verbs:
        category, info = get_verb_category(verb)
        if category != "UNKNOWN":
            print(f"  {verb}: {category} (元数: {get_verb_arity(verb)})")
        else:
            print(f"  {verb}: 未找到")
    
    # 测试新添加的其他动词
    new_verbs = ["转变为", "赋值", "输出到", "激活", "求平均", "平移", 
                 "发明", "取消", "提取", "改进", "分享", "评审", "加密"]
    
    print("\n其他新添加的动词:")
    found_count = 0
    for verb in new_verbs:
        category, info = get_verb_category(verb)
        if category != "UNKNOWN":
            found_count += 1
            print(f"  {verb}: {category}")
        else:
            print(f"  {verb}: 未找到")
    
    print(f"\n新动词识别率: {found_count}/{len(new_verbs)} ({found_count/len(new_verbs)*100:.1f}%)")
    
    # 测试VERB_ARITY表
    print("\n测试VERB_ARITY表:")
    test_verbs = ["加", "减", "乘", "与", "或", "转变为", "输出到"]
    for verb in test_verbs:
        arity = VERB_ARITY.get(verb, "未定义")
        print(f"  {verb}: 元数 = {arity}")
    
    return total_verbs

if __name__ == "__main__":
    total_verbs = test_extended_verbs()
    
    # 与原始版本比较
    print("\n" + "=" * 60)
    print("扩展结果总结:")
    print(f"  扩展后总动词数量: {total_verbs}")
    print(f"  目标数量: 298个")
    print(f"  完成度: {total_verbs}/298 = {total_verbs/298*100:.1f}%")
    
    if total_verbs >= 298:
        print("✅ 动词分类词典扩展成功!")
    else:
        print("⚠️ 动词分类词典扩展未达到目标")