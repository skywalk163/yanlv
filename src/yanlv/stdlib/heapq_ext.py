"""
言律语言heapq模块扩展
提供heapq标准库的中文版本
"""

import heapq
from typing import List, Any, Iterable


def 堆化(列表: List[Any]) -> None:
    """
    将列表转换为堆（就地转换）
    
    参数:
        列表: 要转换的列表
        
    示例:
        >>> 数据 = [3, 1, 4, 1, 5, 9]
        >>> 堆化(数据)
        >>> 数据[0]  # 最小元素
        1
    """
    heapq.heapify(列表)


def 压入堆(堆: List[Any], 元素: Any) -> None:
    """
    将元素压入堆
    
    参数:
        堆: 堆列表
        元素: 要压入的元素
        
    示例:
        >>> 堆 = [1, 2, 3]
        >>> 堆化(堆)
        >>> 压入堆(堆, 0)
        >>> 堆[0]
        0
    """
    heapq.heappush(堆, 元素)


def 弹出堆(堆: List[Any]) -> Any:
    """
    从堆中弹出最小元素
    
    参数:
        堆: 堆列表
        
    返回:
        最小元素
        
    示例:
        >>> 堆 = [1, 2, 3]
        >>> 堆化(堆)
        >>> 弹出堆(堆)
        1
    """
    return heapq.heappop(堆)


def 压入弹出堆(堆: List[Any], 元素: Any) -> Any:
    """
    压入元素并弹出最小元素（更高效）
    
    参数:
        堆: 堆列表
        元素: 要压入的元素
        
    返回:
        最小元素
        
    示例:
        >>> 堆 = [1, 2, 3]
        >>> 堆化(堆)
        >>> 压入弹出堆(堆, 0)
        0
    """
    return heapq.heappushpop(堆, 元素)


def 替换堆(堆: List[Any], 元素: Any) -> Any:
    """
    弹出最小元素并压入新元素
    
    参数:
        堆: 堆列表
        元素: 要压入的元素
        
    返回:
        最小元素
        
    示例:
        >>> 堆 = [1, 2, 3]
        >>> 堆化(堆)
        >>> 替换堆(堆, 4)
        1
    """
    return heapq.heapreplace(堆, 元素)


def 获取前N个最小元素(可迭代对象: Iterable[Any], n: int) -> List[Any]:
    """
    获取前N个最小元素
    
    参数:
        可迭代对象: 可迭代对象
        n: 数量
        
    返回:
        前N个最小元素列表
        
    示例:
        >>> 获取前N个最小元素([3, 1, 4, 1, 5, 9], 3)
        [1, 1, 3]
    """
    return heapq.nsmallest(n, 可迭代对象)


def 获取前N个最大元素(可迭代对象: Iterable[Any], n: int) -> List[Any]:
    """
    获取前N个最大元素
    
    参数:
        可迭代对象: 可迭代对象
        n: 数量
        
    返回:
        前N个最大元素列表
        
    示例:
        >>> 获取前N个最大元素([3, 1, 4, 1, 5, 9], 3)
        [9, 5, 4]
    """
    return heapq.nlargest(n, 可迭代对象)


def 合并有序序列(*序列列表: Iterable[Any]) -> Iterable[Any]:
    """
    合并多个有序序列
    
    参数:
        *序列列表: 有序序列列表
        
    返回:
        合并后的有序迭代器
        
    示例:
        >>> list(合并有序序列([1, 3, 5], [2, 4, 6]))
        [1, 2, 3, 4, 5, 6]
    """
    return heapq.merge(*序列列表)


