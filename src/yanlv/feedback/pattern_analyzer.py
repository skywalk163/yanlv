"""
言律语言模式分析与学习系统

实现歧义模式分析、学习和动态规则调整
"""

from typing import Dict, List, Optional, Any, Tuple
import uuid
from datetime import datetime
from collections import defaultdict
import feedback_model
from feedback_model import (
    AmbiguityPattern, LearningRule,
    FeedbackDataModel
)
import feedback_collector
from feedback_collector import FeedbackCollector


class PatternAnalyzer:
    """模式分析器"""
    
    def __init__(self, data_model: FeedbackDataModel):
        """
        初始化模式分析器
        
        Args:
            data_model: 反馈数据模型
        """
        self.data_model = data_model
        
        # 分析配置
        self.config = {
            'min_frequency': 3,  # 最小频率阈值
            'min_confidence': 0.6,  # 最小置信度阈值
            'pattern_similarity_threshold': 0.8,  # 模式相似度阈值
            'max_patterns': 1000  # 最大模式数量
        }
        
        # 分析结果
        self.analysis_results = {
            'total_patterns': 0,
            'high_frequency_patterns': 0,
            'low_confidence_patterns': 0,
            'patterns_by_type': defaultdict(int)
        }
    
    def analyze_patterns(self) -> Dict[str, Any]:
        """
        分析所有歧义模式
        
        Returns:
            分析结果
        """
        patterns = list(self.data_model.patterns.values())
        
        # 重置分析结果
        self.analysis_results = {
            'total_patterns': len(patterns),
            'high_frequency_patterns': 0,
            'low_confidence_patterns': 0,
            'patterns_by_type': defaultdict(int)
        }
        
        # 分析每个模式
        for pattern in patterns:
            # 统计高频模式
            if pattern.frequency >= self.config['min_frequency']:
                self.analysis_results['high_frequency_patterns'] += 1
            
            # 统计低置信度模式
            if pattern.confidence < self.config['min_confidence']:
                self.analysis_results['low_confidence_patterns'] += 1
            
            # 按类型统计
            pattern_type = self._classify_pattern(pattern)
            self.analysis_results['patterns_by_type'][pattern_type] += 1
        
        return self.analysis_results
    
    def _classify_pattern(self, pattern: AmbiguityPattern) -> str:
        """
        分类歧义模式
        
        Args:
            pattern: 歧义模式
            
        Returns:
            模式类型
        """
        pattern_text = pattern.pattern_text
        
        # 时间表达模式
        if any(word in pattern_text for word in ['年', '月', '日', '时', '分', '秒']):
            return 'time_expression'
        
        # 数量词模式
        if any(word in pattern_text for word in ['个', '只', '条', '件', '次']):
            return 'quantifier'
        
        # 代词模式
        if any(word in pattern_text for word in ['他', '她', '它', '这', '那']):
            return 'pronoun'
        
        # 动词模式
        if any(word in pattern_text for word in ['是', '有', '做', '去', '来']):
            return 'verb'
        
        # 默认
        return 'other'
    
    def find_similar_patterns(self, pattern_text: str) -> List[AmbiguityPattern]:
        """
        查找相似模式
        
        Args:
            pattern_text: 模式文本
            
        Returns:
            相似模式列表
        """
        similar_patterns = []
        
        for pattern in self.data_model.patterns.values():
            similarity = self._calculate_similarity(pattern_text, pattern.pattern_text)
            if similarity >= self.config['pattern_similarity_threshold']:
                similar_patterns.append(pattern)
        
        return similar_patterns
    
    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """
        计算文本相似度
        
        Args:
            text1: 文本1
            text2: 文本2
            
        Returns:
            相似度（0-1）
        """
        # 简单的字符重叠相似度
        if not text1 or not text2:
            return 0.0
        
        set1 = set(text1)
        set2 = set(text2)
        
        intersection = len(set1 & set2)
        union = len(set1 | set2)
        
        if union == 0:
            return 0.0
        
        return intersection / union
    
    def get_pattern_recommendations(self) -> List[Dict[str, Any]]:
        """
        获取模式建议
        
        Returns:
            建议列表
        """
        recommendations = []
        
        # 分析高频低置信度模式
        for pattern in self.data_model.patterns.values():
            if (pattern.frequency >= self.config['min_frequency'] and
                pattern.confidence < self.config['min_confidence']):
                
                recommendations.append({
                    'type': 'low_confidence',
                    'pattern_id': pattern.pattern_id,
                    'pattern_text': pattern.pattern_text,
                    'frequency': pattern.frequency,
                    'confidence': pattern.confidence,
                    'suggestion': f"建议增加 '{pattern.pattern_text}' 的训练数据"
                })
        
        # 分析用户偏好不一致的模式
        for pattern in self.data_model.patterns.values():
            if len(pattern.user_preferences) > 1:
                preferences = list(pattern.user_preferences.values())
                if max(preferences) / sum(preferences) < 0.7:  # 没有明显偏好
                    recommendations.append({
                        'type': 'inconsistent_preference',
                        'pattern_id': pattern.pattern_id,
                        'pattern_text': pattern.pattern_text,
                        'preferences': pattern.user_preferences,
                        'suggestion': f"模式 '{pattern.pattern_text}' 用户偏好不一致，需要更多上下文信息"
                    })
        
        return recommendations
    
    def get_analysis_summary(self) -> Dict[str, Any]:
        """获取分析摘要"""
        return self.analysis_results.copy()


