"""
言律语言动词分类词典

基于语言规范定义的动词分类和元数系统
"""

from typing import Dict, List, Set, Tuple, Optional
from enum import Enum


# ============================================================================
# 动词分类枚举
# ============================================================================

class VerbCategory(Enum):
    """动词分类"""
    STATE_TRANSITION = "STATE_TRANSITION"      # 状态转换
    ASSIGNMENT = "ASSIGNMENT"                  # 赋值
    OUTPUT = "OUTPUT"                          # 输出
    INPUT = "INPUT"                            # 输入
    CONTROL = "CONTROL"                        # 控制
    ARITHMETIC = "ARITHMETIC"                  # 算术
    COMPARISON = "COMPARISON"                  # 比较
    LOGICAL = "LOGICAL"                        # 逻辑
    LIST_OPERATION = "LIST_OPERATION"          # 列表操作
    FUNCTION = "FUNCTION"                      # 函数
    LOOP = "LOOP"                              # 循环
    CONDITION = "CONDITION"                    # 条件
    IO = "IO"                                  # 输入输出


# ============================================================================
# 动词分类词典
# ============================================================================

VERB_CATEGORIES: Dict[str, VerbCategory] = {
    # 状态转换动词
    "变为": VerbCategory.STATE_TRANSITION,
    "变成": VerbCategory.STATE_TRANSITION,
    "转为": VerbCategory.STATE_TRANSITION,
    "切换": VerbCategory.STATE_TRANSITION,
    "改变": VerbCategory.STATE_TRANSITION,
    
    # 赋值动词
    "等于": VerbCategory.ASSIGNMENT,
    "设为": VerbCategory.ASSIGNMENT,
    "赋值": VerbCategory.ASSIGNMENT,
    "是": VerbCategory.ASSIGNMENT,
    "为": VerbCategory.ASSIGNMENT,
    
    # 输出动词
    "印": VerbCategory.OUTPUT,
    "输出": VerbCategory.OUTPUT,
    "打印": VerbCategory.OUTPUT,
    "显示": VerbCategory.OUTPUT,
    "写出": VerbCategory.OUTPUT,
    
    # 输入动词
    "读": VerbCategory.INPUT,
    "输入": VerbCategory.INPUT,
    "读取": VerbCategory.INPUT,
    "获取": VerbCategory.INPUT,
    "接收": VerbCategory.INPUT,
    
    # 控制动词
    "开启": VerbCategory.CONTROL,
    "关闭": VerbCategory.CONTROL,
    "启动": VerbCategory.CONTROL,
    "停止": VerbCategory.CONTROL,
    "暂停": VerbCategory.CONTROL,
    "继续": VerbCategory.CONTROL,
    
    # 算术动词
    "加": VerbCategory.ARITHMETIC,
    "减": VerbCategory.ARITHMETIC,
    "乘": VerbCategory.ARITHMETIC,
    "除": VerbCategory.ARITHMETIC,
    "模": VerbCategory.ARITHMETIC,
    "幂": VerbCategory.ARITHMETIC,
    "负": VerbCategory.ARITHMETIC,
    "绝对": VerbCategory.ARITHMETIC,
    
    # 比较动词
    "大": VerbCategory.COMPARISON,
    "小": VerbCategory.COMPARISON,
    "等": VerbCategory.COMPARISON,
    "不等": VerbCategory.COMPARISON,
    "大于": VerbCategory.COMPARISON,
    "小于": VerbCategory.COMPARISON,
    "等于": VerbCategory.COMPARISON,
    "不等于": VerbCategory.COMPARISON,
    
    # 逻辑动词
    "且": VerbCategory.LOGICAL,
    "或": VerbCategory.LOGICAL,
    "非": VerbCategory.LOGICAL,
    "并且": VerbCategory.LOGICAL,
    "或者": VerbCategory.LOGICAL,
    "取反": VerbCategory.LOGICAL,
    
    # 列表操作动词
    "列": VerbCategory.LIST_OPERATION,
    "首": VerbCategory.LIST_OPERATION,
    "余": VerbCategory.LIST_OPERATION,
    "入": VerbCategory.LIST_OPERATION,
    "长": VerbCategory.LIST_OPERATION,
    "添": VerbCategory.LIST_OPERATION,
    "连": VerbCategory.LIST_OPERATION,
    "含": VerbCategory.LIST_OPERATION,
    "排序": VerbCategory.LIST_OPERATION,
    "反转": VerbCategory.LIST_OPERATION,
    
    # 函数动词
    "定": VerbCategory.FUNCTION,
    "定义": VerbCategory.FUNCTION,
    "调用": VerbCategory.FUNCTION,
    "返回": VerbCategory.FUNCTION,
    "函": VerbCategory.FUNCTION,
    
    # 循环动词
    "对于": VerbCategory.LOOP,
    "遍历": VerbCategory.LOOP,
    "循环": VerbCategory.LOOP,
    "重复": VerbCategory.LOOP,
    "直到": VerbCategory.LOOP,
    
    # 条件动词
    "若": VerbCategory.CONDITION,
    "如果": VerbCategory.CONDITION,
    "当": VerbCategory.CONDITION,
    "只要": VerbCategory.CONDITION,
    "一旦": VerbCategory.CONDITION,
    "否则": VerbCategory.CONDITION,
    
    # IO动词
    "写": VerbCategory.IO,
    "读文件": VerbCategory.IO,
    "写文件": VerbCategory.IO,
}


