"""
言律语言动词分类词典

扩展的动词分类词典，包含13个类别，119个动词
每个类别包含语义角色标注
"""

from typing import Dict, List, Tuple, Any
from enum import Enum


class SemanticRole(Enum):
    """语义角色枚举"""
    CHANGE_OF_STATE = "CHANGE_OF_STATE"          # 状态变化
    VALUE_ASSIGNMENT = "VALUE_ASSIGNMENT"        # 值赋值
    DATA_OUTPUT = "DATA_OUTPUT"                  # 数据输出
    DEVICE_CONTROL = "DEVICE_CONTROL"            # 设备控制
    DATA_PROCESSING = "DATA_PROCESSING"          # 数据处理
    SPATIAL_MOVEMENT = "SPATIAL_MOVEMENT"        # 空间移动
    OBJECT_CREATION = "OBJECT_CREATION"          # 对象创建
    OBJECT_DESTRUCTION = "OBJECT_DESTRUCTION"    # 对象销毁
    DATA_RETRIEVAL = "DATA_RETRIEVAL"            # 数据检索
    DATA_MODIFICATION = "DATA_MODIFICATION"      # 数据修改
    COMMUNICATION = "COMMUNICATION"              # 通信
    COMPARISON = "COMPARISON"                    # 比较
    TRANSFORMATION = "TRANSFORMATION"            # 转换


class VerbCategory(Enum):
    """动词类别枚举"""
    STATE_TRANSITION = "STATE_TRANSITION"        # 状态转换
    ASSIGNMENT = "ASSIGNMENT"                    # 赋值
    OUTPUT = "OUTPUT"                            # 输出
    CONTROL = "CONTROL"                          # 控制
    COMPUTATION = "COMPUTATION"                  # 计算
    MOVEMENT = "MOVEMENT"                        # 移动
    CREATION = "CREATION"                        # 创建
    DESTRUCTION = "DESTRUCTION"                  # 销毁
    QUERY = "QUERY"                              # 查询
    MODIFICATION = "MODIFICATION"                # 修改
    COMMUNICATION = "COMMUNICATION"              # 通信
    COMPARISON = "COMPARISON"                    # 比较
    TRANSFORMATION = "TRANSFORMATION"            # 转换


