"""
言律语言词法分析器 - 重构后的主类

使用模块化架构重构的词法分析器
"""

from typing import List, Optional, Dict, Any, Literal
from .base import YanLuLexerBase
from .token import Token, TokenType
from .tokenizer import YanLuTokenizer, create_tokenizer
from .matcher import create_token_matcher
from .error_handler import ErrorHandler, create_error_handler
from .context_manager import ContextManager, create_context_manager
from .pattern_manager import PatternManager, create_pattern_manager
from .performance_optimizer import PerformanceOptimizer, create_performance_optimizer, OptimizationConfig
from .utils import Position, PerformanceStats, Logger


class YanLuLexer(YanLuLexerBase):
    """言律语言词法分析器（重构版）"""
    
    def __init__(self, segmenter: Literal["jieba", "thulac"] = "jieba", **kwargs):
        """
        初始化词法分析器
        
        Args:
            segmenter: 分词器类型，可选 "jieba" 或 "thulac"
            **kwargs: 配置参数
        """
        super().__init__(segmenter)
        
        # 配置
        self.config = {
            'segmenter': segmenter,
            'strict_mode': kwargs.get('strict_mode', False),
            'verbose': kwargs.get('verbose', False),
            'max_errors': kwargs.get('max_errors', 100),
            'max_warnings': kwargs.get('max_warnings', 1000),
            'enable_cache': kwargs.get('enable_cache', True),
            'cache_size': kwargs.get('cache_size', 1000),
            'timeout': kwargs.get('timeout', 30),
            'max_line_length': kwargs.get('max_line_length', 1000),
        }
        
        # 初始化模块
        self._init_modules()
        
        # 性能统计
        self.stats = {
            'tokens_processed': 0,
            'lines_processed': 0,
            'characters_processed': 0,
            'errors': 0,
            'warnings': 0,
            'cache_hits': 0,
            'cache_misses': 0,
            'processing_time': 0.0,
        }
        
        # 日志
        self.logger = Logger("lexer")
        if self.config['verbose']:
            self.logger.set_level("DEBUG")
    
    def _init_modules(self):
        """初始化所有模块"""
        # 分词器
        self.tokenizer = create_tokenizer(
            segmenter=self.config['segmenter'],
            enable_cache=self.config['enable_cache'],
            cache_size=self.config['cache_size'],
            verbose=self.config['verbose']
        )
        
        # 词元匹配器
        self.token_matcher = create_token_matcher({
            'enable_cache': self.config['enable_cache'],
            'cache_size': self.config['cache_size']
        })
        
        # 错误处理器
        self.error_handler = create_error_handler(
            max_errors=self.config['max_errors'],
            max_warnings=self.config['max_warnings']
        )
        
        # 上下文管理器
        self.context_manager = create_context_manager()
        self.context_manager.set_error_handler(self.error_handler)
        
        # 模式管理器
        self.pattern_manager = create_pattern_manager()
        
        # 性能优化器
        optimizer_config = OptimizationConfig(
            level='basic',
            enable_cache=self.config['enable_cache'],
            cache_size=self.config['cache_size'],
            enable_precompilation=True,
            enable_lazy_loading=True,
            enable_parallel_processing=False,
            max_workers=4,
            batch_size=100,
            timeout_ms=self.config['timeout'] * 1000,
            memory_limit_mb=100
        )
        self.performance_optimizer = create_performance_optimizer(optimizer_config)
        
        # 加载动词分类
        self._load_verb_categories()
    
    def _load_verb_categories(self):
        """加载动词分类"""
        try:
            from .verb_categories_final_fixed2 import VERB_CATEGORIES, VERB_ARITY
            self.verb_categories = VERB_CATEGORIES
            self.verb_arity = VERB_ARITY
            self.logger.info(f"已加载动词分类: {len(self.verb_categories)}个类别, {len(self.verb_arity)}个动词")
        except ImportError as e:
            self.logger.warning(f"无法加载动词分类: {e}")
            self.verb_categories = {}
            self.verb_arity = {}
    
    def _init_segmenter(self):
        """初始化分词器（已由tokenizer模块处理）"""
        pass
    
    def _init_patterns(self):
        """初始化正则表达式模式（已由pattern_manager模块处理）"""
        pass
    
    def _init_dictionaries(self):
        """初始化字典配置（已由matcher模块处理）"""
        pass
    
    def tokenize_line(self, line: str, line_num: int) -> List[Token]:
        """
        将一行源代码转换为词法单元列表
        
        Args:
            line: 源代码行
            line_num: 行号
            
        Returns:
            词法单元列表
        """
        import time
        start_time = time.time()
        
        tokens = []
        position = 0
        
        # 检查行长度
        if len(line) > self.config['max_line_length']:
            self.error_handler.add_warning(
                code="LEXW001",
                message=f"行长度超过限制: {len(line)} > {self.config['max_line_length']}",
                position=Position(line=line_num, column=1, offset=0),
                suggestion="考虑将长行拆分为多行"
            )
        
        # 使用性能优化器进行分词
        segments = self.performance_optimizer.optimize_tokenization(
            line,
            lambda text: self.tokenizer.segment(text)
        )
        
        # 处理每个分词片段
        for segment in segments:
            if not segment.strip():
                # 跳过空白字符
                position += len(segment)
                continue
            
            # 使用性能优化器进行匹配
            token = self.performance_optimizer.optimize_matching(
                segment,
                lambda seg: self._match_token(seg, position, line_num)
            )
            
            if token:
                tokens.append(token)
                self.context_manager.add_token_to_current_context(token)
            
            position += len(segment)
        
        # 更新统计
        processing_time = time.time() - start_time
        self.stats['tokens_processed'] += len(tokens)
        self.stats['lines_processed'] += 1
        self.stats['characters_processed'] += len(line)
        self.stats['processing_time'] += processing_time
        
        # 检查内存使用
        if not self.performance_optimizer.check_memory_usage():
            self.error_handler.add_warning(
                code="SYS001",
                message="内存使用接近限制",
                position=Position(line=line_num, column=1, offset=0),
                suggestion="考虑减少输入大小或优化配置"
            )
        
        return tokens
    
    def _match_token(self, segment: str, position: int, line_num: int) -> Optional[Token]:
        """
        匹配词元类型
        
        Args:
            segment: 分词片段
            position: 在行中的位置
            line_num: 行号
            
        Returns:
            词元对象，如果无法匹配则返回None
        """
        # 计算列号（从1开始）
        column = position + 1
        
        # 使用词元匹配器
        token = self.token_matcher.match_token(segment, position, line_num, column)
        
        if token:
            return token
        
        # 检查是否为动词
        if segment in self.verb_arity:
            return Token(TokenType.VERB, segment, line_num, column, segment)
        
        # 检查是否为中文数字
        from .utils import is_numeric_string
        if is_numeric_string(segment):
            return Token(TokenType.NUMBER, segment, line_num, column, segment)
        
        # 无法识别的词元
        if self.config['strict_mode']:
            self.error_handler.add_error(
                code="LEX001",
                message=f"无法识别的词元: '{segment}'",
                position=Position(line=line_num, column=column, offset=position),
                suggestion="请检查拼写或添加自定义词元类型"
            )
            self.stats['errors'] += 1
            return Token(TokenType.ERROR, segment, line_num, column, segment)
        else:
            # 非严格模式下，将无法识别的词元视为标识符
            self.error_handler.add_warning(
                code="LEXW002",
                message=f"无法识别的词元被视为标识符: '{segment}'",
                position=Position(line=line_num, column=column, offset=position),
                suggestion="启用严格模式以获得更准确的错误报告"
            )
            self.stats['warnings'] += 1
            return Token(TokenType.IDENTIFIER, segment, line_num, column, segment)
    
    def tokenize(self, source_code: str) -> List[Token]:
        """
        将源代码转换为词法单元列表
        
        Args:
            source_code: 源代码字符串
            
        Returns:
            词法单元列表
        """
        import time
        start_time = time.time()
        
        # 重置状态
        self.context_manager.clear_contexts()
        self.error_handler.clear()
        self.performance_optimizer.reset_statistics()
        
        # 进入全局上下文
        self.context_manager.push_context(
            context_type='global',
            start_position=Position(line=1, column=1, offset=0),
            metadata={'source_length': len(source_code)}
        )
        
        # 调用父类方法
        tokens = super().tokenize(source_code)
        
        # 弹出全局上下文
        end_position = Position(
            line=len(source_code.split('\n')) + 1,
            column=1,
            offset=len(source_code)
        )
        self.context_manager.pop_context(end_position)
        
        # 更新统计
        total_time = time.time() - start_time
        self.stats['processing_time'] = total_time
        
        # 记录性能统计
        perf_stats = self.performance_optimizer.get_performance_statistics()
        cache_stats = perf_stats['cache']
        
        self.stats['cache_hits'] = sum(cache['hit_rate'] * 100 for cache in cache_stats.values())
        self.stats['cache_misses'] = 100 - self.stats['cache_hits']
        
        # 记录错误和警告
        self.stats['errors'] = self.error_handler.get_error_count()
        self.stats['warnings'] = self.error_handler.get_warning_count()
        
        # 输出统计信息
        if self.config['verbose']:
            self._print_statistics()
        
        return tokens
    
    def _print_statistics(self):
        """输出统计信息"""
        stats = self.get_statistics()
        perf_stats = self.performance_optimizer.get_performance_statistics()
        
        print("=" * 60)
        print("词法分析统计信息")
        print("=" * 60)
        print(f"处理行数: {stats['lines_processed']}")
        print(f"处理词元: {stats['tokens_processed']}")
        print(f"处理字符: {stats['characters_processed']}")
        print(f"处理时间: {stats['processing_time']:.3f}s")
        print(f"错误数量: {stats['errors']}")
        print(f"警告数量: {stats['warnings']}")
        print(f"缓存命中率: {stats['cache_hits']:.1f}%")
        print("-" * 60)
        
        # 性能优化统计
        opt_stats = perf_stats['optimization']
        print(f"优化次数: {opt_stats['total_optimizations']}")
        print(f"预编译模式: {opt_stats['precompilation_count']}")
        print(f"并行任务: {opt_stats['parallel_tasks']}")
        print(f"超时次数: {opt_stats['timeouts']}")
        print(f"内存警告: {opt_stats['memory_warnings']}")
        print("=" * 60)
        
        # 错误和警告
        if self.error_handler.has_errors() or self.error_handler.has_warnings():
            print("\n错误和警告:")
            print(self.error_handler.format_messages(include_warnings=True, include_infos=False))
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        获取性能统计信息
        
        Returns:
            统计信息字典
        """
        stats = self.stats.copy()
        
        # 添加模块统计
        stats['tokenizer_stats'] = self.tokenizer.get_statistics()
        stats['matcher_stats'] = self.token_matcher.get_statistics()
        stats['context_stats'] = self.context_manager.get_statistics()
        stats['error_stats'] = self.error_handler.get_statistics()
        stats['performance_stats'] = self.performance_optimizer.get_performance_statistics()
        
        return stats
    
    def reset_statistics(self):
        """重置性能统计"""
        self.stats = {
            'tokens_processed': 0,
            'lines_processed': 0,
            'characters_processed': 0,
            'errors': 0,
            'warnings': 0,
            'cache_hits': 0,
            'cache_misses': 0,
            'processing_time': 0.0,
        }
        self.tokenizer.reset()
        self.token_matcher.reset_statistics()
        self.context_manager.reset_statistics()
        self.error_handler.clear()
        self.performance_optimizer.reset_statistics()
    
    def get_config(self) -> Dict[str, Any]:
        """获取配置"""
        return self.config.copy()
    
    def update_config(self, **kwargs):
        """更新配置"""
        old_config = self.config.copy()
        self.config.update(kwargs)
        
        # 如果配置有变化，重新初始化模块
        need_reinit = False
        for key in ['segmenter', 'enable_cache', 'cache_size']:
            if key in kwargs and kwargs[key] != old_config.get(key):
                need_reinit = True
                break
        
        if need_reinit:
            self._init_modules()
    
    def get_errors(self) -> List[Dict[str, Any]]:
        """获取错误列表"""
        return [error.to_dict() for error in self.error_handler.get_all_errors()]
    
    def get_warnings(self) -> List[Dict[str, Any]]:
        """获取警告列表"""
        return [warning.to_dict() for warning in self.error_handler.get_all_warnings()]
    
    def get_context_info(self) -> Dict[str, Any]:
        """获取上下文信息"""
        return {
            'current_context': str(self.context_manager.get_current_context()),
            'context_depth': self.context_manager.get_context_depth(),
            'context_chain': self.context_manager.get_context_stack(),
            'symbol_table': self.context_manager.get_symbol_table()
        }
    
    def add_custom_pattern(self, name: str, pattern: str, token_type: TokenType, 
                           pattern_type: str = "custom", priority: int = 0,
                           description: Optional[str] = None, examples: Optional[List[str]] = None):
        """
        添加自定义模式
        
        Args:
            name: 模式名称
            pattern: 正则表达式模式
            token_type: 词元类型
            pattern_type: 模式类型
            priority: 优先级
            description: 描述
            examples: 示例
        """
        from .pattern_manager import PatternType
        
        pattern_type_enum = PatternType(pattern_type)
        success = self.pattern_manager.add_pattern(
            name=name,
            pattern=pattern,
            token_type=token_type,
            pattern_type=pattern_type_enum,
            priority=priority,
            description=description,
            examples=examples
        )
        
        if success:
            self.logger.info(f"已添加自定义模式: {name}")
        else:
            self.logger.warning(f"添加自定义模式失败: {name}")
    
    def remove_custom_pattern(self, name: str) -> bool:
        """
        移除自定义模式
        
        Args:
            name: 模式名称
            
        Returns:
            是否成功移除
        """
        success = self.pattern_manager.remove_pattern(name)
        if success:
            self.logger.info(f"已移除自定义模式: {name}")
        else:
            self.logger.warning(f"移除自定义模式失败: {name}")
        
        return success
    
    def clear_caches(self):
        """清空所有缓存"""
        self.tokenizer.reset()
        self.token_matcher.clear_cache()
        self.performance_optimizer.clear_caches()
        self.logger.info("已清空所有缓存")
    
    def __str__(self) -> str:
        """返回词法分析器描述"""
        stats = self.get_statistics()
        return (
            f"YanLuLexer("
            f"segmenter={self.config['segmenter']}, "
            f"tokens={stats['tokens_processed']}, "
            f"errors={stats['errors']}, "
            f"warnings={stats['warnings']}"
            f")"
        )
    
    def __repr__(self) -> str:
        """返回词法分析器表示"""
        return self.__str__()


# 工厂函数
def create_lexer(segmenter: Literal["jieba", "thulac"] = "jieba", **kwargs) -> YanLuLexer:
    """
    创建词法分析器
    
    Args:
        segmenter: 分词器类型
        **kwargs: 配置参数
        
    Returns:
        词法分析器实例
    """
    return YanLuLexer(segmenter, **kwargs)


def get_default_lexer() -> YanLuLexer:
    """
    获取默认词法分析器
    
    Returns:
        默认词法分析器实例
    """
    return YanLuLexer(segmenter="jieba", verbose=False)


# 便捷函数
def tokenize(source_code: str, segmenter: Literal["jieba", "thulac"] = "jieba", **kwargs) -> List[Token]:
    """
    便捷函数：将源代码转换为词法单元列表
    
    Args:
        source_code: 源代码字符串
        segmenter: 分词器类型
        **kwargs: 配置参数
        
    Returns:
        词法单元列表
    """
    lexer = create_lexer(segmenter, **kwargs)
    return lexer.tokenize(source_code)


def tokenize_file(filepath: str, segmenter: Literal["jieba", "thulac"] = "jieba", **kwargs) -> List[Token]:
    """
    便捷函数：将文件内容转换为词法单元列表
    
    Args:
        filepath: 文件路径
        segmenter: 分词器类型
        **kwargs: 配置参数
        
    Returns:
        词法单元列表
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        source_code = f.read()
    
    lexer = create_lexer(segmenter, **kwargs)
    return lexer.tokenize(source_code)