class LearningEngine:
    """学习引擎"""
    
    def __init__(self, data_model: FeedbackDataModel):
        """
        初始化学习引擎
        
        Args:
            data_model: 反馈数据模型
        """
        self.data_model = data_model
        self.pattern_analyzer = PatternAnalyzer(data_model)
        
        # 学习配置
        self.config = {
            'learning_rate': 0.1,  # 学习率
            'min_samples': 5,  # 最小样本数
            'confidence_threshold': 0.8,  # 置信度阈值
            'rule_priority_base': 50  # 规则优先级基数
        }
    
    def learn_from_feedbacks(self) -> Dict[str, Any]:
        """
        从反馈中学习
        
        Returns:
            学习结果
        """
        # 分析模式
        pattern_analysis = self.pattern_analyzer.analyze_patterns()
        
        # 学习结果
        learning_results = {
            'patterns_analyzed': pattern_analysis['total_patterns'],
            'rules_created': 0,
            'rules_updated': 0,
            'confidence_improvements': 0
        }
        
        # 从高频模式学习规则
        for pattern in self.data_model.patterns.values():
            if pattern.frequency >= self.config['min_samples']:
                # 获取用户偏好的解释
                preferred = pattern.get_preferred_interpretation()
                
                if preferred:
                    # 创建或更新学习规则
                    rule = self._create_or_update_rule(pattern, preferred)
                    if rule:
                        if rule.usage_count == 0:
                            learning_results['rules_created'] += 1
                        else:
                            learning_results['rules_updated'] += 1
                
                # 更新模式置信度
                old_confidence = pattern.confidence
                self._update_pattern_confidence(pattern)
                
                if pattern.confidence > old_confidence:
                    learning_results['confidence_improvements'] += 1
        
        return learning_results
    
    def _create_or_update_rule(
        self,
        pattern: AmbiguityPattern,
        preferred_interpretation: str
    ) -> Optional[LearningRule]:
        """
        创建或更新学习规则
        
        Args:
            pattern: 歧义模式
            preferred_interpretation: 偏好解释
            
        Returns:
            学习规则
        """
        # 查找现有规则
        existing_rule = None
        for rule in self.data_model.rules.values():
            if rule.condition == pattern.pattern_text:
                existing_rule = rule
                break
        
        if existing_rule:
            # 更新现有规则
            existing_rule.action = preferred_interpretation
            existing_rule.priority = self._calculate_rule_priority(pattern)
            existing_rule.confidence = pattern.confidence
            existing_rule.updated_at = datetime.now()
            existing_rule.source = 'user_feedback'
            return existing_rule
        else:
            # 创建新规则
            rule = LearningRule(
                rule_id=str(uuid.uuid4()),
                condition=pattern.pattern_text,
                action=preferred_interpretation,
                priority=self._calculate_rule_priority(pattern),
                confidence=pattern.confidence,
                source='user_feedback'
            )
            
            self.data_model.add_rule(rule)
            return rule
    
    def _calculate_rule_priority(self, pattern: AmbiguityPattern) -> int:
        """
        计算规则优先级
        
        Args:
            pattern: 歧义模式
            
        Returns:
            优先级
        """
        # 基础优先级 + 频率加成 + 置信度加成
        base_priority = self.config['rule_priority_base']
        frequency_bonus = min(pattern.frequency * 2, 30)  # 最多加30
        confidence_bonus = int(pattern.confidence * 20)  # 最多加20
        
        return base_priority + frequency_bonus + confidence_bonus
    
    def _update_pattern_confidence(self, pattern: AmbiguityPattern):
        """
        更新模式置信度
        
        Args:
            pattern: 歧义模式
        """
        # 基于用户偏好一致性更新置信度
        if not pattern.user_preferences:
            return
        
        preferences = list(pattern.user_preferences.values())
        total = sum(preferences)
        max_preference = max(preferences)
        
        # 一致性得分
        consistency_score = max_preference / total if total > 0 else 0
        
        # 更新置信度
        pattern.confidence = (
            pattern.confidence * (1 - self.config['learning_rate']) +
            consistency_score * self.config['learning_rate']
        )
    
    def apply_learned_rules(self, text: str) -> Optional[str]:
        """
        应用学习规则
        
        Args:
            text: 输入文本
            
        Returns:
            应用结果
        """
        # 按优先级获取规则
        rules = self.data_model.get_rules_by_priority()
        
        for rule in rules:
            if rule.condition in text:
                # 更新规则使用统计
                rule.update_usage(success=True)
                return rule.action
        
        return None
    
    def get_learning_summary(self) -> Dict[str, Any]:
        """获取学习摘要"""
        return {
            'total_patterns': len(self.data_model.patterns),
            'total_rules': len(self.data_model.rules),
            'pattern_analysis': self.pattern_analyzer.get_analysis_summary(),
            'top_patterns': [
                {
                    'text': p.pattern_text,
                    'frequency': p.frequency,
                    'confidence': p.confidence
                }
                for p in self.data_model.get_patterns_by_frequency(10)
            ]
        }


