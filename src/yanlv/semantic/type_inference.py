"""
语义类型推断系统

基于上下文和语义关系进行类型推断
"""

from typing import Dict, List, Optional, Any, Set, Tuple
from enum import Enum
from dataclasses import dataclass, field
# 使用相对导入
try:
    from .context_tracker import SemanticContextTracker, SemanticType, SemanticRelation
except ImportError:
    # 用于独立测试
    from context_tracker import SemanticContextTracker, SemanticType, SemanticRelation


class InferenceRule(Enum):
    """类型推断规则枚举"""
    LITERAL_TYPE = "LITERAL_TYPE"              # 字面量类型推断
    VARIABLE_DECLARATION = "VARIABLE_DECLARATION"  # 变量声明类型推断
    FUNCTION_RETURN = "FUNCTION_RETURN"        # 函数返回类型推断
    OPERATION_RESULT = "OPERATION_RESULT"      # 操作结果类型推断
    CONTEXT_INFERENCE = "CONTEXT_INFERENCE"    # 上下文推断
    SEMANTIC_PATTERN = "SEMANTIC_PATTERN"      # 语义模式推断


@dataclass
class TypeConstraint:
    """类型约束"""
    
    variable: str                     # 变量名
    expected_type: SemanticType       # 期望类型
    confidence: float                 # 置信度 (0.0-1.0)
    source: InferenceRule             # 推断来源
    context: Dict[str, Any] = field(default_factory=dict)  # 上下文信息


