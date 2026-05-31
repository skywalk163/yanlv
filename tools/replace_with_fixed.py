"""
使用修复版本替换原始文件
"""

import shutil
import os

def replace_file():
    """使用修复版本替换原始文件"""
    print("使用修复版本替换原始文件...")
    
    try:
        # 备份原始文件
        src_file = 'src/yanlv/lexer/verb_categories_final.py'
        backup_file = 'src/yanlv/lexer/verb_categories_final_backup_final.py'
        fixed_file = 'src/yanlv/lexer/verb_categories_final_fixed2.py'
        
        if os.path.exists(src_file):
            shutil.copy2(src_file, backup_file)
            print(f"已备份原始文件: {backup_file}")
        
        # 使用修复版本替换
        shutil.copy2(fixed_file, src_file)
        print(f"已替换原始文件为修复版本: {src_file}")
        
        # 验证替换
        if os.path.exists(src_file):
            print("文件替换成功")
            
            # 检查文件大小
            orig_size = os.path.getsize(backup_file) if os.path.exists(backup_file) else 0
            new_size = os.path.getsize(src_file)
            print(f"原始文件大小: {orig_size} 字节")
            print(f"新文件大小: {new_size} 字节")
            
            # 简单验证文件内容
            with open(src_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if 'VERB_CATEGORIES:' in content and 'VERB_ARITY:' in content:
                print("文件包含必要的字典定义")
                
                # 统计行数
                lines = content.split('\n')
                print(f"文件行数: {len(lines)}")
                
                # 检查VERB_CATEGORIES字典
                cat_start = content.find('VERB_CATEGORIES:')
                cat_end = content.find('}', cat_start)
                cat_section = content[cat_start:cat_end+1]
                
                # 计算类别数量
                category_count = cat_section.count('VerbCategory.')
                print(f"动词类别数量: {category_count}")
                
                return True
            else:
                print("错误: 文件缺少必要的字典定义")
                return False
        else:
            print("错误: 替换后文件不存在")
            return False
            
    except Exception as e:
        print(f"替换过程中出现错误: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    if replace_file():
        print("\n替换成功!")
        
        # 运行最终验证
        print("\n运行最终验证...")
        try:
            import sys
            sys.path.insert(0, 'src')
            
            from yanlv.lexer.verb_categories_final import (
                VERB_CATEGORIES, VERB_ARITY,
                get_verb_category, get_verb_arity,
                get_all_verbs
            )
            
            print("导入成功!")
            print(f"VERB_CATEGORIES类型: {type(VERB_CATEGORIES)}")
            print(f"VERB_CATEGORIES键数量: {len(VERB_CATEGORIES)}")
            print(f"VERB_ARITY类型: {type(VERB_ARITY)}")
            print(f"VERB_ARITY键数量: {len(VERB_ARITY)}")
            
            # 测试几个动词
            test_verbs = ["加", "减", "转变为", "输出到", "激活"]
            print("\n测试动词识别:")
            for verb in test_verbs:
                category, info = get_verb_category(verb)
                arity = get_verb_arity(verb)
                print(f"  {verb}: 类别={category}, 元数={arity}")
            
            # 获取所有动词
            all_verbs = get_all_verbs()
            print(f"\n总动词数量: {len(all_verbs)}")
            
            print("\n所有验证通过!")
            
        except Exception as e:
            print(f"验证失败: {e}")
            import traceback
            traceback.print_exc()
    else:
        print("\n替换失败!")