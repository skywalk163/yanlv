"""
修复verb_categories_final.py文件结构
"""

def fix_file_structure():
    """修复文件结构"""
    print("修复verb_categories_final.py文件结构...")
    
    try:
        # 读取文件
        with open('src/yanlv/lexer/verb_categories_final.py', 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # 找到TRANSFORMATION类别的结束位置（第256行）
        transformation_end = 255  # 0-based索引，第256行
        
        # 找到VERB_ARITY字典的开始位置
        verb_arity_start = -1
        for i, line in enumerate(lines):
            if 'VERB_ARITY:' in line:
                verb_arity_start = i
                break
        
        if verb_arity_start == -1:
            print("错误: 未找到VERB_ARITY字典")
            return False
        
        print(f"TRANSFORMATION类别结束于第{transformation_end+1}行")
        print(f"VERB_ARITY字典开始于第{verb_arity_start+1}行")
        
        # 创建修复后的内容
        fixed_lines = []
        
        # 第一部分：直到TRANSFORMATION类别结束
        for i in range(transformation_end + 1):
            fixed_lines.append(lines[i])
        
        # 添加VERB_CATEGORIES字典的结束大括号
        # 检查最后一行是否已经是'}'
        if not fixed_lines[-1].strip().endswith('}'):
            # 移除可能的多余逗号
            if fixed_lines[-1].strip().endswith(','):
                fixed_lines[-1] = fixed_lines[-1].rstrip().rstrip(',') + '\n'
            fixed_lines.append('}\n')
        
        # 添加空行
        fixed_lines.append('\n')
        fixed_lines.append('\n')
        
        # 第二部分：从VERB_ARITY开始
        for i in range(verb_arity_start, len(lines)):
            fixed_lines.append(lines[i])
        
        # 写入修复后的文件
        with open('src/yanlv/lexer/verb_categories_final_fixed2.py', 'w', encoding='utf-8') as f:
            f.writelines(fixed_lines)
        
        print("已创建修复后的文件: verb_categories_final_fixed2.py")
        
        # 验证修复
        print("\n验证修复...")
        
        # 检查文件语法
        try:
            with open('src/yanlv/lexer/verb_categories_final_fixed2.py', 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 简单检查结构
            if 'VERB_CATEGORIES:' in content and 'VERB_ARITY:' in content:
                # 检查VERB_CATEGORIES字典是否正确结束
                cat_start = content.find('VERB_CATEGORIES:')
                cat_end = content.find('}', cat_start)
                cat_content = content[cat_start:cat_end+1]
                
                # 检查是否有不应该在字典中的内容
                if '# 新增动词元数' in cat_content:
                    print("警告: VERB_CATEGORIES字典中仍然包含'新增动词元数'注释")
                else:
                    print("VERB_CATEGORIES字典结构正确")
                
                # 检查VERB_ARITY字典
                arity_start = content.find('VERB_ARITY:')
                arity_end = content.find('}', arity_start)
                arity_content = content[arity_start:arity_end+1]
                
                if '# 新增动词元数' in arity_content:
                    print("VERB_ARITY字典包含'新增动词元数'内容")
                else:
                    print("警告: VERB_ARITY字典中缺少'新增动词元数'内容")
                
                print("基本结构检查通过")
                return True
            else:
                print("错误: 未找到必要的字典定义")
                return False
                
        except Exception as e:
            print(f"验证错误: {e}")
            return False
            
    except Exception as e:
        print(f"修复过程中出现错误: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    if fix_file_structure():
        print("\n修复成功!")
    else:
        print("\n修复失败!")