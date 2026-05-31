#!/usr/bin/env python3
"""
修复导入问题的脚本
"""

import os
import re

# 需要修复的文件列表
files_to_fix = [
    'src/yanlv/lexer/matcher.py',
    'src/yanlv/lexer/error_handler.py',
    'src/yanlv/lexer/context_manager.py',
    'src/yanlv/lexer/pattern_manager.py',
    'src/yanlv/lexer/performance_optimizer.py',
    'src/yanlv/lexer/utils.py',
    'src/yanlv/lexer/base.py',
]

# 需要添加相对导入的模块
modules_to_relative = [
    'lexer_token',
    'tokenizer',
    'matcher',
    'error_handler',
    'context_manager',
    'pattern_manager',
    'performance_optimizer',
    'utils',
    'base',
    'constants',
]

def fix_imports(file_path):
    """修复文件中的导入"""
    if not os.path.exists(file_path):
        print(f"文件不存在: {file_path}")
        return
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # 修复导入语句
    for module in modules_to_relative:
        # 匹配 "from module import" 但不是 "from .module import"
        pattern = f'^from {module} import'
        replacement = f'from .{module} import'
        content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
        
        # 匹配 "import module" 但不是 "import .module"
        pattern = f'^import {module}$'
        replacement = f'from . import {module}'
        content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
    
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"已修复: {file_path}")
    else:
        print(f"无需修复: {file_path}")

def main():
    """主函数"""
    print("开始修复导入问题...")
    
    for file_path in files_to_fix:
        fix_imports(file_path)
    
    print("\n修复完成！")

if __name__ == '__main__':
    main()