"""
言律语言csv模块扩展
提供csv标准库的中文版本
"""

import csv
from typing import List, Dict, Any, Optional, Union
from pathlib import Path


def 读取csv文件(
    文件路径: Union[str, Path],
    编码: str = 'utf-8',
    分隔符: str = ',',
    引用符: str = '"',
    是否有标题: bool = True
) -> List[Dict[str, Any]]:
    """
    读取CSV文件
    
    参数:
        文件路径: CSV文件路径
        编码: 文件编码
        分隔符: 字段分隔符
        引用符: 引用字符
        是否有标题: 是否有标题行
        
    返回:
        数据列表（字典形式）
        
    示例:
        >>> 数据 = 读取csv文件('data.csv')
        >>> 数据[0]['姓名']
        '张三'
    """
    if isinstance(文件路径, Path):
        文件路径 = str(文件路径)
    
    数据列表 = []
    with open(文件路径, 'r', encoding=编码, newline='') as 文件:
        if 是否有标题:
            读取器 = csv.DictReader(文件, delimiter=分隔符, quotechar=引用符)
            for 行 in 读取器:
                数据列表.append(dict(行))
        else:
            读取器 = csv.reader(文件, delimiter=分隔符, quotechar=引用符)
            for 行 in 读取器:
                数据列表.append(行)
    
    return 数据列表


def 写入csv文件(
    文件路径: Union[str, Path],
    数据: List[Dict[str, Any]],
    编码: str = 'utf-8',
    分隔符: str = ',',
    引用符: str = '"',
    标题行: Optional[List[str]] = None
) -> None:
    """
    写入CSV文件
    
    参数:
        文件路径: CSV文件路径
        数据: 要写入的数据
        编码: 文件编码
        分隔符: 字段分隔符
        引用符: 引用字符
        标题行: 标题行（None表示自动从数据中获取）
        
    示例:
        >>> 数据 = [{'姓名': '张三', '年龄': 25}, {'姓名': '李四', '年龄': 30}]
        >>> 写入csv文件('output.csv', 数据)
    """
    if isinstance(文件路径, Path):
        文件路径 = str(文件路径)
    
    if not 数据:
        return
    
    with open(文件路径, 'w', encoding=编码, newline='') as 文件:
        if isinstance(数据[0], dict):
            if 标题行 is None:
                标题行 = list(数据[0].keys())
            写入器 = csv.DictWriter(文件, fieldnames=标题行, delimiter=分隔符, quotechar=引用符)
            写入器.writeheader()
            写入器.writerows(数据)
        else:
            写入器 = csv.writer(文件, delimiter=分隔符, quotechar=引用符)
            写入器.writerows(数据)


def 追加csv行(
    文件路径: Union[str, Path],
    行数据: Dict[str, Any],
    编码: str = 'utf-8',
    分隔符: str = ',',
    引用符: str = '"'
) -> None:
    """
    追加一行到CSV文件
    
    参数:
        文件路径: CSV文件路径
        行数据: 要追加的行数据
        编码: 文件编码
        分隔符: 字段分隔符
        引用符: 引用字符
        
    示例:
        >>> 追加csv行('data.csv', {'姓名': '王五', '年龄': 28})
    """
    if isinstance(文件路径, Path):
        文件路径 = str(文件路径)
    
    with open(文件路径, 'a', encoding=编码, newline='') as 文件:
        写入器 = csv.DictWriter(文件, fieldnames=行数据.keys(), delimiter=分隔符, quotechar=引用符)
        写入器.writerow(行数据)


def 解析csv字符串(
    字符串: str,
    分隔符: str = ',',
    引用符: str = '"'
) -> List[List[str]]:
    """
    解析CSV字符串
    
    参数:
        字符串: CSV格式字符串
        分隔符: 字段分隔符
        引用符: 引用字符
        
    返回:
        解析后的数据列表
        
    示例:
        >>> 解析csv字符串('a,b,c\\n1,2,3')
        [['a', 'b', 'c'], ['1', '2', '3']]
    """
    import io
    数据列表 = []
    读取器 = csv.reader(io.StringIO(字符串), delimiter=分隔符, quotechar=引用符)
    for 行 in 读取器:
        数据列表.append(行)
    return 数据列表


