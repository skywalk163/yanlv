"""
言律语言标准库

提供常用函数和工具
"""

import math
import random
import os
import json
from typing import List, Dict, Any, Optional, Union
from datetime import datetime


# ============================================================================
# 数学函数
# ============================================================================

def 加(a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
    """加法"""
    return a + b


def 减(a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
    """减法"""
    return a - b


def 乘(a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
    """乘法"""
    return a * b


def 除(a: Union[int, float], b: Union[int, float]) -> float:
    """除法"""
    if b == 0:
        raise ValueError("除数不能为0")
    return a / b


def 取余(a: int, b: int) -> int:
    """取余"""
    return a % b


def 幂(base: Union[int, float], exp: Union[int, float]) -> Union[int, float]:
    """幂运算"""
    return base ** exp


def 开方(x: Union[int, float]) -> float:
    """开方"""
    return math.sqrt(x)


def 绝对值(x: Union[int, float]) -> Union[int, float]:
    """绝对值"""
    return abs(x)


def 正弦(x: Union[int, float]) -> float:
    """正弦"""
    return math.sin(x)


def 余弦(x: Union[int, float]) -> float:
    """余弦"""
    return math.cos(x)


def 正切(x: Union[int, float]) -> float:
    """正切"""
    return math.tan(x)


def 对数(x: Union[int, float], base: float = math.e) -> float:
    """对数"""
    return math.log(x, base)


def 指数(x: Union[int, float]) -> float:
    """指数"""
    return math.exp(x)


def 向下取整(x: float) -> int:
    """向下取整"""
    return math.floor(x)


def 向上取整(x: float) -> int:
    """向上取整"""
    return math.ceil(x)


def 四舍五入(x: float, digits: int = 0) -> float:
    """四舍五入"""
    return round(x, digits)


# ============================================================================
# 数组函数
# ============================================================================

def 长度(arr: Union[List, str]) -> int:
    """获取长度"""
    return len(arr)


def 添加(arr: List, item: Any) -> List:
    """添加元素"""
    arr.append(item)
    return arr


def 删除(arr: List, item: Any) -> List:
    """删除元素"""
    if item in arr:
        arr.remove(item)
    return arr


def 插入(arr: List, index: int, item: Any) -> List:
    """插入元素"""
    arr.insert(index, item)
    return arr


def 弹出(arr: List, index: int = -1) -> Any:
    """弹出元素"""
    return arr.pop(index)


def 排序(arr: List, reverse: bool = False) -> List:
    """排序"""
    return sorted(arr, reverse=reverse)


def 反转(arr: List) -> List:
    """反转"""
    return arr[::-1]


def 连接(arr: List, separator: str = '') -> str:
    """连接数组为字符串"""
    return separator.join(str(item) for item in arr)


def 切片(arr: List, start: int, end: int = None) -> List:
    """切片"""
    return arr[start:end]


def 查找(arr: List, item: Any) -> int:
    """查找元素索引"""
    try:
        return arr.index(item)
    except ValueError:
        return -1


def 计数(arr: List, item: Any) -> int:
    """计数"""
    return arr.count(item)


def 最大值(arr: List) -> Any:
    """最大值"""
    return max(arr)


def 最小值(arr: List) -> Any:
    """最小值"""
    return min(arr)


def 求和(arr: List) -> Union[int, float]:
    """求和"""
    return sum(arr)


def 平均值(arr: List) -> float:
    """平均值"""
    return sum(arr) / len(arr)


# ============================================================================
# 字符串函数
# ============================================================================

def 分割(s: str, separator: str = ' ') -> List[str]:
    """分割字符串"""
    return s.split(separator)


def 替换(s: str, old: str, new: str) -> str:
    """替换字符串"""
    return s.replace(old, new)


def 子串(s: str, start: int, end: int = None) -> str:
    """获取子串"""
    return s[start:end]


def 去空格(s: str) -> str:
    """去除首尾空格"""
    return s.strip()


def 转大写(s: str) -> str:
    """转大写"""
    return s.upper()


def 转小写(s: str) -> str:
    """转小写"""
    return s.lower()


def 首字母大写(s: str) -> str:
    """首字母大写"""
    return s.capitalize()


def 是否包含(s: str, sub: str) -> bool:
    """是否包含子串"""
    return sub in s


def 开始以(s: str, prefix: str) -> bool:
    """是否以某字符串开始"""
    return s.startswith(prefix)


def 结束以(s: str, suffix: str) -> bool:
    """是否以某字符串结束"""
    return s.endswith(suffix)


# ============================================================================
# 随机函数
# ============================================================================

def 随机数(min_val: int = 0, max_val: int = 100) -> int:
    """随机整数"""
    return random.randint(min_val, max_val)


def 随机浮点数(min_val: float = 0.0, max_val: float = 1.0) -> float:
    """随机浮点数"""
    return random.uniform(min_val, max_val)


def 随机选择(arr: List) -> Any:
    """随机选择"""
    return random.choice(arr)


def 随机打乱(arr: List) -> List:
    """随机打乱"""
    random.shuffle(arr)
    return arr


# ============================================================================
# 文件函数
# ============================================================================

def 读取文件(filepath: str, encoding: str = 'utf-8') -> str:
    """读取文件"""
    with open(filepath, 'r', encoding=encoding) as f:
        return f.read()


def 写入文件(filepath: str, content: str, encoding: str = 'utf-8') -> None:
    """写入文件"""
    with open(filepath, 'w', encoding=encoding) as f:
        f.write(content)


def 追加文件(filepath: str, content: str, encoding: str = 'utf-8') -> None:
    """追加文件"""
    with open(filepath, 'a', encoding=encoding) as f:
        f.write(content)


def 文件存在(filepath: str) -> bool:
    """检查文件是否存在"""
    return os.path.exists(filepath)


def 删除文件(filepath: str) -> None:
    """删除文件"""
    if os.path.exists(filepath):
        os.remove(filepath)


def 创建目录(dirpath: str) -> None:
    """创建目录"""
    os.makedirs(dirpath, exist_ok=True)


def 列出目录(dirpath: str) -> List[str]:
    """列出目录内容"""
    return os.listdir(dirpath)


# ============================================================================
# JSON函数
# ============================================================================

def 解析JSON(json_str: str) -> Any:
    """解析JSON字符串"""
    return json.loads(json_str)


def 生成JSON(obj: Any, indent: int = 2) -> str:
    """生成JSON字符串"""
    return json.dumps(obj, ensure_ascii=False, indent=indent)


def 读取JSON(filepath: str, encoding: str = 'utf-8') -> Any:
    """读取JSON文件"""
    with open(filepath, 'r', encoding=encoding) as f:
        return json.load(f)


def 写入JSON(filepath: str, obj: Any, encoding: str = 'utf-8') -> None:
    """写入JSON文件"""
    with open(filepath, 'w', encoding=encoding) as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)


# ============================================================================
# 时间函数
# ============================================================================

def 当前时间() -> str:
    """获取当前时间"""
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def 当前日期() -> str:
    """获取当前日期"""
    return datetime.now().strftime('%Y-%m-%d')


def 时间戳() -> float:
    """获取时间戳"""
    return datetime.now().timestamp()


def 格式化时间(timestamp: float, fmt: str = '%Y-%m-%d %H:%M:%S') -> str:
    """格式化时间"""
    return datetime.fromtimestamp(timestamp).strftime(fmt)


# ============================================================================
# 导出
# ============================================================================

__all__ = [
    # 数学函数
    '加', '减', '乘', '除', '取余', '幂', '开方', '绝对值',
    '正弦', '余弦', '正切', '对数', '指数',
    '向下取整', '向上取整', '四舍五入',
    
    # 数组函数
    '长度', '添加', '删除', '插入', '弹出', '排序', '反转',
    '连接', '切片', '查找', '计数',
    '最大值', '最小值', '求和', '平均值',
    
    # 字符串函数
    '分割', '替换', '子串', '去空格',
    '转大写', '转小写', '首字母大写',
    '是否包含', '开始以', '结束以',
    
    # 随机函数
    '随机数', '随机浮点数', '随机选择', '随机打乱',
    
    # 文件函数
    '读取文件', '写入文件', '追加文件',
    '文件存在', '删除文件', '创建目录', '列出目录',
    
    # JSON函数
    '解析JSON', '生成JSON', '读取JSON', '写入JSON',
    
    # 时间函数
    '当前时间', '当前日期', '时间戳', '格式化时间',
]
