"""
言律语言调试器实现

提供断点调试、变量查看、调用栈跟踪等功能
"""

from typing import Dict, Any, Optional, List, Callable
from dataclasses import dataclass, field
from enum import Enum


class DebugState(Enum):
    """调试状态"""
    IDLE = "idle"           # 空闲
    RUNNING = "running"     # 运行中
    PAUSED = "paused"       # 已暂停
    TERMINATED = "terminated"  # 已终止


@dataclass
class Breakpoint:
    """断点"""
    id: int                 # 断点ID
    line: int               # 行号
    condition: str = ""     # 条件表达式
    hit_count: int = 0      # 命中次数
    enabled: bool = True    # 是否启用


@dataclass
class StackFrame:
    """调用栈帧"""
    id: int                 # 帧ID
    name: str               # 函数名
    line: int               # 当前行号
    column: int = 0         # 当前列号
    source: str = ""        # 源文件路径
    variables: Dict[str, Any] = field(default_factory=dict)  # 局部变量


@dataclass
class Variable:
    """变量"""
    name: str               # 变量名
    value: Any              # 变量值
    type: str               # 类型
    variables_reference: int = 0  # 子变量引用(用于展开)


class Debugger:
    """
    调试器
    
    实现断点调试、变量查看、调用栈跟踪等功能
    """
    
    def __init__(self):
        """初始化调试器"""
        self.state = DebugState.IDLE
        self.breakpoints: Dict[str, List[Breakpoint]] = {}  # 文件 -> 断点列表
        self.stack_frames: List[StackFrame] = []  # 调用栈
        self.variables: Dict[str, Any] = {}  # 当前变量
        self.current_line: int = 0  # 当前行号
        self.current_file: str = ""  # 当前文件
        
        self._breakpoint_id_counter = 0
        self._frame_id_counter = 0
        self._variable_ref_counter = 0
        
        # 回调函数
        self._on_breakpoint_hit: Optional[Callable] = None
        self._on_step_complete: Optional[Callable] = None
        self._on_exception: Optional[Callable] = None
    
    def initialize(self) -> None:
        """初始化调试会话"""
        self.state = DebugState.IDLE
        self.breakpoints.clear()
        self.stack_frames.clear()
        self.variables.clear()
        self.current_line = 0
        self.current_file = ""
    
    def set_breakpoints(
        self, 
        file_path: str, 
        lines: List[int],
        conditions: List[str] = None
    ) -> List[Breakpoint]:
        """
        设置断点
        
        Args:
            file_path: 文件路径
            lines: 行号列表
            conditions: 条件表达式列表
            
        Returns:
            断点列表
        """
        # 清除该文件的旧断点
        self.breakpoints[file_path] = []
        
        # 添加新断点
        breakpoints = []
        conditions = conditions or [""] * len(lines)
        
        for line, condition in zip(lines, conditions):
            self._breakpoint_id_counter += 1
            
            breakpoint = Breakpoint(
                id=self._breakpoint_id_counter,
                line=line,
                condition=condition
            )
            
            self.breakpoints[file_path].append(breakpoint)
            breakpoints.append(breakpoint)
        
        return breakpoints
    
    def add_breakpoint(
        self, 
        file_path: str, 
        line: int, 
        condition: str = ""
    ) -> Breakpoint:
        """
        添加断点
        
        Args:
            file_path: 文件路径
            line: 行号
            condition: 条件表达式
            
        Returns:
            断点对象
        """
        self._breakpoint_id_counter += 1
        
        breakpoint = Breakpoint(
            id=self._breakpoint_id_counter,
            line=line,
            condition=condition
        )
        
        if file_path not in self.breakpoints:
            self.breakpoints[file_path] = []
        
        self.breakpoints[file_path].append(breakpoint)
        
        return breakpoint
    
    def remove_breakpoint(self, breakpoint_id: int) -> bool:
        """
        移除断点
        
        Args:
            breakpoint_id: 断点ID
            
        Returns:
            是否成功
        """
        for file_path, breakpoints in self.breakpoints.items():
            for i, bp in enumerate(breakpoints):
                if bp.id == breakpoint_id:
                    del breakpoints[i]
                    return True
        
        return False
    
    def toggle_breakpoint(self, breakpoint_id: int) -> bool:
        """
        切换断点启用状态
        
        Args:
            breakpoint_id: 断点ID
            
        Returns:
            是否成功
        """
        for breakpoints in self.breakpoints.values():
            for bp in breakpoints:
                if bp.id == breakpoint_id:
                    bp.enabled = not bp.enabled
                    return True
        
        return False
    
    def get_breakpoints(self, file_path: str = None) -> List[Breakpoint]:
        """
        获取断点
        
        Args:
            file_path: 文件路径(可选)
            
        Returns:
            断点列表
        """
        if file_path:
            return self.breakpoints.get(file_path, [])
        
        all_breakpoints = []
        for breakpoints in self.breakpoints.values():
            all_breakpoints.extend(breakpoints)
        
        return all_breakpoints
    
    def _check_breakpoint(self, file_path: str, line: int) -> Optional[Breakpoint]:
        """
        检查是否命中断点
        
        Args:
            file_path: 文件路径
            line: 行号
            
        Returns:
            命中的断点(如果有)
        """
        if file_path not in self.breakpoints:
            return None
        
        for bp in self.breakpoints[file_path]:
            if bp.line == line and bp.enabled:
                # 检查条件
                if bp.condition:
                    # 简化实现: 不实际执行条件表达式
                    # 实际实现应该执行条件表达式并检查结果
                    pass
                
                bp.hit_count += 1
                return bp
        
        return None
    
    def push_frame(
        self, 
        name: str, 
        line: int, 
        source: str = "",
        variables: Dict[str, Any] = None
    ) -> StackFrame:
        """
        压入调用栈帧
        
        Args:
            name: 函数名
            line: 行号
            source: 源文件路径
            variables: 局部变量
            
        Returns:
            栈帧对象
        """
        self._frame_id_counter += 1
        
        frame = StackFrame(
            id=self._frame_id_counter,
            name=name,
            line=line,
            source=source,
            variables=variables or {}
        )
        
        self.stack_frames.append(frame)
        
        return frame
    
    def pop_frame(self) -> Optional[StackFrame]:
        """
        弹出调用栈帧
        
        Returns:
            栈帧对象
        """
        if self.stack_frames:
            return self.stack_frames.pop()
        
        return None
    
    def get_stack_frames(self) -> List[StackFrame]:
        """获取调用栈"""
        return self.stack_frames.copy()
    
    def get_current_frame(self) -> Optional[StackFrame]:
        """获取当前栈帧"""
        if self.stack_frames:
            return self.stack_frames[-1]
        
        return None
    
    def set_variable(self, name: str, value: Any, type: str = None) -> Variable:
        """
        设置变量
        
        Args:
            name: 变量名
            value: 变量值
            type: 类型
            
        Returns:
            变量对象
        """
        if type is None:
            type = type(value).__name__
        
        variable = Variable(
            name=name,
            value=value,
            type=type
        )
        
        self.variables[name] = variable
        
        # 如果有当前栈帧,也设置到栈帧中
        current_frame = self.get_current_frame()
        if current_frame:
            current_frame.variables[name] = value
        
        return variable
    
    def get_variable(self, name: str) -> Optional[Variable]:
        """
        获取变量
        
        Args:
            name: 变量名
            
        Returns:
            变量对象
        """
        return self.variables.get(name)
    
    def get_variables(self) -> List[Variable]:
        """获取所有变量"""
        return list(self.variables.values())
    
    def evaluate(self, expression: str) -> Optional[Variable]:
        """
        计算表达式
        
        Args:
            expression: 表达式
            
        Returns:
            计算结果
        """
        # 简化实现: 只支持变量查找
        # 实际实现应该解析和执行表达式
        return self.get_variable(expression)
    
    def start(self) -> None:
        """开始执行"""
        self.state = DebugState.RUNNING
    
    def pause(self) -> None:
        """暂停执行"""
        if self.state == DebugState.RUNNING:
            self.state = DebugState.PAUSED
    
    def continue_execution(self) -> None:
        """继续执行"""
        if self.state == DebugState.PAUSED:
            self.state = DebugState.RUNNING
    
    def step_over(self) -> None:
        """单步跳过"""
        if self.state == DebugState.PAUSED:
            # 简化实现: 只是继续执行
            # 实际实现应该执行一行代码
            self.state = DebugState.RUNNING
    
    def step_into(self) -> None:
        """单步进入"""
        if self.state == DebugState.PAUSED:
            self.state = DebugState.RUNNING
    
    def step_out(self) -> None:
        """单步跳出"""
        if self.state == DebugState.PAUSED:
            self.state = DebugState.RUNNING
    
    def terminate(self) -> None:
        """终止执行"""
        self.state = DebugState.TERMINATED
    
    def is_running(self) -> bool:
        """是否正在运行"""
        return self.state == DebugState.RUNNING
    
    def is_paused(self) -> bool:
        """是否已暂停"""
        return self.state == DebugState.PAUSED
    
    def is_terminated(self) -> bool:
        """是否已终止"""
        return self.state == DebugState.TERMINATED
    
    def set_callbacks(
        self,
        on_breakpoint_hit: Callable = None,
        on_step_complete: Callable = None,
        on_exception: Callable = None
    ) -> None:
        """
        设置回调函数
        
        Args:
            on_breakpoint_hit: 断点命中回调
            on_step_complete: 单步完成回调
            on_exception: 异常回调
        """
        self._on_breakpoint_hit = on_breakpoint_hit
        self._on_step_complete = on_step_complete
        self._on_exception = on_exception
    
    def get_state_info(self) -> Dict[str, Any]:
        """获取状态信息"""
        return {
            'state': self.state.value,
            'current_file': self.current_file,
            'current_line': self.current_line,
            'breakpoints_count': len(self.get_breakpoints()),
            'stack_depth': len(self.stack_frames),
            'variables_count': len(self.variables)
        }


# 全局调试器实例
_global_debugger: Optional[Debugger] = None


def get_global_debugger() -> Debugger:
    """获取全局调试器"""
    global _global_debugger
    if _global_debugger is None:
        _global_debugger = Debugger()
    return _global_debugger
