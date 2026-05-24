"""
言律语言专用分词器 - 支持无空格编程
"""
import re
from typing import List, Tuple, Optional
from .constants import KEYWORDS


class YanLuNoSpaceTokenizer:
    """言律语言无空格分词器"""

    def __init__(self):
        """初始化分词器"""
        # 按长度排序关键词（长的优先匹配）
        self.keywords = sorted(KEYWORDS.keys(), key=len, reverse=True)
        # 字符串模式
        self.string_pattern = re.compile(r'"[^"]*"|\'[^\']*\'')
        # 数字模式
        self.number_pattern = re.compile(r'\d+\.?\d*')

    def segment(self, text: str) -> List[str]:
        """
        分词无空格的言律语言代码

        Args:
            text: 输入文本

        Returns:
            分词结果列表
        """
        segments = []
        i = 0
        n = len(text)

        while i < n:
            # 跳过空白字符
            if text[i].isspace():
                i += 1
                continue

            # 1. 尝试匹配字符串字面量
            if text[i] in ('"', "'"):
                quote = text[i]
                j = i + 1
                while j < n and text[j] != quote:
                    j += 1
                if j < n:
                    segments.append(text[i:j+1])
                    i = j + 1
                    continue

            # 2. 尝试匹配数字
            if text[i].isdigit():
                j = i
                while j < n and (text[j].isdigit() or text[j] == '.'):
                    j += 1
                segments.append(text[i:j])
                i = j
                continue

            # 3. 尝试匹配关键词（优先匹配长的）
            matched = False
            for keyword in self.keywords:
                if text[i:i+len(keyword)] == keyword:
                    segments.append(keyword)
                    i += len(keyword)
                    matched = True
                    break

            if matched:
                continue

            # 4. 尝试匹配标识符（中文字符或英文字母）
            if self._is_identifier_char(text[i]):
                j = i
                while j < n and self._is_identifier_char(text[j]):
                    # 检查是否遇到关键词
                    found_keyword = False
                    for keyword in self.keywords:
                        if text[j:j+len(keyword)] == keyword:
                            found_keyword = True
                            break
                    if found_keyword:
                        break
                    j += 1

                if j > i:
                    segments.append(text[i:j])
                    i = j
                    continue

            # 5. 其他字符（运算符、标点等）
            segments.append(text[i])
            i += 1

        return segments

    def _is_identifier_char(self, char: str) -> bool:
        """检查字符是否可以作为标识符的一部分"""
        # 中文字符
        if '\u4e00' <= char <= '\u9fff':
            return True
        # 英文字母和下划线
        if char.isalpha() or char == '_':
            return True
        return False

    def segment_with_positions(self, text: str) -> List[Tuple[str, int, int]]:
        """
        分词并返回位置信息

        Args:
            text: 输入文本

        Returns:
            (segment, start, end) 元组列表
        """
        segments = self.segment(text)
        result = []
        pos = 0

        for seg in segments:
            # 找到segment在text中的位置
            start = text.find(seg, pos)
            if start != -1:
                end = start + len(seg)
                result.append((seg, start, end))
                pos = end

        return result


def create_yanlv_tokenizer():
    """创建言律语言分词器"""
    return YanLuNoSpaceTokenizer()
