"""
言律语言词法分析器 - 模式管理器

管理正则表达式模式，支持动态添加和匹配
"""

import re
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Tuple, Pattern, Any, Callable
from dataclasses import dataclass, field
from enum import Enum
from .lexer_token import TokenType


class PatternType(Enum):
    """模式类型"""
    KEYWORD = "keyword"
    OPERATOR = "operator"
    PUNCTUATION = "punctuation"
    LITERAL = "literal"
    IDENTIFIER = "identifier"
    VERB = "verb"
    CUSTOM = "custom"


@dataclass
class PatternInfo:
    """模式信息"""
    name: str
    pattern: str
    compiled_pattern: Pattern
    token_type: TokenType
    pattern_type: PatternType
    priority: int = 0
    description: Optional[str] = None
    examples: List[str] = field(default_factory=list)
    
    def __str__(self) -> str:
        """返回模式信息字符串表示"""
        return f"PatternInfo(name={self.name}, type={self.pattern_type}, token={self.token_type})"


class IPatternManager(ABC):
    """模式管理器接口"""
    
    @abstractmethod
    def add_pattern(self, name: str, pattern: str, token_type: TokenType, 
                    pattern_type: PatternType = PatternType.CUSTOM,
                    priority: int = 0, description: Optional[str] = None,
                    examples: Optional[List[str]] = None) -> bool:
        """添加模式"""
        pass
    
    @abstractmethod
    def remove_pattern(self, name: str) -> bool:
        """移除模式"""
        pass
    
    @abstractmethod
    def get_pattern(self, name: str) -> Optional[PatternInfo]:
        """获取模式信息"""
        pass
    
    @abstractmethod
    def match(self, text: str) -> Optional[Tuple[TokenType, str]]:
        """匹配文本"""
        pass
    
    @abstractmethod
    def get_all_patterns(self) -> List[PatternInfo]:
        """获取所有模式"""
        pass
    
    @abstractmethod
    def clear_patterns(self):
        """清空所有模式"""
        pass
    
    @abstractmethod
    def get_pattern_count(self) -> int:
        """获取模式数量"""
        pass


