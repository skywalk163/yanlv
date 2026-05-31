"""
简单修复lexer.py语法错误
"""

def fix_lexer():
    print("修复lexer.py语法错误...")
    
    try:
        # 读取文件
        with open('src/yanlv/lexer/lexer.py', 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # 查找并修复有问题的行
        for i in range(len(lines)):
            line = lines[i]
            if "self.number_pattern = re.compile(r'^\\d+(\\.\\d+)?" in line and not line.strip().endswith("$')"):
                # 修复这一行
                lines[i] = "        self.number_pattern = re.compile(r'^\\d+(\\.\\d+)?$')\n"
                print(f"修复第{i+1}行")
            
            # 检查下一行是否缺少self.identifier_pattern
            if i+1 < len(lines) and "self.identifier_pattern" not in lines[i+1] and "self.number_pattern" in line:
                # 在下一行插入self.identifier_pattern
                lines.insert(i+1, "        self.identifier_pattern = re.compile(r'^[\\u4e00-\\u9fffA-Za-z_][\\u4e00-\\u9fffA-Za-z0-9_]*$')\n")
                print(f"在第{i+2}行添加self.identifier_pattern定义")
                break
        
        # 写入修复后的文件
        with open('src/yanlv/lexer/lexer.py', 'w', encoding='utf-8') as f:
            f.writelines(lines)
        
        print("修复完成")
        
        # 验证修复
        print("\n验证修复...")
        with open('src/yanlv/lexer/lexer.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        if "self.number_pattern = re.compile(r'^\\d+(\\.\\d+)?$')" in content:
            print("self.number_pattern定义正确")
        else:
            print("self.number_pattern定义仍有问题")
        
        if "self.identifier_pattern = re.compile(r'^[\\u4e00-\\u9fffA-Za-z_][\\u4e00-\\u9fffA-Za-z0-9_]*$')" in content:
            print("self.identifier_pattern定义正确")
        else:
            print("self.identifier_pattern定义缺失")
        
        # 尝试解析以验证语法
        import ast
        try:
            ast.parse(content)
            print("语法检查通过")
            return True
        except SyntaxError as e:
            print(f"语法错误: {e}")
            return False
            
    except Exception as e:
        print(f"修复过程中出现错误: {e}")
        return False

if __name__ == "__main__":
    if fix_lexer():
        print("\n修复成功!")
    else:
        print("\n修复失败!")