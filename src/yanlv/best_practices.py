"""
言律语言最佳实践指南

提供代码风格、性能优化、项目结构等最佳实践建议
"""

from typing import List, Dict, Any
from dataclasses import dataclass
from enum import Enum


class PracticeCategory(Enum):
    """最佳实践分类"""
    CODE_STYLE = "代码风格"
    PERFORMANCE = "性能优化"
    PROJECT_STRUCTURE = "项目结构"
    DEBUGGING = "调试技巧"
    SECURITY = "安全编码"


@dataclass
class BestPractice:
    """最佳实践"""
    id: str                    # 实践ID
    title: str                 # 标题
    category: PracticeCategory # 分类
    description: str           # 描述
    good_example: str          # 好的示例
    bad_example: str           # 坏的示例
    explanation: str           # 解释说明


class BestPracticesGuide:
    """
    最佳实践指南
    
    管理所有最佳实践建议
    """
    
    def __init__(self):
        """初始化最佳实践指南"""
        self.practices: Dict[str, BestPractice] = {}
        self._init_practices()
    
    def _init_practices(self) -> None:
        """初始化最佳实践"""
        
        # 代码风格指南
        self.add_practice(BestPractice(
            id="style-001",
            title="使用有意义的变量名",
            category=PracticeCategory.CODE_STYLE,
            description="变量名应该清晰表达其用途,避免使用单字母或无意义的名称",
            good_example="""# 好的实践
定义 用户数量 为 100
定义 总价格 为 商品单价 * 数量
定义 是否已登录 为 真""",
            bad_example="""# 坏的实践
定义 x 为 100
定义 y 为 a * b
定义 flag 为 真""",
            explanation="""
好的变量名能够:
1. 提高代码可读性
2. 减少注释需求
3. 便于团队协作
4. 降低维护成本
"""
        ))
        
        self.add_practice(BestPractice(
            id="style-002",
            title="保持函数功能单一",
            category=PracticeCategory.CODE_STYLE,
            description="每个函数应该只做一件事,保持功能单一和清晰",
            good_example="""# 好的实践
函数 计算总价(商品列表) {
    定义 总价 为 0
    对于 商品 在 商品列表 执行 {
        设 总价 为 总价 + 商品.价格
    }
    返回 总价
}

函数 应用折扣(价格, 折扣率) {
    返回 价格 * 折扣率
}""",
            bad_example="""# 坏的实践
函数 计算并应用折扣(商品列表, 折扣率) {
    # 计算总价和应用折扣混在一起
    定义 总价 为 0
    对于 商品 在 商品列表 执行 {
        设 总价 为 总价 + 商品.价格
    }
    返回 总价 * 折扣率
}""",
            explanation="""
单一职责原则的好处:
1. 函数更易于理解和测试
2. 提高代码复用性
3. 降低修改风险
4. 便于维护和扩展
"""
        ))
        
        self.add_practice(BestPractice(
            id="style-003",
            title="添加适当的注释",
            category=PracticeCategory.CODE_STYLE,
            description="在复杂逻辑处添加注释,解释为什么这样做",
            good_example="""# 好的实践
函数 计算折扣价格(原价, 用户等级) {
    # 根据用户等级应用不同的折扣策略
    # VIP用户享受8折,普通用户享受9折
    若 用户等级 == "VIP" 则 {
        返回 原价 * 0.8
    } 否则 {
        返回 原价 * 0.9
    }
}""",
            bad_example="""# 坏的实践
函数 计算折扣价格(原价, 用户等级) {
    若 用户等级 == "VIP" 则 {
        返回 原价 * 0.8
    } 否则 {
        返回 原价 * 0.9
    }
}""",
            explanation="""
好的注释应该:
1. 解释"为什么"而不是"是什么"
2. 在复杂逻辑处提供上下文
3. 帮助其他开发者理解代码
4. 避免过度注释显而易见的代码
"""
        ))
        
        # 性能优化指南
        self.add_practice(BestPractice(
            id="perf-001",
            title="避免在循环中重复计算",
            category=PracticeCategory.PERFORMANCE,
            description="将循环中不变的计算提取到循环外部",
            good_example="""# 好的实践
定义 系数 为 计算系数()
定义 结果列表 为 []

对于 数据 在 数据列表 执行 {
    # 系数只计算一次
    定义 结果 为 数据 * 系数
    结果列表.添加(结果)
}""",
            bad_example="""# 坏的实践
定义 结果列表 为 []

对于 数据 在 数据列表 执行 {
    # 每次循环都重新计算系数
    定义 结果 为 数据 * 计算系数()
    结果列表.添加(结果)
}""",
            explanation="""
性能优化要点:
1. 减少重复计算
2. 利用缓存机制
3. 优化循环性能
4. 避免不必要的函数调用
"""
        ))
        
        self.add_practice(BestPractice(
            id="perf-002",
            title="使用缓存避免重复计算",
            category=PracticeCategory.PERFORMANCE,
            description="对于计算密集型函数,使用缓存存储结果",
            good_example="""# 好的实践
定义 斐波那契缓存 为 {}

函数 斐波那契 {
    若 n 在 斐波那契缓存 则 {
        返回 斐波那契缓存[n]
    }
    
    若 n <= 1 则 {
        返回 n
    }
    
    定义 结果 为 斐波那契(n-1) + 斐波那契(n-2)
    设 斐波那契缓存[n] 为 结果
    返回 结果
}""",
            bad_example="""# 坏的实践
函数 斐波那契 {
    若 n <= 1 则 {
        返回 n
    }
    返回 斐波那契(n-1) + 斐波那契(n-2)
}""",
            explanation="""
缓存的好处:
1. 显著提升性能
2. 减少计算时间
3. 降低资源消耗
4. 适用于递归和重复计算
"""
        ))
        
        # 项目结构指南
        self.add_practice(BestPractice(
            id="struct-001",
            title="使用清晰的目录结构",
            category=PracticeCategory.PROJECT_STRUCTURE,
            description="组织项目文件,使用清晰的目录结构",
            good_example="""# 好的项目结构
项目名称/
├── 源码/           # 源代码
│   ├── 主程序.yl
│   ├── 工具.yl
│   └── 模块/
├── 测试/           # 测试代码
│   ├── 测试_工具.yl
│   └── 测试_主程序.yl
├── 文档/           # 文档
│   ├── README.md
│   └── API文档.md
└── 配置/           # 配置文件
    └── 设置.json""",
            bad_example="""# 坏的项目结构
项目名称/
├── 主程序.yl
├── 工具.yl
├── 测试1.yl
├── 测试2.yl
├── README.md
└── 设置.json""",
            explanation="""
好的项目结构应该:
1. 分类清晰
2. 易于导航
3. 便于维护
4. 符合约定
"""
        ))
        
        # 调试技巧
        self.add_practice(BestPractice(
            id="debug-001",
            title="使用断点调试",
            category=PracticeCategory.DEBUGGING,
            description="在关键位置设置断点,逐步调试代码",
            good_example="""# 好的实践
函数 处理数据(数据) {
    # 在关键位置设置断点
    断点("开始处理数据")
    
    定义 清洗后数据 为 清洗数据(数据)
    断点("数据清洗完成")
    
    定义 结果 为 分析数据(清洗后数据)
    断点("数据分析完成")
    
    返回 结果
}""",
            bad_example="""# 坏的实践
函数 处理数据(数据) {
    定义 清洗后数据 为 清洗数据(数据)
    定义 结果 为 分析数据(清洗后数据)
    返回 结果
}""",
            explanation="""
调试技巧:
1. 在关键位置设置断点
2. 检查变量值
3. 逐步执行代码
4. 查看调用栈
"""
        ))
        
        # 安全编码指南
        self.add_practice(BestPractice(
            id="security-001",
            title="验证用户输入",
            category=PracticeCategory.SECURITY,
            description="永远不要信任用户输入,必须进行验证",
            good_example="""# 好的实践
函数 处理用户输入(输入) {
    # 验证输入不为空
    若 输入 为 空 则 {
        抛出 错误("输入不能为空")
    }
    
    # 验证输入长度
    若 长度(输入) > 100 则 {
        抛出 错误("输入长度超过限制")
    }
    
    # 验证输入格式
    若 非 是有效格式(输入) 则 {
        抛出 错误("输入格式不正确")
    }
    
    返回 处理(输入)
}""",
            bad_example="""# 坏的实践
函数 处理用户输入(输入) {
    # 直接使用用户输入,没有验证
    返回 处理(输入)
}""",
            explanation="""
安全编码原则:
1. 永远验证用户输入
2. 使用白名单验证
3. 限制输入长度
4. 处理异常情况
"""
        ))
    
    def add_practice(self, practice: BestPractice) -> None:
        """
        添加最佳实践
        
        Args:
            practice: 最佳实践对象
        """
        self.practices[practice.id] = practice
    
    def get_practice(self, practice_id: str) -> BestPractice:
        """
        获取最佳实践
        
        Args:
            practice_id: 实践ID
            
        Returns:
            最佳实践对象
        """
        return self.practices.get(practice_id)
    
    def get_practices_by_category(self, category: PracticeCategory) -> List[BestPractice]:
        """
        按分类获取最佳实践
        
        Args:
            category: 分类
            
        Returns:
            最佳实践列表
        """
        return [
            practice for practice in self.practices.values()
            if practice.category == category
        ]
    
    def get_all_practices(self) -> List[BestPractice]:
        """获取所有最佳实践"""
        return list(self.practices.values())
    
    def generate_guide(self) -> str:
        """
        生成最佳实践指南文档
        
        Returns:
            Markdown格式的指南文档
        """
        lines = []
        
        lines.append("# 言律语言最佳实践指南\n")
        
        # 按分类组织
        for category in PracticeCategory:
            practices = self.get_practices_by_category(category)
            if practices:
                lines.append(f"\n## {category.value}\n")
                
                for practice in practices:
                    lines.append(f"\n### {practice.title}\n")
                    lines.append(f"\n{practice.description}\n")
                    lines.append(f"\n**好的示例:**\n")
                    lines.append(f"```\n{practice.good_example}\n```\n")
                    lines.append(f"\n**坏的示例:**\n")
                    lines.append(f"```\n{practice.bad_example}\n```\n")
                    lines.append(f"\n**说明:**\n{practice.explanation}\n")
        
        return '\n'.join(lines)


# 全局最佳实践指南实例
_global_guide: BestPracticesGuide = None


def get_best_practices_guide() -> BestPracticesGuide:
    """获取全局最佳实践指南"""
    global _global_guide
    if _global_guide is None:
        _global_guide = BestPracticesGuide()
    return _global_guide
