"""
言律语言扩展标准库

提供日期时间、JSON、正则表达式等实用函数
"""

from typing import Any, Dict, List, Optional
import json
import re
from datetime import datetime, timedelta
import hashlib
import random


class DateTimeFunctions:
    """日期时间函数"""
    
    @staticmethod
    def 当前时间() -> str:
        """获取当前时间"""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    @staticmethod
    def 当前日期() -> str:
        """获取当前日期"""
        return datetime.now().strftime("%Y-%m-%d")
    
    @staticmethod
    def 格式化时间(timestamp: str, 格式: str = "%Y-%m-%d %H:%M:%S") -> str:
        """
        格式化时间
        
        Args:
            timestamp: 时间戳字符串
            格式: 格式字符串
            
        Returns:
            格式化后的时间字符串
        """
        try:
            dt = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
            return dt.strftime(格式)
        except:
            return timestamp
    
    @staticmethod
    def 时间差(开始时间: str, 结束时间: str) -> int:
        """
        计算时间差(秒)
        
        Args:
            开始时间: 开始时间字符串
            结束时间: 结束时间字符串
            
        Returns:
            时间差(秒)
        """
        try:
            start = datetime.strptime(开始时间, "%Y-%m-%d %H:%M:%S")
            end = datetime.strptime(结束时间, "%Y-%m-%d %H:%M:%S")
            return int((end - start).total_seconds())
        except:
            return 0


class JSONFunctions:
    """JSON函数"""
    
    @staticmethod
    def 解析JSON(json字符串: str) -> Any:
        """
        解析JSON字符串
        
        Args:
            json字符串: JSON格式字符串
            
        Returns:
            解析后的对象
        """
        try:
            return json.loads(json字符串)
        except:
            return None
    
    @staticmethod
    def 生成JSON(对象: Any, 缩进: int = 2) -> str:
        """
        生成JSON字符串
        
        Args:
            对象: 要转换的对象
            缩进: 缩进空格数
            
        Returns:
            JSON字符串
        """
        try:
            return json.dumps(对象, ensure_ascii=False, indent=缩进)
        except:
            return ""
    
    @staticmethod
    def 美化JSON(json字符串: str) -> str:
        """
        美化JSON字符串
        
        Args:
            json字符串: JSON格式字符串
            
        Returns:
            美化后的JSON字符串
        """
        try:
            obj = json.loads(json字符串)
            return json.dumps(obj, ensure_ascii=False, indent=2)
        except:
            return json字符串


class RegexFunctions:
    """正则表达式函数"""
    
    @staticmethod
    def 匹配(文本: str, 模式: str) -> bool:
        """
        检查是否匹配
        
        Args:
            文本: 要检查的文本
            模式: 正则表达式模式
            
        Returns:
            是否匹配
        """
        try:
            return bool(re.search(模式, 文本))
        except:
            return False
    
    @staticmethod
    def 查找所有(文本: str, 模式: str) -> List[str]:
        """
        查找所有匹配
        
        Args:
            文本: 要搜索的文本
            模式: 正则表达式模式
            
        Returns:
            匹配列表
        """
        try:
            return re.findall(模式, 文本)
        except:
            return []
    
    @staticmethod
    def 替换(文本: str, 模式: str, 替换文本: str) -> str:
        """
        替换匹配文本
        
        Args:
            文本: 原文本
            模式: 正则表达式模式
            替换文本: 替换后的文本
            
        Returns:
            替换后的文本
        """
        try:
            return re.sub(模式, 替换文本, 文本)
        except:
            return 文本
    
    @staticmethod
    def 分割(文本: str, 模式: str) -> List[str]:
        """
        按模式分割文本
        
        Args:
            文本: 要分割的文本
            模式: 正则表达式模式
            
        Returns:
            分割后的列表
        """
        try:
            return re.split(模式, 文本)
        except:
            return [文本]


class CryptoFunctions:
    """加密函数"""
    
    @staticmethod
    def MD5哈希(文本: str) -> str:
        """
        计算MD5哈希
        
        Args:
            文本: 要哈希的文本
            
        Returns:
            MD5哈希值
        """
        return hashlib.md5(文本.encode()).hexdigest()
    
    @staticmethod
    def SHA256哈希(文本: str) -> str:
        """
        计算SHA256哈希
        
        Args:
            文本: 要哈希的文本
            
        Returns:
            SHA256哈希值
        """
        return hashlib.sha256(文本.encode()).hexdigest()


class RandomFunctions:
    """随机数函数"""
    
    @staticmethod
    def 随机整数(最小值: int, 最大值: int) -> int:
        """
        生成随机整数
        
        Args:
            最小值: 最小值
            最大值: 最大值
            
        Returns:
            随机整数
        """
        return random.randint(最小值, 最大值)
    
    @staticmethod
    def 随机浮点数(最小值: float, 最大值: float) -> float:
        """
        生成随机浮点数
        
        Args:
            最小值: 最小值
            最大值: 最大值
            
        Returns:
            随机浮点数
        """
        return random.uniform(最小值, 最大值)
    
    @staticmethod
    def 随机选择(列表: List[Any]) -> Any:
        """
        从列表中随机选择
        
        Args:
            列表: 要选择的列表
            
        Returns:
            随机选择的元素
        """
        if not 列表:
            return None
        return random.choice(列表)
    
    @staticmethod
    def 打乱顺序(列表: List[Any]) -> List[Any]:
        """
        打乱列表顺序
        
        Args:
            列表: 要打乱的列表
            
        Returns:
            打乱后的列表
        """
        result = 列表.copy()
        random.shuffle(result)
        return result


class StringFunctions:
    """字符串函数"""
    
    @staticmethod
    def 去除空白(文本: str) -> str:
        """去除首尾空白"""
        return 文本.strip()
    
    @staticmethod
    def 转大写(文本: str) -> str:
        """转换为大写"""
        return 文本.upper()
    
    @staticmethod
    def 转小写(文本: str) -> str:
        """转换为小写"""
        return 文本.lower()
    
    @staticmethod
    def 首字母大写(文本: str) -> str:
        """首字母大写"""
        return 文本.capitalize()
    
    @staticmethod
    def 是否包含(文本: str, 子串: str) -> bool:
        """检查是否包含子串"""
        return 子串 in 文本
    
    @staticmethod
    def 统计出现(文本: str, 子串: str) -> int:
        """统计子串出现次数"""
        return 文本.count(子串)


# 创建全局实例
datetime_funcs = DateTimeFunctions()
json_funcs = JSONFunctions()
regex_funcs = RegexFunctions()
crypto_funcs = CryptoFunctions()
random_funcs = RandomFunctions()
string_funcs = StringFunctions()
