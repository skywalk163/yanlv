"""
创建最终的verb_categories_final.py版本
"""

def create_final_version():
    """创建最终版本"""
    print("创建最终的verb_categories_final.py版本...")
    
    try:
        # 读取原始文件
        with open('src/yanlv/lexer/verb_categories_final.py', 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # 找到关键位置
        transformation_end = 255  # TRANSFORMATION类别结束位置（0-based）
        verb_arity_start = 432    # VERB_ARITY开始位置（0-based，第433行）
        
        print(f"TRANSFORMATION类别结束于第{transformation_end+1}行")
        print(f"VERB_ARITY字典开始于第{verb_arity_start+1}行")
        
        # 提取'新增动词元数'部分（第258-432行）
        new_verbs_section = []
        for i in range(257, verb_arity_start):  # 第258-432行
            new_verbs_section.append(lines[i])
        
        print(f"提取了{len(new_verbs_section)}行'新增动词元数'内容")
        
        # 创建最终版本
        final_lines = []
        
        # 第一部分：直到TRANSFORMATION类别结束
        for i in range(transformation_end + 1):
            final_lines.append(lines[i])
        
        # 添加VERB_CATEGORIES字典的结束大括号
        # 检查最后一行是否已经是'}'
        if not final_lines[-1].strip().endswith('}'):
            # 移除可能的多余逗号
            if final_lines[-1].strip().endswith(','):
                final_lines[-1] = final_lines[-1].rstrip().rstrip(',') + '\n'
            final_lines.append('}\n')
        
        # 添加空行
        final_lines.append('\n')
        final_lines.append('\n')
        
        # 第二部分：VERB_ARITY字典（包含新增动词元数）
        # 添加VERB_ARITY字典开始
        for i in range(verb_arity_start, verb_arity_start + 1):
            final_lines.append(lines[i])
        
        # 添加新增动词元数内容
        final_lines.append('    # 新增动词元数\n')
        for line in new_verbs_section:
            if line.strip() and not line.strip().startswith('#'):
                final_lines.append(line)
        
        # 添加原始VERB_ARITY内容（从第434行开始）
        for i in range(verb_arity_start + 1, len(lines)):
            final_lines.append(lines[i])
        
        # 写入最终文件
        with open('src/yanlv/lexer/verb_categories_final_corrected.py', 'w', encoding='utf-8') as f:
            f.writelines(final_lines)
        
        print("已创建最终版本: verb_categories_final_corrected.py")
        
        # 验证最终版本
        print("\n验证最终版本...")
        
        # 检查文件语法
        try:
            with open('src/yanlv/lexer/verb_categories_final_corrected.py', 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 导入检查
            import ast
            ast.parse(content)
            print("语法检查通过")
            
            # 检查结构
            if 'VERB_CATEGORIES:' in content and 'VERB_ARITY:' in content:
                print("找到VERB_CATEGORIES和VERB_ARITY字典")
                
                # 统计行数
                line_count = len(content.split('\n'))
                print(f"文件总行数: {line_count}")
                
                # 检查新增动词是否在VERB_ARITY中
                if "'转变为': 2" in content and "'转变为': 2" in content[content.find('VERB_ARITY:'):]:
                    print("新增动词已正确添加到VERB_ARITY字典中")
                else:
                    print("警告: 新增动词可能未正确添加")
                
                return True
            else:
                print("错误: 未找到必要的字典定义")
                return False
                
        except SyntaxError as e:
            print(f"语法错误: {e}")
            # 显示错误位置
            lines = content.split('\n')
            error_line = e.lineno - 1
            start = max(0, error_line - 3)
            end = min(len(lines), error_line + 3)
            print(f"\n错误位置附近的代码 (第{error_line+1}行):")
            for i in range(start, end):
                prefix = ">>> " if i == error_line else "    "
                print(f"{prefix}{i+1:4d}: {lines[i]}")
            return False
        except Exception as e:
            print(f"验证错误: {e}")
            return False
            
    except Exception as e:
        print(f"创建过程中出现错误: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    if create_final_version():
        print("\n创建成功!")
        
        # 替换原始文件
        import shutil
        import os
        try:
            # 备份原始文件
            if os.path.exists('src/yanlv/lexer/verb_categories_final.py'):
                shutil.copy2('src/yanlv/lexer/verb_categories_final.py', 
                           'src/yanlv/lexer/verb_categories_final_backup2.py')
                print("已备份原始文件: verb_categories_final_backup2.py")
            
            # 替换为修正版本
            shutil.copy2('src/yanlv/lexer/verb_categories_final_corrected.py',
                        'src/yanlv/lexer/verb_categories_final.py')
            print("已替换原始文件为修正版本")
            
        except Exception as e:
            print(f"替换文件时出错: {e}")
    else:
        print("\n创建失败!")