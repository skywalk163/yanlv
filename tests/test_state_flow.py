"""
言律语言状态流语法测试
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from yanlv.state_flow import (
    StateFlowParser, StateType,
    parse_state_flow, state_flow_to_python
)


class TestStateFlowParser(unittest.TestCase):
    """测试状态流解析器"""
    
    def setUp(self):
        self.parser = StateFlowParser()
    
    def test_parse_state_definition(self):
        """测试状态定义解析"""
        text = "订单状态为已付款"
        state = self.parser._parse_state_definition(text)
        
        self.assertIsNotNone(state)
        self.assertEqual(state.name, "已付款")
        self.assertEqual(state.state_type, StateType.NORMAL)
    
    def test_parse_initial_state(self):
        """测试初始状态解析"""
        text = "初始状态为新建"
        state = self.parser._parse_initial_state(text)
        
        self.assertIsNotNone(state)
        self.assertEqual(state.name, "新建")
        self.assertEqual(state.state_type, StateType.INITIAL)
    
    def test_parse_final_state(self):
        """测试终止状态解析"""
        text = "终止状态为已完成"
        state = self.parser._parse_final_state(text)
        
        self.assertIsNotNone(state)
        self.assertEqual(state.name, "已完成")
        self.assertEqual(state.state_type, StateType.FINAL)
    
    def test_parse_state_transition(self):
        """测试状态转换解析"""
        text = "订单状态变为已付款，准备发货"
        transition = self.parser._parse_state_transition(text)
        
        self.assertIsNotNone(transition)
        self.assertEqual(transition.to_state, "已付款")
        self.assertEqual(transition.action, "准备发货")
    
    def test_parse_conditional_transition(self):
        """测试条件转换解析"""
        text = "当收到付款时，状态变为已付款"
        transition = self.parser._parse_conditional_transition(text)
        
        self.assertIsNotNone(transition)
        self.assertEqual(transition.condition, "收到付款")
        self.assertEqual(transition.to_state, "已付款")
    
    def test_parse_full_state_machine(self):
        """测试完整状态机解析"""
        text = """
初始状态为新建
订单状态为已付款
订单状态为已发货
终止状态为已完成

订单状态变为已付款，准备发货
订单状态变为已发货，通知用户
当收到签收时，状态变为已完成
"""
        machine = self.parser.parse(text)
        
        self.assertIsNotNone(machine)
        self.assertEqual(len(machine.states), 4)
        self.assertGreater(len(machine.transitions), 0)
    
    def test_to_python_code(self):
        """测试Python代码生成"""
        text = """
初始状态为新建
订单状态为已付款
订单状态变为已付款，准备发货
"""
        machine = self.parser.parse(text)
        code = self.parser.to_python_code(machine)
        
        self.assertIn("class", code)
        self.assertIn("StateMachine", code)
        self.assertIn("已付款", code)
    
    def test_parse_state_flow_function(self):
        """测试parse_state_flow函数"""
        text = "订单状态为已付款"
        machine = parse_state_flow(text)
        
        self.assertIsNotNone(machine)
        self.assertEqual(len(machine.states), 1)
    
    def test_state_flow_to_python_function(self):
        """测试state_flow_to_python函数"""
        text = "订单状态为已付款"
        code = state_flow_to_python(text)
        
        self.assertIn("class", code)
        self.assertIn("StateMachine", code)


class TestStateFlowExamples(unittest.TestCase):
    """测试状态流示例"""
    
    def setUp(self):
        self.parser = StateFlowParser()
    
    def test_order_processing(self):
        """测试订单处理状态机"""
        text = """
初始状态为新建
订单状态为已付款
订单状态为已发货
订单状态为已签收
终止状态为已完成

订单状态变为已付款，准备发货
订单状态变为已发货，通知用户
订单状态变为已签收，更新库存
当用户确认时，状态变为已完成
"""
        machine = self.parser.parse(text)
        
        self.assertIsNotNone(machine)
        self.assertEqual(len(machine.states), 5)
        self.assertGreaterEqual(len(machine.transitions), 4)
    
    def test_user_authentication(self):
        """测试用户认证状态机"""
        text = """
初始状态为未登录
用户状态为已登录
用户状态为已登出

当输入正确密码时，状态变为已登录
当点击登出时，状态变为已登出
"""
        machine = self.parser.parse(text)
        
        self.assertIsNotNone(machine)
        self.assertEqual(len(machine.states), 3)
    
    def test_traffic_light(self):
        """测试交通灯状态机"""
        text = """
初始状态为红灯
交通灯状态为绿灯
交通灯状态为黄灯

当计时器到期时，状态变为绿灯
当计时器到期时，状态变为黄灯
当计时器到期时，状态变为红灯
"""
        machine = self.parser.parse(text)
        
        self.assertIsNotNone(machine)
        self.assertEqual(len(machine.states), 3)


if __name__ == '__main__':
    unittest.main()