# 扩展的动词分类词典 (13个类别，119个动词)
VERB_CATEGORIES: Dict[str, Dict[str, Any]] = {
    # 状态转换动词 (9个)
    VerbCategory.STATE_TRANSITION.value: {
        "verbs": ["变为", "变成", "转为", "切换为", "转换为", "变化为", "转成", "改成", "调整为"],
        "pattern": r'^[^变为]+变为[^。]+[。]$',
        "interpretation": "STATE_TRANSITION",
        "semantic_role": SemanticRole.CHANGE_OF_STATE.value,
        "arity": 2,  # 主语 + 新状态
        "examples": [
            "温度变为30度。",
            "状态切换为开启。",
            "颜色调整为红色。"
        ]
    },
    
    # 赋值动词 (9个)
    VerbCategory.ASSIGNMENT.value: {
        "verbs": ["等于", "设为", "设置为", "赋值为", "=", "是", "定义为", "指定为", "赋给"],
        "pattern": r'^[^等于]+等于[^。]+[。]$',
        "interpretation": "ASSIGNMENT",
        "semantic_role": SemanticRole.VALUE_ASSIGNMENT.value,
        "arity": 2,  # 变量 + 值
        "examples": [
            "x等于10。",
            "名称设为张三。",
            "结果赋值为真。"
        ]
    },
    
    # 输出动词 (10个)
    VerbCategory.OUTPUT.value: {
        "verbs": ["印", "打印", "显示", "输出", "记录", "输出为", "展示", "呈现", "打印出", "显示为"],
        "pattern": r'^印[^。]+[。]$',
        "interpretation": "OUTPUT_STATEMENT",
        "semantic_role": SemanticRole.DATA_OUTPUT.value,
        "arity": 1,  # 输出内容
        "examples": [
            "印'你好，世界'。",
            "显示结果。",
            "记录日志。"
        ]
    },
    
    # 控制动词 (10个)
    VerbCategory.CONTROL.value: {
        "verbs": ["开启", "关闭", "启动", "停止", "执行", "运行", "暂停", "继续", "重启", "终止"],
        "pattern": r'^[^开启]+开启[^。]*[。]$',
        "interpretation": "CONTROL_STATEMENT",
        "semantic_role": SemanticRole.DEVICE_CONTROL.value,
        "arity": 1,  # 控制对象
        "examples": [
            "开启风扇。",
            "停止程序。",
            "执行任务。"
        ]
    },
    
    # 计算动词 (10个)
    VerbCategory.COMPUTATION.value: {
        "verbs": ["计算", "求和", "求积", "比较", "排序", "过滤", "映射", "归约", "统计", "分析"],
        "pattern": r'^计算[^。]+[。]$',
        "interpretation": "COMPUTATION",
        "semantic_role": SemanticRole.DATA_PROCESSING.value,
        "arity": -1,  # 可变参数
        "examples": [
            "计算总和。",
            "排序列表。",
            "分析数据。"
        ]
    },
    
    # 移动动词 (10个)
    VerbCategory.MOVEMENT.value: {
        "verbs": ["移动", "前进", "后退", "旋转", "转向", "跳跃", "飞行", "行走", "跑动", "滑动"],
        "pattern": r'^[^移动]+移动[^。]*[。]$',
        "interpretation": "MOVEMENT_ACTION",
        "semantic_role": SemanticRole.SPATIAL_MOVEMENT.value,
        "arity": 1,  # 移动对象
        "examples": [
            "移动物体。",
            "前进10米。",
            "旋转90度。"
        ]
    },
    
    # 创建动词 (10个)
    VerbCategory.CREATION.value: {
        "verbs": ["创建", "生成", "建立", "构造", "初始化", "新建", "产生", "制造", "组建", "设立"],
        "pattern": r'^创建[^。]+[。]$',
        "interpretation": "CREATION_ACTION",
        "semantic_role": SemanticRole.OBJECT_CREATION.value,
        "arity": 1,  # 创建对象
        "examples": [
            "创建文件。",
            "生成报告。",
            "建立连接。"
        ]
    },
    
    # 销毁动词 (10个)
    VerbCategory.DESTRUCTION.value: {
        "verbs": ["删除", "销毁", "清除", "移除", "释放", "消灭", "拆除", "丢弃", "废除", "撤销"],
        "pattern": r'^删除[^。]+[。]$',
        "interpretation": "DESTRUCTION_ACTION",
        "semantic_role": SemanticRole.OBJECT_DESTRUCTION.value,
        "arity": 1,  # 销毁对象
        "examples": [
            "删除文件。",
            "清除缓存。",
            "释放内存。"
        ]
    },
    
    # 查询动词 (10个)
    VerbCategory.QUERY.value: {
        "verbs": ["查询", "搜索", "查找", "获取", "读取", "检索", "查找", "搜索", "获取", "读取"],
        "pattern": r'^查询[^。]+[。]$',
        "interpretation": "QUERY_ACTION",
        "semantic_role": SemanticRole.DATA_RETRIEVAL.value,
        "arity": 1,  # 查询目标
        "examples": [
            "查询用户。",
            "搜索文件。",
            "获取数据。"
        ]
    },
    
    # 修改动词 (10个)
    VerbCategory.MODIFICATION.value: {
        "verbs": ["修改", "更新", "编辑", "调整", "改变", "修正", "变更", "改动", "调节", "优化"],
        "pattern": r'^修改[^。]+[。]$',
        "interpretation": "MODIFICATION_ACTION",
        "semantic_role": SemanticRole.DATA_MODIFICATION.value,
        "arity": 2,  # 修改对象 + 新值
        "examples": [
            "修改配置。",
            "更新数据。",
            "调整参数。"
        ]
    },
    
    # 通信动词 (10个)
    VerbCategory.COMMUNICATION.value: {
        "verbs": ["发送", "接收", "传输", "传递", "通知", "报告", "告知", "通信", "传达", "广播"],
        "pattern": r'^发送[^。]+[。]$',
        "interpretation": "COMMUNICATION_ACTION",
        "semantic_role": SemanticRole.COMMUNICATION.value,
        "arity": 2,  # 发送者 + 消息/接收者
        "examples": [
            "发送消息。",
            "接收数据。",
            "通知用户。"
        ]
    },
    
    # 比较动词 (10个)
    VerbCategory.COMPARISON.value: {
        "verbs": ["比较", "对比", "对照", "匹配", "检查", "验证", "测试", "评估", "衡量", "判断"],
        "pattern": r'^比较[^。]+[。]$',
        "interpretation": "COMPARISON_ACTION",
        "semantic_role": SemanticRole.COMPARISON.value,
        "arity": 2,  # 比较对象A + 比较对象B
        "examples": [
            "比较大小。",
            "检查结果。",
            "验证数据。"
        ]
    },
    
    # 数学运算动词 (20个)
    "MATH_OPERATION": {
        "verbs": ["加", "减", "乘", "除", "模", "幂", "开方", "对数", "指数", "正弦", "余弦", "正切", "反正弦", "反余弦", "反正切", "绝对值", "取整", "舍入", "取余", "求商"],
        "pattern": r'^[^加]+加[^。]*[。]$',
        "interpretation": "MATH_OPERATION",
        "semantic_role": "MATH_OPERATION",
        "arity": 2,
        "examples": [
            "计算加法。",
            "求平方根。",
            "计算三角函数。"
        ]
    },

    # 逻辑运算动词 (20个)
    "LOGIC_OPERATION": {
        "verbs": ["与", "或", "非", "且", "或者", "不是", "异或", "同或", "蕴含", "等价", "真", "假", "成立", "不成立", "满足", "不满足", "符合", "不符合", "匹配", "不匹配"],
        "pattern": r'^[^与]+与[^。]*[。]$',
        "interpretation": "LOGIC_OPERATION",
        "semantic_role": "LOGIC_OPERATION",
        "arity": 2,
        "examples": [
            "逻辑与运算。",
            "判断条件。",
            "验证逻辑。"
        ]
    },
    
    # 转换动词 (10个)
    VerbCategory.TRANSFORMATION.value: {
        "verbs": ["转换", "变换", "翻译", "解析", "编译", "解释", "编码", "解码", "格式化", "序列化"],
        "pattern": r'^转换[^。]+[。]$',
        "interpretation": "TRANSFORMATION_ACTION",
        "semantic_role": SemanticRole.TRANSFORMATION.value,
        "arity": 2,  # 输入 + 输出格式
        "examples": [
            "转换格式。",
            "翻译文本。",
            "解析数据。"
        ]
    }
}


