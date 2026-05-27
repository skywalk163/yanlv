"""
言律语言语法迁移工具

将旧语法(使用"结束"关键字)转换为新语法(使用缩进)
"""

import re
from typing import List, Tuple


class SyntaxMigrator:
    """语法迁移器"""
    
    def __init__(self):
        """初始化迁移器"""
        self.block_keywords = ['如果', '循环', '函数', '否则', '当']
        self.end_keyword = '结束'
    
    def convert_to_indent_syntax(self, code: str) -> str:
        """
        将旧语法转换为新语法
        
        Args:
            code: 旧语法代码
            
        Returns:
            新语法代码
        """
        lines = code.split('\n')
        result = []
        indent_stack = [0]  # 缩进栈
        current_indent = 0
        
        for line in lines:
            stripped = line.strip()
            
            # 跳过空行
            if not stripped:
                result.append('')
                continue
            
            # 移除"结束"关键字
            if stripped == self.end_keyword:
                # 弹出缩进栈
                if len(indent_stack) > 1:
                    indent_stack.pop()
                    current_indent = indent_stack[-1]
                continue
            
            # 检查是否是块开始关键字
            is_block_start = False
            for keyword in self.block_keywords:
                if stripped.startswith(keyword):
                    is_block_start = True
                    break
            
            # 添加缩进
            indented_line = '    ' * current_indent + stripped
            result.append(indented_line)
            
            # 如果是块开始,增加缩进
            if is_block_start:
                current_indent += 1
                indent_stack.append(current_indent)
        
        return '\n'.join(result)
    
    def convert_file(self, input_file: str, output_file: str) -> None:
        """
        转换文件
        
        Args:
            input_file: 输入文件路径
            output_file: 输出文件路径
        """
        with open(input_file, 'r', encoding='utf-8') as f:
            old_code = f.read()
        
        new_code = self.convert_to_indent_syntax(old_code)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(new_code)
    
    def analyze_code(self, code: str) -> dict:
        """
        分析代码,统计需要迁移的内容
        
        Args:
            code: 代码字符串
            
        Returns:
            分析结果
        """
        lines = code.split('\n')
        
        end_count = 0
        block_count = 0
        
        for line in lines:
            stripped = line.strip()
            if stripped == self.end_keyword:
                end_count += 1
            
            for keyword in self.block_keywords:
                if stripped.startswith(keyword):
                    block_count += 1
                    break
        
        return {
            'total_lines': len(lines),
            'end_keywords': end_count,
            'block_keywords': block_count,
            'needs_migration': end_count > 0,
            'migration_ratio': end_count / block_count if block_count > 0 else 0
        }


def migrate_code(code: str) -> str:
    """
    便捷函数: 迁移代码
    
    Args:
        code: 旧语法代码
        
    Returns:
        新语法代码
    """
    migrator = SyntaxMigrator()
    return migrator.convert_to_indent_syntax(code)


def migrate_file(input_file: str, output_file: str) -> None:
    """
    便捷函数: 迁移文件
    
    Args:
        input_file: 输入文件路径
        output_file: 输出文件路径
    """
    migrator = SyntaxMigrator()
    migrator.convert_file(input_file, output_file)


# 示例用法
if __name__ == '__main__':
    # 示例代码
    old_code = """如果 条件 成立 则
    输出 "条件为真"
    循环 5 次 执行
        输出 "循环"
    结束
    输出 "完成"
结束
输出 "程序结束" """
    
    print("旧语法:")
    print(old_code)
    print("\n" + "="*60 + "\n")
    
    migrator = SyntaxMigrator()
    new_code = migrator.convert_to_indent_syntax(old_code)
    
    print("新语法:")
    print(new_code)
    print("\n" + "="*60 + "\n")
    
    # 分析
    analysis = migrator.analyze_code(old_code)
    print("分析结果:")
    for key, value in analysis.items():
        print(f"  {key}: {value}")
