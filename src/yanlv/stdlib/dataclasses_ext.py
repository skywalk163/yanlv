"""
言律语言dataclasses模块扩展
提供dataclasses标准库的中文版本
"""

from dataclasses import dataclass, field, Field, asdict, astuple, replace
from typing import Any, Optional, List, Dict, Type


def 数据类(
    类对象: Optional[Type] = None,
    *,
    不可变: bool = False,
    生成字典方法: bool = True,
    生成元组方法: bool = True,
    生成初始化方法: bool = True,
    生成表示方法: bool = True,
    生成比较方法: bool = True,
    生成哈希方法: Optional[bool] = None,
    排序: bool = False
):
    """
    数据类装饰器
    
    参数:
        类对象: 要装饰的类
        不可变: 是否创建不可变数据类
        生成字典方法: 是否生成__dict__方法
        生成元组方法: 是否生成__tuple__方法
        生成初始化方法: 是否生成__init__方法
        生成表示方法: 是否生成__repr__方法
        生成比较方法: 是否生成比较方法
        生成哈希方法: 是否生成__hash__方法
        排序: 是否生成排序方法
        
    返回:
        装饰后的类
        
    示例:
        >>> @数据类
        ... class 人:
        ...     姓名: str
        ...     年龄: int
        >>> p = 人('张三', 25)
        >>> p.姓名
        '张三'
    """
    def 装饰器(cls):
        return dataclass(
            cls,
            frozen=不可变,
            dict=生成字典方法,
            tuple=生成元组方法,
            init=生成初始化方法,
            repr=生成表示方法,
            eq=生成比较方法,
            hash=生成哈希方法,
            order=排序
        )
    
    if 类对象 is None:
        return 装饰器
    return 装饰器(类对象)


def 字段(
    默认值: Any = None,
    默认工厂: Optional[callable] = None,
    表示: bool = True,
    比较: bool = True,
    哈希: Optional[bool] = None,
    初始化: bool = True
) -> Any:
    """
    定义数据类字段
    
    参数:
        默认值: 字段默认值
        默认工厂: 默认值工厂函数
        表示: 是否包含在repr中
        比较: 是否参与比较
        哈希: 是否参与哈希
        初始化: 是否在__init__中
        
    返回:
        字段定义
        
    示例:
        >>> @数据类
        ... class 配置:
        ...     名称: str
        ...     选项: list = 字段(默认工厂=list)
    """
    return field(
        default=默认值,
        default_factory=默认工厂,
        repr=表示,
        compare=比较,
        hash=哈希,
        init=初始化
    )


def 转为字典(对象: Any) -> Dict[str, Any]:
    """
    将数据类对象转换为字典
    
    参数:
        对象: 数据类对象
        
    返回:
        字典表示
        
    示例:
        >>> @数据类
        ... class 人:
        ...     姓名: str
        ...     年龄: int
        >>> p = 人('张三', 25)
        >>> 转为字典(p)
        {'姓名': '张三', '年龄': 25}
    """
    return asdict(对象)


def 转为元组(对象: Any) -> tuple:
    """
    将数据类对象转换为元组
    
    参数:
        对象: 数据类对象
        
    返回:
        元组表示
        
    示例:
        >>> @数据类
        ... class 人:
        ...     姓名: str
        ...     年龄: int
        >>> p = 人('张三', 25)
        >>> 转为元组(p)
        ('张三', 25)
    """
    return astuple(对象)


def 替换字段(对象: Any, **更改) -> Any:
    """
    创建数据类对象的副本，替换指定字段
    
    参数:
        对象: 原数据类对象
        **更改: 要更改的字段
        
    返回:
        新的数据类对象
        
    示例:
        >>> @数据类
        ... class 人:
        ...     姓名: str
        ...     年龄: int
        >>> p1 = 人('张三', 25)
        >>> p2 = 替换字段(p1, 年龄=26)
        >>> p2.年龄
        26
    """
    return replace(对象, **更改)


