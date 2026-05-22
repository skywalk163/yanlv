"""
简单验证扩展后的动词分类词典
"""

import sys
import os

def validate_verb_categories():
    """验证动词分类词典"""
    print("验证扩展后的动词分类词典")
    print("=" * 60)
    
    try:
        # 直接导入verb_categories_final模块
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
        
        # 动态导入
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "verb_categories_final", 
            os.path.join(os.path.dirname(__file__), 'src', 'yanlv', 'lexer', 'verb_categories_final.py')
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        VERB_CATEGORIES = module.VERB_CATEGORIES
        VERB_ARITY = module.VERB_ARITY
        
        # 统计信息
        total_verbs = 0
        category_info = {}
        
        print("动词分类统计:")
        for category_name, category_data in VERB_CATEGORIES.items():
            verb_count = len(category_data["verbs"])
            total_verbs += verb_count
            category_info[category_name] = verb_count
            print(f"  {category_name}: {verb_count}个动词")
        
        print(f"\n总计: {total_verbs}个动词")
        print(f"类别数量: {len(VERB_CATEGORIES)}个")
        
        # 测试新添加的动词
        print("\n测试新添加的动词:")
        
        # 测试数学运算动词
        math_verbs = ["加", "减", "乘", "除", "开方", "对数", "正弦", "余弦", "正切"]
        math_found = 0
        for verb in math_verbs:
            if verb in VERB_ARITY:
                math_found += 1
                print(f"  {verb}: 找到 (元数: {VERB_ARITY[verb]})")
            else:
                print(f"  {verb}: 未找到")
        
        print(f"\n数学运算动词识别率: {math_found}/{len(math_verbs)} ({math_found/len(math_verbs)*100:.1f}%)")
        
        # 测试逻辑运算动词
        logic_verbs = ["与", "或", "非", "且", "异或", "同或", "蕴含", "等价"]
        logic_found = 0
        for verb in logic_verbs:
            if verb in VERB_ARITY:
                logic_found += 1
                print(f"  {verb}: 找到 (元数: {VERB_ARITY[verb]})")
            else:
                print(f"  {verb}: 未找到")
        
        print(f"\n逻辑运算动词识别率: {logic_found}/{len(logic_verbs)} ({logic_found/len(logic_verbs)*100:.1f}%)")
        
        # 测试其他新动词
        new_verbs = ["转变为", "赋值", "输出到", "激活", "求平均", "平移", 
                     "发明", "取消", "提取", "改进", "分享", "评审", "加密"]
        
        print("\n其他新添加的动词:")
        other_found = 0
        for verb in new_verbs:
            found = False
            for category_data in VERB_CATEGORIES.values():
                if verb in category_data["verbs"]:
                    other_found += 1
                    print(f"  {verb}: 找到")
                    found = True
                    break
            if not found:
                print(f"  {verb}: 未找到")
        
        print(f"\n其他新动词识别率: {other_found}/{len(new_verbs)} ({other_found/len(new_verbs)*100:.1f}%)")
        
        # 总体统计
        total_tested = len(math_verbs) + len(logic_verbs) + len(new_verbs)
        total_found = math_found + logic_found + other_found
        overall_rate = total_found / total_tested * 100
        
        print(f"\n总体识别率: {total_found}/{total_tested} ({overall_rate:.1f}%)")
        
        # 检查VERB_ARITY表
        print("\n检查VERB_ARITY表:")
        test_verbs = ["加", "减", "乘", "与", "或", "转变为", "输出到", "激活"]
        for verb in test_verbs:
            arity = VERB_ARITY.get(verb, "未定义")
            print(f"  {verb}: 元数 = {arity}")
        
        # 检查所有动词
        all_verbs = []
        for category_data in VERB_CATEGORIES.values():
            all_verbs.extend(category_data["verbs"])
        
        print(f"\n所有动词数量: {len(all_verbs)}")
        
        # 检查是否有重复动词
        verb_set = set(all_verbs)
        if len(all_verbs) == len(verb_set):
            print("没有重复动词")
        else:
            duplicates = len(all_verbs) - len(verb_set)
            print(f"发现 {duplicates} 个重复动词")
            
            # 找出重复的动词
            from collections import Counter
            verb_counts = Counter(all_verbs)
            duplicates_list = [verb for verb, count in verb_counts.items() if count > 1]
            if duplicates_list:
                print(f"重复动词: {duplicates_list[:10]}")  # 只显示前10个
        
        return True
        
    except Exception as e:
        print(f"验证过程中出现错误: {e}")
        import traceback
        traceback.print_exc()
        return False

