"""
言律语言pprint模块扩展
提供pprint标准库的中文版本
"""

import pprint
from typing import Any, Optional, IO
import sys


def 美化打印(
    对象: Any,
    流: Optional[IO] = None,
    缩进: int = 1,
    宽度: int = 80,
    深度: Optional[int] = None,
    排序键: bool = True,
    紧凑: bool = False
) -> None:
    """
    美化打印对象
    
    参数:
        对象: 要打印的对象
        流: 输出流（None表示标准输出）
        缩进: 缩进空格数
        宽度: 每行最大宽度
        深度: 最大打印深度
        排序键: 是否排序字典键
        紧凑: 是否紧凑格式
        
    示例:
        >>> 数据 = {'姓名': '张三', '技能': ['Python', 'Java', 'Go']}
        >>> 美化打印(数据)
        {'姓名': '张三', '技能': ['Python', 'Java', 'Go']}
    """
    if 流 is None:
        流 = sys.stdout
    
    打印器 = pprint.PrettyPrinter(
        indent=缩进,
        width=宽度,
        depth=深度,
        stream=流,
        sort_dicts=排序键,
        compact=紧凑
    )
    打印器.pprint(对象)


def 格式化对象(
    对象: Any,
    缩进: int = 1,
    宽度: int = 80,
    深度: Optional[int] = None,
    排序键: bool = True,
    紧凑: bool = False
) -> str:
    """
    格式化对象为字符串
    
    参数:
        对象: 要格式化的对象
        缩进: 缩进空格数
        宽度: 每行最大宽度
        深度: 最大格式化深度
        排序键: 是否排序字典键
        紧凑: 是否紧凑格式
        
    返回:
        格式化后的字符串
        
    示例:
        >>> 数据 = {'a': 1, 'b': 2}
        >>> 格式化对象(数据)
        "{'a': 1, 'b': 2}"
    """
    return pprint.pformat(
        对象,
        indent=缩进,
        width=宽度,
        depth=深度,
        sort_dicts=排序键,
        compact=紧凑
    )


def 安全表示(
    对象: Any,
    最大宽度: int = 80,
    最大字符串长度: Optional[int] = None
) -> str:
    """
    安全地获取对象的可打印表示
    
    参数:
        对象: 要表示的对象
        最大宽度: 最大宽度
        最大字符串长度: 字符串最大长度
        
    返回:
        安全表示字符串
        
    示例:
        >>> 安全表示([1, 2, 3])
        '[1, 2, 3]'
    """
    try:
        表示 = repr(对象)
        if 最大字符串长度 and len(表示) > 最大字符串长度:
            表示 = 表示[:最大字符串长度] + '...'
        if len(表示) > 最大宽度:
            表示 = 表示[:最大宽度] + '...'
        return 表示
    except Exception:
        return '<无法表示的对象>'


def 打印字典(
    字典对象: dict,
    键宽度: Optional[int] = None,
    显示类型: bool = False,
    排序键: bool = True
) -> None:
    """
    美化打印字典
    
    参数:
        字典对象: 要打印的字典
        键宽度: 键的显示宽度（None表示自动）
        显示类型: 是否显示值的类型
        排序键: 是否排序键
        
    示例:
        >>> 打印字典({'姓名': '张三', '年龄': 25})
        姓名: 张三
        年龄: 25
    """
    if not 字典对象:
        print('{}')
        return
    
    键列表 = sorted(字典对象.keys()) if 排序键 else 字典对象.keys()
    
    if 键宽度 is None:
        键宽度 = max(len(str(键)) for 键 in 键列表)
    
    for 键 in 键列表:
        值 = 字典对象[键]
        键字符串 = str(键).ljust(键宽度)
        
        if 显示类型:
            类型字符串 = f' ({type(值).__name__})'
            print(f'{键字符串}: {值}{类型字符串}')
        else:
            print(f'{键字符串}: {值}')


