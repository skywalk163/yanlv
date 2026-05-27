"""
性能监控器测试

测试PerformanceMonitor的功能
"""

import pytest
import time
from yanlv.performance_monitor import (
    PerformanceMonitor, 
    PerformanceContext,
    get_global_monitor,
    monitor_operation
)


class TestPerformanceMonitor:
    """PerformanceMonitor测试类"""
    
    def test_monitor_initialization(self):
        """测试监控器初始化"""
        monitor = PerformanceMonitor()
        assert monitor.enabled
        assert len(monitor.records) == 0
    
    def test_monitor_operation(self):
        """测试操作监控"""
        monitor = PerformanceMonitor()
        
        # 开始操作
        op_id = monitor.start_operation("test_op")
        time.sleep(0.001)  # 模拟操作
        record = monitor.end_operation(op_id)
        
        assert record is not None
        assert record.operation == "test_op"
        assert record.duration > 0
        assert record.success
    
    def test_monitor_operation_failure(self):
        """测试操作失败监控"""
        monitor = PerformanceMonitor()
        
        op_id = monitor.start_operation("test_op")
        record = monitor.end_operation(op_id, success=False, error="测试错误")
        
        assert not record.success
        assert record.error == "测试错误"
    
    def test_monitor_disabled(self):
        """测试禁用监控"""
        monitor = PerformanceMonitor(enabled=False)
        
        op_id = monitor.start_operation("test_op")
        record = monitor.end_operation(op_id)
        
        assert op_id == ""
        assert record is None
    
    def test_monitor_metrics(self):
        """测试指标记录"""
        monitor = PerformanceMonitor()
        
        monitor.record_metric("cache_hit_rate", 0.85, unit="%")
        monitor.record_metric("memory_usage", 1024, unit="MB")
        
        assert len(monitor.metrics["cache_hit_rate"]) == 1
        assert len(monitor.metrics["memory_usage"]) == 1
    
    def test_monitor_counters(self):
        """测试计数器"""
        monitor = PerformanceMonitor()
        
        monitor.increment_counter("requests")
        monitor.increment_counter("requests")
        monitor.increment_counter("requests", delta=5)
        
        assert monitor.counters["requests"] == 7
    
    def test_monitor_gauges(self):
        """测试仪表"""
        monitor = PerformanceMonitor()
        
        monitor.set_gauge("cpu_usage", 45.5)
        monitor.set_gauge("memory_usage", 1024.0)
        
        assert monitor.gauges["cpu_usage"] == 45.5
        assert monitor.gauges["memory_usage"] == 1024.0
    
    def test_monitor_stats(self):
        """测试统计信息"""
        monitor = PerformanceMonitor()
        
        # 执行多个操作
        for i in range(10):
            op_id = monitor.start_operation("test_op")
            time.sleep(0.001)
            monitor.end_operation(op_id, success=(i % 2 == 0))
        
        stats = monitor.get_operation_stats("test_op")
        
        assert stats['total_calls'] == 10
        assert stats['success_count'] == 5
        assert stats['failure_count'] == 5
        assert stats['success_rate'] == 0.5
        assert stats['avg_time_ms'] > 0
    
    def test_monitor_all_stats(self):
        """测试所有统计信息"""
        monitor = PerformanceMonitor()
        
        # 执行操作
        for _ in range(5):
            op_id = monitor.start_operation("op1")
            monitor.end_operation(op_id)
        
        for _ in range(3):
            op_id = monitor.start_operation("op2")
            monitor.end_operation(op_id)
        
        monitor.increment_counter("counter1", 10)
        monitor.set_gauge("gauge1", 100.0)
        
        all_stats = monitor.get_all_stats()
        
        assert all_stats['total_operations'] == 8
        assert 'op1' in all_stats['operations']
        assert 'op2' in all_stats['operations']
        assert all_stats['counters']['counter1'] == 10
        assert all_stats['gauges']['gauge1'] == 100.0
    
    def test_monitor_recent_records(self):
        """测试最近记录"""
        monitor = PerformanceMonitor()
        
        # 执行多个操作
        for i in range(20):
            op_id = monitor.start_operation(f"op{i}")
            monitor.end_operation(op_id)
        
        recent = monitor.get_recent_records(limit=10)
        
        assert len(recent) == 10
        # 应该是最后10个操作
        assert recent[-1].operation == "op19"
    
    def test_monitor_clear(self):
        """测试清空数据"""
        monitor = PerformanceMonitor()
        
        # 添加数据
        op_id = monitor.start_operation("test")
        monitor.end_operation(op_id)
        monitor.increment_counter("counter")
        monitor.set_gauge("gauge", 1.0)
        
        # 清空
        monitor.clear()
        
        assert len(monitor.records) == 0
        assert len(monitor.counters) == 0
        assert len(monitor.gauges) == 0


