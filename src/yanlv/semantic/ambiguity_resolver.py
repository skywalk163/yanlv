"""
言律语言歧义消解器

基于语义上下文和类型推断的歧义消解系统
"""

from typing import List, Dict, Any, Optional, Tuple
from enum import Enum
from .context_tracker import SemanticContextTracker, SemanticType, SemanticRelation
from .type_inference import TypeInferenceSystem


class AmbiguityType(Enum):
    """歧义类型枚举"""
    TIME_EXPRESSION = "time_expression"  # 时间表达式歧义
    QUANTIFIER = "quantifier"  # 量词歧义
    SUBJECT_OMISSION = "subject_omission"  # 主语省略歧义
    CONTEXT_DEPENDENT = "context_dependent"  # 上下文依赖歧义
    NESTED = "nested"  # 嵌套歧义
    MULTIPLE_MEANING = "multiple_meaning"  # 多义歧义
    PRONOUN_REFERENCE = "pronoun_reference"  # 代词指代歧义
    ELLIPSIS = "ellipsis"  # 省略歧义
    COORDINATION = "coordination"  # 并列结构歧义
    MODIFIER_ATTACHMENT = "modifier_attachment"  # 修饰语附着歧义


class AmbiguityResolutionStrategy(Enum):
    """歧义消解策略枚举"""
    CONTEXT_BASED = "context_based"  # 基于上下文
    TYPE_BASED = "type_based"  # 基于类型
    FREQUENCY_BASED = "frequency_based"  # 基于频率
    SEMANTIC_ROLE = "semantic_role"  # 基于语义角色
    SYNTACTIC_PATTERN = "syntactic_pattern"  # 基于句法模式
    USER_FEEDBACK = "user_feedback"  # 基于用户反馈


