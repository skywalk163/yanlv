"""
验证扩展后的动词分类词典
"""

import sys
import os

# 添加src目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def validate_verb_categories():
    """验证动词分类词典"""
    print("验证扩展后的动词分类词典")
    print("=" * 60)
    
    try:
        # 尝试导入扩展后的词典
        from yanlv.lexer.verb_categories_final import (
            VERB_CATEGORIES, VERB_ARITY, 
            get_verb_category, get_verb_arity,
            get_semantic_role, get_verb_interpretation,
            get_all_verbs, get_verbs_by_category, get_category_by_verb
        )
        print("成功导入扩展后的动词分类词典")
        
        # 统计信息
        total_verbs = 0
        category_info = {}
        
        for category_name, category_data in VERB_CATEGORIES.items():
            verb_count = len(category_data["verbs"])
            total_verbs += verb_count
            category_info[category_name] = verb_count
            print(f"{category_name}: {verb_count}个动词")
        
        print(f"\n总计: {total_verbs}个动词")
        print(f"类别数量: {len(VERB_CATEGORIES)}个")
        
        # 测试新添加的动词
        print("\n测试新添加的动词:")
        
        # 测试数学运算动词
        math_verbs = ["加", "减", "乘", "除", "开方", "对数", "正弦", "余弦", "正切"]
        math_found = 0
        for verb in math_verbs:
            category, info = get_verb_category(verb)
            if category != "UNKNOWN":
                math_found += 1
                print(f"  {verb}: {category} (元数: {get_verb_arity(verb)})")
            else:
                print(f"  {verb}: 未找到")
        
        print(f"\n数学运算动词识别率: {math_found}/{len(math_verbs)} ({math_found/len(math_verbs)*100:.1f}%)")
        
        # 测试逻辑运算动词
        logic_verbs = ["与", "或", "非", "且", "异或", "同或", "蕴含", "等价"]
        logic_found = 0
        for verb in logic_verbs:
            category, info = get_verb_category(verb)
            if category != "UNKNOWN":
                logic_found += 1
                print(f"  {verb}: {category} (元数: {get_verb_arity(verb)})")
            else:
                print(f"  {verb}: 未找到")
        
        print(f"\n逻辑运算动词识别率: {logic_found}/{len(logic_verbs)} ({logic_found/len(logic_verbs)*100:.1f}%)")
        
        # 测试其他新动词
        new_verbs = ["转变为", "赋值", "输出到", "激活", "求平均", "平移", 
                     "发明", "取消", "提取", "改进", "分享", "评审", "加密"]
        
        print("\n其他新添加的动词:")
        other_found = 0
        for verb in new_verbs:
            category, info = get_verb_category(verb)
            if category != "UNKNOWN":
                other_found += 1
                print(f"  {verb}: {category}")
            else:
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
        all_verbs = get_all_verbs()
        print(f"\n所有动词数量: {len(all_verbs)}")
        
        # 检查是否有重复动词
        verb_set = set(all_verbs)
        if len(all_verbs) == len(verb_set):
            print("没有重复动词")
        else:
            duplicates = len(all_verbs) - len(verb_set)
            print(f"发现 {duplicates} 个重复动词")
        
        return True
        
    except ImportError as e:
        print(f"导入错误: {e}")
        print("尝试导入原始版本...")
        
        try:
            from yanlv.lexer.verb_categories import (
                VERB_CATEGORIES, VERB_ARITY, 
                get_verb_category, get_verb_arity,
                get_semantic_role, get_verb_interpretation,
                get_all_verbs, get_verbs_by_category, get_category_by_verb
            )
            print("成功导入原始动词分类词典")
            
            # 统计原始版本
            total_verbs = 0
            for category_name, category_data in VERB_CATEGORIES.items():
                verb_count = len(category_data["verbs"])
                total_verbs += verb_count
                print(f"{category_name}: {verb_count}个动词")
            
            print(f"\n原始版本总计: {total_verbs}个动词")
            print(f"类别数量: {len(VERB_CATEGORIES)}个")
            
            return False
            
        except ImportError as e2:
            print(f"导入原始版本也失败: {e2}")
            return False
    
    except Exception as e:
        print(f"验证过程中出现错误: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_lexer_with_new_verbs():
    """测试词法分析器是否能识别新动词"""
    print("\n" + "=" * 60)
    print("测试词法分析器与新动词的兼容性")
    print("=" * 60)
    
    try:
        # 尝试导入修复后的lexer
        from yanlv.lexer.lexer_simple import YanLuLexerSimple
        print("成功导入简化的词法分析器")
        
        # 创建词法分析器
        lexer = YanLuLexerSimple(segmenter="jieba")
        
        # 测试句子
        test_sentences = [
            "加1和2。",
            "与真和假。",
            "转变为开启状态。",
            "输出到文件。",
            "激活系统。",
        ]
        
        for sentence in test_sentences:
            print(f"\n测试句子: {sentence}")
            try:
                tokens = lexer.tokenize(sentence)
                print(f"  分词结果: {[token.value for token in tokens]}")
                print(f"  词元类型: {[token.type.name for token in tokens]}")
                
                # 检查是否识别为动词
                verb_tokens = [token for token in tokens if token.type.name == "VERB"]
                if verb_tokens:
                    print(f"  识别出的动词: {[token.value for token in verb_tokens]}")
                else:
                    print("  未识别出动词")
                    
            except Exception as e:
                print(f"  错误: {e}")
        
        return True
        
    except ImportError as e:
        print(f"导入词法分析器失败: {e}")
        return False
    except Exception as e:
        print(f"测试过程中出现错误: {e}")
        return False

if __name__ == "__main__":
    print("扩展动词分类词典验证")
    print("=" * 60)
    
    # 验证动词分类词典
    dict_valid = validate_verb_categories()
    
    # 测试词法分析器
    lexer_valid = test_lexer_with_new_verbs()
    
    print("\n" + "=" * 60)
    print("验证结果总结:")
    print(f"  动词分类词典: {'通过' if dict_valid else '失败'}")
    print(f"  词法分析器兼容性: {'通过' if lexer_valid else '失败'}")
    
    if dict_valid and lexer_valid:
        print("\n所有验证通过!")
    else:
        print("\n部分验证失败，需要进一步检查。")