"""
言律语言shutil模块扩展
提供shutil标准库的中文版本
"""

import shutil
import os
from typing import Optional, List
from pathlib import Path


def 复制文件(
    源文件: str,
    目标文件: str,
    保留元数据: bool = True
) -> str:
    """
    复制文件
    
    参数:
        源文件: 源文件路径
        目标文件: 目标文件路径
        保留元数据: 是否保留元数据（权限、时间戳等）
        
    返回:
        目标文件路径
        
    示例:
        >>> 复制文件('source.txt', 'dest.txt')
        'dest.txt'
    """
    if 保留元数据:
        return shutil.copy2(源文件, 目标文件)
    return shutil.copy(源文件, 目标文件)


def 复制目录(
    源目录: str,
    目标目录: str,
    忽略模式: Optional[List[str]] = None
) -> str:
    """
    复制目录
    
    参数:
        源目录: 源目录路径
        目标目录: 目标目录路径
        忽略模式: 要忽略的文件模式列表
        
    返回:
        目标目录路径
        
    示例:
        >>> 复制目录('src', 'dest')
        'dest'
    """
    if 忽略模式:
        忽略函数 = shutil.ignore_patterns(*忽略模式)
        return shutil.copytree(源目录, 目标目录, ignore=忽略函数)
    return shutil.copytree(源目录, 目标目录)


def 移动文件或目录(
    源路径: str,
    目标路径: str
) -> str:
    """
    移动文件或目录
    
    参数:
        源路径: 源路径
        目标路径: 目标路径
        
    返回:
        目标路径
        
    示例:
        >>> 移动文件或目录('old.txt', 'new.txt')
        'new.txt'
    """
    return shutil.move(源路径, 目标路径)


def 删除目录(
    目录路径: str,
    忽略错误: bool = False
) -> None:
    """
    删除目录及其内容
    
    参数:
        目录路径: 目录路径
        忽略错误: 是否忽略错误
        
    示例:
        >>> 删除目录('mydir')
    """
    shutil.rmtree(目录路径, ignore_errors=忽略错误)


def 获取磁盘使用情况(路径: str = '.') -> tuple:
    """
    获取磁盘使用情况
    
    参数:
        路径: 路径（默认当前目录）
        
    返回:
        (总空间, 已用空间, 可用空间)元组（字节）
        
    示例:
        >>> 总空间, 已用空间, 可用空间 = 获取磁盘使用情况()
        >>> print(f'可用空间: {可用空间 / (1024**3):.2f} GB')
    """
    return shutil.disk_usage(路径)


def 获取磁盘使用情况字典(路径: str = '.') -> dict:
    """
    获取磁盘使用情况（字典形式）
    
    参数:
        路径: 路径
        
    返回:
        {'总空间', '已用空间', '可用空间', '使用率'}字典
        
    示例:
        >>> 信息 = 获取磁盘使用情况字典()
        >>> print(信息['使用率'])
    """
    总空间, 已用空间, 可用空间 = shutil.disk_usage(路径)
    使用率 = (已用空间 / 总空间) * 100 if 总空间 > 0 else 0
    
    return {
        '总空间': 总空间,
        '已用空间': 已用空间,
        '可用空间': 可用空间,
        '使用率': 使用率
    }


def 创建归档(
    归档名称: str,
    格式: str,
    根目录: str,
    基目录: Optional[str] = None
) -> str:
    """
    创建归档文件（压缩包）
    
    参数:
        归档名称: 归档文件名称（不含扩展名）
        格式: 格式（'zip', 'tar', 'gztar', 'bztar', 'xztar'）
        根目录: 根目录
        基目录: 基目录（None表示根目录）
        
    返回:
        归档文件路径
        
    示例:
        >>> 创建归档('backup', 'zip', 'mydir')
        'backup.zip'
    """
    return shutil.make_archive(归档名称, 格式, 根目录, base_dir=基目录)


def 解压归档(
    归档文件: str,
    解压目录: Optional[str] = None,
    格式: Optional[str] = None
) -> str:
    """
    解压归档文件
    
    参数:
        归档文件: 归档文件路径
        解压目录: 解压目录（None表示当前目录）
        格式: 格式（None表示自动检测）
        
    返回:
        解压目录路径
        
    示例:
        >>> 解压归档('backup.zip', 'output')
        'output'
    """
    return shutil.unpack_archive(归档文件, 解压目录, format=格式)


def 查找可执行文件(名称: str, 路径: Optional[str] = None) -> Optional[str]:
    """
    查找可执行文件
    
    参数:
        名称: 可执行文件名称
        路径: 搜索路径（None表示系统PATH）
        
    返回:
        可执行文件路径或None
        
    示例:
        >>> 查找可执行文件('python')
        '/usr/bin/python'
    """
    return shutil.which(名称, path=路径)


