"""
言律语言itertools模块扩展
提供itertools标准库的中文版本
"""

from typing import TypeVar, Callable, Any, Optional, Iterable, Iterator
from itertools import (
    count, cycle, repeat,
    accumulate, chain, compress, dropwhile, takewhile, 
    filterfalse, groupby, islice, starmap, tee,
    product, permutations, combinations, combinations_with_replacement
)

T = TypeVar('T')
R = TypeVar('R')


# ============================================================================
# 无限迭代器
# ============================================================================

def 计数迭代器(起始: int = 0, 步长: int = 1) -> Iterator[int]:
    """
    创建无限计数迭代器
    
    参数:
        起始: 起始值
        步长: 步长
        
    返回:
        计数迭代器
        
    示例:
        >>> it = 计数迭代器(10, 2)
        >>> 下一个元素(it)
        10
        >>> 下一个元素(it)
        12
    """
    return count(起始, 步长)


def 循环迭代器(可迭代对象: Iterable[T]) -> Iterator[T]:
    """
    创建无限循环迭代器
    
    参数:
        可迭代对象: 可迭代对象
        
    返回:
        循环迭代器
        
    示例:
        >>> it = 循环迭代器([1, 2, 3])
        >>> 下一个元素(it)
        1
        >>> 下一个元素(it)
        2
        >>> 下一个元素(it)
        3
        >>> 下一个元素(it)
        1
    """
    return cycle(可迭代对象)


def 重复迭代器(对象: T, 次数: Optional[int] = None) -> Iterator[T]:
    """
    创建重复迭代器
    
    参数:
        对象: 要重复的对象
        次数: 重复次数（None表示无限）
        
    返回:
        重复迭代器
        
    示例:
        >>> 列表(重复迭代器(10, 3))
        [10, 10, 10]
    """
    return repeat(对象, 次数)


# ============================================================================
# 终止迭代器
# ============================================================================

def 累积计算(
    可迭代对象: Iterable[T],
    函数: Optional[Callable[[T, T], T]] = None,
    初始值: Optional[T] = None
) -> Iterator[T]:
    """
    累积计算
    
    参数:
        可迭代对象: 可迭代对象
        函数: 累积函数（默认为加法）
        初始值: 初始值
        
    返回:
        累积结果迭代器
        
    示例:
        >>> 列表(累积计算([1, 2, 3, 4]))
        [1, 3, 6, 10]
    """
    if 初始值 is not None:
        return accumulate(可迭代对象, 函数, initial=初始值)
    return accumulate(可迭代对象, 函数)


def 链式迭代(*可迭代对象: Iterable[T]) -> Iterator[T]:
    """
    链式连接多个可迭代对象
    
    参数:
        *可迭代对象: 可迭代对象
        
    返回:
        链式迭代器
        
    示例:
        >>> 列表(链式迭代([1, 2], [3, 4]))
        [1, 2, 3, 4]
    """
    return chain(*可迭代对象)


def 压缩迭代(
    数据: Iterable[T],
    选择器: Iterable[bool]
) -> Iterator[T]:
    """
    根据选择器压缩数据
    
    参数:
        数据: 数据可迭代对象
        选择器: 布尔选择器
        
    返回:
        压缩后的迭代器
        
    示例:
        >>> 列表(压缩迭代([1, 2, 3, 4], [True, False, True, False]))
        [1, 3]
    """
    return compress(数据, 选择器)


def 丢弃元素(
    条件函数: Callable[[T], bool],
    可迭代对象: Iterable[T]
) -> Iterator[T]:
    """
    丢弃满足条件的元素
    
    参数:
        条件函数: 条件函数
        可迭代对象: 可迭代对象
        
    返回:
        迭代器
        
    示例:
        >>> 列表(丢弃元素(lambda x: x < 3, [1, 2, 3, 4, 1, 2]))
        [3, 4, 1, 2]
    """
    return dropwhile(条件函数, 可迭代对象)


def 获取元素(
    条件函数: Callable[[T], bool],
    可迭代对象: Iterable[T]
) -> Iterator[T]:
    """
    获取满足条件的元素
    
    参数:
        条件函数: 条件函数
        可迭代对象: 可迭代对象
        
    返回:
        迭代器
        
    示例:
        >>> 列表(获取元素(lambda x: x < 3, [1, 2, 3, 4, 1, 2]))
        [1, 2]
    """
    return takewhile(条件函数, 可迭代对象)


def 过滤假值(
    条件函数: Optional[Callable[[T], bool]] = None,
    可迭代对象: Optional[Iterable[T]] = None
) -> Iterator[T]:
    """
    过滤假值或满足条件的元素
    
    参数:
        条件函数: 条件函数（None表示过滤假值）
        可迭代对象: 可迭代对象
        
    返回:
        过滤后的迭代器
        
    示例:
        >>> 列表(过滤假值(None, [0, 1, 2, 0, 3]))
        [1, 2, 3]
    """
    if 可迭代对象 is None:
        return filterfalse(条件函数)
    return filterfalse(条件函数, 可迭代对象)


def 分组迭代(
    可迭代对象: Iterable[T],
    键函数: Optional[Callable[[T], Any]] = None
) -> Iterator[tuple[Any, Iterator[T]]]:
    """
    分组迭代
    
    参数:
        可迭代对象: 可迭代对象
        键函数: 分组键函数
        
    返回:
        (键, 组)迭代器
        
    示例:
        >>> for 键, 组 in 分组迭代('aaabbbcc'):
        ...     打印(键, 列表(组))
        a ['a', 'a', 'a']
        b ['b', 'b', 'b']
        c ['c', 'c']
    """
    return groupby(可迭代对象, 键函数)


