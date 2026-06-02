"""
言律语言re模块扩展
提供re标准库的中文版本
"""

import re
from typing import Optional, List, Union, Pattern


def 编译正则(
    模式: str,
    忽略大小写: bool = False,
    多行模式: bool = False,
    点匹配换行: bool = False,
    详细模式: bool = False
) -> Pattern:
    """
    编译正则表达式模式
    
    参数:
        模式: 正则表达式字符串
        忽略大小写: 是否忽略大小写
        多行模式: 是否启用多行模式
        点匹配换行: 是否让.匹配换行符
        详细模式: 是否启用详细模式（允许注释）
        
    返回:
        编译后的正则表达式对象
        
    示例:
        >>> 模式 = 编译正则(r'\\d+')
        >>> 模式.findall('abc123def456')
        ['123', '456']
    """
    flags = 0
    if 忽略大小写:
        flags |= re.IGNORECASE
    if 多行模式:
        flags |= re.MULTILINE
    if 点匹配换行:
        flags |= re.DOTALL
    if 详细模式:
        flags |= re.VERBOSE
    
    return re.compile(模式, flags)


def 匹配(
    模式: Union[str, Pattern],
    字符串: str,
    忽略大小写: bool = False
) -> Optional[re.Match]:
    """
    从字符串开头匹配正则表达式
    
    参数:
        模式: 正则表达式字符串或编译对象
        字符串: 要匹配的字符串
        忽略大小写: 是否忽略大小写
        
    返回:
        匹配对象或None
        
    示例:
        >>> 结果 = 匹配(r'hello', 'hello world')
        >>> 结果.group()
        'hello'
    """
    flags = re.IGNORECASE if 忽略大小写 else 0
    if isinstance(模式, str):
        return re.match(模式, 字符串, flags)
    return 模式.match(字符串)


def 搜索(
    模式: Union[str, Pattern],
    字符串: str,
    忽略大小写: bool = False
) -> Optional[re.Match]:
    """
    在字符串中搜索正则表达式的第一个匹配
    
    参数:
        模式: 正则表达式字符串或编译对象
        字符串: 要搜索的字符串
        忽略大小写: 是否忽略大小写
        
    返回:
        匹配对象或None
        
    示例:
        >>> 结果 = 搜索(r'\\d+', 'abc123def')
        >>> 结果.group()
        '123'
    """
    flags = re.IGNORECASE if 忽略大小写 else 0
    if isinstance(模式, str):
        return re.search(模式, 字符串, flags)
    return 模式.search(字符串)


def 查找所有(
    模式: Union[str, Pattern],
    字符串: str,
    忽略大小写: bool = False
) -> List[str]:
    """
    查找字符串中所有匹配的子串
    
    参数:
        模式: 正则表达式字符串或编译对象
        字符串: 要搜索的字符串
        忽略大小写: 是否忽略大小写
        
    返回:
        匹配的子串列表
        
    示例:
        >>> 查找所有(r'\\d+', 'abc123def456ghi789')
        ['123', '456', '789']
    """
    flags = re.IGNORECASE if 忽略大小写 else 0
    if isinstance(模式, str):
        return re.findall(模式, 字符串, flags)
    return 模式.findall(字符串)


def 查找所有匹配(
    模式: Union[str, Pattern],
    字符串: str,
    忽略大小写: bool = False
) -> List[re.Match]:
    """
    查找字符串中所有匹配，返回匹配对象迭代器
    
    参数:
        模式: 正则表达式字符串或编译对象
        字符串: 要搜索的字符串
        忽略大小写: 是否忽略大小写
        
    返回:
        匹配对象列表
        
    示例:
        >>> for 匹配 in 查找所有匹配(r'\\d+', 'abc123def456'):
        ...     print(匹配.group())
        123
        456
    """
    flags = re.IGNORECASE if 忽略大小写 else 0
    if isinstance(模式, str):
        return list(re.finditer(模式, 字符串, flags))
    return list(模式.finditer(字符串))


def 替换(
    模式: Union[str, Pattern],
    替换内容: Union[str, callable],
    字符串: str,
    次数: int = 0,
    忽略大小写: bool = False
) -> str:
    """
    替换字符串中匹配的子串
    
    参数:
        模式: 正则表达式字符串或编译对象
        替换内容: 替换字符串或函数
        字符串: 要处理的字符串
        次数: 最大替换次数（0表示全部）
        忽略大小写: 是否忽略大小写
        
    返回:
        替换后的字符串
        
    示例:
        >>> 替换(r'\\d+', 'NUM', 'abc123def456')
        'abcNUMdefNUM'
    """
    flags = re.IGNORECASE if 忽略大小写 else 0
    if isinstance(模式, str):
        return re.sub(模式, 替换内容, 字符串, count=次数, flags=flags)
    return 模式.sub(替换内容, 字符串, count=次数)


