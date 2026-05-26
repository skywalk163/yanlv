"""
言律语言语境省略语法处理器

实现语境省略语法的解析和补全，利用上下文推断省略的语法元素
"""

from typing import List, Dict, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum


class OmissionType(Enum):
    """省略类型"""
    SUBJECT = "SUBJECT"           # 主语省略
    OBJECT = "OBJECT"             # 宾语省略
    VERB = "VERB"                 # 动词省略
    CONDITION = "CONDITION"       # 条件省略
    VARIABLE = "VARIABLE"         # 变量省略
    PARAMETER = "PARAMETER"       # 参数省略


@dataclass
class TopicChain:
    """主题链"""
    topics: List[str]             # 主题序列
    current_topic: Optional[str]  # 当前主题
    scope_depth: int              # 作用域深度
    history: List[Tuple[str, int]]  # 主题历史（主题，深度）


@dataclass
class OmissionContext:
    """省略上下文"""
    subject: Optional[str]        # 主语
    verb: Optional[str]           # 动词
    object: Optional[str]         # 宾语
    condition: Optional[str]      # 条件
    variables: Dict[str, Any]     # 变量上下文
    scope_stack: List[str]        # 作用域栈


@dataclass
class OmittedElement:
    """省略的元素"""
    omission_type: OmissionType
    original_text: str
    inferred_value: str
    confidence: float             # 推断置信度
    context_source: str           # 上下文来源


