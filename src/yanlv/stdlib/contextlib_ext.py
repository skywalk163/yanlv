"""
言律语言contextlib模块扩展
提供contextlib标准库的中文版本
"""

from contextlib import (
    contextmanager, closing, suppress,
    redirect_stdout, redirect_stderr, redirect_stdin,
    ExitStack, nullcontext, AbstractContextManager
)
from typing import Callable, Any, Optional, Type, IO
from io import StringIO


def 上下文管理器装饰器(函数: Callable) -> Callable:
    """
    将生成器函数转换为上下文管理器
    
    参数:
        函数: 生成器函数
        
    返回:
        上下文管理器装饰器
        
    示例:
        >>> @上下文管理器装饰器
        ... def 打开文件(文件名):
        ...     f = open(文件名, 'r')
        ...     try:
        ...         yield f
        ...     finally:
        ...         f.close()
    """
    return contextmanager(函数)


class 关闭上下文:
    """
    自动关闭对象的上下文管理器
    
    参数:
        对象: 需要关闭的对象
        
    示例:
        >>> with 关闭上下文(open('file.txt')) as f:
        ...     data = f.read()
    """
    
    def __init__(self, 对象: Any):
        self.对象 = 对象
    
    def __enter__(self):
        return self.对象
    
    def __exit__(self, *args):
        if hasattr(self.对象, 'close'):
            self.对象.close()


class 忽略异常:
    """
    忽略指定异常的上下文管理器
    
    参数:
        *异常类型: 要忽略的异常类型
        
    示例:
        >>> with 忽略异常(FileNotFoundError):
        ...     os.remove('不存在的文件')
    """
    
    def __init__(self, *异常类型: Type[Exception]):
        self.异常类型 = 异常类型
    
    def __enter__(self):
        return self
    
    def __exit__(self, 异常类型, 异常值, 回溯):
        return 异常类型 is not None and issubclass(异常类型, self.异常类型)


class 重定向标准输出:
    """
    重定向标准输出的上下文管理器
    
    参数:
        目标: 目标文件对象
        
    示例:
        >>> 输出 = StringIO()
        >>> with 重定向标准输出(输出):
        ...     print('hello')
        >>> 输出.getvalue()
        'hello\\n'
    """
    
    def __init__(self, 目标: IO):
        self.目标 = 目标
        self.管理器 = redirect_stdout(目标)
    
    def __enter__(self):
        return self.管理器.__enter__()
    
    def __exit__(self, *args):
        return self.管理器.__exit__(*args)


class 重定向标准错误:
    """
    重定向标准错误的上下文管理器
    
    参数:
        目标: 目标文件对象
        
    示例:
        >>> 错误输出 = StringIO()
        >>> with 重定向标准错误(错误输出):
        ...     import sys
        ...     print('error', file=sys.stderr)
    """
    
    def __init__(self, 目标: IO):
        self.目标 = 目标
        self.管理器 = redirect_stderr(目标)
    
    def __enter__(self):
        return self.管理器.__enter__()
    
    def __exit__(self, *args):
        return self.管理器.__exit__(*args)


class 重定向标准输入:
    """
    重定向标准输入的上下文管理器
    
    参数:
        源: 源文件对象
        
    示例:
        >>> 输入源 = StringIO('hello\\n')
        >>> with 重定向标准输入(输入源):
        ...     line = input()
    """
    
    def __init__(self, 源: IO):
        self.源 = 源
        self.管理器 = redirect_stdin(源)
    
    def __enter__(self):
        return self.管理器.__enter__()
    
    def __exit__(self, *args):
        return self.管理器.__exit__(*args)


