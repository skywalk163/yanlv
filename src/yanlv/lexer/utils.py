"""
言律语言词法分析器 - 工具模块

包含各种工具函数和辅助类
"""

import re
import time
import hashlib
import json
from typing import Any, Dict, List, Optional, Tuple, Union, Callable
from dataclasses import dataclass, asdict
from enum import Enum
from pathlib import Path


# ============================================================================
# 数据类型定义
# ============================================================================

@dataclass
class Position:
    """位置信息"""
    line: int
    column: int
    offset: int
    
    def __str__(self) -> str:
        return f"({self.line}:{self.column})"
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Position':
        """从字典创建"""
        return cls(**data)


@dataclass
class Range:
    """范围信息"""
    start: Position
    end: Position
    
    def __str__(self) -> str:
        return f"{self.start}-{self.end}"
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'start': self.start.to_dict(),
            'end': self.end.to_dict()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Range':
        """从字典创建"""
        return cls(
            start=Position.from_dict(data['start']),
            end=Position.from_dict(data['end'])
        )


@dataclass
class ErrorInfo:
    """错误信息"""
    code: str
    message: str
    position: Position
    severity: str  # 'error', 'warning', 'info'
    suggestion: Optional[str] = None
    
    def __str__(self) -> str:
        base = f"{self.severity.upper()}[{self.code}] at {self.position}: {self.message}"
        if self.suggestion:
            base += f"\n建议: {self.suggestion}"
        return base
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        result = asdict(self)
        result['position'] = self.position.to_dict()
        return result
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ErrorInfo':
        """从字典创建"""
        data = data.copy()
        data['position'] = Position.from_dict(data['position'])
        return cls(**data)


