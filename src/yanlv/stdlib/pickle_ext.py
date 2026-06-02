"""
言律语言pickle模块扩展
提供pickle标准库的中文版本
"""

import pickle
from typing import Any, Optional
from pathlib import Path


def 序列化对象(
    对象: Any,
    协议版本: Optional[int] = None,
    固定顺序: bool = False
) -> bytes:
    """
    将对象序列化为字节
    
    参数:
        对象: 要序列化的对象
        协议版本: pickle协议版本（None表示最高版本）
        固定顺序: 是否固定字典顺序
        
    返回:
        序列化后的字节
        
    示例:
        >>> 数据 = {'姓名': '张三', '年龄': 25}
        >>> 字节 = 序列化对象(数据)
    """
    return pickle.dumps(对象, protocol=协议版本, fix_imports=固定顺序)


def 反序列化对象(
    字节: bytes,
    编码: str = 'ASCII',
    错误处理: str = 'strict'
) -> Any:
    """
    从字节反序列化对象
    
    参数:
        字节: 序列化的字节
        编码: 编码方式
        错误处理: 错误处理方式
        
    返回:
        反序列化后的对象
        
    示例:
        >>> 字节 = 序列化对象({'姓名': '张三'})
        >>> 数据 = 反序列化对象(字节)
        >>> 数据
        {'姓名': '张三'}
    """
    return pickle.loads(字节, encoding=编码, errors=错误处理)


def 保存对象到文件(
    文件路径: str,
    对象: Any,
    协议版本: Optional[int] = None,
    固定顺序: bool = False
) -> None:
    """
    将对象保存到文件
    
    参数:
        文件路径: 文件路径
        对象: 要保存的对象
        协议版本: pickle协议版本
        固定顺序: 是否固定字典顺序
        
    示例:
        >>> 数据 = {'姓名': '张三', '年龄': 25}
        >>> 保存对象到文件('data.pkl', 数据)
    """
    with open(文件路径, 'wb') as 文件:
        pickle.dump(对象, 文件, protocol=协议版本, fix_imports=固定顺序)


def 从文件加载对象(
    文件路径: str,
    编码: str = 'ASCII',
    错误处理: str = 'strict'
) -> Any:
    """
    从文件加载对象
    
    参数:
        文件路径: 文件路径
        编码: 编码方式
        错误处理: 错误处理方式
        
    返回:
        加载的对象
        
    示例:
        >>> 数据 = 从文件加载对象('data.pkl')
        >>> 数据
        {'姓名': '张三', '年龄': 25}
    """
    with open(文件路径, 'rb') as 文件:
        return pickle.load(文件, encoding=编码, errors=错误处理)


def 获取协议版本() -> int:
    """
    获取最高pickle协议版本
    
    返回:
        最高协议版本号
        
    示例:
        >>> 获取协议版本()
        5
    """
    return pickle.HIGHEST_PROTOCOL


def 获取默认协议版本() -> int:
    """
    获取默认pickle协议版本
    
    返回:
        默认协议版本号
    """
    return pickle.DEFAULT_PROTOCOL


def 计算对象大小(对象: Any) -> int:
    """
    计算对象序列化后的大小
    
    参数:
        对象: 要计算的对象
        
    返回:
        序列化后的字节大小
        
    示例:
        >>> 计算对象大小({'姓名': '张三'})
        45
    """
    return len(序列化对象(对象))


def 深度复制对象(对象: Any) -> Any:
    """
    使用pickle深度复制对象
    
    参数:
        对象: 要复制的对象
        
    返回:
        复制后的对象
        
    示例:
        >>> 原对象 = {'数据': [1, 2, 3]}
        >>> 新对象 = 深度复制对象(原对象)
        >>> 新对象['数据'].append(4)
        >>> 原对象['数据']
        [1, 2, 3]
    """
    return 反序列化对象(序列化对象(对象))


def 是否可序列化(对象: Any) -> bool:
    """
    检查对象是否可序列化
    
    参数:
        对象: 要检查的对象
        
    返回:
        是否可序列化
        
    示例:
        >>> 是否可序列化({'姓名': '张三'})
        True
        >>> 是否可序列化(lambda x: x)
        False
    """
    try:
        序列化对象(对象)
        return True
    except (pickle.PicklingError, TypeError):
        return False


def 合并序列化对象(*对象列表: Any) -> bytes:
    """
    合并多个对象为一个序列化字节流
    
    参数:
        *对象列表: 要合并的对象
        
    返回:
        合并后的字节流
        
    示例:
        >>> 字节流 = 合并序列化对象({'a': 1}, {'b': 2})
    """
    import io
    缓冲区 = io.BytesIO()
    
    for 对象 in 对象列表:
        pickle.dump(对象, 缓冲区)
    
    return 缓冲区.getvalue()


def 从字节流加载多个对象(字节流: bytes) -> list:
    """
    从字节流加载多个对象
    
    参数:
        字节流: 序列化的字节流
        
    返回:
        对象列表
        
    示例:
        >>> 字节流 = 合并序列化对象({'a': 1}, {'b': 2})
        >>> 对象列表 = 从字节流加载多个对象(字节流)
        >>> 对象列表
        [{'a': 1}, {'b': 2}]
    """
    import io
    缓冲区 = io.BytesIO(字节流)
    对象列表 = []
    
    while True:
        try:
            对象 = pickle.load(缓冲区)
            对象列表.append(对象)
        except EOFError:
            break
    
    return 对象列表


# ============================================================================
# 导出所有函数
# ============================================================================

__all__ = [
    '序列化对象',
    '反序列化对象',
    '保存对象到文件',
    '从文件加载对象',
    '获取协议版本',
    '获取默认协议版本',
    '计算对象大小',
    '深度复制对象',
    '是否可序列化',
    '合并序列化对象',
    '从字节流加载多个对象',
]