VERB_ARITY: Dict[str, int] = {
    # 算术运算
    '加': 2, '减': 2, '乘': 2, '除': 2, '模': 2, '幂': 2,
    '负': 1, '绝对': 1,
    
    # 比较运算
    '大': 2, '小': 2, '等': 2, '不等': 2,
    
    # 逻辑运算
    '且': 2, '或': 2, '非': 1,
    
    # 列表操作
    '列': -1,  # 可变参数
    '首': 1, '余': 1, '入': 2, '长': 1, '添': 2, '连': 2, '含': 2,
    
    # 高阶函数
    '皆': 2, '只': 2, '归': 3,
    
    # I/O操作
    '印': 1, '读': 1, '写': 2, '行': 1,
    
    # 状态转换动词
    '变为': 2, '变成': 2, '转为': 2, '切换为': 2, '转换为': 2,
    '变化为': 2, '转成': 2, '改成': 2, '调整为': 2,
    
    # 赋值动词
    '等于': 2, '设为': 2, '设置为': 2, '赋值为': 2, '是': 2,
    '定义为': 2, '指定为': 2, '赋给': 2,
    
    # 输出动词
    '打印': 1, '显示': 1, '输出': 1, '记录': 1, '输出为': 2,
    '展示': 1, '呈现': 1, '打印出': 1, '显示为': 2,
    
    # 控制动词
    '开启': 1, '关闭': 1, '启动': 1, '停止': 1, '执行': 1,
    '运行': 1, '暂停': 1, '继续': 1, '重启': 1, '终止': 1,
    
    # 计算动词
    '计算': -1, '求和': -1, '求积': -1, '比较': 2, '排序': 1,
    '过滤': 2, '映射': 2, '归约': 3, '统计': 1, '分析': 1,
    
    # 移动动词
    '移动': 1, '前进': 1, '后退': 1, '旋转': 1, '转向': 1,
    '跳跃': 1, '飞行': 1, '行走': 1, '跑动': 1, '滑动': 1,
    
    # 创建动词
    '创建': 1, '生成': 1, '建立': 1, '构造': 1, '初始化': 1,
    '新建': 1, '产生': 1, '制造': 1, '组建': 1, '设立': 1,
    
    # 销毁动词
    '删除': 1, '销毁': 1, '清除': 1, '移除': 1, '释放': 1,
    '消灭': 1, '拆除': 1, '丢弃': 1, '废除': 1, '撤销': 1,
    
    # 查询动词
    '查询': 1, '搜索': 1, '查找': 1, '获取': 1, '读取': 1,
    '检索': 1,
    
    # 修改动词
    '修改': 2, '更新': 2, '编辑': 2, '调整': 2, '改变': 2,
    '修正': 2, '变更': 2, '改动': 2, '调节': 2, '优化': 2,
    
    # 通信动词
    '发送': 2, '接收': 1, '传输': 2, '传递': 2, '通知': 2,
    '报告': 2, '告知': 2, '通信': 2, '传达': 2, '广播': 2,
    
    # 比较动词
    '对比': 2, '对照': 2, '匹配': 2, '检查': 1, '验证': 1,
    '测试': 1, '评估': 1, '衡量': 1, '判断': 1,
    
    # 转换动词
    '转换': 2, '变换': 2, '翻译': 2, '解析': 1, '编译': 1,
    '解释': 1, '编码': 2, '解码': 2, '格式化': 1, '序列化': 1,
}


