"""
言律语言glob模块扩展
提供glob标准库的中文版本
"""

import glob
from typing import List, Iterator
from pathlib import Path


def 查找文件(
    模式: str,
    递归: bool = False,
    包含隐藏文件: bool = False
) -> List[str]:
    """
    根据模式查找文件
    
    参数:
        模式: 文件模式（支持通配符*和?）
        递归: 是否递归查找（支持**）
        包含隐藏文件: 是否包含隐藏文件
        
    返回:
        匹配的文件路径列表
        
    示例:
        >>> 查找文件('*.txt')
        ['file1.txt', 'file2.txt']
        >>> 查找文件('**/*.py', 递归=True)
        ['src/main.py', 'src/utils/helper.py']
    """
    if 递归:
        文件列表 = glob.glob(模式, recursive=True)
    else:
        文件列表 = glob.glob(模式)
    
    if not 包含隐藏文件:
        文件列表 = [f for f in 文件列表 if not Path(f).name.startswith('.')]
    
    return 文件列表


def 查找文件迭代器(
    模式: str,
    递归: bool = False
) -> Iterator[str]:
    """
    根据模式查找文件（返回迭代器）
    
    参数:
        模式: 文件模式
        递归: 是否递归查找
        
    返回:
        文件路径迭代器
        
    示例:
        >>> for 文件 in 查找文件迭代器('*.txt'):
        ...     print(文件)
    """
    if 递归:
        return glob.iglob(模式, recursive=True)
    return glob.iglob(模式)


def 查找所有Python文件(目录: str = '.', 递归: bool = True) -> List[str]:
    """
    查找所有Python文件
    
    参数:
        目录: 搜索目录
        递归: 是否递归查找
        
    返回:
        Python文件列表
        
    示例:
        >>> 查找所有Python文件()
        ['main.py', 'utils.py']
    """
    模式 = '**/*.py' if 递归 else '*.py'
    完整模式 = f'{目录}/{模式}' if 目录 != '.' else 模式
    return 查找文件(完整模式, 递归=递归)


def 查找所有文本文件(目录: str = '.', 递归: bool = True) -> List[str]:
    """
    查找所有文本文件
    
    参数:
        目录: 搜索目录
        递归: 是否递归查找
        
    返回:
        文本文件列表
    """
    模式 = '**/*.txt' if 递归 else '*.txt'
    完整模式 = f'{目录}/{模式}' if 目录 != '.' else 模式
    return 查找文件(完整模式, 递归=递归)


def 查找所有图片文件(目录: str = '.', 递归: bool = True) -> List[str]:
    """
    查找所有图片文件
    
    参数:
        目录: 搜索目录
        递归: 是否递归查找
        
    返回:
        图片文件列表
    """
    图片扩展名 = ['*.jpg', '*.jpeg', '*.png', '*.gif', '*.bmp', '*.svg']
    结果 = []
    
    for 扩展名 in 图片扩展名:
        模式 = f'**/{扩展名}' if 递归 else 扩展名
        完整模式 = f'{目录}/{模式}' if 目录 != '.' else 模式
        结果.extend(查找文件(完整模式, 递归=递归))
    
    return 结果


def 查找所有代码文件(目录: str = '.', 递归: bool = True) -> List[str]:
    """
    查找所有代码文件
    
    参数:
        目录: 搜索目录
        递归: 是否递归查找
        
    返回:
        代码文件列表
    """
    代码扩展名 = ['*.py', '*.js', '*.java', '*.cpp', '*.c', '*.go', '*.rs', '*.ts']
    结果 = []
    
    for 扩展名 in 代码扩展名:
        模式 = f'**/{扩展名}' if 递归 else 扩展名
        完整模式 = f'{目录}/{模式}' if 目录 != '.' else 模式
        结果.extend(查找文件(完整模式, 递归=递归))
    
    return 结果


def 查找空目录(目录: str = '.') -> List[str]:
    """
    查找空目录
    
    参数:
        目录: 搜索目录
        
    返回:
        空目录列表
    """
    import os
    空目录列表 = []
    
    for 根目录, 子目录, 文件 in os.walk(目录):
        if not 子目录 and not 文件:
            空目录列表.append(根目录)
    
    return 空目录列表


def 查找大文件(
    目录: str = '.',
    最小大小MB: float = 10,
    递归: bool = True
) -> List[tuple]:
    """
    查找大文件
    
    参数:
        目录: 搜索目录
        最小大小MB: 最小文件大小（MB）
        递归: 是否递归查找
        
    返回:
        (文件路径, 大小MB)列表
    """
    import os
    大文件列表 = []
    最小大小字节 = 最小大小MB * 1024 * 1024
    
    模式 = '**/*' if 递归 else '*'
    完整模式 = f'{目录}/{模式}' if 目录 != '.' else 模式
    
    for 文件路径 in 查找文件(完整模式, 递归=递归):
        if os.path.isfile(文件路径):
            大小 = os.path.getsize(文件路径)
            if 大小 >= 最小大小字节:
                大小MB = 大小 / (1024 * 1024)
                大文件列表.append((文件路径, 大小MB))
    
    return 大文件列表


def 查找重复文件(目录: str = '.') -> dict:
    """
    查找重复文件（基于文件大小）
    
    参数:
        目录: 搜索目录
        
    返回:
        {大小: [文件列表]}字典
    """
    import os
    from collections import defaultdict
    
    大小字典 = defaultdict(list)
    
    for 文件路径 in 查找文件(f'{目录}/**/*', 递归=True):
        if os.path.isfile(文件路径):
            大小 = os.path.getsize(文件路径)
            大小字典[大小].append(文件路径)
    
    # 只返回有重复的大小
    return {k: v for k, v in 大小字典.items() if len(v) > 1}


def 统计文件类型(目录: str = '.', 递归: bool = True) -> dict:
    """
    统计文件类型
    
    参数:
        目录: 搜索目录
        递归: 是否递归查找
        
    返回:
        {扩展名: 数量}字典
    """
    from collections import defaultdict
    import os
    
    类型统计 = defaultdict(int)
    
    模式 = '**/*' if 递归 else '*'
    完整模式 = f'{目录}/{模式}' if 目录 != '.' else 模式
    
    for 文件路径 in 查找文件(完整模式, 递归=递归):
        if os.path.isfile(文件路径):
            扩展名 = Path(文件路径).suffix.lower()
            if not 扩展名:
                扩展名 = '无扩展名'
            类型统计[扩展名] += 1
    
    return dict(类型统计)


# ============================================================================
# 导出所有函数
# ============================================================================

__all__ = [
    '查找文件',
    '查找文件迭代器',
    '查找所有Python文件',
    '查找所有文本文件',
    '查找所有图片文件',
    '查找所有代码文件',
    '查找空目录',
    '查找大文件',
    '查找重复文件',
    '统计文件类型',
]