class 退出栈:
    """
    管理多个上下文管理器的栈
    
    示例:
        >>> with 退出栈() as 栈:
        ...     f1 = 栈.enter_context(open('file1.txt'))
        ...     f2 = 栈.enter_context(open('file2.txt'))
        ...     # 使用f1和f2
    """
    
    def __init__(self):
        self.栈 = ExitStack()
    
    def __enter__(self):
        self.栈.__enter__()
        return self
    
    def __exit__(self, *args):
        return self.栈.__exit__(*args)
    
    def 进入上下文(self, 上下文管理器: Any) -> Any:
        """进入一个上下文管理器并返回其值"""
        return self.栈.enter_context(上下文管理器)
    
    def 推入回调(self, 回调: Callable, *参数, **关键字参数) -> Any:
        """推入一个退出回调"""
        return self.栈.push(回调, *参数, **关键字参数)
    
    def 回调(self, 回调: Callable, *参数, **关键字参数) -> Callable:
        """注册一个退出回调"""
        return self.栈.callback(回调, *参数, **关键字参数)


class 空上下文:
    """
    空上下文管理器（不执行任何操作）
    
    参数:
        结果: enter方法返回的结果
        
    示例:
        >>> with 空上下文() as x:
        ...     print(x is None)
        True
    """
    
    def __init__(self, 结果: Any = None):
        self.结果 = 结果
        self.管理器 = nullcontext(结果)
    
    def __enter__(self):
        return self.管理器.__enter__()
    
    def __exit__(self, *args):
        return self.管理器.__exit__(*args)


def 捕获输出(函数: Callable) -> Callable:
    """
    捕获函数的标准输出
    
    参数:
        函数: 要捕获输出的函数
        
    返回:
        装饰后的函数
        
    示例:
        >>> @捕获输出
        ... def 打印信息():
        ...     print('hello')
        >>> 打印信息()
        'hello\\n'
    """
    def 包装函数(*args, **kwargs):
        输出 = StringIO()
        with 重定向标准输出(输出):
            函数(*args, **kwargs)
        return 输出.getvalue()
    return 包装函数


class 计时上下文:
    """
    计时代码块执行时间的上下文管理器
    
    示例:
        >>> with 计时上下文() as 计时器:
        ...     # 执行一些代码
        ...     pass
        >>> print(计时器.耗时)
    """
    
    def __init__(self):
        self.开始时间 = None
        self.结束时间 = None
        self.耗时 = None
    
    def __enter__(self):
        import time
        self.开始时间 = time.time()
        return self
    
    def __exit__(self, *args):
        import time
        self.结束时间 = time.time()
        self.耗时 = self.结束时间 - self.开始时间


class 临时修改对象:
    """
    临时修改对象属性的上下文管理器
    
    参数:
        对象: 要修改的对象
        属性名: 属性名称
        新值: 新值
        
    示例:
        >>> class 配置:
        ...     调试模式 = False
        >>> cfg = 配置()
        >>> with 临时修改对象(cfg, '调试模式', True):
        ...     print(cfg.调试模式)
        True
        >>> print(cfg.调试模式)
        False
    """
    
    def __init__(self, 对象: Any, 属性名: str, 新值: Any):
        self.对象 = 对象
        self.属性名 = 属性名
        self.新值 = 新值
        self.原值 = None
    
    def __enter__(self):
        self.原值 = getattr(self.对象, self.属性名)
        setattr(self.对象, self.属性名, self.新值)
        return self
    
    def __exit__(self, *args):
        setattr(self.对象, self.属性名, self.原值)


class 锁定上下文:
    """
    锁定上下文管理器（用于线程同步）
    
    参数:
        锁: 锁对象
        
    示例:
        >>> import threading
        >>> 锁 = threading.Lock()
        >>> with 锁定上下文(锁):
        ...     # 执行需要同步的代码
        ...     pass
    """
    
    def __init__(self, 锁: Any):
        self.锁 = 锁
    
    def __enter__(self):
        self.锁.acquire()
        return self
    
    def __exit__(self, *args):
        self.锁.release()


# ============================================================================
# 导出所有类和函数
# ============================================================================

__all__ = [
    # 装饰器
    '上下文管理器装饰器',
    
    # 上下文管理器类
    '关闭上下文', '忽略异常', '重定向标准输出',
    '重定向标准错误', '重定向标准输入',
    '退出栈', '空上下文',
    
    # 工具上下文管理器
    '计时上下文', '临时修改对象', '锁定上下文',
    
    # 装饰器工具
    '捕获输出',
]
