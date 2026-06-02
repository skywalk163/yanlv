"""
言律语言json模块扩展
提供json标准库的中文版本
"""

import json
from typing import Any, Optional, Callable, Union
from pathlib import Path


def 转为json字符串(
    对象: Any,
    缩进: Optional[int] = None,
    确保ascii: bool = False,
    排序键: bool = False,
    默认处理: Optional[Callable] = None
) -> str:
    """
    将对象转换为JSON字符串
    
    参数:
        对象: 要转换的对象
        缩进: 缩进空格数（None表示紧凑格式）
        确保ascii: 是否确保ASCII编码
        排序键: 是否排序键
        默认处理: 无法序列化时的处理函数
        
    返回:
        JSON字符串
        
    示例:
        >>> 数据 = {'姓名': '张三', '年龄': 25}
        >>> 转为json字符串(数据, 缩进=2)
        '{\\n  "姓名": "张三",\\n  "年龄": 25\\n}'
    """
    return json.dumps(
        对象,
        indent=缩进,
        ensure_ascii=确保ascii,
        sort_keys=排序键,
        default=默认处理
    )


def 从json字符串(字符串: str) -> Any:
    """
    从JSON字符串解析对象
    
    参数:
        字符串: JSON字符串
        
    返回:
        解析后的对象
        
    示例:
        >>> 从json字符串('{"姓名": "张三", "年龄": 25}')
        {'姓名': '张三', '年龄': 25}
    """
    return json.loads(字符串)


def 保存json文件(
    文件路径: Union[str, Path],
    对象: Any,
    缩进: int = 2,
    确保ascii: bool = False,
    排序键: bool = False,
    编码: str = 'utf-8'
) -> None:
    """
    将对象保存为JSON文件
    
    参数:
        文件路径: 文件路径
        对象: 要保存的对象
        缩进: 缩进空格数
        确保ascii: 是否确保ASCII编码
        排序键: 是否排序键
        编码: 文件编码
        
    示例:
        >>> 数据 = {'姓名': '张三', '年龄': 25}
        >>> 保存json文件('data.json', 数据)
    """
    if isinstance(文件路径, Path):
        文件路径 = str(文件路径)
    
    with open(文件路径, 'w', encoding=编码) as f:
        json.dump(
            对象,
            f,
            indent=缩进,
            ensure_ascii=确保ascii,
            sort_keys=排序键
        )


def 加载json文件(
    文件路径: Union[str, Path],
    编码: str = 'utf-8'
) -> Any:
    """
    从JSON文件加载对象
    
    参数:
        文件路径: 文件路径
        编码: 文件编码
        
    返回:
        加载的对象
        
    示例:
        >>> 数据 = 加载json文件('data.json')
        >>> 打印(数据)
        {'姓名': '张三', '年龄': 25}
    """
    if isinstance(文件路径, Path):
        文件路径 = str(文件路径)
    
    with open(文件路径, 'r', encoding=编码) as f:
        return json.load(f)


def 格式化json(
    字符串或对象: Union[str, Any],
    缩进: int = 2
) -> str:
    """
    格式化JSON
    
    参数:
        字符串或对象: JSON字符串或对象
        缩进: 缩进空格数
        
    返回:
        格式化后的JSON字符串
        
    示例:
        >>> 格式化json('{"姓名":"张三","年龄":25}')
        '{\\n  "姓名": "张三",\\n  "年龄": 25\\n}'
    """
    if isinstance(字符串或对象, str):
        对象 = json.loads(字符串或对象)
    else:
        对象 = 字符串或对象
    
    return json.dumps(对象, indent=缩进, ensure_ascii=False)


def 压缩json(字符串或对象: Union[str, Any]) -> str:
    """
    压缩JSON（移除空白）
    
    参数:
        字符串或对象: JSON字符串或对象
        
    返回:
        压缩后的JSON字符串
        
    示例:
        >>> 压缩json('{\\n  "姓名": "张三",\\n  "年龄": 25\\n}')
        '{"姓名":"张三","年龄":25}'
    """
    if isinstance(字符串或对象, str):
        对象 = json.loads(字符串或对象)
    else:
        对象 = 字符串或对象
    
    return json.dumps(对象, separators=(',', ':'), ensure_ascii=False)


def 验证json(字符串: str) -> bool:
    """
    验证JSON字符串是否有效
    
    参数:
        字符串: JSON字符串
        
    返回:
        是否有效
        
    示例:
        >>> 验证json('{"姓名": "张三"}')
        True
        >>> 验证json('{invalid}')
        False
    """
    try:
        json.loads(字符串)
        return True
    except (json.JSONDecodeError, ValueError):
        return False


def 合并json对象(*对象: dict) -> dict:
    """
    合并多个JSON对象
    
    参数:
        *对象: 要合并的对象
        
    返回:
        合并后的对象
        
    示例:
        >>> 合并json对象({'a': 1}, {'b': 2}, {'c': 3})
        {'a': 1, 'b': 2, 'c': 3}
    """
    结果 = {}
    for obj in 对象:
        结果.update(obj)
    return 结果


def 深度复制json对象(对象: Any) -> Any:
    """
    深度复制JSON对象
    
    参数:
        对象: 要复制的对象
        
    返回:
        复制后的对象
        
    示例:
        >>> 原对象 = {'a': [1, 2, 3]}
        >>> 新对象 = 深度复制json对象(原对象)
        >>> 新对象['a'].append(4)
        >>> 原对象['a']
        [1, 2, 3]
    """
    return json.loads(json.dumps(对象))


def 获取json路径(对象: dict, 路径: str, 默认值: Any = None) -> Any:
    """
    通过路径获取JSON对象中的值
    
    参数:
        对象: JSON对象
        路径: 路径（用.分隔）
        默认值: 默认值
        
    返回:
        找到的值或默认值
        
    示例:
        >>> 数据 = {'用户': {'姓名': '张三', '年龄': 25}}
        >>> 获取json路径(数据, '用户.姓名')
        '张三'
        >>> 获取json路径(数据, '用户.地址', '未知')
        '未知'
    """
    键列表 = 路径.split('.')
    当前 = 对象
    
    for 键 in 键列表:
        if isinstance(当前, dict) and 键 in 当前:
            当前 = 当前[键]
        else:
            return 默认值
    
    return 当前


def 设置json路径(对象: dict, 路径: str, 值: Any) -> dict:
    """
    通过路径设置JSON对象中的值
    
    参数:
        对象: JSON对象
        路径: 路径（用.分隔）
        值: 要设置的值
        
    返回:
        修改后的对象
        
    示例:
        >>> 数据 = {'用户': {'姓名': '张三'}}
        >>> 设置json路径(数据, '用户.年龄', 25)
        {'用户': {'姓名': '张三', '年龄': 25}}
    """
    键列表 = 路径.split('.')
    当前 = 对象
    
    for 键 in 键列表[:-1]:
        if 键 not in 当前:
            当前[键] = {}
        当前 = 当前[键]
    
    当前[键列表[-1]] = 值
    return 对象


# ============================================================================
# 导出所有函数
# ============================================================================

__all__ = [
    '转为json字符串',
    '从json字符串',
    '保存json文件',
    '加载json文件',
    '格式化json',
    '压缩json',
    '验证json',
    '合并json对象',
    '深度复制json对象',
    '获取json路径',
    '设置json路径',
]
