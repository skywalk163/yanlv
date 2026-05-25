"""
言律语言语句结束处理器

实现混合模式的语句结束策略：
- 句号 。：强制语句结束
- 换行 \\n：
  - 如果下一行缩进 > 当前行：进入子块
  - 如果下一行缩进 < 当前行：退出当前块
  - 如果下一行缩进 == 当前行：
    - 如果当前行以句号结尾：开始新语句
    - 如果当前行不以句号结尾：视为续行（拼接两行）
"""

from typing import List, Tuple
import re


class StatementProcessor:
    """语句结束处理器"""

    def __init__(self):
        """初始化处理器"""
        self.period = '。'  # 中文句号
        self.indent_pattern = re.compile(r'^(\s*)')  # 缩进模式

    def process_source(self, source_code: str) -> str:
        """
        处理源代码，应用混合模式的语句结束策略

        Args:
            source_code: 原始源代码

        Returns:
            处理后的源代码
        """
        lines = source_code.split('\n')
        processed_lines = []

        i = 0
        while i < len(lines):
            current_line = lines[i]
            current_indent = self._get_indent(current_line)
            current_stripped = current_line.strip()

            # 空行直接保留
            if not current_stripped:
                processed_lines.append(current_line)
                i += 1
                continue

            # 检查是否以句号结尾
            ends_with_period = current_stripped.endswith(self.period)

            # 检查下一行
            if i + 1 < len(lines):
                next_line = lines[i + 1]
                next_indent = self._get_indent(next_line)
                next_stripped = next_line.strip()

                # 如果下一行是空行，当前行结束
                if not next_stripped:
                    processed_lines.append(current_line)
                    i += 1
                    continue

                # 缩进比较
                if len(next_indent) > len(current_indent):
                    # 进入子块，当前行结束
                    processed_lines.append(current_line)
                    i += 1
                elif len(next_indent) < len(current_indent):
                    # 退出当前块，当前行结束
                    processed_lines.append(current_line)
                    i += 1
                else:
                    # 缩进相同
                    if ends_with_period:
                        # 当前语句结束，开始新语句
                        processed_lines.append(current_line)
                        i += 1
                    else:
                        # 续行：拼接当前行和下一行
                        # 移除当前行末尾的空白，添加空格，然后拼接下一行
                        merged_line = current_line.rstrip() + ' ' + next_stripped
                        # 用合并后的行替换当前行，跳过下一行
                        lines[i] = merged_line
                        # 不增加i，继续处理合并后的行
                        continue
            else:
                # 最后一行，直接添加
                processed_lines.append(current_line)
                i += 1

        return '\n'.join(processed_lines)

    def _get_indent(self, line: str) -> str:
        """
        获取行的缩进

        Args:
            line: 代码行

        Returns:
            缩进字符串
        """
        match = self.indent_pattern.match(line)
        return match.group(1) if match else ''

    def process_lines(self, lines: List[str]) -> List[str]:
        """
        处理多行代码

        Args:
            lines: 代码行列表

        Returns:
            处理后的代码行列表
        """
        source_code = '\n'.join(lines)
        processed_code = self.process_source(source_code)
        return processed_code.split('\n')


def create_statement_processor() -> StatementProcessor:
    """创建语句处理器实例"""
    return StatementProcessor()
