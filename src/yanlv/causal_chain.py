"""
言律语言因果链语法解析器

实现因果链语法的解析和执行，将"事件-响应"关系映射为控制流结构
"""

from typing import List, Dict, Tuple, Optional, Any
from dataclasses import dataclass
from enum import Enum


class CausalChainType(Enum):
    """因果链类型"""
    SIMPLE = "SIMPLE"           # 简单因果：条件 → 动作
    MULTI_CONDITION = "MULTI_CONDITION"  # 多条件因果
    STATE_CHANGE = "STATE_CHANGE"  # 状态变化因果
    EVENT_LISTEN = "EVENT_LISTEN"  # 事件监听因果
    CHAINED = "CHAINED"         # 链式因果


@dataclass
class CausalCondition:
    """因果条件"""
    text: str                   # 条件文本
    variables: List[str]        # 涉及的变量
    operators: List[str]        # 比较运算符
    values: List[Any]           # 比较值


@dataclass
class CausalAction:
    """因果动作"""
    text: str                   # 动作文本
    verb: str                   # 动词
    parameters: List[str]       # 参数


@dataclass
class CausalChain:
    """因果链"""
    chain_type: CausalChainType
    conditions: List[CausalCondition]
    actions: List[CausalAction]
    original_text: str
    priority: int = 0           # 优先级（用于多条件因果链）