def 打印列表(
    列表对象: list,
    显示索引: bool = True,
    索引宽度: int = 4,
    显示类型: bool = False
) -> None:
    """
    美化打印列表
    
    参数:
        列表对象: 要打印的列表
        显示索引: 是否显示索引
        索引宽度: 索引显示宽度
        显示类型: 是否显示元素类型
        
    示例:
        >>> 打印列表(['a', 'b', 'c'])
        [0]: a
        [1]: b
        [2]: c
    """
    if not 列表对象:
        print('[]')
        return
    
    for 索引, 元素 in enumerate(列表对象):
        if 显示索引:
            索引字符串 = f'[{索引}]'.ljust(索引宽度 + 2)
            if 显示类型:
                类型字符串 = f' ({type(元素).__name__})'
                print(f'{索引字符串} {元素}{类型字符串}')
            else:
                print(f'{索引字符串} {元素}')
        else:
            if 显示类型:
                类型字符串 = f' ({type(元素).__name__})'
                print(f'{元素}{类型字符串}')
            else:
                print(元素)


def 打印表格(
    数据: list,
    标题行: Optional[list] = None,
    列宽度: Optional[list] = None,
    对齐方式: str = '左',
    边框: bool = True
) -> None:
    """
    打印表格形式的数据
    
    参数:
        数据: 二维列表数据
        标题行: 标题行
        列宽度: 各列宽度（None表示自动）
        对齐方式: '左', '右', '中'
        边框: 是否显示边框
        
    示例:
        >>> 打印表格([['张三', 25], ['李四', 30]], 标题行=['姓名', '年龄'])
        +------+------+
        | 姓名 | 年龄 |
        +------+------+
        | 张三 |   25 |
        | 李四 |   30 |
        +------+------+
    """
    if not 数据 and not 标题行:
        return
    
    # 合并标题和数据
    所有行 = []
    if 标题行:
        所有行.append(标题行)
    所有行.extend(数据)
    
    # 计算列数
    if not 所有行:
        return
    
    列数 = max(len(行) for 行 in 所有行)
    
    # 计算列宽度
    if 列宽度 is None:
        列宽度 = []
        for i in range(列数):
            最大宽度 = max(len(str(行[i])) if i < len(行) else 0 for 行 in 所有行)
            列宽度.append(最大宽度)
    
    # 对齐函数
    def 对齐(文本, 宽度):
        文本 = str(文本)
        if 对齐方式 == '左':
            return 文本.ljust(宽度)
        elif 对齐方式 == '右':
            return 文本.rjust(宽度)
        else:
            return 文本.center(宽度)
    
    # 打印边框
    def 打印边框行():
        if 边框:
            边框部分 = ['+' + '-' * (宽 + 2) for 宽 in 列宽度]
            print(''.join(边框部分) + '+')
    
    # 打印数据行
    def 打印数据行(行, 是否标题=False):
        单元格 = []
        for i in range(列数):
            if i < len(行):
                单元格内容 = 对齐(行[i], 列宽度[i])
            else:
                单元格内容 = ' ' * 列宽度[i]
            单元格.append(f'| {单元格内容} ')
        print(''.join(单元格) + '|')
    
    # 打印表格
    打印边框行()
    
    if 标题行:
        打印数据行(标题行, 是否标题=True)
        打印边框行()
    
    for 行 in 数据:
        打印数据行(行)
    
    打印边框行()


def 创建美化打印器(
    缩进: int = 1,
    宽度: int = 80,
    深度: Optional[int] = None,
    流: Optional[IO] = None,
    排序键: bool = True
) -> pprint.PrettyPrinter:
    """
    创建美化打印器对象
    
    参数:
        缩进: 缩进空格数
        宽度: 每行最大宽度
        深度: 最大打印深度
        流: 输出流
        排序键: 是否排序字典键
        
    返回:
        PrettyPrinter对象
        
    示例:
        >>> 打印器 = 创建美化打印器(缩进=2, 宽度=40)
        >>> 打印器.pprint({'a': 1, 'b': 2})
    """
    return pprint.PrettyPrinter(
        indent=缩进,
        width=宽度,
        depth=深度,
        stream=流,
        sort_dicts=排序键
    )


def 判断是否可读(对象: Any) -> bool:
    """
    判断对象是否可读（可安全打印）
    
    参数:
        对象: 要判断的对象
        
    返回:
        是否可读
        
    示例:
        >>> 判断是否可读([1, 2, 3])
        True
    """
    try:
        repr(对象)
        return True
    except Exception:
        return False


# ============================================================================
# 导出所有函数
# ============================================================================

__all__ = [
    # 基本功能
    '美化打印', '格式化对象', '安全表示',
    
    # 特定类型打印
    '打印字典', '打印列表',
    
    # 表格打印
    '打印表格',
    
    # 工具
    '创建美化打印器', '判断是否可读',
]
