"""
简化的言律语言词法分析器

用于测试分词器集成
"""

import re
import jieba
from typing import List, Literal
from .token import Token, TokenType
from .verb_categories import VERB_ARITY, get_verb_category, get_verb_arity


class YanLuLexerSimple:
    """简化的言律语言词法分析器"""
    
    def __init__(self, segmenter: Literal["jieba", "thulac"] = "jieba"):
        """
        初始化词法分析器
        
        Args:
            segmenter: 分词器类型，可选 "jieba" 或 "thulac"
        """
        self.segmenter_type = segmenter
        self.segmenter = None
        self._init_segmenter()
        
        # 中文标点符号
        self.chinese_punctuation = {
            '。': TokenType.PERIOD,
            '，': TokenType.COMMA,
            '；': TokenType.SEMICOLON,
            '：': TokenType.COLON,
            '、': TokenType.ENUMERATION,
            '！': TokenType.EXCLAMATION,
            '？': TokenType.QUESTION,
        }
        
        # 关键词
        self.keywords = {
            '如果': TokenType.IF,
            '否则': TokenType.ELSE,
            '当': TokenType.WHEN,
            '就': TokenType.THEN,
            '对于': TokenType.FOR,
            '在': TokenType.IN,
            '一直': TokenType.WHILE,
            '定': TokenType.DEF,
            '定义': TokenType.DEF,
            '设': TokenType.SET,
            '是': TokenType.IS,
            '等于': TokenType.IS,
            '返回': TokenType.RETURN,
        }
        
        # 编译正则表达式
        self.number_pattern = re.compile(r'^\d+(\.\d+)?$')
        self.identifier_pattern = re.compile(r'^[\u4e00-\u9fffA-Za-z_][\u4e00-\u9fffA-Za-z0-9_]*$')
    
    def _init_segmenter(self):
        """初始化分词器"""
        if self.segmenter_type == "thulac":
            try:
                import thulac
                # 使用seg_only=True只进行分词，不进行词性标注
                self.segmenter = thulac.thulac(seg_only=True, model_path=None)
                print(f"使用THULAC分词器 (seg_only模式)")
            except ImportError:
                print("警告: 未安装THULAC，回退到jieba分词器")
                print("安装命令: pip install thulac")
                self.segmenter_type = "jieba"
                self.segmenter = jieba
        else:
            # 默认使用jieba
            self.segmenter = jieba
            print(f"使用jieba分词器")
    
    def _segment(self, text: str) -> List[str]:
        """
        分词方法
        
        Args:
            text: 待分词的文本
            
        Returns:
            分词结果列表
        """
        if self.segmenter_type == "thulac":
            # THULAC分词
            result = self.segmenter.cut(text, text=True)
            return result.split()
        else:
            # jieba分词
            return list(self.segmenter.lcut(text))
    
    def tokenize(self, source_code: str) -> List[Token]:
        """
        将源代码转换为词法单元列表
        
        Args:
            source_code: 源代码字符串
            
        Returns:
            词法单元列表
        """
        tokens = []
        position = 0
        line_num = 1
        column = 1
        
        # 使用分词器进行中文分词
        segments = self._segment(source_code)
        segment_index = 0
        
        while position < len(source_code):
            # 跳过空白字符
            if source_code[position].isspace():
                if source_code[position] == '\n':
                    tokens.append(Token(TokenType.NEWLINE, '\n', line_num, column, '\n'))
                    line_num += 1
                    column = 1
                else:
                    column += 1
                position += 1
                continue
            
            # 处理标点符号
            current_char = source_code[position]
            if current_char in self.chinese_punctuation:
                token_type = self.chinese_punctuation[current_char]
                tokens.append(Token(token_type, current_char, line_num, column, current_char))
                position += 1
                column += 1
                continue
            
            # 处理分词结果
            if segment_index < len(segments):
                segment = segments[segment_index]
                segment_index += 1
                
                # 检查是否为关键词
                if segment in self.keywords:
                    token_type = self.keywords[segment]
                # 检查是否为动词
                elif segment in VERB_ARITY:
                    token_type = TokenType.VERB
                # 检查是否为数字
                elif self.number_pattern.match(segment):
                    token_type = TokenType.NUMBER
                # 默认识别符
                else:
                    token_type = TokenType.IDENTIFIER
                
                tokens.append(Token(token_type, segment, line_num, column, segment))
                position += len(segment)
                column += len(segment)
            else:
                # 如果没有更多分词，跳过字符
                position += 1
                column += 1
        
        # 添加文件结束标记
        tokens.append(Token(TokenType.EOF, '', line_num, column, ''))
        
        return tokens