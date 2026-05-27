"""
言律语言代码格式化工具

提供代码自动格式化功能,统一代码风格
"""

from typing import List, Tuple, Optional
import re


class CodeFormatter:
    """
    代码格式化器
    
    自动格式化言律语言代码,统一代码风格
    """
    
    def __init__(self, indent_size: int = 4):
        """
        初始化格式化器
        
        Args:
            indent_size: 缩进大小
        """
        self.indent_size = indent_size
        self.indent_char = ' '  # 使用空格缩进
    
    def format(self, code: str) -> str:
        """
        格式化代码
        
        Args:
            code: 原始代码
            
        Returns:
            格式化后的代码
        """
        # 分行处理
        lines = code.split('\n')
        
        # 1. 去除行尾空白
        lines = [line.rstrip() for line in lines]
        
        # 2. 统一缩进
        lines = self._normalize_indentation(lines)
        
        # 3. 添加空行
        lines = self._add_blank_lines(lines)
        
        # 4. 格式化运算符周围的空格
        lines = self._format_operators(lines)
        
        # 5. 格式化逗号后的空格
        lines = self._format_commas(lines)
        
        return '\n'.join(lines)
    
    def _normalize_indentation(self, lines: List[str]) -> List[str]:
        """
        统一缩进
        
        Args:
            lines: 代码行列表
            
        Returns:
            处理后的代码行列表
        """
        result = []
        indent_level = 0
        
        for line in lines:
            # 去除原有缩进
            stripped = line.lstrip()
            
            if not stripped:
                # 空行
                result.append('')
                continue
            
            # 检查是否减少缩进(右大括号)
            if stripped.startswith('}'):
                indent_level = max(0, indent_level - 1)
            
            # 添加缩进
            indent = self.indent_char * (self.indent_size * indent_level)
            result.append(indent + stripped)
            
            # 检查是否增加缩进(左大括号)
            if stripped.endswith('{'):
                indent_level += 1
        
        return result
    
    def _add_blank_lines(self, lines: List[str]) -> List[str]:
        """
        添加空行
        
        Args:
            lines: 代码行列表
            
        Returns:
            处理后的代码行列表
        """
        result = []
        
        for i, line in enumerate(lines):
            result.append(line)
            
            # 在函数定义后添加空行
            if line.strip().startswith('函数') and line.strip().endswith('{'):
                if i + 1 < len(lines) and lines[i + 1].strip():
                    result.append('')
            
            # 在右大括号后添加空行(如果不是最后一个)
            if line.strip() == '}' and i + 1 < len(lines):
                next_line = lines[i + 1].strip()
                if next_line and not next_line.startswith('}'):
                    result.append('')
        
        return result
    
    def _format_operators(self, lines: List[str]) -> List[str]:
        """
        格式化运算符周围的空格
        
        Args:
            lines: 代码行列表
            
        Returns:
            处理后的代码行列表
        """
        operators = ['+', '-', '*', '/', '%', '=', '<', '>', '且', '或']
        
        result = []
        
        for line in lines:
            stripped = line.lstrip()
            indent = line[:len(line) - len(stripped)]
            
            # 跳过字符串内的内容
            if '"' in stripped or "'" in stripped:
                result.append(line)
                continue
            
            # 格式化运算符
            for op in operators:
                # 确保运算符两边有空格
                pattern = rf'(\S)\s*{re.escape(op)}\s*(\S)'
                replacement = rf'\1 {op} \2'
                stripped = re.sub(pattern, replacement, stripped)
            
            result.append(indent + stripped)
        
        return result
    
    def _format_commas(self, lines: List[str]) -> List[str]:
        """
        格式化逗号后的空格
        
        Args:
            lines: 代码行列表
            
        Returns:
            处理后的代码行列表
        """
        result = []
        
        for line in lines:
            stripped = line.lstrip()
            indent = line[:len(line) - len(stripped)]
            
            # 跳过字符串内的内容
            if '"' in stripped or "'" in stripped:
                result.append(line)
                continue
            
            # 确保逗号后有空格
            stripped = re.sub(r',\s*', ', ', stripped)
            
            result.append(indent + stripped)
        
        return result
    
    def format_file(self, file_path: str) -> str:
        """
        格式化文件
        
        Args:
            file_path: 文件路径
            
        Returns:
            格式化后的代码
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            code = f.read()
        
        return self.format(code)
    
    def check_format(self, code: str) -> Tuple[bool, List[Tuple[int, str, str]]]:
        """
        检查代码格式
        
        Args:
            code: 原始代码
            
        Returns:
            (是否格式正确, 差异列表)
        """
        formatted = self.format(code)
        
        if code == formatted:
            return True, []
        
        # 找出差异
        original_lines = code.split('\n')
        formatted_lines = formatted.split('\n')
        
        differences = []
        
        for i, (orig, fmt) in enumerate(zip(original_lines, formatted_lines)):
            if orig != fmt:
                differences.append((i + 1, orig, fmt))
        
        return False, differences


# 全局格式化器实例
_global_formatter: Optional[CodeFormatter] = None


def get_global_formatter() -> CodeFormatter:
    """获取全局格式化器"""
    global _global_formatter
    if _global_formatter is None:
        _global_formatter = CodeFormatter()
    return _global_formatter


def format_code(code: str) -> str:
    """
    格式化代码(便捷函数)
    
    Args:
        code: 原始代码
        
    Returns:
        格式化后的代码
    """
    return get_global_formatter().format(code)
