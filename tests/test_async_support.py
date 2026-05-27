"""
异步支持测试

测试AsyncManager的功能
"""

import pytest
import asyncio
from yanlv.async_support import (
    AsyncFunction,
    AsyncTask,
    AsyncManager,
    AsyncEventLoop,
    async_func,
    sleep,
    gather,
    wait_for,
    get_async_manager
)


class TestAsyncFunction:
    """异步函数测试"""
    
    @pytest.mark.asyncio
    async def test_async_function_call(self):
        """测试异步函数调用"""
        async def test_func(x):
            await asyncio.sleep(0.01)
            return x * 2
        
        func = AsyncFunction(test_func, "test")
        result = await func.call(5)
        assert result == 10
    
    @pytest.mark.asyncio
    async def test_sync_function_call(self):
        """测试同步函数调用"""
        def test_func(x):
            return x * 3
        
        func = AsyncFunction(test_func, "test")
        result = await func.call(5)
        assert result == 15


class TestAsyncTask:
    """异步任务测试"""
    
    @pytest.mark.asyncio
    async def test_task_execution(self):
        """测试任务执行"""
        async def test_coro():
            await asyncio.sleep(0.01)
            return "完成"
        
        task = AsyncTask(test_coro(), "test_task")
        result = await task.wait()
        assert result == "完成"
        assert task.is_done()
    
    @pytest.mark.asyncio
    async def test_task_exception(self):
        """测试任务异常"""
        async def test_coro():
            await asyncio.sleep(0.01)
            raise ValueError("测试异常")
        
        task = AsyncTask(test_coro(), "test_task")
        with pytest.raises(ValueError):
            await task.wait()


class TestAsyncManager:
    """异步管理器测试"""
    
    def test_manager_initialization(self):
        """测试管理器初始化"""
        manager = AsyncManager()
        assert len(manager.functions) == 0
        assert len(manager.tasks) == 0
    
    def test_register_function(self):
        """测试注册函数"""
        manager = AsyncManager()
        
        async def test_func():
            return 42
        
        manager.register_function("test", test_func)
        assert "test" in manager.functions
    
    @pytest.mark.asyncio
    async def test_call_function(self):
        """测试调用函数"""
        manager = AsyncManager()
        
        async def test_func(x):
            return x * 2
        
        manager.register_function("test", test_func)
        result = await manager.call_function("test", 5)
        assert result == 10
    
    @pytest.mark.asyncio
    async def test_create_task(self):
        """测试创建任务"""
        manager = AsyncManager()
        
        async def test_coro():
            await asyncio.sleep(0.01)
            return "任务完成"
        
        task = manager.create_task(test_coro(), "test_task")
        result = await task.wait()
        assert result == "任务完成"
    
    @pytest.mark.asyncio
    async def test_wait_all(self):
        """测试等待所有任务"""
        manager = AsyncManager()
        
        async def task1():
            await asyncio.sleep(0.01)
            return 1
        
        async def task2():
            await asyncio.sleep(0.01)
            return 2
        
        manager.create_task(task1(), "task1")
        manager.create_task(task2(), "task2")
        
        results = await manager.wait_all()
        assert 1 in results
        assert 2 in results


class TestAsyncEventLoop:
    """异步事件循环测试"""
    
    def test_get_loop(self):
        """测试获取事件循环"""
        event_loop = AsyncEventLoop()
        loop = event_loop.get_loop()
        assert loop is not None


class TestAsyncDecorators:
    """异步装饰器测试"""
    
    @pytest.mark.asyncio
    async def test_async_decorator(self):
        """测试异步装饰器"""
        @async_func
        async def test_func(x):
            await asyncio.sleep(0.01)
            return x * 2
        
        result = await test_func(5)
        assert result == 10
    
    @pytest.mark.asyncio
    async def test_async_decorator_sync(self):
        """测试异步装饰器(同步函数)"""
        @async_func
        def test_func(x):
            return x * 3
        
        result = await test_func(5)
        assert result == 15


class TestAsyncUtilities:
    """异步工具函数测试"""
    
    @pytest.mark.asyncio
    async def test_sleep(self):
        """测试异步休眠"""
        import time
        start = time.time()
        await sleep(0.1)
        end = time.time()
        assert end - start >= 0.1
    
    @pytest.mark.asyncio
    async def test_gather(self):
        """测试并发执行"""
        async def task1():
            await asyncio.sleep(0.01)
            return 1
        
        async def task2():
            await asyncio.sleep(0.01)
            return 2
        
        results = await gather(task1(), task2())
        assert results == [1, 2]
    
    @pytest.mark.asyncio
    async def test_wait_for(self):
        """测试带超时等待"""
        async def slow_task():
            await asyncio.sleep(0.01)
            return "完成"
        
        result = await wait_for(slow_task(), timeout=1.0)
        assert result == "完成"
    
    @pytest.mark.asyncio
    async def test_wait_for_timeout(self):
        """测试超时"""
        async def slow_task():
            await asyncio.sleep(2.0)
            return "完成"
        
        with pytest.raises(asyncio.TimeoutError):
            await wait_for(slow_task(), timeout=0.1)


class TestGlobalManager:
    """全局管理器测试"""
    
    def test_get_global_manager(self):
        """测试获取全局管理器"""
        manager1 = get_async_manager()
        manager2 = get_async_manager()
        
        # 应该是同一个实例
        assert manager1 is manager2


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