class ContextOmissionProcessor:
    """语境省略处理器"""
    
    def __init__(self):
        """初始化处理器"""
        self.topic_chain = TopicChain(
            topics=[],
            current_topic=None,
            scope_depth=0,
            history=[]
        )
        self.omission_context = OmissionContext(
            subject=None,
            verb=None,
            object=None,
            condition=None,
            variables={},
            scope_stack=[]
        )
        self.omitted_elements: List[OmittedElement] = []
        
        # 省略规则
        self.omission_rules = {
            # 主语省略规则
            'subject_omission': [
                '继续', '然后', '接着', '之后', '并且'
            ],
            # 动词省略规则
            'verb_omission': [
                '也', '同样', '一样', '相同'
            ],
            # 条件省略规则
            'condition_omission': [
                '那么', '则', '就', '于是'
            ]
        }
    
    def process(self, text: str) -> Tuple[str, List[OmittedElement]]:
        """
        处理文本，补全省略的元素
        
        Args:
            text: 输入文本
            
        Returns:
            (补全后的文本, 省略元素列表)
        """
        # 识别省略
        omissions = self._detect_omissions(text)
        
        # 推断省略的值
        for omission in omissions:
            inferred = self._infer_omitted_value(omission, text)
            omission.inferred_value = inferred
        
        # 补全文本
        completed_text = self._complete_text(text, omissions)
        
        # 更新上下文
        self._update_context(completed_text)
        
        return completed_text, omissions
    
    def _detect_omissions(self, text: str) -> List[OmittedElement]:
        """检测省略"""
        omissions = []
        
        # 检测主语省略
        for keyword in self.omission_rules['subject_omission']:
            if keyword in text:
                omissions.append(OmittedElement(
                    omission_type=OmissionType.SUBJECT,
                    original_text=text,
                    inferred_value='',
                    confidence=0.8,
                    context_source=f'keyword:{keyword}'
                ))
                break
        
        # 检测动词省略
        for keyword in self.omission_rules['verb_omission']:
            if keyword in text:
                omissions.append(OmittedElement(
                    omission_type=OmissionType.VERB,
                    original_text=text,
                    inferred_value='',
                    confidence=0.9,
                    context_source=f'keyword:{keyword}'
                ))
                break
        
        # 检测条件省略
        for keyword in self.omission_rules['condition_omission']:
            if keyword in text:
                omissions.append(OmittedElement(
                    omission_type=OmissionType.CONDITION,
                    original_text=text,
                    inferred_value='',
                    confidence=0.95,
                    context_source=f'keyword:{keyword}'
                ))
                break
        
        return omissions
    
    def _infer_omitted_value(self, omission: OmittedElement, text: str) -> str:
        """推断省略的值"""
        if omission.omission_type == OmissionType.SUBJECT:
            # 从主题链推断主语
            if self.topic_chain.current_topic:
                return self.topic_chain.current_topic
            elif self.omission_context.subject:
                return self.omission_context.subject
            else:
                return '它'  # 默认主语
        
        elif omission.omission_type == OmissionType.VERB:
            # 从上下文推断动词
            if self.omission_context.verb:
                return self.omission_context.verb
            else:
                return '是'  # 默认动词
        
        elif omission.omission_type == OmissionType.CONDITION:
            # 从上下文推断条件
            if self.omission_context.condition:
                return self.omission_context.condition
            else:
                return '真'  # 默认条件
        
        return ''
    
    def _complete_text(self, text: str, omissions: List[OmittedElement]) -> str:
        """补全文本"""
        if not omissions:
            return text
        
        # 按省略类型补全
        for omission in omissions:
            if omission.omission_type == OmissionType.SUBJECT:
                # 在文本前添加主语
                if omission.inferred_value:
                    text = f"{omission.inferred_value}{text}"
            
            elif omission.omission_type == OmissionType.VERB:
                # 在适当位置添加动词
                if omission.inferred_value:
                    # 简化处理：在文本中添加动词
                    pass
            
            elif omission.omission_type == OmissionType.CONDITION:
                # 条件省略通常不需要补全
                pass
        
        return text
    
    def _update_context(self, text: str):
        """更新上下文"""
        # 提取主语
        subject = self._extract_subject(text)
        if subject:
            self.omission_context.subject = subject
            self._update_topic_chain(subject)
        
        # 提取动词
        verb = self._extract_verb(text)
        if verb:
            self.omission_context.verb = verb
        
        # 提取宾语
        obj = self._extract_object(text)
        if obj:
            self.omission_context.object = obj
    
    def _extract_subject(self, text: str) -> Optional[str]:
        """提取主语"""
        # 简化实现：查找第一个名词性成分
        keywords = ['温度', '湿度', '光线', '订单', '用户', '系统', '数据']
        for keyword in keywords:
            if keyword in text:
                return keyword
        return None
    
    def _extract_verb(self, text: str) -> Optional[str]:
        """提取动词"""
        verbs = ['大于', '小于', '等于', '变为', '开启', '关闭', '输出', '处理']
        for verb in verbs:
            if verb in text:
                return verb
        return None
    
    def _extract_object(self, text: str) -> Optional[str]:
        """提取宾语"""
        # 简化实现
        return None
    
    def _update_topic_chain(self, topic: str):
        """更新主题链"""
        # 添加到主题历史
        self.topic_chain.history.append((topic, self.topic_chain.scope_depth))
        
        # 更新当前主题
        self.topic_chain.current_topic = topic
        
        # 添加到主题序列
        if topic not in self.topic_chain.topics:
            self.topic_chain.topics.append(topic)
    
    def enter_scope(self, scope_name: str):
        """进入新作用域"""
        self.topic_chain.scope_depth += 1
        self.omission_context.scope_stack.append(scope_name)
    
    def exit_scope(self):
        """退出作用域"""
        if self.topic_chain.scope_depth > 0:
            self.topic_chain.scope_depth -= 1
        if self.omission_context.scope_stack:
            self.omission_context.scope_stack.pop()
    
    def set_variable(self, name: str, value: Any):
        """设置变量"""
        self.omission_context.variables[name] = value
    
    def get_variable(self, name: str) -> Optional[Any]:
        """获取变量"""
        return self.omission_context.variables.get(name)
    
    def get_current_topic(self) -> Optional[str]:
        """获取当前主题"""
        return self.topic_chain.current_topic
    
    def get_topic_chain(self) -> List[str]:
        """获取主题链"""
        return self.topic_chain.topics.copy()
    
    def get_omission_statistics(self) -> Dict[str, int]:
        """获取省略统计"""
        stats = {}
        for omission in self.omitted_elements:
            type_name = omission.omission_type.value
            stats[type_name] = stats.get(type_name, 0) + 1
        return stats


# ============================================================================
# 辅助函数
# ============================================================================

def create_context_omission_processor() -> ContextOmissionProcessor:
    """创建语境省略处理器"""
    return ContextOmissionProcessor()


def process_context_omission(text: str) -> Tuple[str, List[OmittedElement]]:
    """处理语境省略"""
    processor = create_context_omission_processor()
    return processor.process(text)


# ============================================================================
# 导出
# ============================================================================

__all__ = [
    'OmissionType',
    'TopicChain',
    'OmissionContext',
    'OmittedElement',
    'ContextOmissionProcessor',
    'create_context_omission_processor',
    'process_context_omission',
]