# ============================================================================
# 动词元数定义
# ============================================================================

VERB_ARITY: Dict[str, int] = {
    # 算术运算 (二元)
    "加": 2, "减": 2, "乘": 2, "除": 2, "模": 2, "幂": 2,
    "负": 1, "绝对": 1,
    
    # 比较运算 (二元)
    "大": 2, "小": 2, "等": 2, "不等": 2,
    "大于": 2, "小于": 2, "等于": 2, "不等于": 2,
    
    # 逻辑运算
    "且": 2, "或": 2, "非": 1,
    "并且": 2, "或者": 2, "取反": 1,
    
    # 列表操作
    "列": -1,  # 可变参数
    "首": 1, "余": 1, "入": 2, "长": 1, "添": 2, "连": 2, "含": 2,
    "排序": 1, "反转": 1,
    
    # 高阶函数
    "皆": 2, "只": 2, "归": 3,
    
    # I/O操作
    "印": 1, "读": 1, "写": 2, "行": 1,
    "输出": 1, "输入": 1, "打印": 1, "显示": 1,
    
    # 赋值
    "等于": 2, "设为": 2, "赋值": 2, "是": 2, "为": 2,
    
    # 状态转换
    "变为": 2, "变成": 2, "转为": 2, "切换": 2, "改变": 2,
    
    # 控制
    "开启": 1, "关闭": 1, "启动": 1, "停止": 1, "暂停": 1, "继续": 1,
}


# ============================================================================
# 语义角色定义
# ============================================================================

class SemanticRole(Enum):
    """语义角色"""
    AGENT = "AGENT"           # 施事者
    PATIENT = "PATIENT"       # 受事者
    THEME = "THEME"           # 主题
    GOAL = "GOAL"             # 目标
    SOURCE = "SOURCE"         # 来源
    INSTRUMENT = "INSTRUMENT" # 工具
    LOCATION = "LOCATION"     # 位置
    TIME = "TIME"             # 时间
    MANNER = "MANNER"         # 方式
    CAUSE = "CAUSE"           # 原因
    RESULT = "RESULT"         # 结果


# ============================================================================
# 动词语义角色映射
# ============================================================================

VERB_SEMANTIC_ROLES: Dict[str, List[SemanticRole]] = {
    # 状态转换: 施事者 + 目标状态
    "变为": [SemanticRole.AGENT, SemanticRole.GOAL],
    "变成": [SemanticRole.AGENT, SemanticRole.GOAL],
    "转为": [SemanticRole.AGENT, SemanticRole.GOAL],
    
    # 赋值: 主题 + 值
    "等于": [SemanticRole.THEME, SemanticRole.RESULT],
    "设为": [SemanticRole.THEME, SemanticRole.RESULT],
    "是": [SemanticRole.THEME, SemanticRole.RESULT],
    
    # 输出: 主题
    "印": [SemanticRole.THEME],
    "输出": [SemanticRole.THEME],
    "打印": [SemanticRole.THEME],
    
    # 输入: 目标
    "读": [SemanticRole.GOAL],
    "输入": [SemanticRole.GOAL],
    
    # 算术: 操作数1 + 操作数2
    "加": [SemanticRole.THEME, SemanticRole.INSTRUMENT],
    "减": [SemanticRole.THEME, SemanticRole.INSTRUMENT],
    "乘": [SemanticRole.THEME, SemanticRole.INSTRUMENT],
    "除": [SemanticRole.THEME, SemanticRole.INSTRUMENT],
}


# ============================================================================
# 辅助函数
# ============================================================================

def get_verb_category(verb: str) -> Optional[VerbCategory]:
    """获取动词的分类"""
    return VERB_CATEGORIES.get(verb)


def get_verb_arity(verb: str) -> int:
    """获取动词的元数，默认为1"""
    return VERB_ARITY.get(verb, 1)


def get_semantic_role(verb: str, position: int) -> Optional[SemanticRole]:
    """获取动词在指定位置的语义角色"""
    roles = VERB_SEMANTIC_ROLES.get(verb, [])
    if 0 <= position < len(roles):
        return roles[position]
    return None


def get_verb_interpretation(verb: str) -> Dict[str, any]:
    """获取动词的完整解释"""
    return {
        "verb": verb,
        "category": get_verb_category(verb),
        "arity": get_verb_arity(verb),
        "semantic_roles": VERB_SEMANTIC_ROLES.get(verb, []),
    }