@dataclass
class PerformanceStats:
    """性能统计"""
    total_time: float = 0.0
    tokenization_time: float = 0.0
    matching_time: float = 0.0
    parsing_time: float = 0.0
    memory_usage_mb: float = 0.0
    tokens_processed: int = 0
    lines_processed: int = 0
    characters_processed: int = 0
    cache_hits: int = 0
    cache_misses: int = 0
    errors: int = 0
    warnings: int = 0
    
    def __str__(self) -> str:
        return (
            f"性能统计:\n"
            f"  总时间: {self.total_time:.3f}s\n"
            f"  分词时间: {self.tokenization_time:.3f}s\n"
            f"  匹配时间: {self.matching_time:.3f}s\n"
            f"  解析时间: {self.parsing_time:.3f}s\n"
            f"  内存使用: {self.memory_usage_mb:.2f}MB\n"
            f"  处理词元: {self.tokens_processed}\n"
            f"  处理行数: {self.lines_processed}\n"
            f"  处理字符: {self.characters_processed}\n"
            f"  缓存命中: {self.cache_hits}\n"
            f"  缓存未命中: {self.cache_misses}\n"
            f"  错误数: {self.errors}\n"
            f"  警告数: {self.warnings}"
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'PerformanceStats':
        """从字典创建"""
        return cls(**data)
    
    def merge(self, other: 'PerformanceStats') -> 'PerformanceStats':
        """合并性能统计"""
        result = PerformanceStats()
        for field in self.__dataclass_fields__:
            if field.endswith('_time'):
                setattr(result, field, getattr(self, field) + getattr(other, field))
            elif field.endswith('_mb'):
                setattr(result, field, max(getattr(self, field), getattr(other, field)))
            else:
                setattr(result, field, getattr(self, field) + getattr(other, field))
        return result


# ============================================================================
# 工具函数
# ============================================================================

def normalize_text(text: str) -> str:
    """
    规范化文本
    
    Args:
        text: 输入文本
        
    Returns:
        规范化后的文本
    """
    # 移除BOM头
    if text.startswith('\ufeff'):
        text = text[1:]
    
    # 统一换行符
    text = text.replace('\r\n', '\n').replace('\r', '\n')
    
    # 移除尾随空白
    text = text.rstrip()
    
    return text


def split_lines(text: str) -> List[str]:
    """
    将文本分割为行
    
    Args:
        text: 输入文本
        
    Returns:
        行列表
    """
    return text.split('\n')


def calculate_line_info(text: str, offset: int) -> Tuple[int, int]:
    """
    根据偏移量计算行号和列号
    
    Args:
        text: 完整文本
        offset: 字符偏移量
        
    Returns:
        (行号, 列号)
    """
    if offset < 0 or offset > len(text):
        return 1, 1
    
    lines = text[:offset].split('\n')
    line_num = len(lines)
    column = len(lines[-1]) + 1 if lines else 1
    
    return line_num, column


def calculate_position(text: str, offset: int) -> Position:
    """
    根据偏移量计算位置
    
    Args:
        text: 完整文本
        offset: 字符偏移量
        
    Returns:
        位置对象
    """
    line_num, column = calculate_line_info(text, offset)
    return Position(line=line_num, column=column, offset=offset)


def escape_string(s: str) -> str:
    """
    转义字符串中的特殊字符
    
    Args:
        s: 输入字符串
        
    Returns:
        转义后的字符串
    """
    escape_map = {
        '\n': '\\n',
        '\r': '\\r',
        '\t': '\\t',
        '\"': '\\"',
        '\\': '\\\\',
    }
    
    result = []
    for char in s:
        if char in escape_map:
            result.append(escape_map[char])
        else:
            result.append(char)
    
    return ''.join(result)


def unescape_string(s: str) -> str:
    """
    反转义字符串
    
    Args:
        s: 转义后的字符串
        
    Returns:
        原始字符串
    """
    escape_map = {
        '\\n': '\n',
        '\\r': '\r',
        '\\t': '\t',
        '\\"': '\"',
        '\\\\': '\\',
    }
    
    # 简单的反转义实现
    for escaped, unescaped in escape_map.items():
        s = s.replace(escaped, unescaped)
    
    return s


def is_valid_identifier(name: str) -> bool:
    """
    检查是否为有效的标识符
    
    Args:
        name: 标识符名称
        
    Returns:
        是否为有效标识符
    """
    # 检查是否为空
    if not name:
        return False
    
    # 检查首字符
    first_char = name[0]
    if not (first_char.isalpha() or first_char == '_' or '\u4e00' <= first_char <= '\u9fff'):
        return False
    
    # 检查后续字符
    for char in name[1:]:
        if not (char.isalnum() or char == '_' or '\u4e00' <= char <= '\u9fff'):
            return False
    
    return True


def is_numeric_string(s: str) -> bool:
    """
    检查字符串是否为数字
    
    Args:
        s: 输入字符串
        
    Returns:
        是否为数字
    """
    # 整数
    if s.isdigit():
        return True
    
    # 浮点数
    try:
        float(s)
        return True
    except ValueError:
        pass
    
    # 中文数字
    chinese_digits = {'零', '〇', '一', '二', '三', '四', '五', '六', '七', '八', '九', '十', '百', '千', '万', '亿', '兆'}
    if all(char in chinese_digits for char in s):
        return True
    
    return False


def parse_chinese_number(s: str) -> Optional[int]:
    """
    解析中文数字
    
    Args:
        s: 中文数字字符串
        
    Returns:
        整数值，如果无法解析则返回None
    """
    chinese_digits = {
        '零': 0, '〇': 0, '一': 1, '二': 2, '三': 3, '四': 4,
        '五': 5, '六': 6, '七': 7, '八': 8, '九': 9,
        '十': 10, '百': 100, '千': 1000, '万': 10000,
        '亿': 100000000, '兆': 1000000000000,
    }
    
    try:
        result = 0
        temp = 0
        last_unit = 1
        
        for char in s:
            if char in chinese_digits:
                value = chinese_digits[char]
                if value < 10:
                    temp = value
                else:
                    if temp == 0:
                        temp = 1
                    result += temp * value
                    temp = 0
                    last_unit = value
        
        result += temp
        
        return result
    except:
        return None


def calculate_hash(text: str, algorithm: str = 'md5') -> str:
    """
    计算文本哈希值
    
    Args:
        text: 输入文本
        algorithm: 哈希算法，可选 'md5', 'sha1', 'sha256'
        
    Returns:
        哈希值字符串
    """
    if algorithm == 'md5':
        hasher = hashlib.md5()
    elif algorithm == 'sha1':
        hasher = hashlib.sha1()
    elif algorithm == 'sha256':
        hasher = hashlib.sha256()
    else:
        raise ValueError(f"不支持的哈希算法: {algorithm}")
    
    hasher.update(text.encode('utf-8'))
    return hasher.hexdigest()


def format_time(seconds: float) -> str:
    """
    格式化时间
    
    Args:
        seconds: 秒数
        
    Returns:
        格式化后的时间字符串
    """
    if seconds < 0.001:
        return f"{seconds * 1_000_000:.2f}µs"
    elif seconds < 1:
        return f"{seconds * 1000:.2f}ms"
    else:
        return f"{seconds:.3f}s"


def format_size(bytes_count: int) -> str:
    """
    格式化大小
    
    Args:
        bytes_count: 字节数
        
    Returns:
        格式化后的大小字符串
    """
    if bytes_count < 1024:
        return f"{bytes_count}B"
    elif bytes_count < 1024 * 1024:
        return f"{bytes_count / 1024:.2f}KB"
    elif bytes_count < 1024 * 1024 * 1024:
        return f"{bytes_count / (1024 * 1024):.2f}MB"
    else:
        return f"{bytes_count / (1024 * 1024 * 1024):.2f}GB"


# ============================================================================
# 缓存工具
# ============================================================================

class Cache:
    """简单的缓存实现"""
    
    def __init__(self, max_size: int = 1000):
        """
        初始化缓存
        
        Args:
            max_size: 最大缓存大小
        """
        self.max_size = max_size
        self._cache = {}
        self._access_order = []
    
    def get(self, key: str) -> Any:
        """
        获取缓存值
        
        Args:
            key: 缓存键
            
        Returns:
            缓存值，如果不存在则返回None
        """
        if key in self._cache:
            # 更新访问顺序
            if key in self._access_order:
                self._access_order.remove(key)
            self._access_order.append(key)
            return self._cache[key]
        return None
    
    def set(self, key: str, value: Any):
        """
        设置缓存值
        
        Args:
            key: 缓存键
            value: 缓存值
        """
        # 如果缓存已满，移除最久未使用的项
        if len(self._cache) >= self.max_size and key not in self._cache:
            oldest_key = self._access_order.pop(0)
            del self._cache[oldest_key]
        
        self._cache[key] = value
        if key in self._access_order:
            self._access_order.remove(key)
        self._access_order.append(key)
    
    def clear(self):
        """清空缓存"""
        self._cache.clear()
        self._access_order.clear()
    
    def size(self) -> int:
        """获取缓存大小"""
        return len(self._cache)
    
    def hit_rate(self, hits: int, misses: int) -> float:
        """
        计算命中率
        
        Args:
            hits: 命中次数
            misses: 未命中次数
            
        Returns:
            命中率
        """
        total = hits + misses
        return hits / total if total > 0 else 0.0


# ============================================================================
# 性能监控器
# ============================================================================

class PerformanceMonitor:
    """性能监控器"""
    
    def __init__(self):
        """初始化性能监控器"""
        self.stats = PerformanceStats()
        self._start_time = None
        self._timers = {}
    
    def start(self):
        """开始计时"""
        self._start_time = time.time()
    
    def stop(self):
        """停止计时并更新总时间"""
        if self._start_time:
            elapsed = time.time() - self._start_time
            self.stats.total_time += elapsed
            self._start_time = None
    
    def start_timer(self, name: str):
        """
        开始指定计时器
        
        Args:
            name: 计时器名称
        """
        self._timers[name] = time.time()
    
    def stop_timer(self, name: str) -> float:
        """
        停止指定计时器并返回耗时
        
        Args:
            name: 计时器名称
            
        Returns:
            耗时（秒）
        """
        if name in self._timers:
            elapsed = time.time() - self._timers[name]
            del self._timers[name]
            
            # 更新对应的统计字段
            if name == 'tokenization':
                self.stats.tokenization_time += elapsed
            elif name == 'matching':
                self.stats.matching_time += elapsed
            elif name == 'parsing':
                self.stats.parsing_time += elapsed
            
            return elapsed
        return 0.0
    
    def increment(self, field: str, amount: int = 1):
        """
        递增统计字段
        
        Args:
            field: 字段名
            amount: 增量
        """
        if hasattr(self.stats, field):
            current = getattr(self.stats, field)
            setattr(self.stats, field, current + amount)
    
    def update_memory_usage(self):
        """更新内存使用统计"""
        try:
            import psutil
            process = psutil.Process()
            memory_info = process.memory_info()
            self.stats.memory_usage_mb = memory_info.rss / (1024 * 1024)
        except ImportError:
            # psutil未安装，跳过内存统计
            pass
    
    def get_stats(self) -> PerformanceStats:
        """获取性能统计"""
        return self.stats
    
    def reset(self):
        """重置性能统计"""
        self.stats = PerformanceStats()
        self._timers.clear()
        self._start_time = None
    
    def __enter__(self):
        """上下文管理器入口"""
        self.start()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器出口"""
        self.stop()


# ============================================================================
# 配置管理
# ============================================================================

class ConfigManager:
    """配置管理器"""
    
    def __init__(self, default_config: Dict[str, Any] = None):
        """
        初始化配置管理器
        
        Args:
            default_config: 默认配置
        """
        self.default_config = default_config or {}
        self.config = self.default_config.copy()
        self._listeners = []
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        获取配置值
        
        Args:
            key: 配置键
            default: 默认值
            
        Returns:
            配置值
        """
        return self.config.get(key, default)
    
    def set(self, key: str, value: Any):
        """
        设置配置值
        
        Args:
            key: 配置键
            value: 配置值
        """
        old_value = self.config.get(key)
        self.config[key] = value
        
        # 通知监听器
        for listener in self._listeners:
            listener(key, old_value, value)
    
    def update(self, new_config: Dict[str, Any]):
        """
        批量更新配置
        
        Args:
            new_config: 新配置
        """
        for key, value in new_config.items():
            self.set(key, value)
    
    def reset(self):
        """重置为默认配置"""
        self.config = self.default_config.copy()
    
    def add_listener(self, listener: Callable[[str, Any, Any], None]):
        """
        添加配置变更监听器
        
        Args:
            listener: 监听器函数，参数为 (key, old_value, new_value)
        """
        self._listeners.append(listener)
    
    def remove_listener(self, listener: Callable[[str, Any, Any], None]):
        """移除配置变更监听器"""
        if listener in self._listeners:
            self._listeners.remove(listener)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return self.config.copy()
    
    def from_dict(self, config_dict: Dict[str, Any]):
        """从字典加载"""
        self.config = config_dict.copy()
    
    def save_to_file(self, filepath: str):
        """
        保存配置到文件
        
        Args:
            filepath: 文件路径
        """
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, ensure_ascii=False, indent=2)
    
    def load_from_file(self, filepath: str):
        """
        从文件加载配置
        
        Args:
            filepath: 文件路径
        """
        with open(filepath, 'r', encoding='utf-8') as f:
            self.config = json.load(f)