def 分割(
    模式: Union[str, Pattern],
    字符串: str,
    最大分割数: int = 0,
    忽略大小写: bool = False
) -> List[str]:
    """
    根据正则表达式分割字符串
    
    参数:
        模式: 正则表达式字符串或编译对象
        字符串: 要分割的字符串
        最大分割数: 最大分割次数（0表示不限）
        忽略大小写: 是否忽略大小写
        
    返回:
        分割后的字符串列表
        
    示例:
        >>> 分割(r'\\s+', 'hello  world\\tfrom\\npython')
        ['hello', 'world', 'from', 'python']
    """
    flags = re.IGNORECASE if 忽略大小写 else 0
    if isinstance(模式, str):
        return re.split(模式, 字符串, maxsplit=最大分割数, flags=flags)
    return 模式.split(字符串, maxsplit=最大分割数)


def 转义(字符串: str) -> str:
    """
    转义字符串中的特殊字符
    
    参数:
        字符串: 要转义的字符串
        
    返回:
        转义后的字符串
        
    示例:
        >>> 转义('a.b*c+d')
        'a\\.b\\*c\\+d'
    """
    return re.escape(字符串)


def 提取分组(
    模式: Union[str, Pattern],
    字符串: str,
    分组编号: int = 0
) -> Optional[str]:
    """
    提取匹配的分组内容
    
    参数:
        模式: 正则表达式字符串或编译对象
        字符串: 要匹配的字符串
        分组编号: 分组编号（0表示整个匹配）
        
    返回:
        分组内容或None
        
    示例:
        >>> 提取分组(r'(\\d+)-(\\d+)', 'abc123-456def', 1)
        '123'
    """
    匹配结果 = 搜索(模式, 字符串)
    if 匹配结果:
        try:
            return 匹配结果.group(分组编号)
        except IndexError:
            return None
    return None


def 提取所有分组(
    模式: Union[str, Pattern],
    字符串: str
) -> List[tuple]:
    """
    提取所有匹配的分组内容
    
    参数:
        模式: 正则表达式字符串或编译对象
        字符串: 要匹配的字符串
        
    返回:
        分组元组列表
        
    示例:
        >>> 提取所有分组(r'(\\d+)-(\\d+)', 'abc123-456def789-012')
        [('123', '456'), ('789', '012')]
    """
    return 查找所有(模式, 字符串)


def 是否匹配(
    模式: Union[str, Pattern],
    字符串: str,
    忽略大小写: bool = False
) -> bool:
    """
    检查字符串是否匹配正则表达式
    
    参数:
        模式: 正则表达式字符串或编译对象
        字符串: 要检查的字符串
        忽略大小写: 是否忽略大小写
        
    返回:
        是否匹配
        
    示例:
        >>> 是否匹配(r'\\d+', '123')
        True
        >>> 是否匹配(r'\\d+', 'abc')
        False
    """
    return 搜索(模式, 字符串, 忽略大小写) is not None


def 计算匹配数(
    模式: Union[str, Pattern],
    字符串: str,
    忽略大小写: bool = False
) -> int:
    """
    计算匹配的次数
    
    参数:
        模式: 正则表达式字符串或编译对象
        字符串: 要搜索的字符串
        忽略大小写: 是否忽略大小写
        
    返回:
        匹配次数
        
    示例:
        >>> 计算匹配数(r'\\d+', 'abc123def456ghi789')
        3
    """
    return len(查找所有(模式, 字符串, 忽略大小写))


# ============================================================================
# 常用正则表达式模式
# ============================================================================

数字模式 = r'\d+'
字母模式 = r'[a-zA-Z]+'
中文模式 = r'[\u4e00-\u9fa5]+'
邮箱模式 = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
手机号模式 = r'1[3-9]\d{9}'
身份证模式 = r'\d{17}[\dXx]'
网址模式 = r'https?://[^\s]+'
IP地址模式 = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,}'
空白字符模式 = r'\s+'


# ============================================================================
# 导出所有函数和常量
# ============================================================================

__all__ = [
    # 编译和匹配
    '编译正则', '匹配', '搜索',
    
    # 查找
    '查找所有', '查找所有匹配',
    
    # 替换和分割
    '替换', '分割',
    
    # 工具函数
    '转义', '提取分组', '提取所有分组',
    '是否匹配', '计算匹配数',
    
    # 常用模式
    '数字模式', '字母模式', '中文模式', '邮箱模式',
    '手机号模式', '身份证模式', '网址模式', 'IP地址模式',
    '空白字符模式',
]
