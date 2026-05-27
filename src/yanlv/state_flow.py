"""
言律语言状态流语法解析器

实现状态定义、状态转换和状态机生成
"""

from typing import List, Dict, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum


class StateType(Enum):
    """状态类型"""
    INITIAL = "INITIAL"       # 初始状态
    NORMAL = "NORMAL"         # 正常状态
    FINAL = "FINAL"           # 终止状态
    ERROR = "ERROR"           # 错误状态


@dataclass
class State:
    """状态定义"""
    name: str
    variables: Dict[str, Any] = field(default_factory=dict)
    state_type: StateType = StateType.NORMAL
    on_enter: Optional[str] = None   # 进入状态时的动作
    on_exit: Optional[str] = None    # 退出状态时的动作


@dataclass
class StateTransition:
    """状态转换"""
    from_state: str
    to_state: str
    condition: Optional[str] = None   # 转换条件
    action: Optional[str] = None      # 转换时的动作
    priority: int = 0                 # 优先级


@dataclass
class StateMachine:
    """状态机"""
    name: str
    states: List[State] = field(default_factory=list)
    transitions: List[StateTransition] = field(default_factory=list)
    initial_state: Optional[str] = None
    current_state: Optional[str] = None


class StateFlowParser:
    """状态流语法解析器"""
    
    def __init__(self):
        """初始化解析器"""
        self.state_machines: Dict[str, StateMachine] = {}
        self.current_machine: Optional[StateMachine] = None
        
        # 状态关键词
        self.state_keywords = {
            '状态', '变为', '变成', '转为', '切换',
            '初始', '终止', '错误'
        }
        
        # 转换关键词
        self.transition_keywords = {
            '当', '如果', '一旦', '只要'
        }
    
    def parse(self, text: str) -> Optional[StateMachine]:
        """
        解析状态流文本
        
        Args:
            text: 状态流文本
            
        Returns:
            状态机对象
        """
        lines = text.strip().split('\n')
        
        # 解析状态定义
        states = self._parse_states(lines)
        
        # 解析状态转换
        transitions = self._parse_transitions(lines)
        
        # 创建状态机
        if states:
            machine = StateMachine(
                name="state_machine",
                states=states,
                transitions=transitions,
                initial_state=states[0].name if states else None
            )
            return machine
        
        return None
    
    def _parse_states(self, lines: List[str]) -> List[State]:
        """解析状态定义"""
        states = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # 解析状态定义
            # 格式：订单状态为已付款
            if '状态为' in line or '状态是' in line:
                state = self._parse_state_definition(line)
                if state:
                    states.append(state)
            
            # 解析初始状态
            elif '初始状态' in line:
                state = self._parse_initial_state(line)
                if state:
                    states.append(state)
            
            # 解析终止状态
            elif '终止状态' in line or '最终状态' in line:
                state = self._parse_final_state(line)
                if state:
                    states.append(state)
        
        return states
    
    def _parse_state_definition(self, line: str) -> Optional[State]:
        """解析状态定义"""
        # 提取状态名
        # 例如：订单状态为已付款 -> 已付款
        if '状态为' in line:
            parts = line.split('状态为')
        elif '状态是' in line:
            parts = line.split('状态是')
        else:
            return None
        
        if len(parts) >= 2:
            state_name = parts[1].strip().rstrip('。')
            return State(
                name=state_name,
                state_type=StateType.NORMAL
            )
        
        return None
    
    def _parse_initial_state(self, line: str) -> Optional[State]:
        """解析初始状态"""
        if '为' in line:
            parts = line.split('为')
        elif '是' in line:
            parts = line.split('是')
        else:
            return None
        
        if len(parts) >= 2:
            state_name = parts[1].strip().rstrip('。')
            return State(
                name=state_name,
                state_type=StateType.INITIAL
            )
        
        return None
    
    def _parse_final_state(self, line: str) -> Optional[State]:
        """解析终止状态"""
        if '为' in line:
            parts = line.split('为')
        elif '是' in line:
            parts = line.split('是')
        else:
            return None
        
        if len(parts) >= 2:
            state_name = parts[1].strip().rstrip('。')
            return State(
                name=state_name,
                state_type=StateType.FINAL
            )
        
        return None
    
    def _parse_transitions(self, lines: List[str]) -> List[StateTransition]:
        """解析状态转换"""
        transitions = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # 解析状态转换
            # 格式：订单状态变为已付款，准备发货
            if '变为' in line or '变成' in line or '转为' in line:
                transition = self._parse_state_transition(line)
                if transition:
                    transitions.append(transition)
            
            # 解析条件转换
            # 格式：当收到付款时，状态变为已付款
            elif line.startswith('当') or line.startswith('如果'):
                transition = self._parse_conditional_transition(line)
                if transition:
                    transitions.append(transition)
        
        return transitions
    
    def _parse_state_transition(self, line: str) -> Optional[StateTransition]:
        """解析状态转换"""
        # 提取源状态和目标状态
        # 例如：订单状态变为已付款 -> (None, 已付款)
        
        if '变为' in line:
            parts = line.split('变为')
        elif '变成' in line:
            parts = line.split('变成')
        elif '转为' in line:
            parts = line.split('转为')
        else:
            return None
        
        if len(parts) >= 2:
            to_state = parts[1].split('，')[0].strip().rstrip('。')
            
            # 提取动作
            action = None
            if '，' in parts[1]:
                action = parts[1].split('，')[1].strip().rstrip('。')
            
            return StateTransition(
                from_state="",  # 需要从上下文推断
                to_state=to_state,
                action=action
            )
        
        return None
    
    def _parse_conditional_transition(self, line: str) -> Optional[StateTransition]:
        """解析条件转换"""
        # 移除前缀
        line = line.replace('当', '').replace('如果', '').replace('一旦', '')
        
        # 分割条件和动作
        if '时' in line:
            parts = line.split('时')
        elif '则' in line:
            parts = line.split('则')
        else:
            return None
        
        if len(parts) >= 2:
            condition = parts[0].strip()
            action_part = parts[1].strip().rstrip('。')
            
            # 提取目标状态
            to_state = None
            if '变为' in action_part:
                state_parts = action_part.split('变为')
                to_state = state_parts[1].strip().rstrip('。')
            
            return StateTransition(
                from_state="",
                to_state=to_state or "",
                condition=condition,
                action=action_part
            )
        
        return None
    
    def to_python_code(self, machine: StateMachine) -> str:
        """
        将状态机转换为Python代码
        
        Args:
            machine: 状态机对象
            
        Returns:
            Python代码字符串
        """
        lines = []
        
        # 生成状态类
        lines.append(f"class {machine.name.title().replace('_', '')}StateMachine:")
        lines.append(f"    \"\"\"自动生成的状态机\"\"\"")
        lines.append(f"    ")
        lines.append(f"    def __init__(self):")
        lines.append(f"        self.current_state = '{machine.initial_state}'")
        lines.append(f"        self.states = {repr([s.name for s in machine.states])}")
        lines.append(f"    ")
        
        # 生成状态检查方法
        for state in machine.states:
            lines.append(f"    def is_{state.name.lower()}(self):")
            lines.append(f"        \"\"\"检查是否在{state.name}状态\"\"\"")
            lines.append(f"        return self.current_state == '{state.name}'")
            lines.append(f"    ")
        
        # 生成转换方法
        for i, transition in enumerate(machine.transitions):
            method_name = f"transition_{i+1}"
            lines.append(f"    def {method_name}(self):")
            lines.append(f"        \"\"\"状态转换: {transition.from_state} -> {transition.to_state}\"\"\"")
            
            if transition.condition:
                lines.append(f"        if {self._condition_to_python(transition.condition)}:")
                lines.append(f"            self.current_state = '{transition.to_state}'")
                if transition.action:
                    lines.append(f"            # {transition.action}")
                lines.append(f"            return True")
                lines.append(f"        return False")
            else:
                lines.append(f"        self.current_state = '{transition.to_state}'")
                if transition.action:
                    lines.append(f"        # {transition.action}")
                lines.append(f"        return True")
            lines.append(f"    ")
        
        return '\n'.join(lines)
    
    def _condition_to_python(self, condition: str) -> str:
        """将条件转换为Python表达式"""
        # 简化处理
        return f"'{condition}'"


# ============================================================================
# 辅助函数
# ============================================================================

def create_state_flow_parser() -> StateFlowParser:
    """创建状态流解析器"""
    return StateFlowParser()


def parse_state_flow(text: str) -> Optional[StateMachine]:
    """解析状态流文本"""
    parser = create_state_flow_parser()
    return parser.parse(text)


def state_flow_to_python(text: str) -> str:
    """将状态流文本转换为Python代码"""
    machine = parse_state_flow(text)
    if machine:
        parser = create_state_flow_parser()
        return parser.to_python_code(machine)
    return ''


# ============================================================================
# 导出
# ============================================================================

__all__ = [
    'StateType',
    'State',
    'StateTransition',
    'StateMachine',
    'StateFlowParser',
    'create_state_flow_parser',
    'parse_state_flow',
    'state_flow_to_python',
]
