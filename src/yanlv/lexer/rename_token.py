#!/usr/bin/env python3
"""
重命名token.py文件以避免与Python标准库冲突
"""

import os
import shutil

# 重命名token.py为lexer_token.py
old_path = os.path.join(os.path.dirname(__file__), "token.py")
new_path = os.path.join(os.path.dirname(__file__), "lexer_token.py")

if os.path.exists(old_path):
    shutil.move(old_path, new_path)
    print(f"已重命名 {old_path} -> {new_path}")
else:
    print(f"文件不存在: {old_path}")

# 更新所有引用token.py的文件
files_to_update = [
    "constants.py",
    "matcher.py",
    "lexer_modular.py",
    "__init__.py",
    "base.py",
    "error_handler.py",
    "test_modular.py"
]

for filename in files_to_update:
    filepath = os.path.join(os.path.dirname(__file__), filename)
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 替换导入语句
        new_content = content.replace('from .token import', 'from .lexer_token import')
        new_content = new_content.replace('from token import', 'from lexer_token import')
        new_content = new_content.replace('import .token', 'import .lexer_token')
        
        if content != new_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"已更新 {filename}")
        else:
            print(f"无需更新 {filename}")
    else:
        print(f"文件不存在: {filename}")

print("重命名完成！")