class TypeInferenceSystem:
    """类型推断系统"""
    
    def __init__(self, context_tracker: SemanticContextTracker):
        """
        初始化类型推断系统
        
        Args:
            context_tracker: 语义上下文跟踪器
        """
        self.context = context_tracker
        self.type_constraints: Dict[str, List[TypeConstraint]] = {}
        self.type_hints: Dict[str, SemanticType] = {}
        self.inference_rules: Dict[InferenceRule, Any] = self._initialize_rules()
        
    def _initialize_rules(self) -> Dict[InferenceRule, Any]:
        """初始化推断规则"""
        return {
            InferenceRule.LITERAL_TYPE: self._infer_from_literal,
            InferenceRule.VARIABLE_DECLARATION: self._infer_from_declaration,
            InferenceRule.FUNCTION_RETURN: self._infer_from_function,
            InferenceRule.OPERATION_RESULT: self._infer_from_operation,
            InferenceRule.CONTEXT_INFERENCE: self._infer_from_context,
            InferenceRule.SEMANTIC_PATTERN: self._infer_from_pattern,
        }
    
    def infer_type(self, expression: str, position: Tuple[int, int]) -> Optional[SemanticType]:
        """
        推断表达式的类型
        
        Args:
            expression: 表达式文本
            position: 位置(行,列)
            
        Returns:
            推断的类型，如果无法推断返回None
        """
        # 应用所有推断规则
        constraints = self._apply_all_rules(expression, position)
        
        if not constraints:
            return None
            
        # 选择置信度最高的类型
        best_constraint = max(constraints, key=lambda c: c.confidence)
        return best_constraint.expected_type
    
    def _apply_all_rules(self, expression: str, position: Tuple[int, int]) -> List[TypeConstraint]:
        """应用所有推断规则"""
        constraints = []
        
        for rule_name, rule_func in self.inference_rules.items():
            try:
                constraint = rule_func(expression, position)
                if constraint:
                    if isinstance(constraint, list):
                        constraints.extend(constraint)
                    else:
                        constraints.append(constraint)
            except Exception as e:
                # 规则应用失败，继续下一个规则
                continue
                
        return constraints
    
    def _infer_from_literal(self, expression: str, position: Tuple[int, int]) -> Optional[TypeConstraint]:
        """从字面量推断类型"""
        expression = expression.strip()
        
        # 布尔字面量
        if expression in ["真", "假", "true", "false", "True", "False"]:
            return TypeConstraint(
                variable=expression,
                expected_type=SemanticType.STATE,
                confidence=1.0,
                source=InferenceRule.LITERAL_TYPE,
                context={"literal": expression, "type": "boolean"}
            )
        
        # 数字字面量
        if expression.replace(".", "", 1).replace("-", "", 1).isdigit():
            return TypeConstraint(
                variable=expression,
                expected_type=SemanticType.PROPERTY,
                confidence=0.9,
                source=InferenceRule.LITERAL_TYPE,
                context={"literal": expression, "type": "number"}
            )
        
        # 字符串字面量
        if (expression.startswith("'") and expression.endswith("'")) or \
           (expression.startswith('"') and expression.endswith('"')):
            content = expression[1:-1]
            
            # 根据内容进一步推断
            if content.endswith("状态"):
                expected_type = SemanticType.STATE
                confidence = 0.8
            elif content.endswith("动作"):
                expected_type = SemanticType.ACTION
                confidence = 0.8
            elif content.endswith("属性"):
                expected_type = SemanticType.PROPERTY
                confidence = 0.8
            elif "错误" in content or "异常" in content:
                expected_type = SemanticType.EVENT
                confidence = 0.7
            else:
                expected_type = SemanticType.ENTITY
                confidence = 0.6
                
            return TypeConstraint(
                variable=expression,
                expected_type=expected_type,
                confidence=confidence,
                source=InferenceRule.LITERAL_TYPE,
                context={"literal": content, "type": "string"}
            )
        
        # 中文数字
        chinese_numbers = {"零", "一", "二", "三", "四", "五", "六", "七", "八", "九", "十", "百", "千", "万"}
        if all(char in chinese_numbers for char in expression):
            return TypeConstraint(
                variable=expression,
                expected_type=SemanticType.PROPERTY,
                confidence=0.8,
                source=InferenceRule.LITERAL_TYPE,
                context={"literal": expression, "type": "chinese_number"}
            )
        
        return None
    
    def _infer_from_declaration(self, expression: str, position: Tuple[int, int]) -> Optional[TypeConstraint]:
        """从变量声明推断类型"""
        # 检查是否是变量声明语句
        declaration_patterns = [
            ("定", "是"),      # 定x是值
            ("定", "等于"),    # 定x等于值
            ("设", "是"),      # 设x是值
            ("设", "等于"),    # 设x等于值
        ]
        
        for prefix, infix in declaration_patterns:
            if expression.startswith(prefix) and infix in expression:
                # 提取变量名和值
                parts = expression[len(prefix):].split(infix, 1)
                if len(parts) == 2:
                    var_name = parts[0].strip()
                    value_expr = parts[1].strip().rstrip("。")
                    
                    # 推断值的类型
                    value_type = self.infer_type(value_expr, position)
                    if value_type:
                        return TypeConstraint(
                            variable=var_name,
                            expected_type=value_type,
                            confidence=0.9,
                            source=InferenceRule.VARIABLE_DECLARATION,
                            context={"prefix": prefix, "infix": infix, "value": value_expr}
                        )
        
        return None
    
    def _infer_from_function(self, expression: str, position: Tuple[int, int]) -> Optional[TypeConstraint]:
        """从函数调用推断类型"""
        # 检查是否是函数调用
        if "，" in expression and "。" in expression:
            # 可能是意合式函数调用: 参数，函数名。
            parts = expression.split("，")
            if len(parts) >= 2:
                func_name = parts[-1].strip().rstrip("。")
                
                # 检查函数是否已注册
                func_sig = self.context.get_function_signature(func_name)
                if func_sig:
                    return TypeConstraint(
                        variable=expression,
                        expected_type=func_sig["return_type"],
                        confidence=0.8,
                        source=InferenceRule.FUNCTION_RETURN,
                        context={"function": func_name, "signature": func_sig}
                    )
        
        return None
    
    def _infer_from_operation(self, expression: str, position: Tuple[int, int]) -> Optional[TypeConstraint]:
        """从操作推断类型"""
        # 算术操作
        arithmetic_ops = ["加", "减", "乘", "除", "模", "幂"]
        for op in arithmetic_ops:
            if op in expression:
                return TypeConstraint(
                    variable=expression,
                    expected_type=SemanticType.PROPERTY,
                    confidence=0.7,
                    source=InferenceRule.OPERATION_RESULT,
                    context={"operation": op, "type": "arithmetic"}
                )
        
        # 比较操作
        comparison_ops = ["大", "小", "等", "不等", "大于", "小于", "等于", "不等于"]
        for op in comparison_ops:
            if op in expression:
                return TypeConstraint(
                    variable=expression,
                    expected_type=SemanticType.STATE,
                    confidence=0.8,
                    source=InferenceRule.OPERATION_RESULT,
                    context={"operation": op, "type": "comparison"}
                )
        
        # 逻辑操作
        logic_ops = ["且", "或", "非", "并且", "或者", "不是"]
        for op in logic_ops:
            if op in expression:
                return TypeConstraint(
                    variable=expression,
                    expected_type=SemanticType.STATE,
                    confidence=0.8,
                    source=InferenceRule.OPERATION_RESULT,
                    context={"operation": op, "type": "logic"}
                )
        
        return None
    
    def _infer_from_context(self, expression: str, position: Tuple[int, int]) -> Optional[TypeConstraint]:
        """从上下文推断类型"""
        # 获取当前主题
        current_topic = self.context.get_topic()
        if not current_topic:
            return None
        
        # 根据主题推断类型
        topic_lower = current_topic.lower()
        
        if any(word in topic_lower for word in ["温度", "湿度", "压力", "速度", "距离"]):
            # 物理量相关主题
            return TypeConstraint(
                variable=expression,
                expected_type=SemanticType.PROPERTY,
                confidence=0.6,
                source=InferenceRule.CONTEXT_INFERENCE,
                context={"topic": current_topic, "category": "physical_quantity"}
            )
        
        elif any(word in topic_lower for word in ["状态", "模式", "开关", "开启", "关闭"]):
            # 状态相关主题
            return TypeConstraint(
                variable=expression,
                expected_type=SemanticType.STATE,
                confidence=0.7,
                source=InferenceRule.CONTEXT_INFERENCE,
                context={"topic": current_topic, "category": "state"}
            )
        
        elif any(word in topic_lower for word in ["动作", "操作", "执行", "运行"]):
            # 动作相关主题
            return TypeConstraint(
                variable=expression,
                expected_type=SemanticType.ACTION,
                confidence=0.7,
                source=InferenceRule.CONTEXT_INFERENCE,
                context={"topic": current_topic, "category": "action"}
            )
        
        elif any(word in topic_lower for word in ["用户", "设备", "系统", "对象"]):
            # 实体相关主题
            return TypeConstraint(
                variable=expression,
                expected_type=SemanticType.ENTITY,
                confidence=0.6,
                source=InferenceRule.CONTEXT_INFERENCE,
                context={"topic": current_topic, "category": "entity"}
            )
        
        return None
    
    def _infer_from_pattern(self, expression: str, position: Tuple[int, int]) -> Optional[TypeConstraint]:
        """从语义模式推断类型"""
        # 状态转换模式: X变为Y
        if "变为" in expression or "变成" in expression or "转为" in expression:
            return TypeConstraint(
                variable=expression,
                expected_type=SemanticType.EVENT,
                confidence=0.8,
                source=InferenceRule.SEMANTIC_PATTERN,
                context={"pattern": "state_transition"}
            )
        
        # 条件判断模式: 如果X就Y
        if "如果" in expression or "要是" in expression:
            if "就" in expression:
                return TypeConstraint(
                    variable=expression,
                    expected_type=SemanticType.RELATION,
                    confidence=0.7,
                    source=InferenceRule.SEMANTIC_PATTERN,
                    context={"pattern": "conditional"}
                )
        
        # 循环模式: 对于X在Y
        if "对于" in expression and "在" in expression:
            return TypeConstraint(
                variable=expression,
                expected_type=SemanticType.RELATION,
                confidence=0.7,
                source=InferenceRule.SEMANTIC_PATTERN,
                context={"pattern": "loop"}
            )
        
        # 函数定义模式: 定X是函Y
        if "定" in expression and "是函" in expression:
            return TypeConstraint(
                variable=expression,
                expected_type=SemanticType.ACTION,
                confidence=0.8,
                source=InferenceRule.SEMANTIC_PATTERN,
                context={"pattern": "function_definition"}
            )
        
        return None
    
    def add_type_constraint(self, constraint: TypeConstraint) -> None:
        """添加类型约束"""
        if constraint.variable not in self.type_constraints:
            self.type_constraints[constraint.variable] = []
        self.type_constraints[constraint.variable].append(constraint)
        
        # 更新类型提示
        self._update_type_hints(constraint.variable)
    
    def _update_type_hints(self, variable: str) -> None:
        """更新类型提示"""
        if variable not in self.type_constraints:
            return
            
        constraints = self.type_constraints[variable]
        
        # 计算每个类型的平均置信度
        type_scores: Dict[SemanticType, List[float]] = {}
        for constraint in constraints:
            if constraint.expected_type not in type_scores:
                type_scores[constraint.expected_type] = []
            type_scores[constraint.expected_type].append(constraint.confidence)
        
        # 选择平均置信度最高的类型
        best_type = None
        best_score = -1.0
        
        for type_, scores in type_scores.items():
            avg_score = sum(scores) / len(scores)
            if avg_score > best_score:
                best_score = avg_score
                best_type = type_
        
        if best_type and best_score >= 0.5:  # 置信度阈值
            self.type_hints[variable] = best_type
    
    def get_type_hint(self, variable: str) -> Optional[SemanticType]:
        """获取类型提示"""
        return self.type_hints.get(variable)
    
    def get_all_constraints(self, variable: str) -> List[TypeConstraint]:
        """获取变量的所有类型约束"""
        return self.type_constraints.get(variable, [])
    
    def clear_constraints(self, variable: str = None) -> None:
        """清除类型约束"""
        if variable is None:
            self.type_constraints.clear()
            self.type_hints.clear()
        elif variable in self.type_constraints:
            del self.type_constraints[variable]
            if variable in self.type_hints:
                del self.type_hints[variable]
    
    def infer_expression_type(self, expression: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        推断表达式的类型（高级接口）
        
        Args:
            expression: 表达式
            context: 上下文信息
            
        Returns:
            类型推断结果
        """
        if context is None:
            context = {}
            
        position = context.get("position", (0, 0))
        
        # 应用所有推断规则
        constraints = self._apply_all_rules(expression, position)
        
        if not constraints:
            return {
                "expression": expression,
                "type": None,
                "confidence": 0.0,
                "constraints": [],
                "suggestions": []
            }
        
        # 按类型分组
        type_groups: Dict[SemanticType, List[TypeConstraint]] = {}
        for constraint in constraints:
            if constraint.expected_type not in type_groups:
                type_groups[constraint.expected_type] = []
            type_groups[constraint.expected_type].append(constraint)
        
        # 计算每个类型的总置信度
        type_scores = []
        for type_, type_constraints in type_groups.items():
            total_confidence = sum(c.confidence for c in type_constraints)
            avg_confidence = total_confidence / len(type_constraints)
            type_scores.append((type_, avg_confidence, type_constraints))
        
        # 按置信度排序
        type_scores.sort(key=lambda x: x[1], reverse=True)
        
        # 生成建议
        suggestions = []
        for i, (type_, confidence, constraints_list) in enumerate(type_scores[:3]):  # 取前3个
            rule_sources = [c.source.value for c in constraints_list]
            suggestions.append({
                "type": type_.value,
                "confidence": confidence,
                "sources": list(set(rule_sources)),
                "constraint_count": len(constraints_list)
            })
        
        best_type, best_confidence, best_constraints = type_scores[0] if type_scores else (None, 0.0, [])
        
        return {
            "expression": expression,
            "type": best_type.value if best_type else None,
            "confidence": best_confidence,
            "constraints": [{
                "source": c.source.value,
                "confidence": c.confidence,
                "context": c.context
            } for c in best_constraints],
            "suggestions": suggestions
        }


# 测试函数
def test_type_inference_system():
    """测试类型推断系统"""
    print("类型推断系统测试")
    print("=" * 50)
    
    # 创建上下文跟踪器
    from .context_tracker import SemanticContextTracker
    context = SemanticContextTracker()
    
    # 创建类型推断系统
    inference_system = TypeInferenceSystem(context)
    
    # 测试1: 字面量类型推断
    print("测试1: 字面量类型推断")
    test_cases = [
        ("真", SemanticType.STATE),
        ("25", SemanticType.PROPERTY),
        ("'开启状态'", SemanticType.STATE),
        ("'用户动作'", SemanticType.ACTION),
        ("'温度属性'", SemanticType.PROPERTY),
        ("'系统错误'", SemanticType.EVENT),
        ("'普通字符串'", SemanticType.ENTITY),
        ("二十五", SemanticType.PROPERTY),
    ]
    
    for expr, expected_type in test_cases:
        result = inference_system.infer_expression_type(expr)
        inferred_type = SemanticType(result["type"]) if result["type"] else None
        print(f"  {expr:15} -> {inferred_type.value if inferred_type else 'None':15} "
              f"(期望: {expected_type.value}, 置信度: {result['confidence']:.2f})")
    print()
    
    # 测试2: 变量声明推断
    print("测试2: 变量声明推断")
    context.set_topic("温度控制")
    
    test_cases = [
        ("定温度是25", SemanticType.PROPERTY),
        ("设状态等于真", SemanticType.STATE),
        ("定动作为'开启'", SemanticType.ACTION),
    ]
    
    for expr, expected_type in test_cases:
        result = inference_system.infer_expression_type(expr)
        inferred_type = SemanticType(result["type"]) if result["type"] else None
        print(f"  {expr:20} -> {inferred_type.value if inferred_type else 'None':15} "
              f"(期望: {expected_type.value}, 置信度: {result['confidence']:.2f})")
    print()
    
    # 测试3: 操作推断
    print("测试3: 操作推断")
    test_cases = [
        ("温度加5", SemanticType.PROPERTY),
        ("x大y", SemanticType.STATE),
        ("条件1且条件2", SemanticType.STATE),
    ]
    
    for expr, expected_type in test_cases:
        result = inference_system.infer_expression_type(expr)
        inferred_type = SemanticType(result["type"]) if result["type"] else None
        print(f"  {expr:20} -> {inferred_type.value if inferred_type else 'None':15} "
              f"(期望: {expected_type.value}, 置信度: {result['confidence']:.2f})")
    print()
    
    # 测试4: 上下文推断
    print("测试4: 上下文推断")
    
    # 设置不同主题
    contexts = [
        ("温度监控", "当前温度", SemanticType.PROPERTY),
        ("系统状态", "运行状态", SemanticType.STATE),
        ("用户操作", "点击按钮", SemanticType.ACTION),
        ("设备管理", "服务器", SemanticType.ENTITY),
    ]
    
    for topic, expr, expected_type in contexts:
        context.set_topic(topic)
        result = inference_system.infer_expression_type(expr)
        inferred_type = SemanticType(result["type"]) if result["type"] else None
        print(f"  主题: {topic:15}, 表达式: {expr:15} -> "
              f"{inferred_type.value if inferred_type else 'None':15} "
              f"(期望: {expected_type.value}, 置信度: {result['confidence']:.2f})")
    print()
    
    # 测试5: 语义模式推断
    print("测试5: 语义模式推断")
    test_cases = [
        ("温度变为30度", SemanticType.EVENT),
        ("如果温度高就开风扇", SemanticType.RELATION),
        ("对于i在1到10", SemanticType.RELATION),
        ("定计算是函x", SemanticType.ACTION),
    ]
    
    for expr, expected_type in test_cases:
        result = inference_system.infer_expression_type(expr)
        inferred_type = SemanticType(result["type"]) if result["type"] else None
        print(f"  {expr:25} -> {inferred_type.value if inferred_type else 'None':15} "
              f"(期望: {expected_type.value}, 置信度: {result['confidence']:.2f})")
    print()
    
    # 测试6: 类型约束管理
    print("测试6: 类型约束管理")
    
    # 添加类型约束
    constraint1 = TypeConstraint(
        variable="温度",
        expected_type=SemanticType.PROPERTY,
        confidence=0.9,
        source=InferenceRule.LITERAL_TYPE,
        context={"value": 25}
    )
    
    constraint2 = TypeConstraint(
        variable="温度",
        expected_type=SemanticType.PROPERTY,
        confidence=0.8,
        source=InferenceRule.CONTEXT_INFERENCE,
        context={"topic": "温度控制"}
    )
    
    inference_system.add_type_constraint(constraint1)
    inference_system.add_type_constraint(constraint2)
    
    # 获取类型提示
    type_hint = inference_system.get_type_hint("温度")
    print(f"  变量'温度'的类型提示: {type_hint.value if type_hint else 'None'}")
    
    # 获取所有约束
    constraints = inference_system.get_all_constraints("温度")
    print(f"  变量'温度'的约束数量: {len(constraints)}")
    for i, c in enumerate(constraints, 1):
        print(f"    约束{i}: {c.source.value} (置信度: {c.confidence:.2f})")
    
    # 清除约束
    inference_system.clear_constraints("温度")
    type_hint_after = inference_system.get_type_hint("温度")
    print(f"  清除后类型提示: {type_hint_after.value if type_hint_after else 'None'}")
    print()
    
    # 测试7: 复杂表达式推断
    print("测试7: 复杂表达式推断")
    complex_expr = "定结果等于温度加5，如果结果大30就'高温警告'"
    
    # 分步推断
    parts = [
        ("温度加5", SemanticType.PROPERTY),
        ("结果大30", SemanticType.STATE),
        ("'高温警告'", SemanticType.EVENT),
    ]
    
    for expr, expected_type in parts:
        result = inference_system.infer_expression_type(expr)
        inferred_type = SemanticType(result["type"]) if result["type"] else None
        print(f"  {expr:20} -> {inferred_type.value if inferred_type else 'None':15} "
              f"(期望: {expected_type.value}, 置信度: {result['confidence']:.2f})")
    
    print("=" * 50)
    print("测试完成")


if __name__ == "__main__":
    test_type_inference_system()