def 获取文件大小(文件路径: str) -> int:
    """
    获取文件大小（字节）
    
    参数:
        文件路径: 文件路径
        
    返回:
        文件大小
        
    示例:
        >>> 获取文件大小('test.txt')
        1024
    """
    return os.path.getsize(文件路径)


def 获取目录大小(目录路径: str) -> int:
    """
    获取目录总大小（字节）
    
    参数:
        目录路径: 目录路径
        
    返回:
        目录总大小
        
    示例:
        >>> 获取目录大小('mydir')
        10240
    """
    总大小 = 0
    for 根目录, 子目录, 文件列表 in os.walk(目录路径):
        for 文件名 in 文件列表:
            文件路径 = os.path.join(根目录, 文件名)
            try:
                总大小 += os.path.getsize(文件路径)
            except OSError:
                pass
    return 总大小


def 格式化文件大小(字节数: int) -> str:
    """
    格式化文件大小为易读形式
    
    参数:
        字节数: 字节数
        
    返回:
        格式化后的字符串
        
    示例:
        >>> 格式化文件大小(1024)
        '1.00 KB'
        >>> 格式化文件大小(1536)
        '1.50 KB'
    """
    for 单位 in ['B', 'KB', 'MB', 'GB', 'TB', 'PB']:
        if 字节数 < 1024.0:
            return f'{字节数:.2f} {单位}'
        字节数 /= 1024.0
    return f'{字节数:.2f} EB'


def 复制文件内容(
    源文件: str,
    目标文件: str,
    块大小: int = 65536
) -> None:
    """
    复制文件内容（手动复制）
    
    参数:
        源文件: 源文件路径
        目标文件: 目标文件路径
        块大小: 复制块大小
        
    示例:
        >>> 复制文件内容('source.txt', 'dest.txt')
    """
    with open(源文件, 'rb') as 源:
        with open(目标文件, 'wb') as 目标:
            while True:
                块 = 源.read(块大小)
                if not 块:
                    break
                目标.write(块)


def 安全删除文件(文件路径: str, 忽略错误: bool = True) -> bool:
    """
    安全删除文件
    
    参数:
        文件路径: 文件路径
        忽略错误: 是否忽略错误
        
    返回:
        是否成功删除
        
    示例:
        >>> 安全删除文件('test.txt')
        True
    """
    try:
        if os.path.exists(文件路径):
            if os.path.isfile(文件路径):
                os.remove(文件路径)
            elif os.path.isdir(文件路径):
                shutil.rmtree(文件路径)
        return True
    except Exception:
        if not 忽略错误:
            raise
        return False


def 同步目录(
    源目录: str,
    目标目录: str,
    删除多余文件: bool = False
) -> dict:
    """
    同步目录
    
    参数:
        源目录: 源目录
        目标目录: 目标目录
        删除多余文件: 是否删除目标目录中多余的文件
        
    返回:
        {'复制': 数量, '删除': 数量}字典
        
    示例:
        >>> 同步目录('src', 'dest')
        {'复制': 10, '删除': 0}
    """
    统计 = {'复制': 0, '删除': 0}
    
    # 确保目标目录存在
    os.makedirs(目标目录, exist_ok=True)
    
    # 复制源目录文件
    for 项目 in os.listdir(源目录):
        源路径 = os.path.join(源目录, 项目)
        目标路径 = os.path.join(目标目录, 项目)
        
        if os.path.isdir(源路径):
            子统计 = 同步目录(源路径, 目标路径, 删除多余文件)
            统计['复制'] += 子统计['复制']
            统计['删除'] += 子统计['删除']
        else:
            shutil.copy2(源路径, 目标路径)
            统计['复制'] += 1
    
    # 删除目标目录中多余的文件
    if 删除多余文件:
        for 项目 in os.listdir(目标目录):
            目标路径 = os.path.join(目标目录, 项目)
            源路径 = os.path.join(源目录, 项目)
            
            if not os.path.exists(源路径):
                安全删除文件(目标路径)
                统计['删除'] += 1
    
    return 统计


# ============================================================================
# 导出所有函数
# ============================================================================

__all__ = [
    '复制文件',
    '复制目录',
    '移动文件或目录',
    '删除目录',
    '获取磁盘使用情况',
    '获取磁盘使用情况字典',
    '创建归档',
    '解压归档',
    '查找可执行文件',
    '获取文件大小',
    '获取目录大小',
    '格式化文件大小',
    '复制文件内容',
    '安全删除文件',
    '同步目录',
]
