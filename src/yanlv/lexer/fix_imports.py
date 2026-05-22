#!/usr/bin/env python3
"""
修复所有模块的导入问题
"""

import os
import re

def fix_imports_in_file(filepath):
    """修复单个文件中的导入"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 替换相对导入为绝对导入
    new_content = content
    
    # 替换 from .module import 为 from module import
    new_content = re.sub(r'from \.(\w+) import', r'from \1 import', new_content)
    
    # 替换 import .module 为 import module
    new_content = re.sub(r'import \.(\w+)', r'import \1', new_content)
    
    if content != new_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"已修复导入: {os.path.basename(filepath)}")
        return True
    return False

def main():
    """主函数"""
    lexer_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 需要修复的文件列表
    files_to_fix = [
        "base.py",
        "constants.py",
        "tokenizer.py",
        "matcher.py",
        "utils.py",
        "error_handler.py",
        "pattern_manager.py",
        "context_manager.py",
        "performance_optimizer.py",
        "lexer_modular.py",
        "__init__.py",
        "test_modular.py"
    ]
    
    fixed_count = 0
    for filename in files_to_fix:
        filepath = os.path.join(lexer_dir, filename)
        if os.path.exists(filepath):
            if fix_imports_in_file(filepath):
                fixed_count += 1
        else:
            print(f"文件不存在: {filename}")
    
    print(f"修复完成！共修复了 {fixed_count} 个文件")

if __name__ == "__main__":
    main()