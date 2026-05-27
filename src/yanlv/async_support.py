"""
言律语言异步编程支持

实现async/await语法支持
"""

from typing import Any, Callable, Optional, List
import asyncio
import functools


class AsyncFunction:
    """异步函数包装类"""
    
    def __init__(self, func: Callable, name: str):
        """
        初始化异步函数
        
        Args:
            func: 函数对象
            name: 函数名
        """
        self.func = func
        self.name = name
        self.is_coroutine = asyncio.iscoroutinefunction(func)
    
    async def call(self, *args, **kwargs) -> Any:
        """
        调用异步函数
        
        Args:
            args: 位置参数
            kwargs: 关键字参数
            
        Returns:
            函数返回值
        """
        if self.is_coroutine:
            return await self.func(*args, **kwargs)
        else:
            # 如果不是协程函数,在事件循环中运行
            return await asyncio.get_event_loop().run_in_executor(
                None, functools.partial(self.func, *args, **kwargs)
            )


class AsyncTask:
    """异步任务"""
    
    def __init__(self, coro, name: str = ""):
        """
        初始化异步任务
        
        Args:
            coro: 协程对象
            name: 任务名
        """
        self.coro = coro
        self.name = name
        self.task: Optional[asyncio.Task] = None
        self.result: Any = None
        self.exception: Optional[Exception] = None
        self.completed = False
    
    def start(self) -> None:
        """启动任务"""
        if self.task is None:
            self.task = asyncio.create_task(self._run())
    
    async def _run(self) -> None:
        """运行任务"""
        try:
            self.result = await self.coro
            self.completed = True
        except Exception as e:
            self.exception = e
            self.completed = True
    
    async def wait(self) -> Any:
        """
        等待任务完成
        
        Returns:
            任务结果
        """
        if self.task is None:
            self.start()
        
        await self.task
        
        if self.exception:
            raise self.exception
        
        return self.result
    
    def is_done(self) -> bool:
        """检查任务是否完成"""
        return self.completed


class AsyncManager:
    """
    异步编程管理器
    
    管理异步函数和任务
    """
    
    def __init__(self):
        """初始化异步管理器"""
        self.functions: dict[str, AsyncFunction] = {}
        self.tasks: List[AsyncTask] = []
    
    def register_function(self, name: str, func: Callable) -> None:
        """
        注册异步函数
        
        Args:
            name: 函数名
            func: 函数对象
        """
        self.functions[name] = AsyncFunction(func, name)
    
    def get_function(self, name: str) -> Optional[AsyncFunction]:
        """
        获取异步函数
        
        Args:
            name: 函数名
            
        Returns:
            异步函数对象
        """
        return self.functions.get(name)
    
    async def call_function(self, name: str, *args, **kwargs) -> Any:
        """
        调用异步函数
        
        Args:
            name: 函数名
            args: 位置参数
            kwargs: 关键字参数
            
        Returns:
            函数返回值
        """
        func = self.get_function(name)
        if func is None:
            raise NameError(f"未定义的异步函数: {name}")
        
        return await func.call(*args, **kwargs)
    
    def create_task(self, coro, name: str = "") -> AsyncTask:
        """
        创建异步任务
        
        Args:
            coro: 协程对象
            name: 任务名
            
        Returns:
            异步任务
        """
        task = AsyncTask(coro, name)
        self.tasks.append(task)
        return task
    
    async def wait_all(self) -> List[Any]:
        """
        等待所有任务完成
        
        Returns:
            所有任务结果列表
        """
        results = []
        for task in self.tasks:
            result = await task.wait()
            results.append(result)
        return results
    
    async def wait_any(self) -> Any:
        """
        等待任意一个任务完成
        
        Returns:
            第一个完成的任务结果
        """
        tasks = [task.wait() for task in self.tasks]
        done, pending = await asyncio.wait(
            tasks,
            return_when=asyncio.FIRST_COMPLETED
        )
        
        # 取消未完成的任务
        for task in pending:
            task.cancel()
        
        # 返回第一个完成的结果
        return await done.pop()
    
    def clear_tasks(self) -> None:
        """清空任务列表"""
        self.tasks.clear()


class AsyncEventLoop:
    """异步事件循环管理"""
    
    def __init__(self):
        """初始化事件循环"""
        self.loop: Optional[asyncio.AbstractEventLoop] = None
    
    def get_loop(self) -> asyncio.AbstractEventLoop:
        """获取事件循环"""
        if self.loop is None:
            try:
                self.loop = asyncio.get_event_loop()
            except RuntimeError:
                self.loop = asyncio.new_event_loop()
                asyncio.set_event_loop(self.loop)
        return self.loop
    
    def run(self, coro) -> Any:
        """
        运行协程
        
        Args:
            coro: 协程对象
            
        Returns:
            协程结果
        """
        loop = self.get_loop()
        return loop.run_until_complete(coro)
    
    def run_forever(self) -> None:
        """永久运行事件循环"""
        loop = self.get_loop()
        loop.run_forever()
    
    def stop(self) -> None:
        """停止事件循环"""
        if self.loop is not None:
            self.loop.stop()


# 异步装饰器
def async_func(func: Callable) -> Callable:
    """
    异步函数装饰器
    
    Args:
        func: 函数对象
        
    Returns:
        包装后的函数
    """
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        if asyncio.iscoroutinefunction(func):
            return await func(*args, **kwargs)
        else:
            loop = asyncio.get_event_loop()
            return await loop.run_in_executor(
                None, functools.partial(func, *args, **kwargs)
            )
    
    return wrapper


# 异步工具函数
async def sleep(seconds: float) -> None:
    """
    异步休眠
    
    Args:
        seconds: 休眠秒数
    """
    await asyncio.sleep(seconds)


async def gather(*coros) -> List[Any]:
    """
    并发执行多个协程
    
    Args:
        coros: 协程对象列表
        
    Returns:
        结果列表
    """
    return await asyncio.gather(*coros)


async def wait_for(coro, timeout: float) -> Any:
    """
    等待协程完成,带超时
    
    Args:
        coro: 协程对象
        timeout: 超时时间(秒)
        
    Returns:
        协程结果
    """
    return await asyncio.wait_for(coro, timeout)


# 全局异步管理器实例
_global_async_manager: Optional[AsyncManager] = None


def get_async_manager() -> AsyncManager:
    """获取全局异步管理器"""
    global _global_async_manager
    if _global_async_manager is None:
        _global_async_manager = AsyncManager()
    return _global_async_manager