class AmbiguityResolver:
    """歧义消解器"""
    
    def __init__(self, context_tracker: SemanticContextTracker, 
                 type_inference: TypeInferenceSystem):
        """
        初始化歧义消解器
        
        Args:
            context_tracker: 语义上下文跟踪器
            type_inference: 类型推断系统
        """
        self.context = context_tracker
        self.type_inference = type_inference
        
        # 歧义消解规则
        self.rules = {
            AmbiguityType.TIME_EXPRESSION: self._resolve_time_expression,
            AmbiguityType.QUANTIFIER: self._resolve_quantifier,
            AmbiguityType.SUBJECT_OMISSION: self._resolve_subject_omission,
            AmbiguityType.CONTEXT_DEPENDENT: self._resolve_context_dependent,
            AmbiguityType.NESTED: self._resolve_nested,
            AmbiguityType.MULTIPLE_MEANING: self._resolve_multiple_meaning,
            AmbiguityType.PRONOUN_REFERENCE: self._resolve_pronoun_reference,
            AmbiguityType.ELLIPSIS: self._resolve_ellipsis,
            AmbiguityType.COORDINATION: self._resolve_coordination,
            AmbiguityType.MODIFIER_ATTACHMENT: self._resolve_modifier_attachment,
        }
        
        # 消解策略权重
        self.strategy_weights = {
            AmbiguityResolutionStrategy.CONTEXT_BASED: 0.4,
            AmbiguityResolutionStrategy.TYPE_BASED: 0.3,
            AmbiguityResolutionStrategy.SEMANTIC_ROLE: 0.2,
            AmbiguityResolutionStrategy.SYNTACTIC_PATTERN: 0.1,
        }
        
        # 用户反馈数据
        self.user_feedback = {}
        
        # 歧义模式库
        self.ambiguity_patterns = self._build_ambiguity_patterns()
    
    def _build_ambiguity_patterns(self) -> Dict[str, AmbiguityType]:
        """构建歧义模式库"""
        patterns = {
            # 时间表达式歧义
            r"(\d+)(秒|分|时|天|周|月|年)(前|后|内|外)": AmbiguityType.TIME_EXPRESSION,
            r"每(天|周|月|年)": AmbiguityType.TIME_EXPRESSION,
            r"([上下]午|晚上|凌晨)(\d+)点": AmbiguityType.TIME_EXPRESSION,
            
            # 量词歧义
            r"(\d+)(个|只|条|张|本|台|辆)": AmbiguityType.QUANTIFIER,
            r"一些|许多|大量|少量|几个": AmbiguityType.QUANTIFIER,
            r"全部|所有|每个|任意": AmbiguityType.QUANTIFIER,
            
            # 主语省略歧义
            r"^[，。；：]": AmbiguityType.SUBJECT_OMISSION,  # 以标点开头
            r"^[变设定印计]": AmbiguityType.SUBJECT_OMISSION,  # 以动词开头
            r"^[和与及跟同]": AmbiguityType.SUBJECT_OMISSION,  # 以连词开头
            
            # 上下文依赖歧义
            r"它|他|她|这|那|此|其": AmbiguityType.CONTEXT_DEPENDENT,
            r"前者|后者|前者|后者": AmbiguityType.CONTEXT_DEPENDENT,
            r"如上|如下|如上所述|如下所述": AmbiguityType.CONTEXT_DEPENDENT,
            
            # 多义歧义
            r"打(开|印|算|电话|字)": AmbiguityType.MULTIPLE_MEANING,
            r"行(走|为|列|程)": AmbiguityType.MULTIPLE_MEANING,
            r"发(现|送|展|光)": AmbiguityType.MULTIPLE_MEANING,
            
            # 代词指代歧义
            r"自己|自身|本人|本身": AmbiguityType.PRONOUN_REFERENCE,
            r"彼此|互相|相互": AmbiguityType.PRONOUN_REFERENCE,
            r"谁|什么|哪里|何时|如何": AmbiguityType.PRONOUN_REFERENCE,
            
            # 省略歧义
            r"……|…": AmbiguityType.ELLIPSIS,
            r"等等|等|之类": AmbiguityType.ELLIPSIS,
            r"省略|略去|跳过": AmbiguityType.ELLIPSIS,
            
            # 并列结构歧义
            r"[、，]和[、，]": AmbiguityType.COORDINATION,
            r"[、，]或[、，]": AmbiguityType.COORDINATION,
            r"[、，]与[、，]": AmbiguityType.COORDINATION,
            
            # 修饰语附着歧义
            r"的[^的]+(的|地|得)": AmbiguityType.MODIFIER_ATTACHMENT,
            r"地[^地]+(的|地|得)": AmbiguityType.MODIFIER_ATTACHMENT,
            r"得[^得]+(的|地|得)": AmbiguityType.MODIFIER_ATTACHMENT,
        }
        
        return patterns
    
    def detect_ambiguity(self, expression: str) -> List[Dict[str, Any]]:
        """
        检测表达式中的歧义
        
        Args:
            expression: 待检测的表达式
            
        Returns:
            歧义检测结果列表
        """
        import re
        
        ambiguities = []
        
        # 检测各种歧义类型
        for pattern, ambiguity_type in self.ambiguity_patterns.items():
            matches = re.finditer(pattern, expression)
            for match in matches:
                ambiguity = {
                    "type": ambiguity_type,
                    "pattern": pattern,
                    "match": match.group(),
                    "start": match.start(),
                    "end": match.end(),
                    "confidence": 0.7,  # 初始置信度
                }
                ambiguities.append(ambiguity)
        
        # 检测嵌套歧义
        if len(ambiguities) > 1:
            # 检查是否有重叠的歧义
            for i in range(len(ambiguities)):
                for j in range(i + 1, len(ambiguities)):
                    a1 = ambiguities[i]
                    a2 = ambiguities[j]
                    
                    # 检查重叠
                    if (a1["start"] <= a2["end"] and a1["end"] >= a2["start"]):
                        nested_ambiguity = {
                            "type": AmbiguityType.NESTED,
                            "pattern": f"{a1['type'].value}+{a2['type'].value}",
                            "match": expression[a1["start"]:max(a1["end"], a2["end"])],
                            "start": min(a1["start"], a2["start"]),
                            "end": max(a1["end"], a2["end"]),
                            "confidence": 0.8,
                            "nested_types": [a1["type"], a2["type"]],
                        }
                        ambiguities.append(nested_ambiguity)
        
        # 根据上下文调整置信度
        for ambiguity in ambiguities:
            ambiguity["confidence"] = self._adjust_confidence(ambiguity, expression)
        
        # 按置信度排序
        ambiguities.sort(key=lambda x: x["confidence"], reverse=True)
        
        return ambiguities
    
    def _adjust_confidence(self, ambiguity: Dict[str, Any], expression: str) -> float:
        """
        根据上下文调整置信度（优化版）

        采用多因素加权计算：
        1. 基础置信度（来自模式匹配）
        2. 上下文相关性
        3. 类型一致性
        4. 历史频率
        5. 用户反馈
        """
        base_confidence = ambiguity["confidence"]
        ambiguity_type = ambiguity["type"]
        match_text = ambiguity.get("match", "")

        # 初始化各因素权重
        weights = {
            "base": 0.3,          # 基础置信度权重
            "context": 0.25,      # 上下文相关性权重
            "type": 0.2,          # 类型一致性权重
            "frequency": 0.15,    # 历史频率权重
            "feedback": 0.1,      # 用户反馈权重
        }

        scores = {"base": base_confidence}

        # 1. 上下文相关性评分
        context_score = 0.5  # 默认中等相关性
        context = self.context.get_recent_context()
        if context:
            # 检查最近的上下文中是否有相关歧义
            relevant_context_count = 0
            for ctx in context[-5:]:  # 最近5个上下文
                if ambiguity_type.value in ctx.get("ambiguity_types", []):
                    relevant_context_count += 1
                # 检查主题相关性
                if "topic" in ctx and ctx["topic"]:
                    topic = ctx["topic"]
                    if topic in expression or topic in match_text:
                        relevant_context_count += 0.5

            # 根据相关上下文数量调整分数
            if relevant_context_count > 0:
                context_score = min(0.5 + relevant_context_count * 0.15, 0.95)

        scores["context"] = context_score

        # 2. 类型一致性评分
        type_score = 0.5  # 默认中等一致性
        type_result = self.type_inference.infer_expression_type(expression)
        if type_result["type"]:
            inferred_type = type_result["type"]

            # 根据歧义类型和推断类型的一致性评分
            type_consistency = {
                AmbiguityType.TIME_EXPRESSION: ["TIME", "NUMBER", "QUANTITY"],
                AmbiguityType.QUANTIFIER: ["NUMBER", "QUANTITY", "COLLECTION"],
                AmbiguityType.SUBJECT_OMISSION: ["ENTITY", "OBJECT"],
                AmbiguityType.CONTEXT_DEPENDENT: ["ENTITY", "OBJECT", "REFERENCE"],
                AmbiguityType.MULTIPLE_MEANING: ["ACTION", "ENTITY"],
            }

            expected_types = type_consistency.get(ambiguity_type, [])
            if inferred_type in expected_types:
                type_score = 0.85  # 高一致性
            elif inferred_type in ["UNKNOWN", "ANY"]:
                type_score = 0.6   # 未知类型，中等分数
            else:
                type_score = 0.3   # 低一致性

        scores["type"] = type_score

        # 3. 历史频率评分
        frequency_score = 0.5  # 默认中等频率
        resolutions = self.context.get_ambiguity_resolutions(limit=20, ambiguity_type=ambiguity_type.value)
        if resolutions:
            # 计算最近的成功率
            recent_confidences = [
                r.get("resolution", {}).get("confidence", 0.5)
                for r in resolutions[-10:]
            ]
            if recent_confidences:
                avg_recent = sum(recent_confidences) / len(recent_confidences)
                # 如果历史表现好，提高分数
                frequency_score = 0.4 + avg_recent * 0.5

        scores["frequency"] = frequency_score

        # 4. 用户反馈评分
        feedback_score = 0.5  # 默认无反馈
        feedback_key = f"{ambiguity_type.value}:{match_text}"
        if feedback_key in self.user_feedback:
            user_confidence = self.user_feedback[feedback_key]
            feedback_score = user_confidence
            # 用户反馈权重加倍（因为用户反馈最可靠）
            weights["feedback"] = 0.2
            weights["base"] = 0.2  # 相应减少基砠权重

        scores["feedback"] = feedback_score

        # 5. 计算加权平均置信度
        total_weight = sum(weights.values())
        weighted_confidence = sum(
            scores[factor] * weights[factor]
            for factor in scores.keys()
        ) / total_weight

        # 6. 应用额外调整因子

        # 歧义位置因子（表达式中间的歧义通常更可靠）
        position = ambiguity.get("start", 0)
        expression_length = len(expression)
        if expression_length > 0:
            position_factor = 1.0 - abs(position - expression_length / 2) / expression_length * 0.2
            weighted_confidence *= position_factor

        # 匹配长度因子（更长的匹配通常更可靠）
        match_length = len(match_text)
        if match_length > 0:
            length_factor = min(1.0, 0.8 + match_length * 0.02)
            weighted_confidence *= length_factor

        # 7. 确保置信度在合理范围
        final_confidence = max(0.1, min(weighted_confidence, 0.98))

        return final_confidence
    
    def resolve_ambiguity(self, expression: str, ambiguity: Dict[str, Any]) -> Dict[str, Any]:
        """
        消解歧义
        
        Args:
            expression: 原始表达式
            ambiguity: 歧义信息
            
        Returns:
            消解结果
        """
        ambiguity_type = ambiguity["type"]
        
        # 调用相应的消解规则
        if ambiguity_type in self.rules:
            resolution = self.rules[ambiguity_type](expression, ambiguity)
        else:
            # 默认消解策略
            resolution = self._resolve_default(expression, ambiguity)
        
        # 记录消解历史
        self.context.add_ambiguity_resolution({
            "expression": expression,
            "ambiguity": ambiguity,
            "resolution": resolution,
        })

        return resolution
    
    def _resolve_time_expression(self, expression: str, ambiguity: Dict[str, Any]) -> Dict[str, Any]:
        """消解时间表达式歧义"""
        import re
        
        match = ambiguity["match"]
        result = {
            "type": "TIME_EXPRESSION",
            "interpretation": None,
            "confidence": 0.8,
            "strategies": [],
        }
        
        # 分析时间表达式
        time_patterns = [
            (r"(\d+)(秒|分|时|天|周|月|年)(前|后|内|外)", "RELATIVE_TIME"),
            (r"每(天|周|月|年)", "PERIODIC_TIME"),
            (r"([上下]午|晚上|凌晨)(\d+)点", "ABSOLUTE_TIME"),
        ]
        
        for pattern, time_type in time_patterns:
            m = re.match(pattern, match)
            if m:
                result["interpretation"] = time_type
                
                # 提取时间单位
                if time_type == "RELATIVE_TIME":
                    amount = m.group(1)
                    unit = m.group(2)
                    direction = m.group(3)
                    result["value"] = {
                        "amount": int(amount),
                        "unit": unit,
                        "direction": direction,
                    }
                elif time_type == "PERIODIC_TIME":
                    unit = m.group(1)
                    result["value"] = {"unit": unit}
                elif time_type == "ABSOLUTE_TIME":
                    period = m.group(1)
                    hour = m.group(2)
                    result["value"] = {
                        "period": period,
                        "hour": int(hour),
                    }
                
                break
        
        # 应用消解策略
        strategies = []
        
        # 1. 基于上下文的策略
        context = self.context.get_recent_context()
        if context:
            for ctx in context:
                if "time_reference" in ctx:
                    result["confidence"] = min(result["confidence"] + 0.1, 0.95)
                    strategies.append(AmbiguityResolutionStrategy.CONTEXT_BASED)
                    break
        
        # 2. 基于类型的策略
        type_result = self.type_inference.infer_expression_type(expression)
        if type_result["type"] == "TIME":
            result["confidence"] = min(result["confidence"] + 0.1, 0.95)
            strategies.append(AmbiguityResolutionStrategy.TYPE_BASED)
        
        result["strategies"] = [s.value for s in strategies]
        
        return result
    
    def _resolve_quantifier(self, expression: str, ambiguity: Dict[str, Any]) -> Dict[str, Any]:
        """消解量词歧义"""
        import re
        
        match = ambiguity["match"]
        result = {
            "type": "QUANTIFIER",
            "interpretation": None,
            "confidence": 0.7,
            "strategies": [],
        }
        
        # 分析量词
        quantifier_patterns = [
            (r"(\d+)(个|只|条|张|本|台|辆)", "COUNTABLE"),
            (r"一些|许多|大量|少量|几个", "INDEFINITE"),
            (r"全部|所有|每个|任意", "UNIVERSAL"),
        ]
        
        for pattern, quant_type in quantifier_patterns:
            m = re.match(pattern, match)
            if m:
                result["interpretation"] = quant_type
                
                if quant_type == "COUNTABLE":
                    amount = m.group(1)
                    classifier = m.group(2)
                    result["value"] = {
                        "amount": int(amount),
                        "classifier": classifier,
                    }
                elif quant_type == "INDEFINITE":
                    result["value"] = {"quantifier": match}
                elif quant_type == "UNIVERSAL":
                    result["value"] = {"quantifier": match}
                
                break
        
        # 应用消解策略
        strategies = []
        
        # 1. 基于语义角色的策略
        semantic_roles = self.context.get_semantic_roles()
        if semantic_roles:
            for role in semantic_roles:
                if role["type"] in ["QUANTITY", "AMOUNT"]:
                    result["confidence"] = min(result["confidence"] + 0.15, 0.95)
                    strategies.append(AmbiguityResolutionStrategy.SEMANTIC_ROLE)
                    break
        
        # 2. 基于句法模式的策略
        if "个" in match or "只" in match or "条" in match:
            # 典型的数量表达模式
            result["confidence"] = min(result["confidence"] + 0.1, 0.95)
            strategies.append(AmbiguityResolutionStrategy.SYNTACTIC_PATTERN)
        
        result["strategies"] = [s.value for s in strategies]
        
        return result
    
    def _resolve_subject_omission(self, expression: str, ambiguity: Dict[str, Any]) -> Dict[str, Any]:
        """消解主语省略歧义"""
        result = {
            "type": "SUBJECT_OMISSION",
            "interpretation": None,
            "confidence": 0.6,
            "strategies": [],
        }
        
        # 从上下文中推断主语
        context = self.context.get_recent_context()
        if context:
            # 查找最近提到的主语
            for ctx in reversed(context):
                if "subject" in ctx:
                    result["interpretation"] = "INFERRED_SUBJECT"
                    result["value"] = {"subject": ctx["subject"]}
                    result["confidence"] = 0.8
                    result["strategies"].append(AmbiguityResolutionStrategy.CONTEXT_BASED.value)
                    break
        
        # 如果没有找到主语，使用默认主语
        if not result["interpretation"]:
            result["interpretation"] = "DEFAULT_SUBJECT"
            result["value"] = {"subject": "它"}
            result["confidence"] = 0.5
            result["strategies"].append(AmbiguityResolutionStrategy.FREQUENCY_BASED.value)
        
        return result
    
    def _resolve_context_dependent(self, expression: str, ambiguity: Dict[str, Any]) -> Dict[str, Any]:
        """消解上下文依赖歧义"""
        match = ambiguity["match"]
        result = {
            "type": "CONTEXT_DEPENDENT",
            "interpretation": None,
            "confidence": 0.7,
            "strategies": [],
        }
        
        # 代词指代消解
        if match in ["它", "他", "她", "这", "那", "此", "其"]:
            # 从上下文中查找最近的先行词
            context = self.context.get_recent_context()
            if context:
                for ctx in reversed(context):
                    if "entities" in ctx and ctx["entities"]:
                        result["interpretation"] = "PRONOUN_REFERENCE"
                        result["value"] = {"referent": ctx["entities"][-1]}
                        result["confidence"] = 0.8
                        result["strategies"].append(AmbiguityResolutionStrategy.CONTEXT_BASED.value)
                        break
        
        # 指示词消解
        elif match in ["前者", "后者", "如上", "如下"]:
            result["interpretation"] = "DEICTIC_REFERENCE"
            result["value"] = {"reference_type": match}
            result["confidence"] = 0.7
            result["strategies"].append(AmbiguityResolutionStrategy.CONTEXT_BASED.value)
        
        return result
    
    def _resolve_nested(self, expression: str, ambiguity: Dict[str, Any]) -> Dict[str, Any]:
        """消解嵌套歧义"""
        nested_types = ambiguity.get("nested_types", [])
        result = {
            "type": "NESTED_AMBIGUITY",
            "interpretation": "SEQUENTIAL_RESOLUTION",
            "confidence": 0.6,
            "strategies": [],
            "nested_resolutions": [],
        }
        
        # 按顺序消解嵌套的歧义
        for nested_type in nested_types:
            # 创建嵌套歧义信息
            nested_ambiguity = {
                "type": nested_type,
                "match": ambiguity["match"],
                "start": ambiguity["start"],
                "end": ambiguity["end"],
                "confidence": 0.7,
            }
            
            # 消解嵌套歧义
            if nested_type in self.rules:
                nested_resolution = self.rules[nested_type](expression, nested_ambiguity)
                result["nested_resolutions"].append({
                    "type": nested_type.value,
                    "resolution": nested_resolution,
                })
        
        # 计算综合置信度
        if result["nested_resolutions"]:
            confidences = [r["resolution"]["confidence"] for r in result["nested_resolutions"]]
            result["confidence"] = sum(confidences) / len(confidences)
        
        result["strategies"].append(AmbiguityResolutionStrategy.CONTEXT_BASED.value)
        
        return result
    
    def _resolve_multiple_meaning(self, expression: str, ambiguity: Dict[str, Any]) -> Dict[str, Any]:
        """消解多义歧义"""
        match = ambiguity["match"]
        result = {
            "type": "MULTIPLE_MEANING",
            "interpretation": None,
            "confidence": 0.5,
            "strategies": [],
            "possible_meanings": [],
        }
        
        # 多义字分析
        multi_meaning_words = {
            "打": ["hit", "open", "print", "calculate", "call"],
            "行": ["walk", "behavior", "row", "journey", "okay"],
            "发": ["discover", "send", "develop", "shine"],
        }
        
        # 查找多义字
        for word, meanings in multi_meaning_words.items():
            if word in match:
                result["possible_meanings"] = meanings
                
                # 基于上下文选择最可能的意思
                context = self.context.get_recent_context()
                if context:
                    for ctx in context:
                        if "topic" in ctx:
                            topic = ctx["topic"]
                            # 根据主题选择意思
                            if "计算" in topic or "数学" in topic:
                                result["interpretation"] = "calculate" if word == "打" else meanings[0]
                            elif "通信" in topic or "电话" in topic:
                                result["interpretation"] = "call" if word == "打" else meanings[0]
                            elif "运动" in topic:
                                result["interpretation"] = "hit" if word == "打" else meanings[0]
                
                # 如果没有上下文，使用第一个意思
                if not result["interpretation"]:
                    result["interpretation"] = meanings[0]
                
                result["confidence"] = 0.6
                result["strategies"].append(AmbiguityResolutionStrategy.CONTEXT_BASED.value)
                break
        
        return result
    
    def _resolve_pronoun_reference(self, expression: str, ambiguity: Dict[str, Any]) -> Dict[str, Any]:
        """消解代词指代歧义"""
        match = ambiguity["match"]
        result = {
            "type": "PRONOUN_REFERENCE",
            "interpretation": None,
            "confidence": 0.7,
            "strategies": [],
        }
        
        # 代词类型
        pronoun_types = {
            "自己": "REFLEXIVE",
            "自身": "REFLEXIVE",
            "本人": "REFLEXIVE",
            "本身": "REFLEXIVE",
            "彼此": "RECIPROCAL",
            "互相": "RECIPROCAL",
            "相互": "RECIPROCAL",
            "谁": "INTERROGATIVE",
            "什么": "INTERROGATIVE",
            "哪里": "INTERROGATIVE",
            "何时": "INTERROGATIVE",
            "如何": "INTERROGATIVE",
        }
        
        pronoun_type = pronoun_types.get(match, "PERSONAL")
        result["interpretation"] = pronoun_type
        
        # 从上下文中查找指代
        context = self.context.get_recent_context()
        if context:
            for ctx in reversed(context):
                if "subject" in ctx:
                    result["value"] = {"referent": ctx["subject"]}
                    result["confidence"] = 0.8
                    result["strategies"].append(AmbiguityResolutionStrategy.CONTEXT_BASED.value)
                    break
        
        if "value" not in result:
            result["value"] = {"referent": "未知"}
            result["confidence"] = 0.5
            result["strategies"].append(AmbiguityResolutionStrategy.FREQUENCY_BASED.value)
        
        return result
    
    def _resolve_ellipsis(self, expression: str, ambiguity: Dict[str, Any]) -> Dict[str, Any]:
        """消解省略歧义"""
        match = ambiguity["match"]
        result = {
            "type": "ELLIPSIS",
            "interpretation": None,
            "confidence": 0.6,
            "strategies": [],
        }
        
        # 省略类型
        if match in ["……", "…"]:
            result["interpretation"] = "OMISSION"
            result["value"] = {"type": "trailing_omission"}
        elif match in ["等等", "等", "之类"]:
            result["interpretation"] = "ENUMERATION_OMISSION"
            result["value"] = {"type": "enumeration_omission"}
        elif match in ["省略", "略去", "跳过"]:
            result["interpretation"] = "EXPLICIT_OMISSION"
            result["value"] = {"type": "explicit_omission"}
        
        # 从上下文中推断省略内容
        context = self.context.get_recent_context()
        if context:
            # 查找最近的列表或序列
            for ctx in reversed(context):
                if "list" in ctx or "sequence" in ctx:
                    result["confidence"] = 0.7
                    result["strategies"].append(AmbiguityResolutionStrategy.CONTEXT_BASED.value)
                    break
        
        return result
    
    def _resolve_coordination(self, expression: str, ambiguity: Dict[str, Any]) -> Dict[str, Any]:
        """消解并列结构歧义"""
        import re
        
        match = ambiguity["match"]
        result = {
            "type": "COORDINATION",
            "interpretation": None,
            "confidence": 0.7,
            "strategies": [],
            "conjuncts": [],
        }
        
        # 提取并列项
        pattern = r"([^、，]+)(?:[、，](?:和|或|与))([^、，]+)"
        m = re.search(pattern, expression)
        if m:
            conjunct1 = m.group(1).strip()
            conjunct2 = m.group(2).strip()
            result["conjuncts"] = [conjunct1, conjunct2]
            
            # 判断连接词类型
            if "和" in match or "与" in match:
                result["interpretation"] = "CONJUNCTION"
                result["value"] = {"connector": "and"}
            elif "或" in match:
                result["interpretation"] = "DISJUNCTION"
                result["value"] = {"connector": "or"}
        
        # 基于类型的策略
        if result["conjuncts"]:
            # 推断并列项的类型
            types = []
            for conjunct in result["conjuncts"]:
                type_result = self.type_inference.infer_expression_type(conjunct)
                if type_result["type"]:
                    types.append(type_result["type"])
            
            # 如果类型一致，提高置信度
            if len(set(types)) == 1:
                result["confidence"] = 0.8
                result["strategies"].append(AmbiguityResolutionStrategy.TYPE_BASED.value)
        
        return result
    
    def _resolve_modifier_attachment(self, expression: str, ambiguity: Dict[str, Any]) -> Dict[str, Any]:
        """消解修饰语附着歧义"""
        import re
        
        match = ambiguity["match"]
        result = {
            "type": "MODIFIER_ATTACHMENT",
            "interpretation": None,
            "confidence": 0.6,
            "strategies": [],
        }
        
        # 分析修饰语结构
        patterns = [
            (r"的([^的]+)(的|地|得)", "ATTRIBUTIVE_MODIFIER"),
            (r"地([^地]+)(的|地|得)", "ADVERBIAL_MODIFIER"),
            (r"得([^得]+)(的|地|得)", "COMPLEMENT_MODIFIER"),
        ]
        
        for pattern, modifier_type in patterns:
            m = re.search(pattern, match)
            if m:
                result["interpretation"] = modifier_type
                result["value"] = {
                    "modifier": m.group(1),
                    "particle": m.group(2),
                }
                break
        
        # 基于语义角色的策略
        semantic_roles = self.context.get_semantic_roles()
        if semantic_roles:
            for role in semantic_roles:
                if role["type"] in ["MODIFIER", "ATTRIBUTE"]:
                    result["confidence"] = 0.7
                    result["strategies"].append(AmbiguityResolutionStrategy.SEMANTIC_ROLE.value)
                    break
        
        return result
    
    def _resolve_default(self, expression: str, ambiguity: Dict[str, Any]) -> Dict[str, Any]:
        """默认歧义消解策略"""
        return {
            "type": "UNKNOWN",
            "interpretation": "DEFAULT_RESOLUTION",
            "confidence": 0.5,
            "strategies": [AmbiguityResolutionStrategy.CONTEXT_BASED.value],
            "value": {"expression": expression},
        }
    
    def add_user_feedback(self, ambiguity_type: AmbiguityType, expression: str, 
                         resolution: Dict[str, Any], user_confidence: float):
        """
        添加用户反馈
        
        Args:
            ambiguity_type: 歧义类型
            expression: 表达式
            resolution: 消解结果
            user_confidence: 用户置信度
        """
        feedback_key = f"{ambiguity_type.value}:{expression}"
        self.user_feedback[feedback_key] = user_confidence
        
        # 更新策略权重
        strategies_used = resolution.get("strategies", [])
        for strategy_str in strategies_used:
            try:
                strategy = AmbiguityResolutionStrategy(strategy_str)
                # 根据用户反馈调整权重
                if user_confidence > 0.7:
                    self.strategy_weights[strategy] = min(
                        self.strategy_weights[strategy] + 0.05, 0.5
                    )
                elif user_confidence < 0.3:
                    self.strategy_weights[strategy] = max(
                        self.strategy_weights[strategy] - 0.05, 0.05
                    )
            except ValueError:
                pass
    
    def get_resolution_statistics(self) -> Dict[str, Any]:
        """获取消解统计信息"""
        return self.context.get_ambiguity_statistics()