def 获取字段信息(类或对象: Any) -> List[Field]:
    """
    获取数据类的字段信息
    
    参数:
        类或对象: 数据类或数据类对象
        
    返回:
        字段信息列表
        
    示例:
        >>> @数据类
        ... class 人:
        ...     姓名: str
        ...     年龄: int
        >>> 字段列表 = 获取字段信息(人)
        >>> len(字段列表)
        2
    """
    from dataclasses import fields
    return list(fields(类或对象))


def 获取字段名称(类或对象: Any) -> List[str]:
    """
    获取数据类的字段名称列表
    
    参数:
        类或对象: 数据类或数据类对象
        
    返回:
        字段名称列表
        
    示例:
        >>> @数据类
        ... class 人:
        ...     姓名: str
        ...     年龄: int
        >>> 获取字段名称(人)
        ['姓名', '年龄']
    """
    return [字段.name for 字段 in 获取字段信息(类或对象)]


def 获取字段默认值(类或对象: Any) -> Dict[str, Any]:
    """
    获取数据类字段的默认值
    
    参数:
        类或对象: 数据类或数据类对象
        
    返回:
        字段默认值字典
        
    示例:
        >>> @数据类
        ... class 配置:
        ...     名称: str = '默认'
        ...     数量: int = 0
        >>> 获取字段默认值(配置)
        {'名称': '默认', '数量': 0}
    """
    默认值 = {}
    for 字段 in 获取字段信息(类或对象):
        if 字段.default is not 字段.default_factory:
            if 字段.default_factory is not None:
                默认值[字段.name] = 字段.default_factory()
            else:
                默认值[字段.name] = 字段.default
    return 默认值


def 是否为数据类(对象: Any) -> bool:
    """
    检查对象是否为数据类
    
    参数:
        对象: 要检查的对象
        
    返回:
        是否为数据类
        
    示例:
        >>> @数据类
        ... class 人:
        ...     姓名: str
        >>> 是否为数据类(人)
        True
    """
    from dataclasses import is_dataclass
    return is_dataclass(对象)


def 创建数据类实例(类: Type, 数据: Dict[str, Any]) -> Any:
    """
    从字典创建数据类实例
    
    参数:
        类: 数据类
        数据: 字段数据字典
        
    返回:
        数据类实例
        
    示例:
        >>> @数据类
        ... class 人:
        ...     姓名: str
        ...     年龄: int
        >>> 创建数据类实例(人, {'姓名': '张三', '年龄': 25})
        人(姓名='张三', 年龄=25)
    """
    return 类(**数据)


def 合并数据类对象(对象1: Any, 对象2: Any) -> Any:
    """
    合并两个数据类对象（对象2的字段覆盖对象1）
    
    参数:
        对象1: 第一个数据类对象
        对象2: 第二个数据类对象
        
    返回:
        合并后的新对象
        
    示例:
        >>> @数据类
        ... class 配置:
        ...     名称: str = '默认'
        ...     数量: int = 0
        >>> c1 = 配置('A', 10)
        >>> c2 = 配置('B', 20)
        >>> 合并数据类对象(c1, c2)
        配置(名称='B', 数量=20)
    """
    if type(对象1) != type(对象2):
        raise TypeError("只能合并相同类型的数据类对象")
    
    数据1 = 转为字典(对象1)
    数据2 = 转为字典(对象2)
    合并数据 = {**数据1, **数据2}
    
    return 创建数据类实例(type(对象1), 合并数据)


# ============================================================================
# 导出所有函数
# ============================================================================

__all__ = [
    '数据类',
    '字段',
    '转为字典',
    '转为元组',
    '替换字段',
    '获取字段信息',
    '获取字段名称',
    '获取字段默认值',
    '是否为数据类',
    '创建数据类实例',
    '合并数据类对象',
]
