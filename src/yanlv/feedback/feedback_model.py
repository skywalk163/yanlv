"""
言律语言用户反馈系统

实现用户反馈收集、分析和动态学习功能
"""

from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
import json
import hashlib


class FeedbackType(Enum):
    """反馈类型"""
    AMBIGUITY_RESOLUTION = "ambiguity_resolution"  # 歧义消解反馈
    ERROR_CORRECTION = "error_correction"  # 错误纠正
    SUGGESTION = "suggestion"  # 建议
    RATING = "rating"  # 评分
    USAGE_PATTERN = "usage_pattern"  # 使用模式


class FeedbackSeverity(Enum):
    """反馈严重程度"""
    LOW = "low"  # 低
    MEDIUM = "medium"  # 中
    HIGH = "high"  # 高
    CRITICAL = "critical"  # 关键


class FeedbackStatus(Enum):
    """反馈状态"""
    PENDING = "pending"  # 待处理
    PROCESSING = "processing"  # 处理中
    RESOLVED = "resolved"  # 已解决
    IGNORED = "ignored"  # 已忽略


@dataclass
class AmbiguityFeedback:
    """歧义消解反馈"""
    source_text: str  # 原始文本
    ambiguous_segment: str  # 歧义片段
    system_interpretation: str  # 系统解释
    user_correction: str  # 用户纠正
    context: List[str]  # 上下文
    confidence: float  # 置信度
    timestamp: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'source_text': self.source_text,
            'ambiguous_segment': self.ambiguous_segment,
            'system_interpretation': self.system_interpretation,
            'user_correction': self.user_correction,
            'context': self.context,
            'confidence': self.confidence,
            'timestamp': self.timestamp.isoformat()
        }
    
    def get_hash(self) -> str:
        """获取反馈哈希值（用于去重）"""
        content = f"{self.ambiguous_segment}:{self.system_interpretation}:{self.user_correction}"
        return hashlib.md5(content.encode()).hexdigest()


@dataclass
class UserFeedback:
    """用户反馈"""
    feedback_id: str  # 反馈ID
    feedback_type: FeedbackType  # 反馈类型
    severity: FeedbackSeverity  # 严重程度
    status: FeedbackStatus  # 状态
    content: str  # 反馈内容
    user_id: Optional[str] = None  # 用户ID（匿名）
    session_id: Optional[str] = None  # 会话ID
    metadata: Dict[str, Any] = field(default_factory=dict)  # 元数据
    timestamp: datetime = field(default_factory=datetime.now)
    processed_at: Optional[datetime] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'feedback_id': self.feedback_id,
            'feedback_type': self.feedback_type.value,
            'severity': self.severity.value,
            'status': self.status.value,
            'content': self.content,
            'user_id': self.user_id,
            'session_id': self.session_id,
            'metadata': self.metadata,
            'timestamp': self.timestamp.isoformat(),
            'processed_at': self.processed_at.isoformat() if self.processed_at else None
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'UserFeedback':
        """从字典创建"""
        return cls(
            feedback_id=data['feedback_id'],
            feedback_type=FeedbackType(data['feedback_type']),
            severity=FeedbackSeverity(data['severity']),
            status=FeedbackStatus(data['status']),
            content=data['content'],
            user_id=data.get('user_id'),
            session_id=data.get('session_id'),
            metadata=data.get('metadata', {}),
            timestamp=datetime.fromisoformat(data['timestamp']),
            processed_at=datetime.fromisoformat(data['processed_at']) if data.get('processed_at') else None
        )


@dataclass
class AmbiguityPattern:
    """歧义模式"""
    pattern_id: str  # 模式ID
    pattern_text: str  # 模式文本
    frequency: int  # 出现频率
    common_interpretations: List[str]  # 常见解释
    user_preferences: Dict[str, int]  # 用户偏好统计
    confidence: float  # 置信度
    last_updated: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'pattern_id': self.pattern_id,
            'pattern_text': self.pattern_text,
            'frequency': self.frequency,
            'common_interpretations': self.common_interpretations,
            'user_preferences': self.user_preferences,
            'confidence': self.confidence,
            'last_updated': self.last_updated.isoformat()
        }
    
    def update_preference(self, interpretation: str):
        """更新用户偏好"""
        if interpretation not in self.user_preferences:
            self.user_preferences[interpretation] = 0
        self.user_preferences[interpretation] += 1
        self.frequency += 1
        self.last_updated = datetime.now()
    
    def get_preferred_interpretation(self) -> str:
        """获取用户偏好的解释"""
        if not self.user_preferences:
            return self.common_interpretations[0] if self.common_interpretations else ""
        
        return max(self.user_preferences.items(), key=lambda x: x[1])[0]


@dataclass
class LearningRule:
    """学习规则"""
    rule_id: str  # 规则ID
    condition: str  # 条件
    action: str  # 动作
    priority: int  # 优先级
    confidence: float  # 置信度
    source: str  # 来源（用户反馈/系统学习）
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    usage_count: int = 0
    success_count: int = 0
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'rule_id': self.rule_id,
            'condition': self.condition,
            'action': self.action,
            'priority': self.priority,
            'confidence': self.confidence,
            'source': self.source,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'usage_count': self.usage_count,
            'success_count': self.success_count
        }
    
    def update_usage(self, success: bool):
        """更新使用统计"""
        self.usage_count += 1
        if success:
            self.success_count += 1
        self.updated_at = datetime.now()
    
    def get_success_rate(self) -> float:
        """获取成功率"""
        if self.usage_count == 0:
            return 0.0
        return self.success_count / self.usage_count


