"""
修复lexer.py语法错误
"""

import re

def fix_lexer_syntax():
    """修复lexer.py中的语法错误"""
    print("修复lexer.py语法错误...")
    
    try:
        # 读取文件
        with open('src/yanlv/lexer/lexer.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 查找有问题的行
        lines = content.split('\n')
        fixed_lines = []
        
        for i, line in enumerate(lines):
            # 检查第147行附近的正则表达式问题
            if i == 146:  # 0-based索引，第147行
                if "self.number_pattern = re.compile(r'^\\d+(\\.\\d+)?" in line and not line.endswith("$')"):
                    # 修复这一行
                    fixed_line = "        self.number_pattern = re.compile(r'^\\d+(\\.\\d+)?$')"
                    fixed_lines.append(fixed_line)
                    print(f"修复第{i+1}行: {line[:50]}... -> {fixed_line}")
                else:
                    fixed_lines.append(line)
            elif i == 147:
                # 下一行应该是self.identifier_pattern
                if "self.identifier_pattern" not in line:
                    # 添加缺失的行
                    fixed_lines.append("        self.identifier_pattern = re.compile(r'^[\\u4e00-\\u9fffA-Za-z_][\\u4e00-\\u9fffA-Za-z0-9_]*$')")
                    print(f"在第{i+1}行添加self.identifier_pattern定义")
                fixed_lines.append(line)
            else:
                fixed_lines.append(line)
        
        # 写入修复后的文件
        fixed_content = '\n'.join(fixed_lines)
        with open('src/yanlv/lexer/lexer.py', 'w', encoding='utf-8') as f:
            f.write(fixed_content)
        
        print("lexer.py语法错误已修复")
        
        # 验证修复
        print("\n验证修复...")
        try:
            with open('src/yanlv/lexer/lexer.py', 'r', encoding='utf-8') as f:
                test_content = f.read()
            
            # 检查关键行
            if "self.number_pattern = re.compile(r'^\\d+(\\.\\d+)?$')" in test_content:
                print("self.number_pattern定义正确")
            else:
                print("self.number_pattern定义仍有问题")
            
            if "self.identifier_pattern = re.compile(r'^[\\u4e00-\\u9fffA-Za-z_][\\u4e00-\\u9fffA-Za-z0-9_]*
            
        except SyntaxError as e:
            print(f"❌ 语法错误: {e}")
            return False
        
        return True
        
    except Exception as e:
        print(f"修复过程中出现错误: {e}")
        return False

if __name__ == "__main__":
    success = fix_lexer_syntax()
    if success:
        print("\n修复完成!")
    else:
        print("\n修复失败!"))" in test_content:
                print("self.identifier_pattern定义正确")
            else:
                print("self.identifier_pattern定义缺失")
            
            # 尝试导入以验证语法
            import ast
            ast.parse(test_content)
            print("语法检查通过")
            
        except SyntaxError as e:
            print(f"❌ 语法错误: {e}")
            return False
        
        return True
        
    except Exception as e:
        print(f"修复过程中出现错误: {e}")
        return False

if __name__ == "__main__":
    success = fix_lexer_syntax()
    if success:
        print("\n修复完成!")
    else:
        print("\n修复失败!")