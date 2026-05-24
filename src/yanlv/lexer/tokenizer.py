"""
言律语言词法分析器 - 分词器模块

包含分词器接口和实现
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
import jieba
from .constants import DEFAULT_CONFIG, SEGMENTER_CONFIG, KEYWORDS
import re


class ITokenizer(ABC):
    """分词器接口"""
    
    @abstractmethod
    def segment(self, text: str) -> List[str]:
        """
        将文本分词为片段列表
        
        Args:
            text: 待分词的文本
            
        Returns:
            分词结果列表
        """
        pass
    
    @abstractmethod
    def get_segmenter_type(self) -> str:
        """
        获取分词器类型
        
        Returns:
            分词器类型名称
        """
        pass
    
    @abstractmethod
    def get_config(self) -> Dict[str, Any]:
        """
        获取配置
        
        Returns:
            配置字典
        """
        pass
    
    @abstractmethod
    def update_config(self, **kwargs):
        """
        更新配置
        
        Args:
            **kwargs: 配置参数
        """
        pass
    
    @abstractmethod
    def reset(self):
        """重置分词器状态"""
        pass


class BaseTokenizer(ITokenizer):
    """分词器基类"""
    
    def __init__(self, segmenter_type: str = "jieba", **kwargs):
        """
        初始化分词器
        
        Args:
            segmenter_type: 分词器类型
            **kwargs: 配置参数
        """
        self.segmenter_type = segmenter_type
        self.config = DEFAULT_CONFIG.copy()
        self.config.update(SEGMENTER_CONFIG.get(segmenter_type, {}))
        self.config.update(kwargs)
        
        # 性能统计
        self.stats = {
            'segments_processed': 0,
            'characters_processed': 0,
            'cache_hits': 0,
            'cache_misses': 0,
            'processing_time': 0.0,
        }
        
        # 缓存
        self._cache = {}
        self._cache_enabled = self.config.get('enable_cache', True)
        self._cache_size = self.config.get('cache_size', 1000)
    
    def get_segmenter_type(self) -> str:
        """获取分词器类型"""
        return self.segmenter_type
    
    def get_config(self) -> Dict[str, Any]:
        """获取配置"""
        return self.config.copy()
    
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
    
    def reset(self):
        """重置分词器状态"""
        self.stats = {
            'segments_processed': 0,
            'characters_processed': 0,
            'cache_hits': 0,
            'cache_misses': 0,
            'processing_time': 0.0,
        }
        self._cache.clear()
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        获取性能统计信息
        
        Returns:
            统计信息字典
        """
        return self.stats.copy()
    
    def _clean_cache(self):
        """清理缓存，保留最近使用的项"""
        if len(self._cache) > self._cache_size:
            # 简单实现：清除一半缓存
            items = list(self._cache.items())
            items_to_remove = items[:len(items) // 2]
            for key, _ in items_to_remove:
                del self._cache[key]
    
    def _update_stats(self, text: str, cache_hit: bool = False, processing_time: float = 0.0):
        """更新统计信息"""
        self.stats['segments_processed'] += 1
        self.stats['characters_processed'] += len(text)
        if cache_hit:
            self.stats['cache_hits'] += 1
        else:
            self.stats['cache_misses'] += 1
        self.stats['processing_time'] += processing_time
    
    def __str__(self) -> str:
        """返回分词器描述"""
        return f"{self.__class__.__name__}(type={self.segmenter_type}, stats={self.stats})"
    
    def __repr__(self) -> str:
        """返回分词器表示"""
        return self.__str__()


class JiebaTokenizer(BaseTokenizer):
    """jieba分词器实现"""
    
    def __init__(self, **kwargs):
        """
        初始化jieba分词器
        
        Args:
            **kwargs: 配置参数
        """
        super().__init__("jieba", **kwargs)
        self._init_jieba()
    
    def _init_jieba(self):
        """初始化jieba分词器"""
        # 加载用户词典
        user_dict = self.config.get('user_dict')
        if user_dict:
            jieba.load_userdict(user_dict)
        
        # 设置HMM模式
        self._use_hmm = self.config.get('hmm', True)
        
        # 初始化缓存
        self._cache = {}
    
    def segment(self, text: str) -> List[str]:
        """
        使用jieba进行分词
        
        Args:
            text: 待分词的文本
            
        Returns:
            分词结果列表
        """
        import time
        start_time = time.time()
        
        # 检查缓存
        cache_key = text
        if self._cache_enabled and cache_key in self._cache:
            result = self._cache[cache_key]
            processing_time = time.time() - start_time
            self._update_stats(text, cache_hit=True, processing_time=processing_time)
            return result
        
        # 执行分词
        try:
            # 使用jieba进行分词
            if self._use_hmm:
                segments = list(jieba.lcut(text, HMM=True))
            else:
                segments = list(jieba.lcut(text, HMM=False))
            
            # 更新缓存
            if self._cache_enabled:
                self._cache[cache_key] = segments
                # 检查缓存大小
                if len(self._cache) > self._cache_size:
                    self._clean_cache()
            
            processing_time = time.time() - start_time
            self._update_stats(text, cache_hit=False, processing_time=processing_time)
            
            return segments
            
        except Exception as e:
            # 分词失败，返回单个字符列表
            if self.config.get('verbose', False):
                print(f"jieba分词失败: {e}")
            
            # 回退到按字符分割
            segments = list(text)
            processing_time = time.time() - start_time
            self._update_stats(text, cache_hit=False, processing_time=processing_time)
            
            return segments
    
    def set_user_dict(self, dict_path: str):
        """
        设置用户词典
        
        Args:
            dict_path: 词典文件路径
        """
        try:
            jieba.load_userdict(dict_path)
            self.config['user_dict'] = dict_path
        except Exception as e:
            if self.config.get('verbose', False):
                print(f"加载用户词典失败: {e}")
    
    def add_word(self, word: str, freq: Optional[int] = None, tag: Optional[str] = None):
        """
        添加新词到词典
        
        Args:
            word: 词语
            freq: 词频
            tag: 词性标签
        """
        jieba.add_word(word, freq=freq, tag=tag)


class ThulacTokenizer(BaseTokenizer):
    """THULAC分词器实现"""
    
    def __init__(self, **kwargs):
        """
        初始化THULAC分词器
        
        Args:
            **kwargs: 配置参数
        """
        super().__init__("thulac", **kwargs)
        self._thulac = None
        self._init_thulac()
    
    def _init_thulac(self):
        """初始化THULAC分词器"""
        try:
            import thulac
            # 使用seg_only=True只进行分词，不进行词性标注
            self._thulac = thulac.thulac(
                seg_only=self.config.get('seg_only', True),
                model_path=self.config.get('model_path'),
            )
        except ImportError:
            raise ImportError(
                "THULAC未安装，请使用: pip install thulac\n"
                "或者使用jieba分词器: YanLuTokenizer(segmenter='jieba')"
            )
        
        # 加载用户词典
        user_dict = self.config.get('user_dict')
        if user_dict and hasattr(self._thulac, 'set_user_dict'):
            self._thulac.set_user_dict(user_dict)
    
    def segment(self, text: str) -> List[str]:
        """
        使用THULAC进行分词
        
        Args:
            text: 待分词的文本
            
        Returns:
            分词结果列表
        """
        import time
        start_time = time.time()
        
        # 检查缓存
        cache_key = text
        if self._cache_enabled and cache_key in self._cache:
            result = self._cache[cache_key]
            processing_time = time.time() - start_time
            self._update_stats(text, cache_hit=True, processing_time=processing_time)
            return result
        
        # 执行分词
        try:
            if self._thulac is None:
                self._init_thulac()
            
            # 使用THULAC进行分词
            result = self._thulac.cut(text, text=True)
            segments = result.split()
            
            # 更新缓存
            if self._cache_enabled:
                self._cache[cache_key] = segments
                # 检查缓存大小
                if len(self._cache) > self._cache_size:
                    self._clean_cache()
            
            processing_time = time.time() - start_time
            self._update_stats(text, cache_hit=False, processing_time=processing_time)
            
            return segments
            
        except Exception as e:
            # 分词失败，返回单个字符列表
            if self.config.get('verbose', False):
                print(f"THULAC分词失败: {e}")
            
            # 回退到按字符分割
            segments = list(text)
            processing_time = time.time() - start_time
            self._update_stats(text, cache_hit=False, processing_time=processing_time)
            
            return segments
    
    def set_user_dict(self, dict_path: str):
        """
        设置用户词典
        
        Args:
            dict_path: 词典文件路径
        """
        try:
            if hasattr(self._thulac, 'set_user_dict'):
                self._thulac.set_user_dict(dict_path)
                self.config['user_dict'] = dict_path
        except Exception as e:
            if self.config.get('verbose', False):
                print(f"设置THULAC用户词典失败: {e}")


class YanLuTokenizer:
    """言律语言分词器（工厂类）"""
    
    @staticmethod
    def create(segmenter: str = "jieba", **kwargs) -> ITokenizer:
        """
        创建分词器实例

        Args:
            segmenter: 分词器类型，可选 "jieba"、"thulac" 或 "yanlv_nospace"
            **kwargs: 配置参数

        Returns:
            分词器实例

        Raises:
            ValueError: 不支持的的分词器类型
        """
        if segmenter == "jieba":
            return JiebaTokenizer(**kwargs)
        elif segmenter == "thulac":
            return ThulacTokenizer(**kwargs)
        elif segmenter == "yanlv_nospace":
            return YanLuNoSpaceTokenizer(**kwargs)
        else:
            raise ValueError(f"不支持的的分词器类型: {segmenter}")
    
    @staticmethod
    def get_available_tokenizers() -> List[str]:
        """
        获取可用的分词器列表
        
        Returns:
            可用分词器名称列表
        """
        tokenizers = ["jieba"]
        try:
            import thulac
            tokenizers.append("thulac")
        except ImportError:
            pass
        return tokenizers
    
    @staticmethod
    def get_tokenizer_info(segmenter: str) -> Dict[str, Any]:
        """
        获取分词器信息
        
        Args:
            segmenter: 分词器类型
            
        Returns:
            分词器信息字典
        """
        info = {
            "name": segmenter,
            "available": False,
            "description": "",
            "config_options": {}
        }
        
        if segmenter == "jieba":
            info.update({
                "available": True,
                "description": "结巴中文分词器，支持中文分词",
                "config_options": SEGMENTER_CONFIG.get("jieba", {})
            })
        elif segmenter == "thulac":
            try:
                import thulac
                info.update({
                    "available": True,
                    "description": "清华大学中文分词器，准确率较高",
                    "config_options": SEGMENTER_CONFIG.get("thulac", {})
                })
            except ImportError:
                info.update({
                    "available": False,
                    "description": "THULAC未安装，请使用: pip install thulac"
                })
        
        return info


# 默认分词器工厂函数
def create_tokenizer(segmenter: str = "jieba", **kwargs) -> ITokenizer:
    """
    创建分词器实例（便捷函数）
    
    Args:
        segmenter: 分词器类型，可选 "jieba" 或 "thulac"
        **kwargs: 配置参数
        
    Returns:
        分词器实例
    """
    return YanLuTokenizer.create(segmenter, **kwargs)


def get_available_tokenizers() -> List[str]:
    """
    获取可用的分词器列表（便捷函数）
    
    Returns:
        可用分词器名称列表
    """
    return YanLuTokenizer.get_available_tokenizers()


def get_tokenizer_info(segmenter: str) -> Dict[str, Any]:
    """
    获取分词器信息（便捷函数）

    Args:
        segmenter: 分词器类型

    Returns:
        分词器信息字典
    """
    return YanLuTokenizer.get_tokenizer_info(segmenter)


class YanLuNoSpaceTokenizer(ITokenizer):
    """言律语言无空格分词器 - 支持无空格编程"""

    def __init__(self, **kwargs):
        """初始化分词器"""
        self.config = kwargs
        # 按长度排序关键词（长的优先匹配）
        self.keywords = sorted(KEYWORDS.keys(), key=len, reverse=True)
        # 统计信息
        self._stats = {
            'total_calls': 0,
            'total_chars': 0,
            'total_segments': 0
        }

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

        # 更新统计
        self._stats['total_calls'] += 1
        self._stats['total_chars'] += len(text)
        self._stats['total_segments'] += len(segments)

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

    def get_segmenter_type(self) -> str:
        """获取分词器类型"""
        return "yanlv_nospace"

    def get_config(self) -> Dict[str, Any]:
        """获取配置"""
        return self.config

    def update_config(self, **kwargs):
        """更新配置"""
        self.config.update(kwargs)

    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        return self._stats.copy()

    def reset_stats(self):
        """重置统计信息"""
        self._stats = {
            'total_calls': 0,
            'total_chars': 0,
            'total_segments': 0
        }

    def reset(self):
        """重置分词器状态"""
        self.reset_stats()