class 最小堆:
    """
    最小堆类
    
    示例:
        >>> 堆 = 最小堆()
        >>> 堆.压入(3)
        >>> 堆.压入(1)
        >>> 堆.压入(2)
        >>> 堆.弹出()
        1
    """
    
    def __init__(self, 初始数据: Iterable[Any] = None):
        """
        初始化最小堆
        
        参数:
            初始数据: 初始数据
        """
        self.数据 = list(初始数据) if 初始数据 else []
        if self.数据:
            heapq.heapify(self.数据)
    
    def 压入(self, 元素: Any) -> None:
        """压入元素"""
        heapq.heappush(self.数据, 元素)
    
    def 弹出 -> Any:
        """弹出最小元素"""
        if not self.数据:
            raise IndexError("堆为空")
        return heapq.heappop(self.数据)
    
    def 查看最小(self) -> Any:
        """查看最小元素（不弹出）"""
        if not self.数据:
            raise IndexError("堆为空")
        return self.数据[0]
    
    def 压入弹出(self, 元素: Any) -> Any:
        """压入元素并弹出最小元素"""
        if not self.数据:
            return 元素
        return heapq.heappushpop(self.数据, 元素)
    
    def 替换(self, 元素: Any) -> Any:
        """弹出最小元素并压入新元素"""
        if not self.数据:
            raise IndexError("堆为空")
        return heapq.heapreplace(self.数据, 元素)
    
    def 大小(self) -> int:
        """获取堆大小"""
        return len(self.数据)
    
    def 是否为空(self) -> bool:
        """检查堆是否为空"""
        return len(self.数据) == 0
    
    def 清空(self) -> None:
        """清空堆"""
        self.数据.clear()
    
    def 转为列表(self) -> List[Any]:
        """转为列表（不保证有序）"""
        return self.数据.copy()
    
    def 排序输出(self) -> List[Any]:
        """排序输出所有元素"""
        结果 = []
        临时堆 = self.数据.copy()
        while 临时堆:
            结果.append(heapq.heappop(临时堆))
        return 结果
    
    def __len__(self):
        return len(self.数据)
    
    def __bool__(self):
        return bool(self.数据)


class 最大堆:
    """
    最大堆类
    
    示例:
        >>> 堆 = 最大堆()
        >>> 堆.压入(1)
        >>> 堆.压入(3)
        >>> 堆.压入(2)
        >>> 堆.弹出()
        3
    """
    
    def __init__(self, 初始数据: Iterable[Any] = None):
        """
        初始化最大堆
        
        参数:
            初始数据: 初始数据
        """
        self.数据 = [-x for x in 初始数据] if 初始数据 else []
        if self.数据:
            heapq.heapify(self.数据)
    
    def 压入(self, 元素: Any) -> None:
        """压入元素"""
        heapq.heappush(self.数据, -元素)
    
    def 弹出 -> Any:
        """弹出最大元素"""
        if not self.数据:
            raise IndexError("堆为空")
        return -heapq.heappop(self.数据)
    
    def 查看最大(self) -> Any:
        """查看最大元素（不弹出）"""
        if not self.数据:
            raise IndexError("堆为空")
        return -self.数据[0]
    
    def 压入弹出(self, 元素: Any) -> Any:
        """压入元素并弹出最大元素"""
        if not self.数据:
            return 元素
        return -heapq.heappushpop(self.数据, -元素)
    
    def 替换(self, 元素: Any) -> Any:
        """弹出最大元素并压入新元素"""
        if not self.数据:
            raise IndexError("堆为空")
        return -heapq.heapreplace(self.数据, -元素)
    
    def 大小(self) -> int:
        """获取堆大小"""
        return len(self.数据)
    
    def 是否为空(self) -> bool:
        """检查堆是否为空"""
        return len(self.数据) == 0
    
    def 清空(self) -> None:
        """清空堆"""
        self.数据.clear()
    
    def 转为列表(self) -> List[Any]:
        """转为列表（不保证有序）"""
        return [-x for x in self.数据]
    
    def 排序输出(self) -> List[Any]:
        """排序输出所有元素（降序）"""
        结果 = []
        临时堆 = self.数据.copy()
        while 临时堆:
            结果.append(-heapq.heappop(临时堆))
        return 结果
    
    def __len__(self):
        return len(self.数据)
    
    def __bool__(self):
        return bool(self.数据)


# ============================================================================
# 导出所有函数和类
# ============================================================================

__all__ = [
    '堆化',
    '压入堆',
    '弹出堆',
    '压入弹出堆',
    '替换堆',
    '获取前N个最小元素',
    '获取前N个最大元素',
    '合并有序序列',
    '最小堆',
    '最大堆',
]