def 切片迭代(
    可迭代对象: Iterable[T],
    起始: int,
    结束: Optional[int] = None,
    步长: Optional[int] = None
) -> Iterator[T]:
    """
    切片迭代器
    
    参数:
        可迭代对象: 可迭代对象
        起始: 起始索引
        结束: 结束索引
        步长: 步长
        
    返回:
        切片迭代器
        
    示例:
        >>> 列表(切片迭代(range(10), 2, 8, 2))
        [2, 4, 6]
    """
    if 步长 is None:
        return islice(可迭代对象, 起始, 结束)
    return islice(可迭代对象, 起始, 结束, 步长)


def 配对迭代(可迭代对象: Iterable[T]) -> Iterator[tuple[T, T]]:
    """
    配对迭代
    
    参数:
        可迭代对象: 可迭代对象
        
    返回:
        配对迭代器
        
    示例:
        >>> 列表(配对迭代([1, 2, 3, 4]))
        [(1, 2), (2, 3), (3, 4)]
    """
    from itertools import pairwise
    return pairwise(可迭代对象)


def 星号映射(
    函数: Callable[..., R],
    可迭代对象: Iterable[Iterable[Any]]
) -> Iterator[R]:
    """
    星号映射
    
    参数:
        函数: 函数
        可迭代对象: 可迭代对象
        
    返回:
        结果迭代器
        
    示例:
        >>> 列表(星号映射(pow, [(2, 5), (3, 2), (10, 3)]))
        [32, 9, 1000]
    """
    return starmap(函数, 可迭代对象)


def 拉链最长(
    *可迭代对象: Iterable[T],
    填充值: Optional[T] = None
) -> Iterator[tuple[T, ...]]:
    """
    拉链最长
    
    参数:
        *可迭代对象: 可迭代对象
        填充值: 填充值
        
    返回:
        元组迭代器
        
    示例:
        >>> 列表(拉链最长([1, 2, 3], [4, 5], 填充值=0))
        [(1, 4), (2, 5), (3, 0)]
    """
    from itertools import zip_longest
    return zip_longest(*可迭代对象, fillvalue=填充值)


def 分裂迭代器(可迭代对象: Iterable[T], 数量: int = 2) -> tuple[Iterator[T], ...]:
    """
    分裂迭代器
    
    参数:
        可迭代对象: 可迭代对象
        数量: 分裂数量
        
    返回:
        分裂后的迭代器元组
        
    示例:
        >>> it1, it2 = 分裂迭代器([1, 2, 3, 4])
        >>> 列表(it1)
        [1, 2, 3, 4]
        >>> 列表(it2)
        [1, 2, 3, 4]
    """
    return tee(可迭代对象, 数量)


# ============================================================================
# 排列组合迭代器
# ============================================================================

def 笛卡尔积(
    *可迭代对象: Iterable[T],
    重复次数: int = 1
) -> Iterator[tuple[T, ...]]:
    """
    笛卡尔积
    
    参数:
        *可迭代对象: 可迭代对象
        重复次数: 重复次数
        
    返回:
        笛卡尔积迭代器
        
    示例:
        >>> 列表(笛卡尔积([1, 2], [3, 4]))
        [(1, 3), (1, 4), (2, 3), (2, 4)]
    """
    return product(*可迭代对象, repeat=重复次数)


def 排列(
    可迭代对象: Iterable[T],
    长度: Optional[int] = None
) -> Iterator[tuple[T, ...]]:
    """
    排列
    
    参数:
        可迭代对象: 可迭代对象
        长度: 排列长度
        
    返回:
        排列迭代器
        
    示例:
        >>> 列表(排列([1, 2, 3], 2))
        [(1, 2), (1, 3), (2, 1), (2, 3), (3, 1), (3, 2)]
    """
    return permutations(可迭代对象, 长度)


def 组合(
    可迭代对象: Iterable[T],
    长度: int
) -> Iterator[tuple[T, ...]]:
    """
    组合
    
    参数:
        可迭代对象: 可迭代对象
        长度: 组合长度
        
    返回:
        组合迭代器
        
    示例:
        >>> 列表(组合([1, 2, 3, 4], 2))
        [(1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4)]
    """
    return combinations(可迭代对象, 长度)


def 可重复组合(
    可迭代对象: Iterable[T],
    长度: int
) -> Iterator[tuple[T, ...]]:
    """
    可重复组合
    
    参数:
        可迭代对象: 可迭代对象
        长度: 组合长度
        
    返回:
        可重复组合迭代器
        
    示例:
        >>> 列表(可重复组合([1, 2, 3], 2))
        [(1, 1), (1, 2), (1, 3), (2, 2), (2, 3), (3, 3)]
    """
    return combinations_with_replacement(可迭代对象, 长度)


# ============================================================================
# 导出所有函数
# ============================================================================

__all__ = [
    # 无限迭代器
    '计数迭代器', '循环迭代器', '重复迭代器',
    
    # 终止迭代器
    '累积计算', '链式迭代', '压缩迭代', '丢弃元素', '获取元素',
    '过滤假值', '分组迭代', '切片迭代', '配对迭代', '星号映射',
    '拉链最长', '分裂迭代器',
    
    # 排列组合迭代器
    '笛卡尔积', '排列', '组合', '可重复组合',
]