def compare_with_original():
    """与原始版本比较"""
    print("\n" + "=" * 60)
    print("与原始版本比较")
    print("=" * 60)
    
    try:
        # 导入原始版本
        import importlib.util
        spec_original = importlib.util.spec_from_file_location(
            "verb_categories", 
            os.path.join(os.path.dirname(__file__), 'src', 'yanlv', 'lexer', 'verb_categories.py')
        )
        module_original = importlib.util.module_from_spec(spec_original)
        spec_original.loader.exec_module(module_original)
        
        VERB_CATEGORIES_ORIGINAL = module_original.VERB_CATEGORIES
        VERB_ARITY_ORIGINAL = module_original.VERB_ARITY
        
        # 导入扩展版本
        spec_extended = importlib.util.spec_from_file_location(
            "verb_categories_final", 
            os.path.join(os.path.dirname(__file__), 'src', 'yanlv', 'lexer', 'verb_categories_final.py')
        )
        module_extended = importlib.util.module_from_spec(spec_extended)
        spec_extended.loader.exec_module(module_extended)
        
        VERB_CATEGORIES_EXTENDED = module_extended.VERB_CATEGORIES
        VERB_ARITY_EXTENDED = module_extended.VERB_ARITY
        
        # 统计原始版本
        original_verb_count = 0
        for category_data in VERB_CATEGORIES_ORIGINAL.values():
            original_verb_count += len(category_data["verbs"])
        
        # 统计扩展版本
        extended_verb_count = 0
        for category_data in VERB_CATEGORIES_EXTENDED.values():
            extended_verb_count += len(category_data["verbs"])
        
        print(f"原始版本: {original_verb_count}个动词")
        print(f"扩展版本: {extended_verb_count}个动词")
        print(f"增加数量: {extended_verb_count - original_verb_count}个动词")
        print(f"增长率: {(extended_verb_count - original_verb_count) / original_verb_count * 100:.1f}%")
        
        # 比较类别
        original_categories = set(VERB_CATEGORIES_ORIGINAL.keys())
        extended_categories = set(VERB_CATEGORIES_EXTENDED.keys())
        
        print(f"\n原始类别数量: {len(original_categories)}")
        print(f"扩展类别数量: {len(extended_categories)}")
        
        new_categories = extended_categories - original_categories
        if new_categories:
            print(f"新增类别: {new_categories}")
        else:
            print("没有新增类别")
        
        # 比较元数表
        original_arity_count = len(VERB_ARITY_ORIGINAL)
        extended_arity_count = len(VERB_ARITY_EXTENDED)
        
        print(f"\n原始元数表: {original_arity_count}个动词")
        print(f"扩展元数表: {extended_arity_count}个动词")
        print(f"元数表增加: {extended_arity_count - original_arity_count}个动词")
        
        return True
        
    except Exception as e:
        print(f"比较过程中出现错误: {e}")
        return False

if __name__ == "__main__":
    print("扩展动词分类词典验证")
    print("=" * 60)
    
    # 验证动词分类词典
    dict_valid = validate_verb_categories()
    
    # 与原始版本比较
    compare_valid = compare_with_original()
    
    print("\n" + "=" * 60)
    print("验证结果总结:")
    print(f"  动词分类词典验证: {'通过' if dict_valid else '失败'}")
    print(f"  与原始版本比较: {'通过' if compare_valid else '失败'}")
    
    if dict_valid:
        print("\n扩展动词分类词典验证通过!")
    else:
        print("\n扩展动词分类词典验证失败，需要进一步检查。")