"""
言律语言词法分析器 - 模块化实现

使用模块化架构重构的主词法分析器类
"""

from typing import List, Optional, Dict, Any, Literal
import time
from .base import YanLuLexerBase
from .lexer_token import Token, TokenType
from .tokenizer import YanLuTokenizer
from .matcher import create_token_matcher
from .error_handler import ErrorHandler, create_error_handler
from .context_manager import ContextManager, create_context_manager
from .pattern_manager import PatternManager, create_pattern_manager
from .performance_optimizer import PerformanceOptimizer, OptimizationConfig, OptimizationLevel
from .utils import PerformanceMonitor, Logger, normalize_text
from .token_cache import TokenCache, get_global_cache


class ModularYanLuLexer(YanLuLexerBase):
    """模块化言律语言词法分析器"""
    
    def __init__(self, segmenter: Literal["jieba", "thulac", "yanlv_nospace"] = "jieba", **kwargs):
        """初始化模块化词法分析器"""
        super().__init__(segmenter)
        
        # 配置
        self.config = {
            'strict_mode': kwargs.get('strict_mode', False),
            'verbose': kwargs.get('verbose', False),
            'max_errors': kwargs.get('max_errors', 100),
            'enable_cache': kwargs.get('enable_cache', True),
            'cache_size': kwargs.get('cache_size', 1000),
        }
        
        # 初始化模块
        self._init_modules()
        
        # 性能监控
        self.monitor = PerformanceMonitor()
        
        # 日志
        self.logger = Logger("lexer")
        if self.config['verbose']:
            self.logger.set_level("DEBUG")
    
    def _init_modules(self):
        """初始化所有模块"""
        # Token缓存
        if self.config['enable_cache']:
            self.token_cache = get_global_cache()
            if self.token_cache.max_size != self.config['cache_size']:
                self.token_cache.resize(self.config['cache_size'])
        else:
            self.token_cache = None
        
        # 分词器
        self.tokenizer = YanLuTokenizer.create(
            self.segmenter_type,
            enable_cache=self.config['enable_cache'],
            cache_size=self.config['cache_size']
        )
        
        # 词元匹配器
        self.token_matcher = create_token_matcher({
            'enable_cache': self.config['enable_cache'],
            'cache_size': self.config['cache_size']
        })
        
        # 错误处理器
        self.error_handler = create_error_handler(
            max_errors=self.config['max_errors'],
            max_warnings=1000
        )
        
        # 上下文管理器
        self.context_manager = create_context_manager()
        self.context_manager.set_error_handler(self.error_handler)
        
        # 模式管理器
        self.pattern_manager = create_pattern_manager()
        
        # 性能优化器
        optimization_config = OptimizationConfig(
            level=OptimizationLevel.BASIC,
            enable_cache=self.config['enable_cache'],
            cache_size=self.config['cache_size']
        )
        self.optimizer = PerformanceOptimizer(optimization_config)
    
    def _init_segmenter(self):
        """初始化分词器（由基类调用）"""
        pass
    
    def _init_patterns(self):
        """初始化正则表达式模式（由基类调用）"""
        pass
    
    def _init_dictionaries(self):
        """初始化字典配置（由基类调用）"""
        pass
    
    def tokenize_line(self, line: str, line_num: int) -> List[Token]:
        """将一行源代码转换为词法单元列表"""
        tokens = []

        # 跳过空行
        if not line.strip():
            return tokens

        # 规范化文本
        normalized_line = normalize_text(line)

        # 先提取字符串字面量，避免被分词器拆分
        # 记录字符串的位置和内容
        string_ranges = []
        i = 0
        while i < len(normalized_line):
            if normalized_line[i] in ('"', "'"):
                quote = normalized_line[i]
                j = i + 1
                while j < len(normalized_line) and normalized_line[j] != quote:
                    j += 1
                if j < len(normalized_line):
                    # 找到完整的字符串字面量
                    string_ranges.append((i, j+1))
                    i = j + 1
                else:
                    i += 1
            else:
                i += 1

        # 使用分词器进行分词
        raw_segments = self.tokenizer.segment(normalized_line)

        # 计算每个segment在原始字符串中的位置（包括空格）
        segment_positions = []
        pos = 0
        for segment in raw_segments:
            if segment:
                segment_positions.append((segment, pos, pos + len(segment)))
                pos += len(segment)

        # 过滤掉纯空格的segment
        segment_positions = [(s, start, end) for s, start, end in segment_positions if s and not s.isspace()]

        # 处理每个分词片段
        column = 1
        processed_string_ranges = set()  # 记录已处理的字符串范围

        for segment, seg_start, seg_end in segment_positions:
            # 跳过空片段
            if not segment:
                continue

            # 检查是否在字符串范围内
            in_string = False
            for idx, (str_start, str_end) in enumerate(string_ranges):
                if seg_start >= str_start and seg_end <= str_end:
                    in_string = True
                    # 如果这是字符串的开始位置，且还没处理过
                    if seg_start == str_start and idx not in processed_string_ranges:
                        string_literal = normalized_line[str_start:str_end]
                        token = Token(TokenType.STRING, string_literal, line_num, column, string_literal)
                        tokens.append(token)
                        column += len(string_literal)
                        processed_string_ranges.add(idx)
                    break

            if in_string:
                # 如果是字符串的一部分，跳过
                continue

            # 匹配词元类型
            token = self.optimizer.optimize_matching(
                segment,
                lambda s: self._match_token(s, column, line_num)
            )

            if token:
                tokens.append(token)

            # 更新列位置
            column += len(segment)

        # 更新统计
        self.stats['tokens_processed'] += len(tokens)

        return tokens
    
    def _match_token(self, segment: str, column: int, line_num: int) -> Optional[Token]:
        """匹配词元类型"""
        # 使用词元匹配器
        token = self.token_matcher.match_token(segment, 0, line_num, column)
        
        if token:
            return token
        
        # 默认作为标识符
        return Token(TokenType.IDENTIFIER, segment, line_num, column, segment)
    
    def tokenize(self, source_code: str) -> List[Token]:
        """将源代码转换为词法单元列表（重写以添加性能监控和Token缓存）"""
        # 尝试从缓存获取
        if self.token_cache:
            cached_tokens = self.token_cache.get(source_code)
            if cached_tokens is not None:
                # 缓存命中
                self.stats['cache_hits'] = self.stats.get('cache_hits', 0) + 1
                return cached_tokens
        
        # 缓存未命中,开始性能监控
        start_time = time.time()
        self.monitor.start()
        
        try:
            # 重置统计
            self.stats['tokens_processed'] = 0
            self.stats['lines_processed'] = 0
            self.stats['errors'] = 0
            self.stats['warnings'] = 0
            
            # 清空错误处理器
            if self.error_handler:
                self.error_handler.clear()
            
            # 清空上下文管理器
            self.context_manager.clear_contexts()
            
            # 调用基类方法
            tokens = super().tokenize(source_code)
            
            # 更新错误统计
            if self.error_handler:
                self.stats['errors'] = self.error_handler.get_error_count()
                self.stats['warnings'] = self.error_handler.get_warning_count()
            
            # 存入缓存
            if self.token_cache:
                elapsed_time = (time.time() - start_time) * 1000  # 转换为毫秒
                self.token_cache.put(source_code, tokens, time_saved=elapsed_time)
                self.stats['cache_misses'] = self.stats.get('cache_misses', 0) + 1
            
            return tokens
            
        finally:
            # 停止性能监控
            self.monitor.stop()
            
            if self.config.get('verbose', False):
                stats = self.monitor.get_stats()
                self.logger.info(f"词法分析完成: {self.stats['tokens_processed']} 词元, {self.stats['lines_processed']} 行, 耗时 {stats.total_time:.3f}秒")
        """获取错误信息"""
        if self.error_handler:
            return [str(error) for error in self.error_handler.get_all_errors()]
        return []
    
    def get_warnings(self) -> List[str]:
        """获取警告信息"""
        if self.error_handler:
            return [str(warning) for warning in self.error_handler.get_all_warnings()]
        return []
    
    def has_errors(self) -> bool:
        """检查是否有错误"""
        if self.error_handler:
            return self.error_handler.has_errors()
        return False
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """获取性能统计信息"""
        # 先获取optimizer的stats（包含total_operations等）
        stats = self.optimizer.get_performance_stats()
        # 然后更新monitor的stats
        stats.update(self.monitor.get_stats().to_dict())
        # 最后更新lexer的stats（优先级最高）
        stats.update(self.stats)
        
        # 添加Token缓存统计
        if self.token_cache:
            cache_stats = self.token_cache.get_stats()
            stats['token_cache'] = cache_stats.to_dict()
        else:
            stats['token_cache'] = None
        
        return stats
    
    def get_config(self) -> Dict[str, Any]:
        """获取配置"""
        config = self.config.copy()
        config['segmenter'] = self.segmenter_type
        return config
    
    def reset(self):
        """重置分析器状态"""
        self.reset_statistics()
        self.monitor.reset()
        self.optimizer.clear_caches()
        
        if self.error_handler:
            self.error_handler.clear()
        self.context_manager.clear_contexts()


# 工厂函数
def create_lexer(segmenter: Literal["jieba", "thulac"] = "jieba", **kwargs) -> ModularYanLuLexer:
    """创建模块化词法分析器"""
    return ModularYanLuLexer(segmenter, **kwargs)


def get_default_lexer() -> ModularYanLuLexer:
    """获取默认词法分析器"""
    return ModularYanLuLexer()


# 便捷函数
def tokenize(source_code: str, segmenter: Literal["jieba", "thulac"] = "jieba", **kwargs) -> List[Token]:
    """便捷函数：将源代码转换为词法单元列表"""
    lexer = create_lexer(segmenter, **kwargs)
    return lexer.tokenize(source_code)


def tokenize_with_stats(source_code: str, segmenter: Literal["jieba", "thulac"] = "jieba", **kwargs) -> tuple:
    """便捷函数：将源代码转换为词法单元列表并返回统计信息"""
    lexer = create_lexer(segmenter, **kwargs)
    tokens = lexer.tokenize(source_code)
    stats = lexer.get_performance_stats()
    return tokens, stats