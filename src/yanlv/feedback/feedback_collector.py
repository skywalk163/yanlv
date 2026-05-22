"""
言律语言反馈收集系统

实现反馈收集、存储和处理功能
"""

from typing import Dict, List, Optional, Any
import uuid
from datetime import datetime
import feedback_model
from feedback_model import (
    UserFeedback, AmbiguityFeedback, AmbiguityPattern, LearningRule,
    FeedbackType, FeedbackSeverity, FeedbackStatus, FeedbackDataModel
)


class FeedbackCollector:
    """反馈收集器"""
    
    def __init__(self, data_model: Optional[FeedbackDataModel] = None):
        """
        初始化反馈收集器
        
        Args:
            data_model: 反馈数据模型
        """
        self.data_model = data_model or FeedbackDataModel()
        self.session_id = str(uuid.uuid4())
        
        # 配置
        self.config = {
            'auto_save': False,
            'save_interval': 100,
            'max_feedbacks': 10000,
            'anonymize_user': True
        }
        
        # 统计
        self.stats = {
            'feedbacks_collected': 0,
            'ambiguity_feedbacks': 0,
            'auto_corrections': 0
        }
    
    def collect_ambiguity_feedback(
        self,
        source_text: str,
        ambiguous_segment: str,
        system_interpretation: str,
        user_correction: str,
        context: List[str],
        confidence: float = 0.5
    ) -> str:
        """
        收集歧义消解反馈
        
        Args:
            source_text: 原始文本
            ambiguous_segment: 歧义片段
            system_interpretation: 系统解释
            user_correction: 用户纠正
            context: 上下文
            confidence: 置信度
            
        Returns:
            反馈ID
        """
        # 创建歧义反馈
        feedback = AmbiguityFeedback(
            source_text=source_text,
            ambiguous_segment=ambiguous_segment,
            system_interpretation=system_interpretation,
            user_correction=user_correction,
            context=context,
            confidence=confidence
        )
        
        # 添加到数据模型
        feedback_id = self.data_model.add_ambiguity_feedback(feedback)
        
        # 更新统计
        self.stats['ambiguity_feedbacks'] += 1
        self.stats['feedbacks_collected'] += 1
        
        # 同时创建用户反馈记录
        user_feedback = UserFeedback(
            feedback_id=str(uuid.uuid4()),
            feedback_type=FeedbackType.AMBIGUITY_RESOLUTION,
            severity=FeedbackSeverity.MEDIUM,
            status=FeedbackStatus.PENDING,
            content=f"歧义纠正: '{ambiguous_segment}' 从 '{system_interpretation}' 改为 '{user_correction}'",
            session_id=self.session_id,
            metadata={
                'ambiguity_feedback_id': feedback_id,
                'confidence': confidence
            }
        )
        
        self.data_model.add_feedback(user_feedback)
        
        return feedback_id
    
    def collect_error_correction(
        self,
        error_type: str,
        error_message: str,
        correction: str,
        context: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        收集错误纠正反馈
        
        Args:
            error_type: 错误类型
            error_message: 错误消息
            correction: 纠正内容
            context: 上下文
            
        Returns:
            反馈ID
        """
        feedback = UserFeedback(
            feedback_id=str(uuid.uuid4()),
            feedback_type=FeedbackType.ERROR_CORRECTION,
            severity=FeedbackSeverity.HIGH,
            status=FeedbackStatus.PENDING,
            content=f"错误纠正: {error_type} - {error_message} -> {correction}",
            session_id=self.session_id,
            metadata={
                'error_type': error_type,
                'error_message': error_message,
                'correction': correction,
                'context': context or {}
            }
        )
        
        feedback_id = self.data_model.add_feedback(feedback)
        self.stats['feedbacks_collected'] += 1
        
        return feedback_id
    
    def collect_suggestion(
        self,
        suggestion: str,
        category: str,
        priority: int = 1
    ) -> str:
        """
        收集建议反馈
        
        Args:
            suggestion: 建议内容
            category: 建议类别
            priority: 优先级
            
        Returns:
            反馈ID
        """
        severity = FeedbackSeverity.LOW if priority < 3 else FeedbackSeverity.MEDIUM
        
        feedback = UserFeedback(
            feedback_id=str(uuid.uuid4()),
            feedback_type=FeedbackType.SUGGESTION,
            severity=severity,
            status=FeedbackStatus.PENDING,
            content=suggestion,
            session_id=self.session_id,
            metadata={
                'category': category,
                'priority': priority
            }
        )
        
        feedback_id = self.data_model.add_feedback(feedback)
        self.stats['feedbacks_collected'] += 1
        
        return feedback_id
    
    def collect_rating(
        self,
        item_id: str,
        rating: int,
        comment: Optional[str] = None
    ) -> str:
        """
        收集评分反馈
        
        Args:
            item_id: 评分项ID
            rating: 评分（1-5）
            comment: 评论
            
        Returns:
            反馈ID
        """
        if rating < 1 or rating > 5:
            raise ValueError("评分必须在1-5之间")
        
        feedback = UserFeedback(
            feedback_id=str(uuid.uuid4()),
            feedback_type=FeedbackType.RATING,
            severity=FeedbackSeverity.LOW,
            status=FeedbackStatus.PENDING,
            content=f"评分: {rating}/5" + (f" - {comment}" if comment else ""),
            session_id=self.session_id,
            metadata={
                'item_id': item_id,
                'rating': rating,
                'comment': comment
            }
        )
        
        feedback_id = self.data_model.add_feedback(feedback)
        self.stats['feedbacks_collected'] += 1
        
        return feedback_id
    
    def collect_usage_pattern(
        self,
        pattern_type: str,
        pattern_data: Dict[str, Any]
    ) -> str:
        """
        收集使用模式反馈
        
        Args:
            pattern_type: 模式类型
            pattern_data: 模式数据
            
        Returns:
            反馈ID
        """
        feedback = UserFeedback(
            feedback_id=str(uuid.uuid4()),
            feedback_type=FeedbackType.USAGE_PATTERN,
            severity=FeedbackSeverity.LOW,
            status=FeedbackStatus.PENDING,
            content=f"使用模式: {pattern_type}",
            session_id=self.session_id,
            metadata={
                'pattern_type': pattern_type,
                'pattern_data': pattern_data
            }
        )
        
        feedback_id = self.data_model.add_feedback(feedback)
        self.stats['feedbacks_collected'] += 1
        
        return feedback_id
    
    def get_pending_feedbacks(self) -> List[UserFeedback]:
        """获取待处理反馈"""
        return self.data_model.get_pending_feedbacks()
    
    def process_feedback(self, feedback_id: str) -> bool:
        """
        处理反馈
        
        Args:
            feedback_id: 反馈ID
            
        Returns:
            是否成功处理
        """
        feedback = self.data_model.get_feedback(feedback_id)
        if not feedback:
            return False
        
        # 更新状态为处理中
        self.data_model.update_feedback_status(feedback_id, FeedbackStatus.PROCESSING)
        
        try:
            # 根据反馈类型进行处理
            if feedback.feedback_type == FeedbackType.AMBIGUITY_RESOLUTION:
                self._process_ambiguity_feedback(feedback)
            elif feedback.feedback_type == FeedbackType.ERROR_CORRECTION:
                self._process_error_correction(feedback)
            elif feedback.feedback_type == FeedbackType.SUGGESTION:
                self._process_suggestion(feedback)
            
            # 更新状态为已解决
            self.data_model.update_feedback_status(feedback_id, FeedbackStatus.RESOLVED)
            return True
            
        except Exception as e:
            # 处理失败，保持处理中状态
            print(f"处理反馈失败: {e}")
            return False
    
    def _process_ambiguity_feedback(self, feedback: UserFeedback):
        """处理歧义反馈"""
        metadata = feedback.metadata
        ambiguity_id = metadata.get('ambiguity_feedback_id')
        
        if ambiguity_id and ambiguity_id in self.data_model.ambiguity_feedbacks:
            ambiguity_feedback = self.data_model.ambiguity_feedbacks[ambiguity_id]
            
            # 创建或更新歧义模式
            pattern_id = self._get_or_create_pattern(
                ambiguity_feedback.ambiguous_segment,
                ambiguity_feedback.system_interpretation,
                ambiguity_feedback.user_correction
            )
            
            # 更新模式偏好
            if pattern_id:
                pattern = self.data_model.get_pattern(pattern_id)
                if pattern:
                    pattern.update_preference(ambiguity_feedback.user_correction)
    
    def _process_error_correction(self, feedback: UserFeedback):
        """处理错误纠正反馈"""
        # 创建学习规则
        metadata = feedback.metadata
        rule = LearningRule(
            rule_id=str(uuid.uuid4()),
            condition=metadata.get('error_type', ''),
            action=metadata.get('correction', ''),
            priority=50,
            confidence=0.7,
            source='user_feedback'
        )
        
        self.data_model.add_rule(rule)
    
    def _process_suggestion(self, feedback: UserFeedback):
        """处理建议反馈"""
        # 建议通常不需要自动处理
        # 可以记录下来供人工审核
        pass
    
    def _get_or_create_pattern(
        self,
        ambiguous_segment: str,
        system_interpretation: str,
        user_correction: str
    ) -> Optional[str]:
        """获取或创建歧义模式"""
        # 查找现有模式
        for pattern in self.data_model.patterns.values():
            if pattern.pattern_text == ambiguous_segment:
                return pattern.pattern_id
        
        # 创建新模式
        pattern = AmbiguityPattern(
            pattern_id=str(uuid.uuid4()),
            pattern_text=ambiguous_segment,
            frequency=1,
            common_interpretations=[system_interpretation, user_correction],
            user_preferences={user_correction: 1},
            confidence=0.5
        )
        
        return self.data_model.add_pattern(pattern)
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取统计信息"""
        stats = self.stats.copy()
        stats.update(self.data_model.get_statistics())
        return stats
    
    def clear_statistics(self):
        """清空统计"""
        self.stats = {
            'feedbacks_collected': 0,
            'ambiguity_feedbacks': 0,
            'auto_corrections': 0
        }
    
    def export_feedbacks(self) -> str:
        """导出反馈数据"""
        return self.data_model.export_to_json()
    
    def import_feedbacks(self, json_str: str):
        """导入反馈数据"""
        self.data_model.import_from_json(json_str)


class FeedbackEnabledCompiler:
    """支持反馈的编译器"""
    
    def __init__(self, collector: Optional[FeedbackCollector] = None):
        """
        初始化支持反馈的编译器
        
        Args:
            collector: 反馈收集器
        """
        self.collector = collector or FeedbackCollector()
        self.auto_collect = True
    
    def enable_feedback(self):
        """启用反馈收集"""
        self.auto_collect = True
    
    def disable_feedback(self):
        """禁用反馈收集"""
        self.auto_collect = False
    
    def report_ambiguity(
        self,
        source_text: str,
        ambiguous_segment: str,
        system_interpretation: str,
        user_correction: str,
        context: List[str]
    ):
        """
        报告歧义
        
        Args:
            source_text: 原始文本
            ambiguous_segment: 歧义片段
            system_interpretation: 系统解释
            user_correction: 用户纠正
            context: 上下文
        """
        if self.auto_collect:
            self.collector.collect_ambiguity_feedback(
                source_text=source_text,
                ambiguous_segment=ambiguous_segment,
                system_interpretation=system_interpretation,
                user_correction=user_correction,
                context=context
            )
    
    def report_error(
        self,
        error_type: str,
        error_message: str,
        correction: str
    ):
        """
        报告错误
        
        Args:
            error_type: 错误类型
            error_message: 错误消息
            correction: 纠正内容
        """
        if self.auto_collect:
            self.collector.collect_error_correction(
                error_type=error_type,
                error_message=error_message,
                correction=correction
            )
    
    def get_feedback_summary(self) -> Dict[str, Any]:
        """获取反馈摘要"""
        return self.collector.get_statistics()


# 工厂函数
def create_feedback_collector() -> FeedbackCollector:
    """创建反馈收集器"""
    return FeedbackCollector()


def create_feedback_enabled_compiler() -> FeedbackEnabledCompiler:
    """创建支持反馈的编译器"""
    return FeedbackEnabledCompiler()