class DynamicRuleAdjuster:
    """动态规则调整器"""
    
    def __init__(self, data_model: FeedbackDataModel):
        """
        初始化动态规则调整器
        
        Args:
            data_model: 反馈数据模型
        """
        self.data_model = data_model
        self.learning_engine = LearningEngine(data_model)
        
        # 调整配置
        self.config = {
            'adjustment_interval': 100,  # 调整间隔
            'min_adjustment_samples': 10,  # 最小调整样本数
            'priority_adjustment_range': 10  # 优先级调整范围
        }
        
        # 调整统计
        self.adjustment_stats = {
            'total_adjustments': 0,
            'priority_increases': 0,
            'priority_decreases': 0,
            'rules_disabled': 0
        }
    
    def adjust_rules(self) -> Dict[str, Any]:
        """
        调整规则
        
        Returns:
            调整结果
        """
        # 从反馈学习
        learning_results = self.learning_engine.learn_from_feedbacks()
        
        # 调整结果
        adjustment_results = {
            'learning_results': learning_results,
            'rules_adjusted': 0,
            'rules_disabled': 0
        }
        
        # 根据成功率调整规则优先级
        for rule in self.data_model.rules.values():
            if rule.usage_count >= self.config['min_adjustment_samples']:
                success_rate = rule.get_success_rate()
                
                # 成功率高，提高优先级
                if success_rate > 0.8:
                    rule.priority = min(rule.priority + 5, 100)
                    self.adjustment_stats['priority_increases'] += 1
                    adjustment_results['rules_adjusted'] += 1
                
                # 成功率低，降低优先级
                elif success_rate < 0.3:
                    rule.priority = max(rule.priority - 5, 1)
                    self.adjustment_stats['priority_decreases'] += 1
                    adjustment_results['rules_adjusted'] += 1
                    
                    # 成功率极低，禁用规则
                    if success_rate < 0.1:
                        rule.priority = 0
                        self.adjustment_stats['rules_disabled'] += 1
                        adjustment_results['rules_disabled'] += 1
        
        self.adjustment_stats['total_adjustments'] += 1
        
        return adjustment_results
    
    def get_adjustment_summary(self) -> Dict[str, Any]:
        """获取调整摘要"""
        return {
            'adjustment_stats': self.adjustment_stats.copy(),
            'learning_summary': self.learning_engine.get_learning_summary()
        }


# 工厂函数
def create_pattern_analyzer(data_model: FeedbackDataModel) -> PatternAnalyzer:
    """创建模式分析器"""
    return PatternAnalyzer(data_model)


def create_learning_engine(data_model: FeedbackDataModel) -> LearningEngine:
    """创建学习引擎"""
    return LearningEngine(data_model)


def create_dynamic_rule_adjuster(data_model: FeedbackDataModel) -> DynamicRuleAdjuster:
    """创建动态规则调整器"""
    return DynamicRuleAdjuster(data_model)