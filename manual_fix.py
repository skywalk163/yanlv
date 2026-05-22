"""
手动修复verb_categories_final.py文件
"""

def manual_fix():
    """手动修复文件"""
    print("手动修复verb_categories_final.py文件...")
    
    try:
        # 读取原始文件
        with open('src/yanlv/lexer/verb_categories_final.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 找到VERB_CATEGORIES字典的结束位置
        cat_start = content.find('VERB_CATEGORIES: Dict[str, Dict[str, Any]] = {')
        if cat_start == -1:
            print("错误: 未找到VERB_CATEGORIES字典")
            return False
        
        # 找到VERB_CATEGORIES字典的结束
        brace_count = 0
        cat_end = -1
        for i, char in enumerate(content[cat_start:]):
            if char == '{':
                brace_count += 1
            elif char == '}':
                brace_count -= 1
                if brace_count == 0:
                    cat_end = cat_start + i
                    break
        
        if cat_end == -1:
            print("错误: 未找到VERB_CATEGORIES字典的结束")
            return False
        
        print(f"VERB_CATEGORIES字典: 第{cat_start}到第{cat_end}字符")
        
        # 找到TRANSFORMATION类别的结束
        trans_end = content.find('        "examples": [\n            "转换格式。",\n            "翻译文本。",\n            "解析数据。"\n        ]\n    }', cat_start)
        if trans_end == -1:
            print("错误: 未找到TRANSFORMATION类别的结束")
            return False
        
        # 找到TRANSFORMATION类别结束后的位置
        trans_end_pos = trans_end + len('        "examples": [\n            "转换格式。",\n            "翻译文本。",\n            "解析数据。"\n        ]\n    }')
        
        # 检查是否需要添加逗号
        if content[trans_end_pos:trans_end_pos+1] != ',':
            trans_end_pos = content.find('\n', trans_end_pos)
        
        print(f"TRANSFORMATION类别结束位置: 第{trans_end_pos}字符")
        
        # 构建修复后的内容
        # 第一部分: VERB_CATEGORIES字典（到TRANSFORMATION结束）
        part1 = content[:trans_end_pos]
        
        # 确保以}结束VERB_CATEGORIES字典
        if not part1.strip().endswith('}'):
            # 移除可能的多余逗号
            if part1.strip().endswith(','):
                part1 = part1.rstrip().rstrip(',')
            part1 += '\n}'
        
        # 第二部分: VERB_ARITY字典
        # 找到VERB_ARITY开始
        arity_start = content.find('VERB_ARITY: Dict[str, int] = {')
        if arity_start == -1:
            print("错误: 未找到VERB_ARITY字典")
            return False
        
        # 提取'新增动词元数'部分（在TRANSFORMATION之后，VERB_ARITY之前）
        new_verbs = content[trans_end_pos:arity_start].strip()
        
        # 提取VERB_ARITY字典内容
        brace_count = 0
        arity_end = -1
        for i, char in enumerate(content[arity_start:]):
            if char == '{':
                brace_count += 1
            elif char == '}':
                brace_count -= 1
                if brace_count == 0:
                    arity_end = arity_start + i + 1
                    break
        
        if arity_end == -1:
            print("错误: 未找到VERB_ARITY字典的结束")
            return False
        
        arity_content = content[arity_start:arity_end]
        
        # 构建新的VERB_ARITY字典，包含新增动词
        # 找到VERB_ARITY字典中第一个'}'之前的位置
        first_brace = arity_content.find('{')
        last_brace = arity_content.rfind('}')
        
        if first_brace == -1 or last_brace == -1:
            print("错误: VERB_ARITY字典格式错误")
            return False
        
        # 插入新增动词到VERB_ARITY字典中
        arity_before = arity_content[:last_brace]
        arity_after = arity_content[last_brace:]
        
        # 清理new_verbs，移除注释和空行
        new_verbs_lines = new_verbs.split('\n')
        cleaned_new_verbs = []
        for line in new_verbs_lines:
            stripped = line.strip()
            if stripped and not stripped.startswith('#'):
                # 确保有正确的缩进
                if not stripped.startswith('    '):
                    stripped = '    ' + stripped
                cleaned_new_verbs.append(stripped)
        
        if cleaned_new_verbs:
            # 在最后一个元素前添加新增动词
            new_arity_content = arity_before.rstrip()
            if not new_arity_content.endswith(','):
                new_arity_content += ','
            new_arity_content += '\n    \n    # 新增动词元数\n'
            new_arity_content += ',\n'.join(cleaned_new_verbs)
            new_arity_content += '\n' + arity_after
        else:
            new_arity_content = arity_content
        
        # 构建完整内容
        fixed_content = part1 + '\n\n\n' + new_arity_content + content[arity_end:]
        
        # 写入修复后的文件
        with open('src/yanlv/lexer/verb_categories_final_fixed3.py', 'w', encoding='utf-8') as f:
            f.write(fixed_content)
        
        print("已创建修复后的文件: verb_categories_final_fixed3.py")
        
        # 验证修复
        print("\n验证修复...")
        try:
            # 检查语法
            import ast
            ast.parse(fixed_content)
            print("语法检查通过")
            
            # 检查结构
            if 'VERB_CATEGORIES:' in fixed_content and 'VERB_ARITY:' in fixed_content:
                print("找到VERB_CATEGORIES和VERB_ARITY字典")
                
                # 检查新增动词是否在VERB_ARITY中
                if "'转变为': 2" in fixed_content and "'转变为': 2" in fixed_content[fixed_content.find('VERB_ARITY:'):]:
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
            lines = fixed_content.split('\n')
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
        print(f"修复过程中出现错误: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    if manual_fix():
        print("\n修复成功!")
        
        # 替换原始文件
        import shutil
        import os
        try:
            # 备份原始文件
            if os.path.exists('src/yanlv/lexer/verb_categories_final.py'):
                shutil.copy2('src/yanlv/lexer/verb_categories_final.py', 
                           'src/yanlv/lexer/verb_categories_final_backup3.py')
                print("已备份原始文件: verb_categories_final_backup3.py")
            
            # 替换为修正版本
            shutil.copy2('src/yanlv/lexer/verb_categories_final_fixed3.py',
                        'src/yanlv/lexer/verb_categories_final.py')
            print("已替换原始文件为修正版本")
            
            # 运行验证脚本
            print("\n运行验证脚本...")
            import subprocess
            result = subprocess.run(['python', 'validate_verbs_simple.py'], 
                                  capture_output=True, text=True)
            print("验证输出:")
            print(result.stdout)
            if result.stderr:
                print("验证错误:")
                print(result.stderr)
                
        except Exception as e:
            print(f"替换文件时出错: {e}")
    else:
        print("\n修复失败!")