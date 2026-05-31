"""
修复verb_categories_final.py文件结构
"""

def fix_verb_categories():
    """修复动词分类词典文件结构"""
    print("修复verb_categories_final.py文件结构...")
    
    try:
        # 读取文件
        with open('src/yanlv/lexer/verb_categories_final.py', 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # 查找VERB_CATEGORIES字典的结束位置
        in_verb_categories = False
        brace_count = 0
        verb_categories_end = -1
        
        for i, line in enumerate(lines):
            if 'VERB_CATEGORIES: Dict[str, Dict[str, Any]] = {' in line:
                in_verb_categories = True
                brace_count = 1
                print(f"VERB_CATEGORIES字典开始于第{i+1}行")
                continue
            
            if in_verb_categories:
                for char in line:
                    if char == '{':
                        brace_count += 1
                    elif char == '}':
                        brace_count -= 1
                        if brace_count == 0:
                            verb_categories_end = i
                            in_verb_categories = False
                            print(f"VERB_CATEGORIES字典结束于第{i+1}行")
                            break
            
            if verb_categories_end != -1:
                break
        
        if verb_categories_end == -1:
            print("错误: 未找到VERB_CATEGORIES字典的结束位置")
            return False
        
        # 检查第verb_categories_end行之后的内容
        print(f"\n检查第{verb_categories_end+1}行之后的内容:")
        for i in range(verb_categories_end, min(verb_categories_end + 10, len(lines))):
            print(f"第{i+1:4d}: {lines[i].rstrip()}")
        
        # 问题: 在VERB_CATEGORIES字典结束后，还有内容被错误地包含在字典中
        # 我们需要找到真正的VERB_CATEGORIES字典结束位置
        # 让我们查找下一个重要的标记
        
        print("\n查找真正的字典结束位置...")
        
        # 查找下一个重要的定义
        next_definitions = []
        for i in range(verb_categories_end + 1, len(lines)):
            line = lines[i].strip()
            if line.startswith('VERB_ARITY:'):
                next_definitions.append(('VERB_ARITY', i))
                break
            elif line.startswith('def '):
                next_definitions.append(('function', i))
                break
            elif line.startswith('#') and '动词元数' in line:
                print(f"在第{i+1}行找到'动词元数'注释: {line}")
        
        if not next_definitions:
            print("错误: 未找到下一个定义")
            return False
        
        next_def_name, next_def_line = next_definitions[0]
        print(f"下一个定义 '{next_def_name}' 在第{next_def_line+1}行")
        
        # 现在我们需要修复文件
        # 首先备份原始文件
        import shutil
        shutil.copy2('src/yanlv/lexer/verb_categories_final.py', 
                    'src/yanlv/lexer/verb_categories_final_backup.py')
        print("已创建备份文件: verb_categories_final_backup.py")
        
        # 重新构建文件
        fixed_lines = []
        
        # 第一部分: VERB_CATEGORIES字典
        in_dict = False
        brace_count = 0
        for i, line in enumerate(lines):
            if 'VERB_CATEGORIES: Dict[str, Dict[str, Any]] = {' in line:
                in_dict = True
                brace_count = 1
                fixed_lines.append(line)
                continue
            
            if in_dict:
                # 检查是否应该结束字典
                if i >= next_def_line:
                    # 我们已经到达下一个定义，需要结束字典
                    fixed_lines.append('}\n')
                    in_dict = False
                    brace_count = 0
                    # 添加空行
                    fixed_lines.append('\n')
                    # 添加下一个定义
                    fixed_lines.extend(lines[i:])
                    break
                
                # 检查大括号计数
                for char in line:
                    if char == '{':
                        brace_count += 1
                    elif char == '}':
                        brace_count -= 1
                
                fixed_lines.append(line)
                
                # 如果大括号计数为0，字典结束
                if brace_count == 0:
                    in_dict = False
            else:
                fixed_lines.append(line)
        
        # 写入修复后的文件
        with open('src/yanlv/lexer/verb_categories_final_fixed.py', 'w', encoding='utf-8') as f:
            f.writelines(fixed_lines)
        
        print("\n已创建修复后的文件: verb_categories_final_fixed.py")
        
        # 验证修复
        print("\n验证修复...")
        try:
            # 尝试导入修复后的文件
            import importlib.util
            spec = importlib.util.spec_from_file_location(
                "verb_categories_final_fixed", 
                "src/yanlv/lexer/verb_categories_final_fixed.py"
            )
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # 检查VERB_CATEGORIES
            if hasattr(module, 'VERB_CATEGORIES'):
                verb_categories = module.VERB_CATEGORIES
                print(f"VERB_CATEGORIES类型: {type(verb_categories)}")
                print(f"VERB_CATEGORIES键数量: {len(verb_categories)}")
                
                # 检查每个值是否是字典
                all_dicts = True
                for key, value in verb_categories.items():
                    if not isinstance(value, dict):
                        print(f"错误: {key} 的值不是字典，而是 {type(value)}")
                        all_dicts = False
                        break
                
                if all_dicts:
                    print("所有VERB_CATEGORIES值都是字典")
                else:
                    print("VERB_CATEGORIES中有非字典值")
            
            # 检查VERB_ARITY
            if hasattr(module, 'VERB_ARITY'):
                verb_arity = module.VERB_ARITY
                print(f"VERB_ARITY类型: {type(verb_arity)}")
                print(f"VERB_ARITY键数量: {len(verb_arity)}")
            
            print("语法检查通过")
            return True
            
        except Exception as e:
            print(f"验证失败: {e}")
            import traceback
            traceback.print_exc()
            return False
        
    except Exception as e:
        print(f"修复过程中出现错误: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    if fix_verb_categories():
        print("\n修复成功!")
    else:
        print("\n修复失败!")