def get_all_verbs() -> Set[str]:
    """获取所有动词集合"""
    return set(VERB_CATEGORIES.keys())


def get_verbs_by_category(category: VerbCategory) -> List[str]:
    """获取指定分类的所有动词"""
    return [verb for verb, cat in VERB_CATEGORIES.items() if cat == category]


def get_category_by_verb(verb: str) -> Optional[str]:
    """根据动词获取分类名称"""
    category = get_verb_category(verb)
    return category.value if category else None


# ============================================================================
# 动词歧义消解
# ============================================================================

def resolve_verb_ambiguity(verb: str, context: Dict[str, any]) -> str:
    """
    根据上下文消解动词歧义

    Args:
        verb: 动词
        context: 上下文信息

    Returns:
        消解后的动词解释
    """
    # 获取动词的基本信息
    interpretation = get_verb_interpretation(verb)

    # 多义动词消解字典
    multi_meaning_verbs = {
        "打": {
            "contexts": {
                "计算": "calculate",
                "数学": "calculate",
                "运算": "calculate",
                "电话": "call",
                "通信": "call",
                "联系": "call",
                "开": "open",
                "门": "open",
                "文件": "open",
                "印": "print",
                "输出": "print",
                "显示": "print",
                "运动": "hit",
                "击": "hit",
                "球": "hit",
            },
            "default": "hit"
        },
        "行": {
            "contexts": {
                "走": "walk",
                "移动": "walk",
                "运动": "walk",
                "为": "behavior",
                "做法": "behavior",
                "列": "row",
                "表格": "row",
                "程": "journey",
                "旅途": "journey",
                "可以": "okay",
                "能": "okay",
            },
            "default": "walk"
        },
        "发": {
            "contexts": {
                "现": "discover",
                "找到": "discover",
                "送": "send",
                "传输": "send",
                "消息": "send",
                "展": "develop",
                "开发": "develop",
                "光": "shine",
                "亮": "shine",
            },
            "default": "send"
        },
        "开": {
            "contexts": {
                "开启": "open",
                "打开": "open",
                "门": "open",
                "文件": "open",
                "开始": "start",
                "启动": "start",
                "开发": "develop",
                "展开": "develop",
            },
            "default": "open"
        },
        "关": {
            "contexts": {
                "闭": "close",
                "门": "close",
                "文件": "close",
                "联": "relate",
                "相关": "relate",
                "于": "about",
                "关于": "about",
            },
            "default": "close"
        },
        "设": {
            "contexts": {
                "置": "set",
                "配置": "set",
                "定": "define",
                "定义": "define",
                "计": "design",
                "设计": "design",
            },
            "default": "set"
        },
    }

    # 检查是否是多义动词
    if verb in multi_meaning_verbs:
        verb_info = multi_meaning_verbs[verb]

        # 从上下文中获取相关信息
        context_text = context.get("text", "")
        topic = context.get("topic", "")
        recent_words = context.get("recent_words", [])

        # 组合所有上下文信息
        all_context = f"{context_text} {topic} {' '.join(recent_words)}"

        # 匹配上下文关键词
        best_match = None
        best_score = 0

        for keyword, meaning in verb_info["contexts"].items():
            if keyword in all_context:
                # 计算匹配分数（关键词长度作为权重）
                score = len(keyword)
                if score > best_score:
                    best_score = score
                    best_match = meaning

        # 如果找到匹配，返回对应含义
        if best_match:
            interpretation["resolved_meaning"] = best_match
            interpretation["confidence"] = min(0.5 + best_score * 0.1, 0.95)
        else:
            # 使用默认含义
            interpretation["resolved_meaning"] = verb_info["default"]
            interpretation["confidence"] = 0.5

    # 根据动词分类调整解释
    category = interpretation.get("category")
    if category:
        # 基于分类的置信度调整
        if category in [VerbCategory.TRANSFORMATION, VerbCategory.COMMUNICATION]:
            interpretation["confidence"] = interpretation.get("confidence", 0.7) * 1.1
        elif category in [VerbCategory.MOVEMENT, VerbCategory.PERCEPTION]:
            interpretation["confidence"] = interpretation.get("confidence", 0.7) * 1.05

    # 确保置信度在合理范围
    interpretation["confidence"] = min(interpretation.get("confidence", 0.7), 0.95)

    return interpretation
    
    return interpretation


# ============================================================================
# 导出
# ============================================================================

__all__ = [
    'VerbCategory',
    'SemanticRole',
    'VERB_CATEGORIES',
    'VERB_ARITY',
    'VERB_SEMANTIC_ROLES',
    'get_verb_category',
    'get_verb_arity',
    'get_semantic_role',
    'get_verb_interpretation',
    'get_all_verbs',
    'get_verbs_by_category',
    'get_category_by_verb',
    'resolve_verb_ambiguity',
]
