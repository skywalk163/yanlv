"""
言律语言tempfile模块扩展
提供tempfile标准库的中文版本
"""

import tempfile
import os
from typing import Optional


def 创建临时文件(
    后缀: str = '',
    前缀: str = 'tmp',
    目录: Optional[str] = None,
    文本模式: bool = False
) -> tuple:
    """
    创建临时文件
    
    参数:
        后缀: 文件后缀
        前缀: 文件前缀
        目录: 创建目录（None表示系统临时目录）
        文本模式: 是否为文本模式
        
    返回:
        (文件描述符, 文件路径)元组
        
    示例:
        >>> fd, 路径 = 创建临时文件(后缀='.txt')
        >>> # 使用文件
        >>> os.close(fd)
        >>> os.remove(路径)
    """
    return tempfile.mkstemp(suffix=后缀, prefix=前缀, dir=目录, text=文本模式)


def 创建临时目录(
    前缀: str = 'tmp',
    目录: Optional[str] = None
) -> str:
    """
    创建临时目录
    
    参数:
        前缀: 目录前缀
        目录: 父目录（None表示系统临时目录）
        
    返回:
        临时目录路径
        
    示例:
        >>> 路径 = 创建临时目录()
        >>> # 使用目录
        >>> os.rmdir(路径)
    """
    return tempfile.mkdtemp(prefix=前缀, dir=目录)


def 获取临时目录() -> str:
    """
    获取系统临时目录路径
    
    返回:
        临时目录路径
        
    示例:
        >>> 获取临时目录()
        '/tmp'  # Linux/Mac
        'C:\\Users\\...\\AppData\\Local\\Temp'  # Windows
    """
    return tempfile.gettempdir()


def 获取临时目录环境变量() -> str:
    """
    获取临时目录环境变量名
    
    返回:
        环境变量名
    """
    return tempfile.tempdir


class 临时文件上下文:
    """
    临时文件上下文管理器
    
    参数:
        模式: 文件模式
        后缀: 文件后缀
        前缀: 文件前缀
        目录: 创建目录
        删除: 是否在关闭时删除
        
    示例:
        >>> with 临时文件上下文(模式='w', 后缀='.txt') as f:
        ...     f.write('hello')
    """
    
    def __init__(
        self,
        模式: str = 'w+b',
        后缀: str = '',
        前缀: str = 'tmp',
        目录: Optional[str] = None,
        删除: bool = True
    ):
        self.模式 = 模式
        self.后缀 = 后缀
        self.前缀 = 前缀
        self.目录 = 目录
        self.删除 = 删除
        self.文件 = None
    
    def __enter__(self):
        self.文件 = tempfile.NamedTemporaryFile(
            mode=self.模式,
            suffix=self.后缀,
            prefix=self.前缀,
            dir=self.目录,
            delete=self.删除
        )
        return self.文件
    
    def __exit__(self, *args):
        if self.文件:
            self.文件.close()


class 临时目录上下文:
    """
    临时目录上下文管理器
    
    参数:
        前缀: 目录前缀
        目录: 父目录
        忽略删除错误: 是否忽略删除错误
        
    示例:
        >>> with 临时目录上下文() as 目录:
        ...     # 在目录中创建文件
        ...     pass
    """
    
    def __init__(
        self,
        前缀: str = 'tmp',
        目录: Optional[str] = None,
        忽略删除错误: bool = False
    ):
        self.前缀 = 前缀
        self.目录 = 目录
        self.忽略删除错误 = 忽略删除错误
        self.临时目录 = None
    
    def __enter__(self):
        self.临时目录 = tempfile.mkdtemp(prefix=self.前缀, dir=self.目录)
        return self.临时目录
    
    def __exit__(self, *args):
        if self.临时目录:
            try:
                import shutil
                shutil.rmtree(self.临时目录)
            except Exception:
                if not self.忽略删除错误:
                    raise


def 创建命名临时文件(
    模式: str = 'w+b',
    后缀: str = '',
    前缀: str = 'tmp',
    目录: Optional[str] = None,
    删除: bool = True
):
    """
    创建命名临时文件
    
    参数:
        模式: 文件模式
        后缀: 文件后缀
        前缀: 文件前缀
        目录: 创建目录
        删除: 是否在关闭时删除
        
    返回:
        NamedTemporaryFile对象
        
    示例:
        >>> f = 创建命名临时文件(模式='w', 后缀='.txt')
        >>> f.write(b'hello')
        >>> f.close()
    """
    return tempfile.NamedTemporaryFile(
        mode=模式,
        suffix=后缀,
        prefix=前缀,
        dir=目录,
        delete=删除
    )


def 创建临时文件对象(
    模式: str = 'w+b',
    最大大小: Optional[int] = None
):
    """
    创建临时文件对象（内存或磁盘）
    
    参数:
        模式: 文件模式
        最大大小: 最大内存大小（超过则写入磁盘）
        
    返回:
        SpooledTemporaryFile对象
        
    示例:
        >>> f = 创建临时文件对象(模式='w+', 最大大小=1024)
        >>> f.write('hello')
        >>> f.seek(0)
        >>> f.read()
    """
    return tempfile.SpooledTemporaryFile(
        mode=模式,
        max_size=最大大小
    )


def 创建临时文件句柄(
    模式: str = 'w+b',
    后缀: str = '',
    前缀: str = 'tmp',
    目录: Optional[str] = None
):
    """
    创建临时文件句柄（自动删除）
    
    参数:
        模式: 文件模式
        后缀: 文件后缀
        前缀: 文件前缀
        目录: 创建目录
        
    返回:
        TemporaryFile对象
        
    示例:
        >>> f = 创建临时文件句柄(模式='w+')
        >>> f.write(b'hello')
        >>> f.close()  # 文件自动删除
    """
    return tempfile.TemporaryFile(
        mode=模式,
        suffix=后缀,
        prefix=前缀,
        dir=目录
    )


def 在临时目录执行(函数, *参数, **关键字参数):
    """
    在临时目录中执行函数
    
    参数:
        函数: 要执行的函数
        *参数: 函数参数
        **关键字参数: 函数关键字参数
        
    返回:
        函数返回值
        
    示例:
        >>> def 处理文件():
        ...     # 在临时目录中工作
        ...     pass
        >>> 在临时目录执行(处理文件)
    """
    with 临时目录上下文() as 目录:
        原目录 = os.getcwd()
        try:
            os.chdir(目录)
            return 函数(*参数, **关键字参数)
        finally:
            os.chdir(原目录)


def 清理临时文件(文件路径: str, 忽略错误: bool = True) -> bool:
    """
    清理临时文件
    
    参数:
        文件路径: 文件路径
        忽略错误: 是否忽略错误
        
    返回:
        是否成功删除
        
    示例:
        >>> 清理临时文件('/tmp/test.txt')
        True
    """
    try:
        if os.path.isfile(文件路径):
            os.remove(文件路径)
        elif os.path.isdir(文件路径):
            import shutil
            shutil.rmtree(文件路径)
        return True
    except Exception:
        if not 忽略错误:
            raise
        return False


# ============================================================================
# 导出所有函数和类
# ============================================================================

__all__ = [
    '创建临时文件',
    '创建临时目录',
    '获取临时目录',
    '获取临时目录环境变量',
    '临时文件上下文',
    '临时目录上下文',
    '创建命名临时文件',
    '创建临时文件对象',
    '创建临时文件句柄',
    '在临时目录执行',
    '清理临时文件',
]
