"""
言律语言词法分析器 - 词元匹配器模块

包含词元匹配器，用于识别和匹配不同类型的词元
"""

import re
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, Set, Pattern
from .lexer_token import Token, TokenType
from .constants import (
    CHINESE_PUNCTUATION, OPERATORS, GROUPING_SYMBOLS, KEYWORDS,
    CHINESE_NUMBERS, BAI_JIA_XING, CONFLICT_SURNAMES,
    NUMBER_PATTERN, IDENTIFIER_PATTERN, STRING_PATTERN,
    COMMENT_PATTERN, CHINESE_NUMBER_PATTERN
)


class ITokenMatcher(ABC):
    """词元匹配器接口"""
    
    @abstractmethod
    def match_token(self, segment: str, position: int, line_num: int, column: int) -> Optional[Token]:
        """
        匹配词元类型
        
        Args:
            segment: 分词片段
            position: 在行中的位置
            line_num: 行号
            column: 列号
            
        Returns:
            词元对象，如果无法匹配则返回None
        """
        pass
    
    @abstractmethod
    def get_token_type(self, segment: str) -> TokenType:
        """
        获取词元类型
        
        Args:
            segment: 分词片段
            
        Returns:
            词元类型
        """
        pass
    
    @abstractmethod
    def is_chinese_character(self, char: str) -> bool:
        """检查字符是否为中文字符"""
        pass
    
    @abstractmethod
    def is_chinese_punctuation(self, char: str) -> bool:
        """检查字符是否为中文标点"""
        pass
    
    @abstractmethod
    def is_operator(self, char: str) -> bool:
        """检查字符是否为运算符"""
        pass
    
    @abstractmethod
    def is_grouping_symbol(self, char: str) -> bool:
        """检查字符是否为分组符号"""
        pass
    
    @abstractmethod
    def is_keyword(self, word: str) -> bool:
        """检查单词是否为关键词"""
        pass
    
    @abstractmethod
    def is_bai_jia_xing(self, word: str) -> bool:
        """检查单词是否为百家姓"""
        pass
    
    @abstractmethod
    def is_conflict_surname(self, word: str) -> bool:
        """检查单词是否为冲突姓氏"""
        pass