class PatternManager(IPatternManager):
    """模式管理器实现"""
    
    def __init__(self):
        """初始化模式管理器"""
        self._patterns: Dict[str, PatternInfo] = {}
        self._pattern_cache: Dict[str, List[PatternInfo]] = {}
        self._sorted_patterns: List[PatternInfo] = []
        self._need_sort = True
        
        # 初始化内置模式
        self._init_builtin_patterns()
    
    def _init_builtin_patterns(self):
        """初始化内置模式"""
        # 数字模式
        self.add_pattern(
            name="number_integer",
            pattern=r"^\d+$",
            token_type=TokenType.NUMBER,
            pattern_type=PatternType.LITERAL,
            priority=100,
            description="整数",
            examples=["123", "456", "789"]
        )
        
        self.add_pattern(
            name="number_float",
            pattern=r"^\d+\.\d+$",
            token_type=TokenType.NUMBER,
            pattern_type=PatternType.LITERAL,
            priority=90,
            description="浮点数",
            examples=["3.14", "2.718", "0.5"]
        )
        
        # 字符串模式
        self.add_pattern(
            name="string_double_quote",
            pattern=r'^"[^"\\]*(?:\\.[^"\\]*)*"$',
            token_type=TokenType.STRING,
            pattern_type=PatternType.LITERAL,
            priority=100,
            description="双引号字符串",
            examples=['"hello"', '"world"']
        )
        
        # 标识符模式
        self.add_pattern(
            name="identifier",
            pattern=r"^[\u4e00-\u9fffA-Za-z_][\u4e00-\u9fffA-Za-z0-9_]*$",
            token_type=TokenType.IDENTIFIER,
            pattern_type=PatternType.IDENTIFIER,
            priority=50,
            description="标识符（支持中文）",
            examples=["变量", "myVar", "_private"]
        )
        
        # 注释模式
        self.add_pattern(
            name="comment_single_line",
            pattern=r"^#.*$",
            token_type=TokenType.COMMENT,
            pattern_type=PatternType.CUSTOM,
            priority=10,
            description="单行注释",
            examples=["# 这是一个注释", "# TODO: 需要实现"]
        )
        
        # 中文数字模式
        self.add_pattern(
            name="chinese_number",
            pattern=r"^[零〇一二三四五六七八九十百千万亿兆]+$",
            token_type=TokenType.NUMBER,
            pattern_type=PatternType.LITERAL,
            priority=70,
            description="中文数字",
            examples=["一百二十三", "五千六百", "七万八千九百"]
        )
    
    def add_pattern(self, name: str, pattern: str, token_type: TokenType, 
                    pattern_type: PatternType = PatternType.CUSTOM,
                    priority: int = 0, description: Optional[str] = None,
                    examples: Optional[List[str]] = None) -> bool:
        """添加模式"""
        # 检查名称是否已存在
        if name in self._patterns:
            return False
        
        try:
            # 编译正则表达式
            compiled_pattern = re.compile(pattern)
            
            # 创建模式信息
            pattern_info = PatternInfo(
                name=name,
                pattern=pattern,
                compiled_pattern=compiled_pattern,
                token_type=token_type,
                pattern_type=pattern_type,
                priority=priority,
                description=description,
                examples=examples or []
            )
            
            # 添加到模式字典
            self._patterns[name] = pattern_info
            
            # 清空缓存
            self._pattern_cache.clear()
            
            # 标记需要重新排序
            self._need_sort = True
            
            return True
            
        except re.error as e:
            raise ValueError(f"无效的正则表达式模式 '{pattern}': {e}")
    
    def remove_pattern(self, name: str) -> bool:
        """移除模式"""
        if name in self._patterns:
            del self._patterns[name]
            self._pattern_cache.clear()
            self._need_sort = True
            return True
        return False
    
    def get_pattern(self, name: str) -> Optional[PatternInfo]:
        """获取模式信息"""
        return self._patterns.get(name)
    
    def _ensure_sorted(self):
        """确保模式已按优先级排序"""
        if self._need_sort:
            self._sorted_patterns = sorted(
                self._patterns.values(),
                key=lambda p: (-p.priority, p.name)
            )
            self._need_sort = False
    
    def match(self, text: str) -> Optional[Tuple[TokenType, str]]:
        """匹配文本"""
        self._ensure_sorted()
        
        # 按优先级顺序尝试匹配
        for pattern_info in self._sorted_patterns:
            match = pattern_info.compiled_pattern.match(text)
            if match:
                return pattern_info.token_type, match.group()
        
        return None
    
    def find_all_matches(self, text: str) -> List[Tuple[TokenType, str, int, int]]:
        """查找所有匹配"""
        self._ensure_sorted()
        
        matches = []
        i = 0
        text_length = len(text)
        
        while i < text_length:
            best_match = None
            best_pattern = None
            
            # 查找最长的匹配
            for pattern_info in self._sorted_patterns:
                match = pattern_info.compiled_pattern.match(text, i)
                if match:
                    match_length = match.end() - match.start()
                    if best_match is None or match_length > (best_match.end() - best_match.start()):
                        best_match = match
                        best_pattern = pattern_info
            
            if best_match:
                matches.append((
                    best_pattern.token_type,
                    best_match.group(),
                    best_match.start(),
                    best_match.end()
                ))
                i = best_match.end()
            else:
                # 没有匹配，跳过当前字符
                i += 1
        
        return matches
    
    def get_patterns_by_type(self, pattern_type: PatternType) -> List[PatternInfo]:
        """按类型获取模式"""
        cache_key = f"type_{pattern_type.value}"
        if cache_key not in self._pattern_cache:
            patterns = [
                p for p in self._patterns.values()
                if p.pattern_type == pattern_type
            ]
            self._pattern_cache[cache_key] = patterns
        
        return self._pattern_cache[cache_key].copy()
    
    def get_all_patterns(self) -> List[PatternInfo]:
        """获取所有模式"""
        self._ensure_sorted()
        return self._sorted_patterns.copy()
    
    def clear_patterns(self):
        """清空所有模式"""
        self._patterns.clear()
        self._pattern_cache.clear()
        self._sorted_patterns.clear()
        self._need_sort = False
        
        # 重新初始化内置模式
        self._init_builtin_patterns()
    
    def get_pattern_count(self) -> int:
        """获取模式数量"""
        return len(self._patterns)
    
    def has_pattern(self, name: str) -> bool:
        """检查是否存在指定模式"""
        return name in self._patterns
    
    def __str__(self) -> str:
        """返回模式管理器描述"""
        self._ensure_sorted()
        return f"PatternManager(patterns={len(self._patterns)}, sorted={len(self._sorted_patterns)})"
    
    def __repr__(self) -> str:
        """返回模式管理器表示"""
        return self.__str__()


# 工厂函数
def create_pattern_manager() -> IPatternManager:
    """创建模式管理器"""
    return PatternManager()


def get_default_pattern_manager() -> IPatternManager:
    """获取默认模式管理器"""
    return PatternManager()


# 模式匹配工具函数
def match_pattern(text: str, pattern_manager: Optional[IPatternManager] = None) -> Optional[Tuple[TokenType, str]]:
    """使用模式管理器匹配文本"""
    if pattern_manager is None:
        pattern_manager = get_default_pattern_manager()
    
    return pattern_manager.match(text)


def find_all_patterns(text: str, pattern_manager: Optional[IPatternManager] = None) -> List[Tuple[TokenType, str, int, int]]:
    """使用模式管理器查找所有匹配"""
    if pattern_manager is None:
        pattern_manager = get_default_pattern_manager()
    
    return pattern_manager.find_all_matches(text)