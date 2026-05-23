"""
言律语言词法分析器 - 基础模块

包含基础抽象类和主词法分析器类
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Tuple, Dict, Any, Literal
import re
import jieba
from .lexer_token import Token, TokenType


class ILexer(ABC):
    """词法分析器接口"""
    
    @abstractmethod
    def tokenize(self, source_code: str) -> List[Token]:
        """将源代码转换为词法单元列表"""
        pass
    
    @abstractmethod
    def tokenize_line(self, line: str, line_num: int) -> List[Token]:
        """将一行源代码转换为词法单元列表"""
        pass


class ITokenizer(ABC):
    """分词器接口"""
    
    @abstractmethod
    def segment(self, text: str) -> List[str]:
        """将文本分词为片段列表"""
        pass
    
    @abstractmethod
    def get_segmenter_type(self) -> str:
        """获取分词器类型"""
        pass


class ITokenMatcher(ABC):
    """词元匹配器接口"""
    
    @abstractmethod
    def match_token(self, segment: str, position: int, line_num: int, column: int) -> Optional[Token]:
        """匹配词元类型"""
        pass
    
    @abstractmethod
    def get_token_type(self, segment: str) -> TokenType:
        """获取词元类型"""
        pass


class YanLuLexerBase(ILexer):
    """言律语言词法分析器基类"""
    
    def __init__(self, segmenter: Literal["jieba", "thulac"] = "jieba"):
        """
        初始化词法分析器
        
        Args:
            segmenter: 分词器类型，可选 "jieba" 或 "thulac"
        """
        self.segmenter_type = segmenter
        self.segmenter = None
        self._init_segmenter()
        
        # 初始化模式匹配器
        self._init_patterns()
        
        # 初始化字典和配置
        self._init_dictionaries()
        
        # 性能统计
        self.stats = {
            'tokens_processed': 0,
            'lines_processed': 0,
            'errors': 0,
            'warnings': 0
        }
    
    def _init_segmenter(self):
        """初始化分词器 - 由子类实现"""
        raise NotImplementedError("子类必须实现_init_segmenter方法")
    
    def _init_patterns(self):
        """初始化正则表达式模式 - 由子类实现"""
        raise NotImplementedError("子类必须实现_init_patterns方法")
    
    def _init_dictionaries(self):
        """初始化字典配置 - 由子类实现"""
        raise NotImplementedError("子类必须实现_init_dictionaries方法")
    
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
            line_tokens = self.tokenize_line(line, line_num)
            tokens.extend(line_tokens)
            
            # 添加换行符（除非是最后一行）
            if line_num < len(lines):
                tokens.append(Token(TokenType.NEWLINE, '\n', line_num, len(line) + 1, '\n'))
        
        # 添加文件结束标记
        tokens.append(Token(TokenType.EOF, '', len(lines) + 1, 1, ''))
        
        # 更新统计
        self.stats['lines_processed'] += len(lines)
        self.stats['tokens_processed'] += len(tokens)
        
        return tokens
    
    def tokenize_line(self, line: str, line_num: int) -> List[Token]:
        """
        将一行源代码转换为词法单元列表
        
        Args:
            line: 源代码行
            line_num: 行号
            
        Returns:
            词法单元列表
        """
        raise NotImplementedError("子类必须实现tokenize_line方法")
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        获取性能统计信息
        
        Returns:
            统计信息字典
        """
        return self.stats.copy()
    
    def reset_statistics(self):
        """重置性能统计"""
        self.stats = {
            'tokens_processed': 0,
            'lines_processed': 0,
            'errors': 0,
            'warnings': 0
        }
    
    def __str__(self) -> str:
        """返回词法分析器描述"""
        return f"YanLuLexerBase(segmenter={self.segmenter_type}, stats={self.stats})"
    
    def __repr__(self) -> str:
        """返回词法分析器表示"""
        return self.__str__()


# YanLuLexer类已移动到lexer_new.py中
# 这里只保留基类和接口定义