"""
调试器测试

测试Debugger的功能
"""

import pytest
from yanlv.debugger import (
    Debugger, 
    DebugState,
    Breakpoint,
    StackFrame,
    Variable,
    get_global_debugger
)


class TestDebugger:
    """Debugger测试类"""
    
    def test_debugger_initialization(self):
        """测试调试器初始化"""
        debugger = Debugger()
        assert debugger.state == DebugState.IDLE
        assert len(debugger.breakpoints) == 0
        assert len(debugger.stack_frames) == 0
    
    def test_set_breakpoints(self):
        """测试设置断点"""
        debugger = Debugger()
        
        breakpoints = debugger.set_breakpoints("test.yanlv", [10, 20, 30])
        
        assert len(breakpoints) == 3
        assert all(bp.line in [10, 20, 30] for bp in breakpoints)
        assert len(debugger.breakpoints["test.yanlv"]) == 3
    
    def test_add_breakpoint(self):
        """测试添加断点"""
        debugger = Debugger()
        
        bp = debugger.add_breakpoint("test.yanlv", 15, condition="x > 10")
        
        assert bp.line == 15
        assert bp.condition == "x > 10"
        assert bp.enabled
    
    def test_remove_breakpoint(self):
        """测试移除断点"""
        debugger = Debugger()
        
        bp = debugger.add_breakpoint("test.yanlv", 10)
        
        assert debugger.remove_breakpoint(bp.id)
        assert len(debugger.get_breakpoints("test.yanlv")) == 0
    
    def test_toggle_breakpoint(self):
        """测试切换断点状态"""
        debugger = Debugger()
        
        bp = debugger.add_breakpoint("test.yanlv", 10)
        
        assert bp.enabled
        
        debugger.toggle_breakpoint(bp.id)
        assert not bp.enabled
        
        debugger.toggle_breakpoint(bp.id)
        assert bp.enabled
    
    def test_get_breakpoints(self):
        """测试获取断点"""
        debugger = Debugger()
        
        debugger.add_breakpoint("file1.yanlv", 10)
        debugger.add_breakpoint("file1.yanlv", 20)
        debugger.add_breakpoint("file2.yanlv", 30)
        
        # 获取特定文件的断点
        bps1 = debugger.get_breakpoints("file1.yanlv")
        assert len(bps1) == 2
        
        # 获取所有断点
        all_bps = debugger.get_breakpoints()
        assert len(all_bps) == 3


class TestStackFrames:
    """调用栈测试类"""
    
    def test_push_pop_frame(self):
        """测试压入弹出栈帧"""
        debugger = Debugger()
        
        frame1 = debugger.push_frame("main", 10, "test.yanlv")
        frame2 = debugger.push_frame("func", 20, "test.yanlv")
        
        assert len(debugger.stack_frames) == 2
        
        popped = debugger.pop_frame()
        assert popped.id == frame2.id
        assert len(debugger.stack_frames) == 1
    
    def test_get_stack_frames(self):
        """测试获取调用栈"""
        debugger = Debugger()
        
        debugger.push_frame("main", 10)
        debugger.push_frame("func1", 20)
        debugger.push_frame("func2", 30)
        
        frames = debugger.get_stack_frames()
        
        assert len(frames) == 3
        assert frames[0].name == "main"
        assert frames[1].name == "func1"
        assert frames[2].name == "func2"
    
    def test_get_current_frame(self):
        """测试获取当前栈帧"""
        debugger = Debugger()
        
        assert debugger.get_current_frame() is None
        
        debugger.push_frame("main", 10)
        frame = debugger.get_current_frame()
        
        assert frame is not None
        assert frame.name == "main"