def 生成csv字符串(
    数据: List[List[str]],
    分隔符: str = ',',
    引用符: str = '"'
) -> str:
    """
    生成CSV字符串
    
    参数:
        数据: 数据列表
        分隔符: 字段分隔符
        引用符: 引用字符
        
    返回:
        CSV格式字符串
        
    示例:
        >>> 生成csv字符串([['a', 'b'], ['1', '2']])
        'a,b\\r\\n1,2\\r\\n'
    """
    import io
    输出 = io.StringIO()
    写入器 = csv.writer(输出, delimiter=分隔符, quotechar=引用符)
    写入器.writerows(数据)
    return 输出.getvalue()


def 获取csv列(
    数据: List[Dict[str, Any]],
    列名: str
) -> List[Any]:
    """
    从CSV数据中提取指定列
    
    参数:
        数据: CSV数据
        列名: 列名
        
    返回:
        该列的所有值
        
    示例:
        >>> 数据 = [{'姓名': '张三', '年龄': 25}, {'姓名': '李四', '年龄': 30}]
        >>> 获取csv列(数据, '姓名')
        ['张三', '李四']
    """
    return [行[列名] for 行 in 数据]


def 过滤csv行(
    数据: List[Dict[str, Any]],
    条件函数: callable
) -> List[Dict[str, Any]]:
    """
    过滤CSV行
    
    参数:
        数据: CSV数据
        条件函数: 过滤条件函数
        
    返回:
        过滤后的数据
        
    示例:
        >>> 数据 = [{'姓名': '张三', '年龄': 25}, {'姓名': '李四', '年龄': 30}]
        >>> 过滤csv行(数据, lambda 行: 行['年龄'] > 26)
        [{'姓名': '李四', '年龄': 30}]
    """
    return [行 for 行 in 数据 if 条件函数(行)]


def 排序csv数据(
    数据: List[Dict[str, Any]],
    排序列: str,
    降序: bool = False
) -> List[Dict[str, Any]]:
    """
    排序CSV数据
    
    参数:
        数据: CSV数据
        排序列: 排序列名
        降序: 是否降序
        
    返回:
        排序后的数据
        
    示例:
        >>> 数据 = [{'姓名': '张三', '年龄': 30}, {'姓名': '李四', '年龄': 25}]
        >>> 排序csv数据(数据, '年龄')
        [{'姓名': '李四', '年龄': 25}, {'姓名': '张三', '年龄': 30}]
    """
    return sorted(数据, key=lambda 行: 行[排序列], reverse=降序)


def 合并csv文件(
    输出文件: Union[str, Path],
    输入文件列表: List[Union[str, Path]],
    编码: str = 'utf-8'
) -> None:
    """
    合并多个CSV文件
    
    参数:
        输出文件: 输出文件路径
        输入文件列表: 输入文件路径列表
        编码: 文件编码
        
    示例:
        >>> 合并csv文件('merged.csv', ['file1.csv', 'file2.csv'])
    """
    所有数据 = []
    for 文件路径 in 输入文件列表:
        数据 = 读取csv文件(文件路径, 编码=编码)
        所有数据.extend(数据)
    
    写入csv文件(输出文件, 所有数据, 编码=编码)


def csv转json(
    csv文件路径: Union[str, Path],
    json文件路径: Union[str, Path],
    编码: str = 'utf-8'
) -> None:
    """
    将CSV文件转换为JSON文件
    
    参数:
        csv文件路径: CSV文件路径
        json文件路径: JSON文件路径
        编码: 文件编码
        
    示例:
        >>> csv转json('data.csv', 'data.json')
    """
    from .json_ext import 保存json文件
    
    数据 = 读取csv文件(csv文件路径, 编码=编码)
    保存json文件(json文件路径, 数据, 编码=编码)


# ============================================================================
# 导出所有函数
# ============================================================================

__all__ = [
    '读取csv文件',
    '写入csv文件',
    '追加csv行',
    '解析csv字符串',
    '生成csv字符串',
    '获取csv列',
    '过滤csv行',
    '排序csv数据',
    '合并csv文件',
    'csv转json',
]