def get_verb_category(verb: str) -> Tuple[str, Dict[str, Any]]:
    """
    获取动词的类别信息
    
    Args:
        verb: 动词字符串
        
    Returns:
        Tuple[category_name, category_info] 或 ("UNKNOWN", {})
    """
    for category_name, category_info in VERB_CATEGORIES.items():
        if verb in category_info["verbs"]:
            return category_name, category_info
    return "UNKNOWN", {}


def get_verb_arity(verb: str) -> int:
    """
    获取动词的元数
    
    Args:
        verb: 动词字符串
        
    Returns:
        动词的元数，如果未找到返回0
    """
    return VERB_ARITY.get(verb, 0)


def get_semantic_role(verb: str) -> str:
    """
    获取动词的语义角色
    
    Args:
        verb: 动词字符串
        
    Returns:
        语义角色字符串，如果未找到返回"UNKNOWN"
    """
    category_name, category_info = get_verb_category(verb)
    if category_info:
        return category_info.get("semantic_role", "UNKNOWN")
    return "UNKNOWN"


def get_verb_interpretation(verb: str) -> str:
    """
    获取动词的解释类型
    
    Args:
        verb: 动词字符串
        
    Returns:
        解释类型字符串，如果未找到返回"UNKNOWN"
    """
    category_name, category_info = get_verb_category(verb)
    if category_info:
        return category_info.get("interpretation", "UNKNOWN")
    return "UNKNOWN"


def get_all_verbs() -> List[str]:
    """
    获取所有动词列表
    
    Returns:
        所有动词的列表
    """
    all_verbs = []
    for category_info in VERB_CATEGORIES.values():
        all_verbs.extend(category_info["verbs"])
    return all_verbs


def get_verbs_by_category(category: str) -> List[str]:
    """
    获取指定类别的所有动词
    
    Args:
        category: 类别名称
        
    Returns:
        该类别下的所有动词列表
    """
    category_info = VERB_CATEGORIES.get(category)
    if category_info:
        return category_info["verbs"]
    return []


def get_category_by_verb(verb: str) -> str:
    """
    根据动词获取类别
    
    Args:
        verb: 动词字符串
        
    Returns:
        类别名称，如果未找到返回"UNKNOWN"
    """
    for category_name, category_info in VERB_CATEGORIES.items():
        if verb in category_info["verbs"]:
            return category_name
    return "UNKNOWN"


# 测试函数
def test_verb_categories():
    """测试动词分类词典"""
    print("动词分类词典测试")
    print("=" * 50)
    
    # 测试1: 获取所有动词
    all_verbs = get_all_verbs()
    print(f"总动词数量: {len(all_verbs)}")
    print(f"预期数量: 119")
    print(f"实际数量: {len(all_verbs)}")
    print(f"是否匹配: {'是' if len(all_verbs) == 119 else '否'}")
    print()
    
    # 测试2: 测试几个动词
    test_verbs = ["变为", "等于", "印", "开启", "计算", "移动", "创建", "删除", "查询", "修改", "发送", "比较", "转换"]
    
    for verb in test_verbs:
        category, info = get_verb_category(verb)
        arity = get_verb_arity(verb)
        semantic_role = get_semantic_role(verb)
        interpretation = get_verb_interpretation(verb)
        
        print(f"动词: {verb}")
        print(f"  类别: {category}")
        print(f"  元数: {arity}")
        print(f"  语义角色: {semantic_role}")
        print(f"  解释类型: {interpretation}")
        print()
    
    # 测试3: 按类别获取动词
    print("按类别统计:")
    for category_name in VERB_CATEGORIES.keys():
        verbs = get_verbs_by_category(category_name)
        print(f"  {category_name}: {len(verbs)}个动词")
    
    print("=" * 50)
    print("测试完成")


if __name__ == "__main__":
    test_verb_categories()