class TestVariables:
    """变量测试类"""
    
    def test_set_get_variable(self):
        """测试设置获取变量"""
        debugger = Debugger()
        
        var = debugger.set_variable("x", 10, "int")
        
        assert var.name == "x"
        assert var.value == 10
        assert var.type == "int"
        
        retrieved = debugger.get_variable("x")
        assert retrieved.value == 10
    
    def test_get_variables(self):
        """测试获取所有变量"""
        debugger = Debugger()
        
        debugger.set_variable("x", 10)
        debugger.set_variable("y", 20)
        debugger.set_variable("z", 30)
        
        variables = debugger.get_variables()
        
        assert len(variables) == 3
        assert any(v.name == "x" for v in variables)
    
    def test_variable_in_frame(self):
        """测试栈帧中的变量"""
        debugger = Debugger()
        
        debugger.push_frame("func", 10)
        debugger.set_variable("local_var", 100)
        
        current_frame = debugger.get_current_frame()
        assert "local_var" in current_frame.variables
        assert current_frame.variables["local_var"] == 100


class TestDebugState:
    """调试状态测试类"""
    
    def test_state_transitions(self):
        """测试状态转换"""
        debugger = Debugger()
        
        assert debugger.state == DebugState.IDLE
        
        debugger.start()
        assert debugger.is_running()
        
        debugger.pause()
        assert debugger.is_paused()
        
        debugger.continue_execution()
        assert debugger.is_running()
        
        debugger.terminate()
        assert debugger.is_terminated()
    
    def test_step_operations(self):
        """测试单步操作"""
        debugger = Debugger()
        
        debugger.start()
        debugger.pause()
        
        # 单步跳过
        debugger.step_over()
        assert debugger.is_running()
        
        debugger.pause()
        
        # 单步进入
        debugger.step_into()
        assert debugger.is_running()
        
        debugger.pause()
        
        # 单步跳出
        debugger.step_out()
        assert debugger.is_running()


class TestBreakpointHit:
    """断点命中测试类"""
    
    def test_check_breakpoint(self):
        """测试断点命中检查"""
        debugger = Debugger()
        
        debugger.add_breakpoint("test.yanlv", 10)
        
        # 命中断点
        bp = debugger._check_breakpoint("test.yanlv", 10)
        assert bp is not None
        assert bp.hit_count == 1
        
        # 未命中
        bp2 = debugger._check_breakpoint("test.yanlv", 20)
        assert bp2 is None
    
    def test_breakpoint_with_condition(self):
        """测试条件断点"""
        debugger = Debugger()
        
        debugger.add_breakpoint("test.yanlv", 10, condition="x > 5")
        
        bp = debugger._check_breakpoint("test.yanlv", 10)
        assert bp is not None
        assert bp.condition == "x > 5"
    
    def test_disabled_breakpoint(self):
        """测试禁用的断点"""
        debugger = Debugger()
        
        bp = debugger.add_breakpoint("test.yanlv", 10)
        bp.enabled = False
        
        # 不应该命中
        result = debugger._check_breakpoint("test.yanlv", 10)
        assert result is None


class TestEvaluate:
    """表达式计算测试类"""
    
    def test_evaluate_variable(self):
        """测试计算变量"""
        debugger = Debugger()
        
        debugger.set_variable("x", 42)
        
        result = debugger.evaluate("x")
        
        assert result is not None
        assert result.value == 42
    
    def test_evaluate_nonexistent(self):
        """测试计算不存在的变量"""
        debugger = Debugger()
        
        result = debugger.evaluate("nonexistent")
        
        assert result is None


class TestGlobalDebugger:
    """全局调试器测试"""
    
    def test_get_global_debugger(self):
        """测试获取全局调试器"""
        debugger1 = get_global_debugger()
        debugger2 = get_global_debugger()
        
        # 应该是同一个实例
        assert debugger1 is debugger2


class TestDebuggerInfo:
    """调试器信息测试"""
    
    def test_get_state_info(self):
        """测试获取状态信息"""
        debugger = Debugger()
        
        debugger.add_breakpoint("test.yanlv", 10)
        debugger.push_frame("main", 5)
        debugger.set_variable("x", 10)
        
        info = debugger.get_state_info()
        
        assert info['state'] == "idle"
        assert info['breakpoints_count'] == 1
        assert info['stack_depth'] == 1
        assert info['variables_count'] == 1


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
