"""
言律语言operator模块扩展
提供operator标准库的中文版本
"""

import operator
from typing import Any, Callable


# ============================================================================
# 比较操作符
# ============================================================================

def 小于(a: Any, b: Any) -> bool:
    """a < b"""
    return operator.lt(a, b)


def 小于等于(a: Any, b: Any) -> bool:
    """a <= b"""
    return operator.le(a, b)


def 大于(a: Any, b: Any) -> bool:
    """a > b"""
    return operator.gt(a, b)


def 大于等于(a: Any, b: Any) -> bool:
    """a >= b"""
    return operator.ge(a, b)


def 等于(a: Any, b: Any) -> bool:
    """a == b"""
    return operator.eq(a, b)


def 不等于(a: Any, b: Any) -> bool:
    """a != b"""
    return operator.ne(a, b)


# ============================================================================
# 算术操作符
# ============================================================================

def 加法(a: Any, b: Any) -> Any:
    """a + b"""
    return operator.add(a, b)


def 减法(a: Any, b: Any) -> Any:
    """a - b"""
    return operator.sub(a, b)


def 乘法(a: Any, b: Any) -> Any:
    """a * b"""
    return operator.mul(a, b)


def 真除法(a: Any, b: Any) -> Any:
    """a / b"""
    return operator.truediv(a, b)


def 整除法(a: Any, b: Any) -> Any:
    """a // b"""
    return operator.floordiv(a, b)


def 取模(a: Any, b: Any) -> Any:
    """a % b"""
    return operator.mod(a, b)


def 幂运算(a: Any, b: Any) -> Any:
    """a ** b"""
    return operator.pow(a, b)


def 负数(a: Any) -> Any:
    """-a"""
    return operator.neg(a)


def 正数(a: Any) -> Any:
    """+a"""
    return operator.pos(a)


def 绝对值(a: Any) -> Any:
    """abs(a)"""
    return operator.abs(a)


# ============================================================================
# 位操作符
# ============================================================================

def 按位与(a: int, b: int) -> int:
    """a & b"""
    return operator.and_(a, b)


def 按位或(a: int, b: int) -> int:
    """a | b"""
    return operator.or_(a, b)


def 按位异或(a: int, b: int) -> int:
    """a ^ b"""
    return operator.xor(a, b)


def 按位取反(a: int) -> int:
    """~a"""
    return operator.invert(a)


def 左移(a: int, b: int) -> int:
    """a << b"""
    return operator.lshift(a, b)


def 右移(a: int, b: int) -> int:
    """a >> b"""
    return operator.rshift(a, b)


# ============================================================================
# 序列操作符
# ============================================================================

def 索引访问(序列: Any, 索引: int) -> Any:
    """序列[索引]"""
    return operator.getitem(序列, 索引)


def 索引赋值(序列: Any, 索引: int, 值: Any) -> None:
    """序列[索引] = 值"""
    operator.setitem(序列, 索引, 值)


def 索引删除(序列: Any, 索引: int) -> None:
    """del 序列[索引]"""
    operator.delitem(序列, 索引)


def 包含检查(序列: Any, 元素: Any) -> bool:
    """元素 in 序列"""
    return operator.contains(序列, 元素)


def 拼接(a: Any, b: Any) -> Any:
    """a + b (序列拼接)"""
    return operator.concat(a, b)


def 重复(序列: Any, 次数: int) -> Any:
    """序列 * 次数"""
    return operator.mul(序列, 次数)


# ============================================================================
# 属性和项访问
# ============================================================================

def 获取属性(对象: Any, 属性名: str) -> Any:
    """对象.属性名"""
    return operator.attrgetter(属性名)(对象)


def 设置属性(对象: Any, 属性名: str, 值: Any) -> None:
    """对象.属性名 = 值"""
    setattr(对象, 属性名, 值)


def 获取项(对象: Any, 键: Any) -> Any:
    """对象[键]"""
    return operator.itemgetter(键)(对象)


def 调用方法(对象: Any, 方法名: str, *参数, **关键字参数) -> Any:
    """对象.方法名(*参数, **关键字参数)"""
    方法 = getattr(对象, 方法名)
    return 方法(*参数, **关键字参数)


# ============================================================================
# 函数工具
# ============================================================================

def 创建属性获取器(属性名: str) -> Callable:
    """
    创建属性获取器函数
    
    参数:
        属性名: 属性名称
        
    返回:
        属性获取函数
        
    示例:
        >>> 获取姓名 = 创建属性获取器('姓名')
        >>> 获取姓名(对象)
    """
    return operator.attrgetter(属性名)


def 创建项获取器(键: Any) -> Callable:
    """
    创建项获取器函数
    
    参数:
        键: 键值
        
    返回:
        项获取函数
        
    示例:
        >>> 获取第一个 = 创建项获取器(0)
        >>> 获取第一个([1, 2, 3])
        1
    """
    return operator.itemgetter(键)


def 创建方法调用器(方法名: str, *参数, **关键字参数) -> Callable:
    """
    创建方法调用器函数
    
    参数:
        方法名: 方法名称
        *参数: 位置参数
        **关键字参数: 关键字参数
        
    返回:
        方法调用函数
        
    示例:
        >>> 调用追加 = 创建方法调用器('append', 10)
        >>> 调用追加(列表)
    """
    return operator.methodcaller(方法名, *参数, **关键字参数)


def 恒等函数(参数: Any) -> Any:
    """
    恒等函数，返回参数本身
    
    参数:
        参数: 任意参数
        
    返回:
        参数本身
        
    示例:
        >>> 恒等函数(5)
        5
    """
    return 参数


def 常量函数(值: Any) -> Callable:
    """
    创建返回常量值的函数
    
    参数:
        值: 常量值
        
    返回:
        常量函数
        
    示例:
        >>> f = 常量函数(10)
        >>> f()
        10
    """
    return lambda: 值


# ============================================================================
# 逻辑操作符
# ============================================================================

def 逻辑非(a: Any) -> bool:
    """not a"""
    return operator.not_(a)


def 逻辑与(a: Any, b: Any) -> bool:
    """a and b"""
    return a and b


def 逻辑或(a: Any, b: Any) -> bool:
    """a or b"""
    return a or b


def 布尔转换(a: Any) -> bool:
    """bool(a)"""
    return bool(a)


# ============================================================================
# 导出所有函数
# ============================================================================

__all__ = [
    # 比较操作符
    '小于', '小于等于', '大于', '大于等于', '等于', '不等于',
    
    # 算术操作符
    '加法', '减法', '乘法', '真除法', '整除法', '取模', '幂运算',
    '负数', '正数', '绝对值',
    
    # 位操作符
    '按位与', '按位或', '按位异或', '按位取反', '左移', '右移',
    
    # 序列操作符
    '索引访问', '索引赋值', '索引删除', '包含检查', '拼接', '重复',
    
    # 属性和项访问
    '获取属性', '设置属性', '获取项', '调用方法',
    
    # 函数工具
    '创建属性获取器', '创建项获取器', '创建方法调用器',
    '恒等函数', '常量函数',
    
    # 逻辑操作符
    '逻辑非', '逻辑与', '逻辑或', '布尔转换',
]
