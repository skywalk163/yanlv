"""
检查verb_categories_final.py语法
"""

import ast
import sys

def check_syntax(file_path):
    """检查Python文件语法"""
    print(f"检查文件: {file_path}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 尝试解析
        ast.parse(content)
        print("语法检查通过")
        return True
        
    except SyntaxError as e:
        print(f"❌ 语法错误: {e}")
        
        # 显示错误位置附近的代码
        lines = content.split('\n')
        error_line = e.lineno - 1  # ast使用1-based行号
        start_line = max(0, error_line - 3)
        end_line = min(len(lines), error_line + 3)
        
        print(f"\n错误位置附近的代码 (第{error_line + 1}行):")
        for i in range(start_line, end_line):
            prefix = ">>> " if i == error_line else "    "
            print(f"{prefix}{i+1:4d}: {lines[i]}")
        
        return False
    except Exception as e:
        print(f"❌ 其他错误: {e}")
        return False

def check_dict_structure(file_path):
    """检查字典结构"""
    print(f"\n检查字典结构: {file_path}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 查找VERB_CATEGORIES字典
        start = content.find('VERB_CATEGORIES: Dict[str, Dict[str, Any]] = {')
        if start == -1:
            print("❌ 未找到VERB_CATEGORIES字典定义")
            return False
        
        # 查找字典结束位置
        brace_count = 0
        in_dict = False
        dict_content = ""
        
        for i, char in enumerate(content[start:]):
            if char == '{':
                brace_count += 1
                in_dict = True
            elif char == '}':
                brace_count -= 1
            
            dict_content += char
            
            if in_dict and brace_count == 0:
                break
        
        print(f"✅ 找到VERB_CATEGORIES字典，长度: {len(dict_content)}字符")
        
        # 检查键值对
        lines = dict_content.split('\n')
        key_count = 0
        for i, line in enumerate(lines):
            if ':' in line and '#' not in line.split(':')[0]:
                # 检查是否是字典键
                if 'value:' in line or '":' in line or "':" in line:
                    key_count += 1
        
        print(f"✅ 字典包含大约 {key_count} 个键值对")
        
        return True
        
    except Exception as e:
        print(f"❌ 检查字典结构时出错: {e}")
        return False

if __name__ == "__main__":
    file_path = "src/yanlv/lexer/verb_categories_final.py"
    
    print("检查扩展动词分类词典语法")
    print("=" * 60)
    
    syntax_ok = check_syntax(file_path)
    dict_ok = check_dict_structure(file_path)
    
    print("\n" + "=" * 60)
    print("检查结果:")
    print(f"  语法检查: {'通过' if syntax_ok else '失败'}")
    print(f"  字典结构: {'通过' if dict_ok else '失败'}")
    
    if syntax_ok and dict_ok:
        print("\n✅ 文件语法正确!")
    else:
        print("\n❌ 文件有语法问题，需要修复。")