# ============================================================================
# 日志工具
# ============================================================================

class Logger:
    """简单的日志工具"""
    
    def __init__(self, name: str = "lexer", level: str = "INFO"):
        """
        初始化日志工具
        
        Args:
            name: 日志名称
            level: 日志级别，可选 'DEBUG', 'INFO', 'WARNING', 'ERROR'
        """
        self.name = name
        self.level = level.upper()
        self.levels = {'DEBUG': 0, 'INFO': 1, 'WARNING': 2, 'ERROR': 3}
        self._handlers = []
    
    def log(self, level: str, message: str, **kwargs):
        """
        记录日志
        
        Args:
            level: 日志级别
            message: 日志消息
            **kwargs: 额外参数
        """
        if self.levels.get(level.upper(), 99) >= self.levels.get(self.level, 0):
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            log_entry = f"[{timestamp}] [{level.upper()}] [{self.name}] {message}"
            
            if kwargs:
                log_entry += f" {kwargs}"
            
            # 输出到控制台
            print(log_entry)
            
            # 调用处理器
            for handler in self._handlers:
                handler(level, message, **kwargs)
    
    def debug(self, message: str, **kwargs):
        """记录调试日志"""
        self.log('DEBUG', message, **kwargs)
    
    def info(self, message: str, **kwargs):
        """记录信息日志"""
        self.log('INFO', message, **kwargs)
    
    def warning(self, message: str, **kwargs):
        """记录警告日志"""
        self.log('WARNING', message, **kwargs)
    
    def error(self, message: str, **kwargs):
        """记录错误日志"""
        self.log('ERROR', message, **kwargs)
    
    def add_handler(self, handler: Callable[[str, str, Dict], None]):
        """
        添加日志处理器
        
        Args:
            handler: 处理器函数，参数为 (level, message, kwargs)
        """
        self._handlers.append(handler)
    
    def remove_handler(self, handler: Callable[[str, str, Dict], None]):
        """移除日志处理器"""
        if handler in self._handlers:
            self._handlers.remove(handler)
    
    def set_level(self, level: str):
        """
        设置日志级别
        
        Args:
            level: 日志级别
        """
        self.level = level.upper()


# 默认日志实例
default_logger = Logger()


def get_logger(name: str = "lexer") -> Logger:
    """
    获取日志实例
    
    Args:
        name: 日志名称
        
    Returns:
        日志实例
    """
    return Logger(name)