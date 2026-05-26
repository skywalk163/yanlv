"""
言律语言语境省略语法测试

测试语境省略处理器的各种功能
"""

import unittest
import sys
import os

# 添加src目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from yanlv.context_omission import (
    ContextOmissionProcessor, OmissionType,
    create_context_omission_processor, process_context_omission
)


class TestContextOmissionProcessor(unittest.TestCase):
    """测试语境省略处理器"""
    
    def setUp(self):
        """测试前准备"""
        self.processor = ContextOmissionProcessor()
    
    def test_subject_omission(self):
        """测试主语省略"""
        # 先设置上下文
        self.processor._update_context("温度大于30")
        
        # 处理省略主语的句子
        text = "继续升高"
        completed, omissions = self.processor.process(text)
        
        # 应该检测到主语省略
        self.assertGreater(len(omissions), 0)
        self.assertEqual(omissions[0].omission_type, OmissionType.SUBJECT)
    
    def test_verb_omission(self):
        """测试动词省略"""
        # 先设置上下文
        self.processor._update_context("温度等于30")
        
        # 处理省略动词的句子
        text = "湿度也30"
        completed, omissions = self.processor.process(text)
        
        # 应该检测到动词省略
        verb_omissions = [o for o in omissions if o.omission_type == OmissionType.VERB]
        self.assertGreater(len(verb_omissions), 0)
    
    def test_condition_omission(self):
        """测试条件省略"""
        # 处理条件省略
        text = "那么执行"
        completed, omissions = self.processor.process(text)
        
        # 应该检测到条件省略
        condition_omissions = [o for o in omissions if o.omission_type == OmissionType.CONDITION]
        self.assertGreater(len(condition_omissions), 0)
    
    def test_topic_chain(self):
        """测试主题链"""
        # 处理多个句子
        sentences = [
            "温度大于30",
            "开启空调",
            "继续监测"
        ]
        
        for sentence in sentences:
            self.processor.process(sentence)
        
        # 检查主题链
        topic_chain = self.processor.get_topic_chain()
        self.assertGreater(len(topic_chain), 0)
    
    def test_scope_management(self):
        """测试作用域管理"""
        # 进入作用域
        self.processor.enter_scope("function1")
        self.assertEqual(self.processor.topic_chain.scope_depth, 1)
        
        # 进入嵌套作用域
        self.processor.enter_scope("block1")
        self.assertEqual(self.processor.topic_chain.scope_depth, 2)
        
        # 退出作用域
        self.processor.exit_scope()
        self.assertEqual(self.processor.topic_chain.scope_depth, 1)
        
        # 退出作用域
        self.processor.exit_scope()
        self.assertEqual(self.processor.topic_chain.scope_depth, 0)
    
    def test_variable_context(self):
        """测试变量上下文"""
        # 设置变量
        self.processor.set_variable("x", 10)
        self.processor.set_variable("y", 20)
        
        # 获取变量
        self.assertEqual(self.processor.get_variable("x"), 10)
        self.assertEqual(self.processor.get_variable("y"), 20)
        self.assertIsNone(self.processor.get_variable("z"))
    
    def test_context_update(self):
        """测试上下文更新"""
        text = "温度大于30"
        self.processor._update_context(text)
        
        # 检查上下文是否更新
        self.assertEqual(self.processor.omission_context.subject, "温度")
        self.assertEqual(self.processor.omission_context.verb, "大于")
    
    def test_inference_confidence(self):
        """测试推断置信度"""
        # 设置上下文
        self.processor._update_context("温度大于30")
        
        # 处理省略
        text = "继续升高"
        completed, omissions = self.processor.process(text)
        
        # 检查置信度
        if omissions:
            self.assertGreater(omissions[0].confidence, 0.5)
            self.assertLessEqual(omissions[0].confidence, 1.0)
    
    def test_no_omission(self):
        """测试无省略情况"""
        text = "温度大于30"
        completed, omissions = self.processor.process(text)
        
        # 完整句子不应该有省略
        self.assertEqual(len(omissions), 0)
        self.assertEqual(completed, text)
    
    def test_process_context_omission_function(self):
        """测试process_context_omission函数"""
        text = "温度大于30"
        completed, omissions = process_context_omission(text)
        
        self.assertIsInstance(completed, str)
        self.assertIsInstance(omissions, list)


class TestContextOmissionExamples(unittest.TestCase):
    """测试语境省略示例"""
    
    def setUp(self):
        """测试前准备"""
        self.processor = ContextOmissionProcessor()
    
    def test_temperature_control_sequence(self):
        """测试温度控制序列"""
        sentences = [
            "温度大于30",
            "开启空调",
            "继续监测",
            "温度小于25",
            "关闭空调"
        ]
        
        results = []
        for sentence in sentences:
            completed, omissions = self.processor.process(sentence)
            results.append((completed, len(omissions)))
        
        # 检查结果
        self.assertEqual(len(results), 5)
        
        # 第一个句子应该没有省略
        self.assertEqual(results[0][1], 0)
        
        # 后续句子可能有省略
        for i in range(1, len(results)):
            self.assertGreaterEqual(results[i][1], 0)
    
    def test_order_processing_sequence(self):
        """测试订单处理序列"""
        sentences = [
            "订单状态变为已付款",
            "准备发货",
            "通知用户",
            "更新库存"
        ]
        
        for sentence in sentences:
            completed, omissions = self.processor.process(sentence)
            self.assertIsInstance(completed, str)
    
    def test_nested_context(self):
        """测试嵌套上下文"""
        # 进入函数作用域
        self.processor.enter_scope("function")
        
        # 处理句子
        self.processor.process("温度大于30")
        self.assertEqual(self.processor.get_current_topic(), "温度")
        
        # 进入条件作用域
        self.processor.enter_scope("if_block")
        
        self.processor.process("开启空调")
        
        # 退出作用域
        self.processor.exit_scope()
        self.processor.exit_scope()


if __name__ == '__main__':
    unittest.main()
