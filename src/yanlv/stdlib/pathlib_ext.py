"""
言律语言pathlib模块扩展
提供pathlib标准库的中文版本
"""

from pathlib import Path, PurePath, PosixPath, WindowsPath
from typing import Union, Optional, List, Iterator
import os


class 路径对象(Path):
    """
    路径对象，用于文件系统操作
    
    参数:
        路径: 路径字符串
        
    示例:
        >>> p = 路径对象('test.txt')
        >>> p.是否存在()
        False
        >>> p.写入文本('hello')
        >>> p.读取文本()
        'hello'
    """
    
    def __new__(cls, 路径: str = '.'):
        return super().__new__(cls, 路径)
    
    def 是否存在(self) -> bool:
        """检查路径是否存在"""
        return self.exists()
    
    def 是否文件(self) -> bool:
        """检查是否为文件"""
        return self.is_file()
    
    def 是否目录(self) -> bool:
        """检查是否为目录"""
        return self.is_dir()
    
    def 是否链接(self) -> bool:
        """检查是否为符号链接"""
        return self.is_symlink()
    
    def 是否绝对路径(self) -> bool:
        """检查是否为绝对路径"""
        return self.is_absolute()
    
    def 是否相对路径(self) -> bool:
        """检查是否为相对路径"""
        return not self.is_absolute()
    
    def 获取绝对路径(self) -> '路径对象':
        """获取绝对路径"""
        return 路径对象(str(self.absolute()))
    
    def 获取父目录(self) -> '路径对象':
        """获取父目录"""
        return 路径对象(str(self.parent))
    
    def 获取文件名(self) -> str:
        """获取文件名"""
        return self.name
    
    def 获取扩展名(self) -> str:
        """获取文件扩展名"""
        return self.suffix
    
    def 获取所有扩展名(self) -> List[str]:
        """获取所有扩展名"""
        return self.suffixes
    
    def 获取主文件名(self) -> str:
        """获取主文件名（不含扩展名）"""
        return self.stem
    
    def 拼接路径(self, *子路径: str) -> '路径对象':
        """拼接路径"""
        return 路径对象(str(self.joinpath(*子路径)))
    
    def 相对于(self, 其他路径: Union[str, '路径对象']) -> '路径对象':
        """计算相对路径"""
        if isinstance(其他路径, 路径对象):
            return 路径对象(str(self.relative_to(其他路径)))
        return 路径对象(str(self.relative_to(其他路径)))
    
    def 解析路径(self, 严格模式: bool = False) -> '路径对象':
        """解析路径（解析符号链接）"""
        return 路径对象(str(self.resolve(strict=严格模式)))
    
    def 创建目录(self, 父级: bool = True, 存在即忽略: bool = True) -> None:
        """
        创建目录
        
        参数:
            父级: 是否创建父目录
            存在即忽略: 目录存在时是否忽略错误
        """
        self.mkdir(parents=父级, exist_ok=存在即忽略)
    
    def 创建文件(self, 存在即忽略: bool = True) -> None:
        """创建空文件"""
        if not 存在即忽略 or not self.是否存在():
            self.touch()
    
    def 删除文件(self, 缺失即忽略: bool = False) -> None:
        """删除文件"""
        if 缺失即忽略 and not self.是否存在():
            return
        self.unlink()
    
    def 删除目录(self, 递归: bool = False) -> None:
        """删除目录"""
        if 递归:
            import shutil
            shutil.rmtree(self)
        else:
            self.rmdir()
    
    def 读取文本(self, 编码: str = 'utf-8') -> str:
        """读取文本文件"""
        return self.read_text(encoding=编码)
    
    def 写入文本(self, 内容: str, 编码: str = 'utf-8', 追加: bool = False) -> None:
        """写入文本文件"""
        mode = 'a' if 追加 else 'w'
        self.write_text(内容, encoding=编码)
    
    def 读取字节(self) -> bytes:
        """读取字节文件"""
        return self.read_bytes()
    
    def 写入字节(self, 内容: bytes) -> None:
        """写入字节文件"""
        return self.write_bytes(内容)
    
    def 列出目录(self, 模式: Optional[str] = None) -> List['路径对象']:
        """
        列出目录内容
        
        参数:
            模式: glob模式（可选）
            
        返回:
            路径对象列表
        """
        if 模式:
            return [路径对象(str(p)) for p in self.glob(模式)]
        return [路径对象(str(p)) for p in self.iterdir()]
    
    def 递归列出(self, 模式: str = '**/*') -> Iterator['路径对象']:
        """递归列出所有文件"""
        for p in self.glob(模式):
            yield 路径对象(str(p))
    
    def 查找文件(self, 模式: str) -> Iterator['路径对象']:
        """查找匹配的文件"""
        for p in self.glob(模式):
            yield 路径对象(str(p))
    
    def 复制到(self, 目标: Union[str, '路径对象']) -> '路径对象':
        """复制文件或目录"""
        import shutil
        if isinstance(目标, 路径对象):
            目标 = str(目标)
        shutil.copy2(self, 目标)
        return 路径对象(目标)
    
    def 移动到(self, 目标: Union[str, '路径对象']) -> '路径对象':
        """移动文件或目录"""
        import shutil
        if isinstance(目标, 路径对象):
            目标 = str(目标)
        shutil.move(self, 目标)
        return 路径对象(目标)
    
    def 重命名(self, 新名称: str) -> '路径对象':
        """重命名文件或目录"""
        新路径 = self.parent / 新名称
        self.rename(新路径)
        return 路径对象(str(新路径))
    
    def 获取大小(self) -> int:
        """获取文件大小（字节）"""
        return self.stat().st_size
    
    def 获取修改时间(self) -> float:
        """获取修改时间（时间戳）"""
        return self.stat().st_mtime
    
    def 获取访问时间(self) -> float:
        """获取访问时间（时间戳）"""
        return self.stat().st_atime
    
    def 获取创建时间(self) -> float:
        """获取创建时间（时间戳）"""
        return self.stat().st_ctime
    
    def 更改权限(self, 模式: int) -> None:
        """更改文件权限"""
        self.chmod(模式)
    
    def 更改所有者(self, 用户: int, 组: int = None) -> None:
        """更改文件所有者"""
        if 组 is None:
            self.chown(用户)
        else:
            self.chown(用户, 组)
    
    def 打开(self, 模式: str = 'r', 编码: Optional[str] = None):
        """打开文件"""
        return self.open(mode=模式, encoding=编码)
    
    def 替换扩展名(self, 新扩展名: str) -> '路径对象':
        """替换文件扩展名"""
        return 路径对象(str(self.with_suffix(新扩展名)))
    
    def 替换文件名(self, 新文件名: str) -> '路径对象':
        """替换文件名"""
        return 路径对象(str(self.with_name(新文件名)))
    
    def 作为posix路径(self) -> str:
        """转换为POSIX路径字符串"""
        return self.as_posix()
    
    def 作为uri(self) -> str:
        """转换为URI"""
        return self.as_uri()


def 当前目录() -> 路径对象:
    """获取当前工作目录"""
    return 路径对象('.')


def 用户主目录() -> 路径对象:
    """获取用户主目录"""
    return 路径对象(str(Path.home()))


def 临时目录() -> 路径对象:
    """获取临时目录"""
    import tempfile
    return 路径对象(tempfile.gettempdir())


def 创建临时文件(后缀: str = '', 前缀: str = 'tmp') -> 路径对象:
    """创建临时文件"""
    import tempfile
    fd, 路径 = tempfile.mkstemp(suffix=后缀, prefix=前缀)
    os.close(fd)
    return 路径对象(路径)


def 创建临时目录(前缀: str = 'tmp') -> 路径对象:
    """创建临时目录"""
    import tempfile
    return 路径对象(tempfile.mkdtemp(prefix=前缀))


# ============================================================================
# 导出所有类和函数
# ============================================================================

__all__ = [
    '路径对象',
    '当前目录',
    '用户主目录',
    '临时目录',
    '创建临时文件',
    '创建临时目录',
]