class CausalChainParser:
    """因果链解析器"""
    
    def __init__(self):
        """初始化解析器"""
        self.chains: List[CausalChain] = []
        self.condition_keywords = {
            '大于', '小于', '等于', '不等于', '大于等于', '小于等于',
            '为', '包含', '在', '是'
        }
        self.action_keywords = {
            '开启', '关闭', '输出', '打印', '发送', '设置', '返回',
            '准备', '通知', '更新', '处理', '显示', '延迟'
        }
        self.connector_keywords = {'且', '或', '并', '就', '则'}
    
    def parse(self, text: str) -> Optional[CausalChain]:
        """
        解析因果链文本
        
        Args:
            text: 因果链文本，如 "下雨了，带伞。"
            
        Returns:
            解析后的因果链对象
        """
        text = text.strip()
        if not text:
            return None
        
        # 判断因果链类型
        chain_type = self._determine_chain_type(text)
        
        # 根据类型解析
        if chain_type == CausalChainType.SIMPLE:
            return self._parse_simple_chain(text)
        elif chain_type == CausalChainType.MULTI_CONDITION:
            return self._parse_multi_condition_chain(text)
        elif chain_type == CausalChainType.STATE_CHANGE:
            return self._parse_state_change_chain(text)
        elif chain_type == CausalChainType.EVENT_LISTEN:
            return self._parse_event_listen_chain(text)
        elif chain_type == CausalChainType.CHAINED:
            return self._parse_chained_chain(text)
        
        return None
    
    def _determine_chain_type(self, text: str) -> CausalChainType:
        """判断因果链类型"""
        # 事件监听：以"当"开头
        if text.startswith('当') or text.startswith('一旦'):
            return CausalChainType.EVENT_LISTEN
        
        # 状态变化：包含"变为"、"变成"、"转为"
        if '变为' in text or '变成' in text or '转为' in text:
            return CausalChainType.STATE_CHANGE
        
        # 多条件：包含"且"、"或"、"、"
        if '且' in text or '或' in text or '、' in text:
            return CausalChainType.MULTI_CONDITION
        
        # 链式：包含多个"，"分隔的结果
        if text.count('，') > 1:
            return CausalChainType.CHAINED
        
        # 默认为简单因果
        return CausalChainType.SIMPLE
    
    def _parse_simple_chain(self, text: str) -> CausalChain:
        """解析简单因果链"""
        # 分割条件和动作
        parts = text.split('，')
        if len(parts) < 2:
            return None
        
        condition_text = parts[0].strip()
        action_text = parts[1].strip().rstrip('。')
        
        # 解析条件
        condition = self._parse_condition(condition_text)
        
        # 解析动作
        action = self._parse_action(action_text)
        
        return CausalChain(
            chain_type=CausalChainType.SIMPLE,
            conditions=[condition] if condition else [],
            actions=[action] if action else [],
            original_text=text
        )
    
    def _parse_multi_condition_chain(self, text: str) -> CausalChain:
        """解析多条件因果链"""
        # 分割条件和动作
        parts = text.split('，')
        if len(parts) < 2:
            return None
        
        condition_text = parts[0].strip()
        action_text = parts[1].strip().rstrip('。')
        
        # 解析多个条件
        conditions = []
        
        # 处理"且"、"或"连接的条件
        if '且' in condition_text:
            sub_conditions = condition_text.split('且')
            for sub in sub_conditions:
                cond = self._parse_condition(sub.strip())
                if cond:
                    conditions.append(cond)
        elif '或' in condition_text:
            sub_conditions = condition_text.split('或')
            for sub in sub_conditions:
                cond = self._parse_condition(sub.strip())
                if cond:
                    conditions.append(cond)
        elif '、' in condition_text:
            # 条件累积（多个条件触发同一动作）
            sub_conditions = condition_text.split('、')
            for sub in sub_conditions:
                cond = self._parse_condition(sub.strip())
                if cond:
                    conditions.append(cond)
        else:
            cond = self._parse_condition(condition_text)
            if cond:
                conditions.append(cond)
        
        # 解析动作
        action = self._parse_action(action_text)
        
        return CausalChain(
            chain_type=CausalChainType.MULTI_CONDITION,
            conditions=conditions,
            actions=[action] if action else [],
            original_text=text
        )
    
    def _parse_state_change_chain(self, text: str) -> CausalChain:
        """解析状态变化因果链"""
        # 状态变化因果链：订单状态变为已付款，准备发货。
        parts = text.split('，')
        if len(parts) < 2:
            return None
        
        condition_text = parts[0].strip()
        action_text = parts[1].strip().rstrip('。')
        
        # 解析状态变化条件
        condition = self._parse_condition(condition_text)
        
        # 解析动作
        action = self._parse_action(action_text)
        
        return CausalChain(
            chain_type=CausalChainType.STATE_CHANGE,
            conditions=[condition] if condition else [],
            actions=[action] if action else [],
            original_text=text
        )
    
    def _parse_event_listen_chain(self, text: str) -> CausalChain:
        """解析事件监听因果链"""
        # 事件监听因果链：当收到消息时，显示通知。
        # 移除"当"和"时"
        text = text.replace('当', '').replace('一旦', '')
        text = text.replace('时', '，')
        
        parts = text.split('，')
        if len(parts) < 2:
            return None
        
        event_text = parts[0].strip()
        action_text = parts[1].strip().rstrip('。')
        
        # 解析事件条件
        condition = self._parse_condition(event_text)
        
        # 解析动作
        action = self._parse_action(action_text)
        
        return CausalChain(
            chain_type=CausalChainType.EVENT_LISTEN,
            conditions=[condition] if condition else [],
            actions=[action] if action else [],
            original_text=text
        )
    
    def _parse_chained_chain(self, text: str) -> CausalChain:
        """解析链式因果链"""
        # 链式因果链：原始数据，验证格式，结果1。
        parts = [p.strip() for p in text.split('，')]
        if len(parts) < 3:
            return None
        
        # 第一个部分是输入
        input_text = parts[0]
        
        # 中间部分是处理步骤
        actions = []
        for i in range(1, len(parts) - 1):
            action = self._parse_action(parts[i])
            if action:
                actions.append(action)
        
        # 最后部分是输出
        output_text = parts[-1].rstrip('。')
        
        # 创建输入条件
        condition = CausalCondition(
            text=input_text,
            variables=[input_text],
            operators=[],
            values=[]
        )
        
        return CausalChain(
            chain_type=CausalChainType.CHAINED,
            conditions=[condition],
            actions=actions,
            original_text=text
        )
    
    def _parse_condition(self, text: str) -> Optional[CausalCondition]:
        """解析条件"""
        if not text:
            return None
        
        variables = []
        operators = []
        values = []
        
        # 查找比较运算符
        for op in self.condition_keywords:
            if op in text:
                parts = text.split(op)
                if len(parts) >= 2:
                    variables.append(parts[0].strip())
                    operators.append(op)
                    values.append(parts[1].strip())
                    break
        
        # 如果没有找到运算符，整个文本作为变量
        if not variables:
            variables.append(text)
        
        return CausalCondition(
            text=text,
            variables=variables,
            operators=operators,
            values=values
        )
    
    def _parse_action(self, text: str) -> Optional[CausalAction]:
        """解析动作"""
        if not text:
            return None
        
        # 查找动词
        verb = None
        for action_verb in self.action_keywords:
            if action_verb in text:
                verb = action_verb
                break
        
        # 如果没有找到动词，使用第一个词作为动词
        if not verb and text:
            words = text.split()
            if words:
                verb = words[0]
        
        # 提取参数
        parameters = []
        if verb and verb in text:
            param_text = text.replace(verb, '').strip()
            if param_text:
                parameters.append(param_text)
        
        return CausalAction(
            text=text,
            verb=verb or '',
            parameters=parameters
        )
    
    def to_python_code(self, chain: CausalChain) -> str:
        """
        将因果链转换为Python代码
        
        Args:
            chain: 因果链对象
            
        Returns:
            Python代码字符串
        """
        if chain.chain_type == CausalChainType.SIMPLE:
            return self._simple_chain_to_python(chain)
        elif chain.chain_type == CausalChainType.MULTI_CONDITION:
            return self._multi_condition_chain_to_python(chain)
        elif chain.chain_type == CausalChainType.STATE_CHANGE:
            return self._state_change_chain_to_python(chain)
        elif chain.chain_type == CausalChainType.EVENT_LISTEN:
            return self._event_listen_chain_to_python(chain)
        elif chain.chain_type == CausalChainType.CHAINED:
            return self._chained_chain_to_python(chain)
        
        return ''
    
    def _simple_chain_to_python(self, chain: CausalChain) -> str:
        """将简单因果链转换为Python代码"""
        if not chain.conditions or not chain.actions:
            return ''
        
        condition = chain.conditions[0]
        action = chain.actions[0]
        
        # 构建条件表达式
        condition_expr = self._build_condition_expr(condition)
        
        # 构建动作语句
        action_stmt = self._build_action_stmt(action)
        
        return f"if {condition_expr}:\n    {action_stmt}"
    
    def _multi_condition_chain_to_python(self, chain: CausalChain) -> str:
        """将多条件因果链转换为Python代码"""
        if not chain.conditions or not chain.actions:
            return ''
        
        # 构建条件表达式
        condition_exprs = []
        for condition in chain.conditions:
            expr = self._build_condition_expr(condition)
            if expr:
                condition_exprs.append(expr)
        
        # 根据原始文本判断连接方式
        if '且' in chain.original_text:
            condition_expr = ' and '.join(condition_exprs)
        elif '或' in chain.original_text:
            condition_expr = ' or '.join(condition_exprs)
        else:
            # 条件累积，使用or连接
            condition_expr = ' or '.join(condition_exprs)
        
        # 构建动作语句
        action = chain.actions[0]
        action_stmt = self._build_action_stmt(action)
        
        return f"if {condition_expr}:\n    {action_stmt}"
    
    def _state_change_chain_to_python(self, chain: CausalChain) -> str:
        """将状态变化因果链转换为Python代码"""
        # 状态变化因果链通常需要事件监听机制
        # 这里简化处理，转换为条件判断
        return self._simple_chain_to_python(chain)
    
    def _event_listen_chain_to_python(self, chain: CausalChain) -> str:
        """将事件监听因果链转换为Python代码"""
        # 事件监听因果链需要事件系统支持
        # 这里简化处理，转换为条件判断
        if not chain.conditions or not chain.actions:
            return ''
        
        condition = chain.conditions[0]
        action = chain.actions[0]
        
        condition_expr = self._build_condition_expr(condition)
        action_stmt = self._build_action_stmt(action)
        
        return f"# Event listener\nif {condition_expr}:\n    {action_stmt}"
    
    def _chained_chain_to_python(self, chain: CausalChain) -> str:
        """将链式因果链转换为Python代码"""
        if not chain.conditions or not chain.actions:
            return ''
        
        # 链式因果链转换为流水线处理
        lines = []
        input_var = chain.conditions[0].text
        
        for i, action in enumerate(chain.actions):
            output_var = f"result_{i+1}"
            action_stmt = self._build_action_stmt(action, input_var, output_var)
            lines.append(f"{output_var} = {action_stmt}")
            input_var = output_var
        
        return '\n'.join(lines)
    
    def _build_condition_expr(self, condition: CausalCondition) -> str:
        """构建条件表达式"""
        if not condition.variables:
            return 'True'
        
        if not condition.operators:
            # 没有运算符，假设为布尔条件
            return condition.variables[0]
        
        # 构建比较表达式
        var = condition.variables[0]
        op = condition.operators[0]
        val = condition.values[0] if condition.values else ''
        
        # 映射运算符
        op_map = {
            '大于': '>',
            '小于': '<',
            '等于': '==',
            '不等于': '!=',
            '大于等于': '>=',
            '小于等于': '<=',
            '为': '==',
            '包含': 'in',
            '在': 'in',
            '是': '=='
        }
        
        python_op = op_map.get(op, '==')
        
        return f"{var} {python_op} {val}"
    
    def _build_action_stmt(self, action: CausalAction, 
                          input_var: str = None, 
                          output_var: str = None) -> str:
        """构建动作语句"""
        verb = action.verb
        params = action.parameters
        
        # 映射动词到Python函数
        verb_map = {
            '输出': 'print',
            '打印': 'print',
            '显示': 'print',
            '开启': 'open',
            '关闭': 'close',
            '发送': 'send',
            '设置': 'set',
            '返回': 'return',
            '准备': 'prepare',
            '通知': 'notify',
            '更新': 'update',
            '处理': 'process',
            '延迟': 'delay'
        }
        
        python_func = verb_map.get(verb, verb)
        
        if params:
            return f"{python_func}({', '.join(params)})"
        elif input_var:
            return f"{python_func}({input_var})"
        else:
            return f"{python_func}()"


# ============================================================================
# 辅助函数
# ============================================================================

def create_causal_chain_parser() -> CausalChainParser:
    """创建因果链解析器"""
    return CausalChainParser()


def parse_causal_chain(text: str) -> Optional[CausalChain]:
    """解析因果链文本"""
    parser = create_causal_chain_parser()
    return parser.parse(text)


def causal_chain_to_python(text: str) -> str:
    """将因果链文本转换为Python代码"""
    chain = parse_causal_chain(text)
    if chain:
        parser = create_causal_chain_parser()
        return parser.to_python_code(chain)
    return ''


# ============================================================================
# 导出
# ============================================================================

__all__ = [
    'CausalChainType',
    'CausalCondition',
    'CausalAction',
    'CausalChain',
    'CausalChainParser',
    'create_causal_chain_parser',
    'parse_causal_chain',
    'causal_chain_to_python',
]