class FeedbackDataModel:
    """反馈数据模型"""
    
    def __init__(self):
        """初始化反馈数据模型"""
        self.feedbacks: Dict[str, UserFeedback] = {}
        self.ambiguity_feedbacks: Dict[str, AmbiguityFeedback] = {}
        self.patterns: Dict[str, AmbiguityPattern] = {}
        self.rules: Dict[str, LearningRule] = {}
        
        # 统计信息
        self.stats = {
            'total_feedbacks': 0,
            'pending_feedbacks': 0,
            'resolved_feedbacks': 0,
            'patterns_learned': 0,
            'rules_created': 0
        }
    
    def add_feedback(self, feedback: UserFeedback) -> str:
        """添加反馈"""
        self.feedbacks[feedback.feedback_id] = feedback
        self.stats['total_feedbacks'] += 1
        
        if feedback.status == FeedbackStatus.PENDING:
            self.stats['pending_feedbacks'] += 1
        
        return feedback.feedback_id
    
    def add_ambiguity_feedback(self, feedback: AmbiguityFeedback) -> str:
        """添加歧义反馈"""
        feedback_hash = feedback.get_hash()
        self.ambiguity_feedbacks[feedback_hash] = feedback
        return feedback_hash
    
    def add_pattern(self, pattern: AmbiguityPattern) -> str:
        """添加歧义模式"""
        self.patterns[pattern.pattern_id] = pattern
        self.stats['patterns_learned'] += 1
        return pattern.pattern_id
    
    def add_rule(self, rule: LearningRule) -> str:
        """添加学习规则"""
        self.rules[rule.rule_id] = rule
        self.stats['rules_created'] += 1
        return rule.rule_id
    
    def get_feedback(self, feedback_id: str) -> Optional[UserFeedback]:
        """获取反馈"""
        return self.feedbacks.get(feedback_id)
    
    def get_pattern(self, pattern_id: str) -> Optional[AmbiguityPattern]:
        """获取歧义模式"""
        return self.patterns.get(pattern_id)
    
    def get_rule(self, rule_id: str) -> Optional[LearningRule]:
        """获取学习规则"""
        return self.rules.get(rule_id)
    
    def update_feedback_status(self, feedback_id: str, status: FeedbackStatus):
        """更新反馈状态"""
        if feedback_id in self.feedbacks:
            feedback = self.feedbacks[feedback_id]
            old_status = feedback.status
            feedback.status = status
            feedback.processed_at = datetime.now()
            
            # 更新统计
            if old_status == FeedbackStatus.PENDING:
                self.stats['pending_feedbacks'] -= 1
            if status == FeedbackStatus.RESOLVED:
                self.stats['resolved_feedbacks'] += 1
    
    def get_pending_feedbacks(self) -> List[UserFeedback]:
        """获取待处理反馈"""
        return [
            f for f in self.feedbacks.values()
            if f.status == FeedbackStatus.PENDING
        ]
    
    def get_patterns_by_frequency(self, limit: int = 10) -> List[AmbiguityPattern]:
        """按频率获取歧义模式"""
        sorted_patterns = sorted(
            self.patterns.values(),
            key=lambda p: p.frequency,
            reverse=True
        )
        return sorted_patterns[:limit]
    
    def get_rules_by_priority(self) -> List[LearningRule]:
        """按优先级获取学习规则"""
        return sorted(
            self.rules.values(),
            key=lambda r: r.priority,
            reverse=True
        )
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取统计信息"""
        stats = self.stats.copy()
        stats['total_patterns'] = len(self.patterns)
        stats['total_rules'] = len(self.rules)
        stats['ambiguity_feedbacks'] = len(self.ambiguity_feedbacks)
        return stats
    
    def clear(self):
        """清空所有数据"""
        self.feedbacks.clear()
        self.ambiguity_feedbacks.clear()
        self.patterns.clear()
        self.rules.clear()
        self.stats = {
            'total_feedbacks': 0,
            'pending_feedbacks': 0,
            'resolved_feedbacks': 0,
            'patterns_learned': 0,
            'rules_created': 0
        }
    
    def export_to_json(self) -> str:
        """导出为JSON"""
        data = {
            'feedbacks': [f.to_dict() for f in self.feedbacks.values()],
            'ambiguity_feedbacks': [f.to_dict() for f in self.ambiguity_feedbacks.values()],
            'patterns': [p.to_dict() for p in self.patterns.values()],
            'rules': [r.to_dict() for r in self.rules.values()],
            'stats': self.stats
        }
        return json.dumps(data, ensure_ascii=False, indent=2)
    
    def import_from_json(self, json_str: str):
        """从JSON导入"""
        data = json.loads(json_str)
        
        # 导入反馈
        for feedback_data in data.get('feedbacks', []):
            feedback = UserFeedback.from_dict(feedback_data)
            self.feedbacks[feedback.feedback_id] = feedback
        
        # 导入歧义反馈
        for feedback_data in data.get('ambiguity_feedbacks', []):
            feedback = AmbiguityFeedback(**feedback_data)
            feedback.timestamp = datetime.fromisoformat(feedback_data['timestamp'])
            self.ambiguity_feedbacks[feedback.get_hash()] = feedback
        
        # 导入模式
        for pattern_data in data.get('patterns', []):
            pattern = AmbiguityPattern(**pattern_data)
            pattern.last_updated = datetime.fromisoformat(pattern_data['last_updated'])
            self.patterns[pattern.pattern_id] = pattern
        
        # 导入规则
        for rule_data in data.get('rules', []):
            rule = LearningRule(**rule_data)
            rule.created_at = datetime.fromisoformat(rule_data['created_at'])
            rule.updated_at = datetime.fromisoformat(rule_data['updated_at'])
            self.rules[rule.rule_id] = rule
        
        # 导入统计
        self.stats = data.get('stats', self.stats)