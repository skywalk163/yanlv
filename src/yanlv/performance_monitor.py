"""
言律语言性能监控体系

实现全面的性能监控、分析和报告功能
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from collections import defaultdict
import time
import json
import threading


@dataclass
class PerformanceMetric:
    """性能指标"""
    name: str                      # 指标名称
    value: float                   # 指标值
    unit: str                      # 单位
    timestamp: float               # 时间戳
    tags: Dict[str, str] = field(default_factory=dict)  # 标签


@dataclass
class PerformanceRecord:
    """性能记录"""
    operation: str                 # 操作名称
    start_time: float              # 开始时间
    end_time: float = 0.0          # 结束时间
    duration: float = 0.0          # 持续时间(毫秒)
    success: bool = True           # 是否成功
    error: Optional[str] = None    # 错误信息
    metadata: Dict[str, Any] = field(default_factory=dict)  # 元数据


class PerformanceMonitor:
    """
    性能监控器
    
    收集、分析和报告性能数据
    """
    
    def __init__(self, enabled: bool = True):
        """
        初始化性能监控器
        
        Args:
            enabled: 是否启用监控
        """
        self.enabled = enabled
        self.records: List[PerformanceRecord] = []
        self.metrics: Dict[str, List[PerformanceMetric]] = defaultdict(list)
        self.counters: Dict[str, int] = defaultdict(int)
        self.gauges: Dict[str, float] = {}
        self._lock = threading.Lock()
        self._current_operations: Dict[str, float] = {}  # 线程ID -> 开始时间
    
    def start_operation(self, operation: str, **metadata) -> str:
        """
        开始操作监控
        
        Args:
            operation: 操作名称
            **metadata: 元数据
            
        Returns:
            操作ID
        """
        if not self.enabled:
            return ""
        
        start_time = time.time()
        op_id = f"{operation}_{threading.current_thread().ident}_{start_time}"
        
        with self._lock:
            self._current_operations[op_id] = start_time
        
        return op_id
    
    def end_operation(
        self, 
        op_id: str, 
        success: bool = True, 
        error: str = None
    ) -> Optional[PerformanceRecord]:
        """
        结束操作监控
        
        Args:
            op_id: 操作ID
            success: 是否成功
            error: 错误信息
            
        Returns:
            性能记录
        """
        if not self.enabled or not op_id:
            return None
        
        end_time = time.time()
        
        with self._lock:
            start_time = self._current_operations.pop(op_id, None)
            
            if start_time is None:
                return None
            
            # 提取操作名称
            operation = op_id.split('_')[0]
            
            record = PerformanceRecord(
                operation=operation,
                start_time=start_time,
                end_time=end_time,
                duration=(end_time - start_time) * 1000,
                success=success,
                error=error
            )
            
            self.records.append(record)
            
            return record
    
    def record_metric(
        self, 
        name: str, 
        value: float, 
        unit: str = "", 
        **tags
    ) -> None:
        """
        记录指标
        
        Args:
            name: 指标名称
            value: 指标值
            unit: 单位
            **tags: 标签
        """
        if not self.enabled:
            return
        
        metric = PerformanceMetric(
            name=name,
            value=value,
            unit=unit,
            timestamp=time.time(),
            tags=tags
        )
        
        with self._lock:
            self.metrics[name].append(metric)
    
    def increment_counter(self, name: str, delta: int = 1) -> None:
        """
        增加计数器
        
        Args:
            name: 计数器名称
            delta: 增量
        """
        if not self.enabled:
            return
        
        with self._lock:
            self.counters[name] += delta
    
    def set_gauge(self, name: str, value: float) -> None:
        """
        设置仪表值
        
        Args:
            name: 仪表名称
            value: 值
        """
        if not self.enabled:
            return
        
        with self._lock:
            self.gauges[name] = value
    
    def get_operation_stats(self, operation: str) -> Dict[str, Any]:
        """
        获取操作统计信息
        
        Args:
            operation: 操作名称
            
        Returns:
            统计信息
        """
        with self._lock:
            op_records = [
                r for r in self.records 
                if r.operation == operation
            ]
            
            if not op_records:
                return {}
            
            durations = [r.duration for r in op_records]
            success_count = sum(1 for r in op_records if r.success)
            
            return {
                'operation': operation,
                'total_calls': len(op_records),
                'success_count': success_count,
                'failure_count': len(op_records) - success_count,
                'success_rate': success_count / len(op_records),
                'total_time_ms': sum(durations),
                'avg_time_ms': sum(durations) / len(durations),
                'min_time_ms': min(durations),
                'max_time_ms': max(durations)
            }
    
    def get_all_stats(self) -> Dict[str, Any]:
        """获取所有统计信息"""
        with self._lock:
            # 按操作分组统计
            operations = set(r.operation for r in self.records)
            operation_stats = {
                op: self.get_operation_stats(op)
                for op in operations
            }
            
            return {
                'total_operations': len(self.records),
                'operations': operation_stats,
                'counters': dict(self.counters),
                'gauges': dict(self.gauges),
                'metrics_count': {
                    name: len(metrics) 
                    for name, metrics in self.metrics.items()
                }
            }
    
    def get_recent_records(self, limit: int = 100) -> List[PerformanceRecord]:
        """
        获取最近的性能记录
        
        Args:
            limit: 最大数量
            
        Returns:
            性能记录列表
        """
        with self._lock:
            return self.records[-limit:]
    
    def export_to_json(self, file_path: str) -> None:
        """
        导出为JSON文件
        
        Args:
            file_path: 文件路径
        """
        stats = self.get_all_stats()
        
        # 转换记录为可序列化格式
        stats['recent_records'] = [
            {
                'operation': r.operation,
                'duration': r.duration,
                'success': r.success,
                'error': r.error,
                'timestamp': r.start_time
            }
            for r in self.get_recent_records(1000)
        ]
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(stats, f, indent=2, ensure_ascii=False)
    
    def clear(self) -> None:
        """清空所有数据"""
        with self._lock:
            self.records.clear()
            self.metrics.clear()
            self.counters.clear()
            self.gauges.clear()
            self._current_operations.clear()
    
    def enable(self) -> None:
        """启用监控"""
        self.enabled = True
    
    def disable(self) -> None:
        """禁用监控"""
        self.enabled = False


class PerformanceContext:
    """
    性能监控上下文管理器
    
    使用with语句自动监控代码块性能
    """
    
    def __init__(
        self, 
        monitor: PerformanceMonitor, 
        operation: str, 
        **metadata
    ):
        """
        初始化上下文管理器
        
        Args:
            monitor: 性能监控器
            operation: 操作名称
            **metadata: 元数据
        """
        self.monitor = monitor
        self.operation = operation
        self.metadata = metadata
        self.op_id = None
    
    def __enter__(self):
        """进入上下文"""
        self.op_id = self.monitor.start_operation(self.operation, **self.metadata)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """退出上下文"""
        success = exc_type is None
        error = str(exc_val) if exc_val else None
        
        self.monitor.end_operation(self.op_id, success, error)
        
        return False  # 不抑制异常


# 全局性能监控器实例
_global_monitor: Optional[PerformanceMonitor] = None


def get_global_monitor() -> PerformanceMonitor:
    """获取全局性能监控器"""
    global _global_monitor
    if _global_monitor is None:
        _global_monitor = PerformanceMonitor()
    return _global_monitor


def monitor_operation(operation: str, **metadata):
    """
    操作监控装饰器
    
    Args:
        operation: 操作名称
        **metadata: 元数据
        
    Returns:
        装饰器函数
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            monitor = get_global_monitor()
            
            with PerformanceContext(monitor, operation, **metadata):
                return func(*args, **kwargs)
        
        return wrapper
    return decorator