# 测试函数
def test_ambiguity_resolver():
    """测试歧义消解器"""
    print("歧义消解器测试")
    print("=" * 60)
    
    # 创建上下文跟踪器和类型推断系统
    context = SemanticContextTracker()
    type_inference = TypeInferenceSystem(context)
    resolver = AmbiguityResolver(context, type_inference)
    
    # 设置测试上下文
    context.set_topic("温度控制")
    context.add_context({
        "sentence": "温度是25度。",
        "entities": ["温度"],
        "subject": "温度",
    })
    context.add_context({
        "sentence": "风扇状态是关闭。",
        "entities": ["风扇"],
        "subject": "风扇",
    })
    
    # 测试用例
    test_cases = [
        ("温度变为30度后，风扇开启。", "时间表达式歧义"),
        ("三个用户和五个订单，计算折扣。", "量词歧义"),
        ("变为开启状态。", "主语省略歧义"),
        ("它需要调整。", "上下文依赖歧义"),
        ("张三、李四和王五，发送消息。", "并列结构歧义"),
        ("快速地运行程序。", "修饰语附着歧义"),
        ("打开发送文件。", "多义歧义"),
        ("自己完成任务。", "代词指代歧义"),
        ("苹果、香蕉……等等。", "省略歧义"),
    ]
    
    for expression, description in test_cases:
        print(f"\n测试: {description}")
        print(f"表达式: {expression}")
        
        # 检测歧义
        ambiguities = resolver.detect_ambiguity(expression)
        
        if ambiguities:
            print(f"检测到 {len(ambiguities)} 个歧义:")
            for i, ambiguity in enumerate(ambiguities, 1):
                print(f"  {i}. 类型: {ambiguity['type'].value}")
                print(f"     匹配: {ambiguity['match']}")
                print(f"     位置: {ambiguity['start']}-{ambiguity['end']}")
                print(f"     置信度: {ambiguity['confidence']:.2f}")
                
                # 消解歧义
                resolution = resolver.resolve_ambiguity(expression, ambiguity)
                print(f"     消解结果: {resolution['interpretation']}")
                print(f"     消解置信度: {resolution['confidence']:.2f}")
                print(f"     使用策略: {', '.join(resolution['strategies'])}")
        else:
            print("  未检测到歧义")
    
    # 获取统计信息
    stats = resolver.get_resolution_statistics()
    print(f"\n消解统计:")
    print(f"  总消解数: {stats['total_resolutions']}")
    print(f"  平均置信度: {stats['average_confidence']:.2f}")
    print(f"  成功率: {stats['success_rate']:.2%}")
    
    print("=" * 60)
    print("测试完成")


if __name__ == "__main__":
    test_ambiguity_resolver()