class TestPerformanceContext:
    """PerformanceContext测试类"""
    
    def test_context_success(self):
        """测试成功上下文"""
        monitor = PerformanceMonitor()
        
        with PerformanceContext(monitor, "test_op"):
            time.sleep(0.001)
        
        stats = monitor.get_operation_stats("test_op")
        assert stats['total_calls'] == 1
        assert stats['success_count'] == 1
    
    def test_context_failure(self):
        """测试失败上下文"""
        monitor = PerformanceMonitor()
        
        try:
            with PerformanceContext(monitor, "test_op"):
                raise ValueError("测试错误")
        except ValueError:
            pass
        
        stats = monitor.get_operation_stats("test_op")
        assert stats['total_calls'] == 1
        assert stats['failure_count'] == 1


class TestMonitorDecorator:
    """监控装饰器测试类"""
    
    def test_decorator(self):
        """测试装饰器"""
        @monitor_operation("decorated_func")
        def test_func(x):
            time.sleep(0.001)
            return x * 2
        
        result = test_func(5)
        
        assert result == 10
        
        monitor = get_global_monitor()
        stats = monitor.get_operation_stats("decorated_func")
        
        assert stats['total_calls'] == 1
        assert stats['success_count'] == 1
    
    def test_decorator_with_error(self):
        """测试装饰器错误处理"""
        @monitor_operation("error_func")
        def error_func():
            raise ValueError("测试错误")
        
        try:
            error_func()
        except ValueError:
            pass
        
        monitor = get_global_monitor()
        stats = monitor.get_operation_stats("error_func")
        
        assert stats['total_calls'] == 1
        assert stats['failure_count'] == 1


class TestGlobalMonitor:
    """全局监控器测试"""
    
    def test_get_global_monitor(self):
        """测试获取全局监控器"""
        monitor1 = get_global_monitor()
        monitor2 = get_global_monitor()
        
        # 应该是同一个实例
        assert monitor1 is monitor2


class TestPerformanceAnalysis:
    """性能分析测试"""
    
    def test_operation_performance_analysis(self):
        """测试操作性能分析"""
        monitor = PerformanceMonitor()
        
        # 模拟不同性能的操作
        for i in range(10):
            op_id = monitor.start_operation("fast_op")
            time.sleep(0.001)
            monitor.end_operation(op_id)
        
        for i in range(5):
            op_id = monitor.start_operation("slow_op")
            time.sleep(0.005)
            monitor.end_operation(op_id)
        
        fast_stats = monitor.get_operation_stats("fast_op")
        slow_stats = monitor.get_operation_stats("slow_op")
        
        print(f"\n性能分析:")
        print(f"快速操作: {fast_stats['avg_time_ms']:.2f}ms (调用{fast_stats['total_calls']}次)")
        print(f"慢速操作: {slow_stats['avg_time_ms']:.2f}ms (调用{slow_stats['total_calls']}次)")
        
        # 慢操作应该比快操作慢
        assert slow_stats['avg_time_ms'] > fast_stats['avg_time_ms']


if __name__ == '__main__':
    pytest.main([__file__, '-v', '-s'])