class TokenMatcher(ITokenMatcher):
    """词元匹配器实现"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        初始化词元匹配器
        
        Args:
            config: 配置字典
        """
        self.config = config or {}
        self._init_patterns()
        self._init_dictionaries()
        
        # 性能统计
        self.stats = {
            'matches_attempted': 0,
            'matches_successful': 0,
            'cache_hits': 0,
            'cache_misses': 0,
        }
        
        # 缓存
        self._cache = {}
        self._cache_enabled = self.config.get('enable_cache', True)
        self._cache_size = self.config.get('cache_size', 1000)
    
    def _init_patterns(self):
        """初始化正则表达式模式"""
        # 编译正则表达式
        self.number_pattern = re.compile(NUMBER_PATTERN)
        self.identifier_pattern = re.compile(IDENTIFIER_PATTERN)
        self.string_pattern = re.compile(STRING_PATTERN)
        self.comment_pattern = re.compile(COMMENT_PATTERN)
        self.chinese_number_pattern = re.compile(CHINESE_NUMBER_PATTERN)
        
        # 动词模式（从verb_categories导入）
        self.verb_patterns = {}
        try:
            from verb_categories import VERB_ARITY
            self.verb_arity = VERB_ARITY
        except ImportError:
            self.verb_arity = {}
    
    def _init_dictionaries(self):
        """初始化字典"""
        # 从constants导入
        self.chinese_punctuation = CHINESE_PUNCTUATION
        self.operators = OPERATORS
        self.grouping_symbols = GROUPING_SYMBOLS
        self.keywords = KEYWORDS
        self.chinese_numbers = CHINESE_NUMBERS
        self.bai_jia_xing = BAI_JIA_XING
        self.conflict_surnames = CONFLICT_SURNAMES
    
    def match_token(self, segment: str, position: int, line_num: int, column: int) -> Optional[Token]:
        """
        匹配词元类型
        
        Args:
            segment: 分词片段
            position: 在行中的位置
            line_num: 行号
            column: 列号
            
        Returns:
            词元对象，如果无法匹配则返回None
        """
        self.stats['matches_attempted'] += 1
        
        # 检查缓存
        cache_key = segment
        if self._cache_enabled and cache_key in self._cache:
            token_type = self._cache[cache_key]
            self.stats['cache_hits'] += 1
            self.stats['matches_successful'] += 1
            return Token(token_type, segment, line_num, column, segment)
        
        # 匹配词元类型
        token_type = self._match_token_type(segment)
        
        if token_type:
            # 更新缓存
            if self._cache_enabled:
                self._cache[cache_key] = token_type
                # 检查缓存大小
                if len(self._cache) > self._cache_size:
                    self._clean_cache()
            
            self.stats['cache_misses'] += 1
            self.stats['matches_successful'] += 1
            return Token(token_type, segment, line_num, column, segment)
        
        return None
    
    def _match_token_type(self, segment: str) -> Optional[TokenType]:
        """
        匹配词元类型（内部方法）
        
        Args:
            segment: 分词片段
            
        Returns:
            词元类型，如果无法匹配则返回None
        """
        # 空字符串
        if not segment:
            return None
        
        # 单个字符匹配
        if len(segment) == 1:
            char = segment
            
            # 中文标点
            if char in self.chinese_punctuation:
                return self.chinese_punctuation[char]
            
            # 运算符
            if char in self.operators:
                return self.operators[char]
            
            # 分组符号
            if char in self.grouping_symbols:
                return self.grouping_symbols[char]
        
        # 数字
        if self.number_pattern.match(segment):
            return TokenType.NUMBER
        
        # 中文数字
        if self.chinese_number_pattern.match(segment):
            return TokenType.NUMBER
        
        # 字符串字面量
        if self.string_pattern.match(segment):
            return TokenType.STRING
        
        # 注释
        if self.comment_pattern.match(segment):
            return TokenType.COMMENT
        
        # 关键词
        if segment in self.keywords:
            return self.keywords[segment]
        
        # 动词（从verb_categories检查）
        if segment in self.verb_arity:
            return TokenType.VERB
        
        # 标识符
        if self.identifier_pattern.match(segment):
            # 检查是否为百家姓（不能作为变量名）
            if segment in self.bai_jia_xing and segment not in self.conflict_surnames:
                return TokenType.IDENTIFIER
            elif segment in self.conflict_surnames:
                # 冲突姓氏，需要特殊处理
                return None
            else:
                return TokenType.IDENTIFIER
        
        # 布尔值
        if segment in ['真', '假', 'true', 'false', 'True', 'False']:
            return TokenType.BOOLEAN
        
        return None
    
    def get_token_type(self, segment: str) -> TokenType:
        """
        获取词元类型
        
        Args:
            segment: 分词片段
            
        Returns:
            词元类型，如果无法识别则返回TokenType.IDENTIFIER
        """
        token_type = self._match_token_type(segment)
        if token_type:
            return token_type
        else:
            # 默认返回标识符
            return TokenType.IDENTIFIER
    
    def is_chinese_character(self, char: str) -> bool:
        """检查字符是否为中文字符"""
        return '\u4e00' <= char <= '\u9fff'
    
    def is_chinese_punctuation(self, char: str) -> bool:
        """检查字符是否为中文标点"""
        return char in self.chinese_punctuation
    
    def is_operator(self, char: str) -> bool:
        """检查字符是否为运算符"""
        return char in self.operators
    
    def is_grouping_symbol(self, char: str) -> bool:
        """检查字符是否为分组符号"""
        return char in self.grouping_symbols
    
    def is_keyword(self, word: str) -> bool:
        """检查单词是否为关键词"""
        return word in self.keywords
    
    def is_bai_jia_xing(self, word: str) -> bool:
        """检查单词是否为百家姓"""
        return word in self.bai_jia_xing
    
    def is_conflict_surname(self, word: str) -> bool:
        """检查单词是否为冲突姓氏"""
        return word in self.conflict_surnames
    
    def _clean_cache(self):
        """清理缓存，保留最近使用的项"""
        if len(self._cache) > self._cache_size:
            # 简单实现：清除一半缓存
            items = list(self._cache.items())
            items_to_remove = items[:len(items) // 2]
            for key, _ in items_to_remove:
                del self._cache[key]
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        获取性能统计信息
        
        Returns:
            统计信息字典
        """
        stats = self.stats.copy()
        stats['cache_size'] = len(self._cache)
        stats['cache_enabled'] = self._cache_enabled
        stats['cache_hit_rate'] = (
            stats['cache_hits'] / max(stats['matches_attempted'], 1)
        ) if stats['matches_attempted'] > 0 else 0.0
        return stats
    
    def reset_statistics(self):
        """重置性能统计"""
        self.stats = {
            'matches_attempted': 0,
            'matches_successful': 0,
            'cache_hits': 0,
            'cache_misses': 0,
        }
    
    def clear_cache(self):
        """清空缓存"""
        self._cache.clear()
    
    def update_config(self, **kwargs):
        """更新配置"""
        self.config.update(kwargs)
        
        # 更新缓存设置
        if 'enable_cache' in kwargs:
            self._cache_enabled = kwargs['enable_cache']
        if 'cache_size' in kwargs:
            self._cache_size = kwargs['cache_size']
            # 如果缓存大小减小，清理缓存
            if len(self._cache) > self._cache_size:
                self._clean_cache()
    
    def __str__(self) -> str:
        """返回匹配器描述"""
        stats = self.get_statistics()
        return (
            f"TokenMatcher("
            f"matches={stats['matches_attempted']}, "
            f"success_rate={stats['matches_successful']/max(stats['matches_attempted'], 1):.2f}, "
            f"cache_hit_rate={stats['cache_hit_rate']:.2f}"
            f")"
        )
    
    def __repr__(self) -> str:
        """返回匹配器表示"""
        return self.__str__()


class AdvancedTokenMatcher(TokenMatcher):
    """高级词元匹配器，支持更多特性"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        初始化高级词元匹配器
        
        Args:
            config: 配置字典
        """
        super().__init__(config)
        self._init_advanced_patterns()
        
        # 自定义词元类型映射
        self.custom_token_types = {}
        
        # 自定义验证函数
        self.custom_validators = []
    
    def _init_advanced_patterns(self):
        """初始化高级正则表达式模式"""
        # 浮点数模式（科学计数法）
        self.float_pattern = re.compile(r'^\d+\.\d+([eE][+-]?\d+)?$')
        
        # 十六进制数模式
        self.hex_pattern = re.compile(r'^0[xX][0-9a-fA-F]+$')
        
        # 二进制数模式
        self.binary_pattern = re.compile(r'^0[bB][01]+$')
        
        # 八进制数模式
        self.octal_pattern = re.compile(r'^0[oO][0-7]+$')
        
        # 日期模式
        self.date_pattern = re.compile(r'^\d{4}-\d{2}-\d{2}$')
        
        # 时间模式
        self.time_pattern = re.compile(r'^\d{2}:\d{2}:\d{2}(\.\d+)?$')
        
        # 日期时间模式
        self.datetime_pattern = re.compile(r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}(\.\d+)?$')
    
    def _match_token_type(self, segment: str) -> Optional[TokenType]:
        """
        匹配词元类型（重写以支持更多类型）
        
        Args:
            segment: 分词片段
            
        Returns:
            词元类型，如果无法匹配则返回None
        """
        # 首先尝试父类的匹配
        token_type = super()._match_token_type(segment)
        if token_type:
            return token_type
        
        # 尝试高级匹配
        if self.float_pattern.match(segment):
            return TokenType.NUMBER
        
        if self.hex_pattern.match(segment):
            return TokenType.NUMBER
        
        if self.binary_pattern.match(segment):
            return TokenType.NUMBER
        
        if self.octal_pattern.match(segment):
            return TokenType.NUMBER
        
        if self.date_pattern.match(segment):
            return TokenType.STRING
        
        if self.time_pattern.match(segment):
            return TokenType.STRING
        
        if self.datetime_pattern.match(segment):
            return TokenType.STRING
        
        # 尝试自定义词元类型
        if segment in self.custom_token_types:
            return self.custom_token_types[segment]
        
        # 尝试自定义验证函数
        for validator in self.custom_validators:
            result = validator(segment)
            if result:
                return result
        
        return None
    
    def add_custom_token_type(self, pattern: str, token_type: TokenType):
        """
        添加自定义词元类型
        
        Args:
            pattern: 正则表达式模式
            token_type: 词元类型
        """
        try:
            compiled_pattern = re.compile(pattern)
            # 这里简化处理，实际应该存储模式并进行匹配
            # 为了简单起见，我们只存储字符串模式
            self.custom_token_types[pattern] = token_type
        except re.error as e:
            raise ValueError(f"无效的正则表达式模式: {pattern}") from e
    
    def add_custom_validator(self, validator):
        """
        添加自定义验证函数
        
        Args:
            validator: 验证函数，接受字符串参数，返回TokenType或None
        """
        self.custom_validators.append(validator)
    
    def remove_custom_validator(self, validator):
        """移除自定义验证函数"""
        if validator in self.custom_validators:
            self.custom_validators.remove(validator)


# 工厂函数
def create_token_matcher(config: Optional[Dict[str, Any]] = None, advanced: bool = False) -> ITokenMatcher:
    """
    创建词元匹配器
    
    Args:
        config: 配置字典
        advanced: 是否使用高级匹配器
        
    Returns:
        词元匹配器实例
    """
    if advanced:
        return AdvancedTokenMatcher(config)
    else:
        return TokenMatcher(config)


def get_default_token_matcher() -> ITokenMatcher:
    """
    获取默认词元匹配器
    
    Returns:
        默认词元匹配器实例
    """
    return TokenMatcher()


def get_advanced_token_matcher() -> ITokenMatcher:
    """
    获取高级词元匹配器
    
    Returns:
        高级词元匹配器实例
    """
    return AdvancedTokenMatcher()