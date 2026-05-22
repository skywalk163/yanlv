"""
言律语言词法分析器 - 清理版本

支持jieba和THULAC两种中文分词器，实现元数驱动解析
"""

import re
import jieba
from typing import List, Literal
from .token import Token, TokenType
from .verb_categories import VERB_ARITY, get_verb_category, get_verb_arity


class YanLuLexerClean:
    """言律语言词法分析器（清理版本）"""
    
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
            '《': TokenType.BOOK_TITLE,
            '》': TokenType.BOOK_TITLE,
            '……': TokenType.ELLIPSIS,
            '——': TokenType.DASH,
            '～': TokenType.TILDE,
            '·': TokenType.MIDDLE_DOT,
            '【': TokenType.SQUARE_BRACKETS,
            '】': TokenType.SQUARE_BRACKETS,
        }
        
        # 中文数字
        self.chinese_numbers = {
            '零': 0, '〇': 0, '一': 1, '二': 2, '三': 3, '四': 4,
            '五': 5, '六': 6, '七': 7, '八': 8, '九': 9,
            '十': 10, '百': 100, '千': 1000, '万': 10000,
            '亿': 100000000,
        }
        
        # 关键词
        self.keywords = {
            '如果': TokenType.IF,
            '要是': TokenType.IF,
            '否则': TokenType.ELSE,
            '不然': TokenType.ELSE,
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
            '结束': TokenType.END,
            '循环': TokenType.LOOP,
            '遍历': TokenType.FOR_EACH,
            '每个': TokenType.FOR_EACH,
            '直到': TokenType.UNTIL,
            '否则如果': TokenType.ELIF,
            '否则要是': TokenType.ELIF,
        }
        
        # 运算符
        self.operators = {
            '+': TokenType.PLUS,
            '-': TokenType.MINUS,
            '*': TokenType.MULTIPLY,
            '/': TokenType.DIVIDE,
            '%': TokenType.MODULO,
            '^': TokenType.POWER,
            '=': TokenType.EQUAL,
            '≠': TokenType.NOT_EQUAL,
            '<': TokenType.LESS,
            '>': TokenType.GREATER,
            '≤': TokenType.LESS_EQUAL,
            '≥': TokenType.GREATER_EQUAL,
            '且': TokenType.AND,
            '或': TokenType.OR,
            '¬': TokenType.NOT,
        }
        
        # 分组符号
        self.grouping_symbols = {
            '(': TokenType.LPAREN,
            ')': TokenType.RPAREN,
            '[': TokenType.LBRACKET,
            ']': TokenType.RBRACKET,
            '{': TokenType.LBRACE,
            '}': TokenType.RBRACE,
        }
        
        # 百家姓（前20个）
        self.bai_jia_xing = {
            '赵', '钱', '孙', '李', '周', '吴', '郑', '王', '冯', '陈',
            '褚', '卫', '蒋', '沈', '韩', '杨', '朱', '秦', '尤', '许'
        }
        
        # 冲突姓氏（不能作为变量名）
        self.conflict_surnames = {'空', '言', '印'}
        
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
                print("使用THULAC分词器 (seg_only模式)")
            except ImportError:
                print("警告: 未安装THULAC，回退到jieba分词器")
                print("安装命令: pip install thulac")
                self.segmenter_type = "jieba"
                self.segmenter = jieba
        else:
            # 默认使用jieba
            self.segmenter = jieba
            print("使用jieba分词器")
    
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
        lines = source_code.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            line_tokens = self._tokenize_line(line, line_num)
            tokens.extend(line_tokens)
            
            # 添加换行符（除非是最后一行）
            if line_num < len(lines):
                tokens.append(Token(TokenType.NEWLINE, '\n', line_num, len(line) + 1, '\n'))
        
        # 添加文件结束标记
        tokens.append(Token(TokenType.EOF, '', len(lines) + 1, 1, ''))
        
        return tokens
    
    def _tokenize_line(self, line: str, line_num: int) -> List[Token]:
        """
        将一行源代码转换为词法单元列表
        
        Args:
            line: 源代码行
            line_num: 行号
            
        Returns:
            词法单元列表
        """
        tokens = []
        position = 0
        column = 1
        
        # 使用分词器进行中文分词
        segments = self._segment(line)
        segment_index = 0
        
        while position < len(line):
            # 跳过空白字符
            if line[position].isspace():
                if line[position] == '\n':
                    tokens.append(Token(TokenType.NEWLINE, '\n', line_num, column, '\n'))
                position += 1
                column += 1
                continue
            
            # 处理标点符号
            current_char = line[position]
            if current_char in self.chinese_punctuation:
                token_type = self.chinese_punctuation[current_char]
                tokens.append(Token(token_type, current_char, line_num, column, current_char))
                position += 1
                column += 1
                continue
            
            # 处理运算符
            if current_char in self.operators:
                token_type = self.operators[current_char]
                tokens.append(Token(token_type, current_char, line_num, column, current_char))
                position += 1
                column += 1
                continue
            
            # 处理分组符号
            if current_char in self.grouping_symbols:
                token_type = self.grouping_symbols[current_char]
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
                # 检查是否为中文数字
                elif segment in self.chinese_numbers:
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
        
        return tokens


# 简化的测试函数
def test_lexer():
    """测试词法分析器"""
    lexer = YanLuLexerClean(segmenter="jieba")
    
    test_cases = [
        "温度变为30度。",
        "如果温度超过30度，就开启空调。",
        "张三、李四和王五，发送消息。",
        "加1和2。",
        "与真和假。",
    ]
    
    for test_case in test_cases:
        print(f"\n测试: {test_case}")
        tokens = lexer.tokenize(test_case)
        for token in tokens:
            print(f"  {token.type.name}: '{token.value}' (行{token.line}, 列{token.column})")


if __name__ == "__main__":
    print("言律语言词法分析器测试")
    print("=" * 60)
    test_lexer()