"""
言律语言示例程序集

提供丰富的示例程序帮助用户学习
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum


class ExampleCategory(Enum):
    """示例分类"""
    BASIC = "基础示例"        # 基础语法
    ALGORITHM = "算法示例"    # 算法实现
    DATA_STRUCTURE = "数据结构"  # 数据结构
    PRACTICAL = "实用程序"    # 实用程序
    GAME = "游戏示例"         # 游戏程序


@dataclass
class ExampleProgram:
    """示例程序"""
    id: str                    # 示例ID
    title: str                 # 标题
    description: str           # 描述
    category: ExampleCategory  # 分类
    code: str                  # 代码
    output: str                # 预期输出
    explanation: str           # 代码解释
    difficulty: str            # 难度(简单/中等/困难)
    tags: List[str]            # 标签


class ExampleManager:
    """
    示例程序管理器
    
    管理所有示例程序
    """
    
    def __init__(self):
        """初始化示例管理器"""
        self.examples: Dict[str, ExampleProgram] = {}
        self._init_examples()
    
    def _init_examples(self) -> None:
        """初始化示例程序"""
        
        # 基础示例
        self.add_example(ExampleProgram(
            id="basic-001",
            title="Hello World",
            description="最简单的言律语言程序",
            category=ExampleCategory.BASIC,
            code='输出("Hello, World!")',
            output="Hello, World!",
            explanation="""
这是最简单的言律语言程序。
使用"输出"函数将文本打印到控制台。
""",
            difficulty="简单",
            tags=["入门", "输出"]
        ))
        
        self.add_example(ExampleProgram(
            id="basic-002",
            title="变量和运算",
            description="演示变量定义和基本运算",
            category=ExampleCategory.BASIC,
            code="""# 定义变量
定义 a 为 10
定义 b 为 20

# 基本运算
定义 sum 为 a + b
定义 diff 为 a - b
定义 product 为 a * b
定义 quotient 为 b / a

# 输出结果
输出("和: " + sum)
输出("差: " + diff)
输出("积: " + product)
输出("商: " + quotient)""",
            output="""和: 30
差: -10
积: 200
商: 2""",
            explanation="""
演示如何定义变量和进行基本数学运算。
使用"定义"关键字创建变量。
支持加减乘除等基本运算。
""",
            difficulty="简单",
            tags=["变量", "运算", "基础"]
        ))
        
        self.add_example(ExampleProgram(
            id="basic-003",
            title="条件判断",
            description="演示条件判断语句",
            category=ExampleCategory.BASIC,
            code="""定义 score 为 85

若 score >= 90 则 {
    输出("优秀")
} 否则 若 score >= 80 则 {
    输出("良好")
} 否则 若 score >= 60 则 {
    输出("及格")
} 否则 {
    输出("不及格")
}""",
            output="良好",
            explanation="""
演示条件判断语句的使用。
使用"若...则...否则"结构。
支持多级条件判断。
""",
            difficulty="简单",
            tags=["条件", "判断", "基础"]
        ))
        
        self.add_example(ExampleProgram(
            id="basic-004",
            title="循环语句",
            description="演示循环语句",
            category=ExampleCategory.BASIC,
            code="""# 打印1到10
定义 i 为 1
当 i <= 10 执行 {
    输出(i)
    设 i 为 i + 1
}""",
            output="""1
2
3
4
5
6
7
8
9
10""",
            explanation="""
演示循环语句的使用。
使用"当...执行"结构。
注意更新循环变量避免死循环。
""",
            difficulty="简单",
            tags=["循环", "基础"]
        ))
        
        # 算法示例
        self.add_example(ExampleProgram(
            id="algo-001",
            title="计算阶乘",
            description="使用递归计算阶乘",
            category=ExampleCategory.ALGORITHM,
            code="""函数 阶乘 {
    若 n <= 1 则 {
        返回 1
    }
    返回 n * 阶乘(n - 1)
}

# 计算5的阶乘
定义 result 为 阶乘(5)
输出("5! = " + result)""",
            output="5! = 120",
            explanation="""
使用递归函数计算阶乘。
递归函数调用自身来解决问题。
基准情况: n <= 1 时返回1。
""",
            difficulty="中等",
            tags=["递归", "阶乘", "算法"]
        ))
        
        self.add_example(ExampleProgram(
            id="algo-002",
            title="斐波那契数列",
            description="生成斐波那契数列",
            category=ExampleCategory.ALGORITHM,
            code="""函数 斐波那契 {
    若 n <= 1 则 {
        返回 n
    }
    返回 斐波那契(n - 1) + 斐波那契(n - 2)
}

# 输出前10个斐波那契数
定义 i 为 0
当 i < 10 执行 {
    输出(斐波那契
    设 i 为 i + 1
}""",
            output="""0
1
1
2
3
5
8
13
21
34""",
            explanation="""
使用递归生成斐波那契数列。
每个数是前两个数之和。
F(0)=0, F(1)=1, F(n)=F(n-1)+F(n-2)。
""",
            difficulty="中等",
            tags=["递归", "斐波那契", "算法"]
        ))
        
        self.add_example(ExampleProgram(
            id="algo-003",
            title="冒泡排序",
            description="实现冒泡排序算法",
            category=ExampleCategory.ALGORITHM,
            code="""函数 冒泡排序 {
    定义 n 为 长度
    定义 i 为 0
    
    当 i < n - 1 执行 {
        定义 j 为 0
        当 j < n - i - 1 执行 {
            若 arr[j] > arr[j + 1] 则 {
                # 交换元素
                定义 temp 为 arr[j]
                设 arr[j] 为 arr[j + 1]
                设 arr[j + 1] 为 temp
            }
            设 j 为 j + 1
        }
        设 i 为 i + 1
    }
    
    返回 arr
}

# 测试排序
定义 numbers 为 [64, 34, 25, 12, 22, 11, 90]
定义 sorted 为 冒泡排序
输出("排序结果: " + sorted)""",
            output="排序结果: [11, 12, 22, 25, 34, 64, 90]",
            explanation="""
实现经典的冒泡排序算法。
通过相邻元素比较和交换进行排序。
时间复杂度O(n²)。
""",
            difficulty="中等",
            tags=["排序", "算法", "数组"]
        ))
        
        # 实用程序
        self.add_example(ExampleProgram(
            id="practical-001",
            title="计算器",
            description="简单的四则运算计算器",
            category=ExampleCategory.PRACTICAL,
            code="""函数 计算器(a, b, op) {
    若 op == "+" 则 {
        返回 a + b
    } 否则 若 op == "-" 则 {
        返回 a - b
    } 否则 若 op == "*" 则 {
        返回 a * b
    } 否则 若 op == "/" 则 {
        若 b == 0 则 {
            输出("错误: 除数不能为0")
            返回 空
        }
        返回 a / b
    } 否则 {
        输出("错误: 不支持的运算符")
        返回 空
    }
}

# 测试计算器
输出("10 + 5 = " + 计算器(10, 5, "+"))
输出("10 - 5 = " + 计算器(10, 5, "-"))
输出("10 * 5 = " + 计算器(10, 5, "*"))
输出("10 / 5 = " + 计算器(10, 5, "/"))""",
            output="""10 + 5 = 15
10 - 5 = 5
10 * 5 = 50
10 / 5 = 2""",
            explanation="""
实现一个简单的四则运算计算器。
支持加减乘除四种运算。
包含除零检查。
""",
            difficulty="简单",
            tags=["计算器", "实用", "函数"]
        ))
        
        self.add_example(ExampleProgram(
            id="practical-002",
            title="猜数字游戏",
            description="简单的猜数字游戏",
            category=ExampleCategory.GAME,
            code="""# 生成随机数(简化版)
定义 target 为 42
定义 attempts 为 0
定义 max_attempts 为 5

输出("猜数字游戏! (1-100)")
输出("你有" + max_attempts + "次机会")

当 attempts < max_attempts 执行 {
    定义 guess 为 输入("请输入你的猜测: ")
    设 attempts 为 attempts + 1
    
    若 guess == target 则 {
        输出("恭喜! 你猜对了!")
        输出("你用了" + attempts + "次")
        停止
    } 否则 若 guess < target 则 {
        输出("太小了!")
    } 否则 {
        输出("太大了!")
    }
}

若 attempts >= max_attempts 则 {
    输出("游戏结束! 正确答案是" + target)
}""",
            output="""猜数字游戏! (1-100)
你有5次机会
请输入你的猜测: 50
太大了!
请输入你的猜测: 30
太小了!
请输入你的猜测: 42
恭喜! 你猜对了!
你用了3次""",
            explanation="""
实现一个简单的猜数字游戏。
玩家有有限次数的猜测机会。
程序会提示猜测是太大还是太小。
""",
            difficulty="中等",
            tags=["游戏", "交互", "循环"]
        ))
    
    def add_example(self, example: ExampleProgram) -> None:
        """
        添加示例
        
        Args:
            example: 示例程序对象
        """
        self.examples[example.id] = example
    
    def get_example(self, example_id: str) -> Optional[ExampleProgram]:
        """
        获取示例
        
        Args:
            example_id: 示例ID
            
        Returns:
            示例程序对象
        """
        return self.examples.get(example_id)
    
    def get_examples_by_category(self, category: ExampleCategory) -> List[ExampleProgram]:
        """
        按分类获取示例
        
        Args:
            category: 分类
            
        Returns:
            示例列表
        """
        return [
            example for example in self.examples.values()
            if example.category == category
        ]
    
    def get_all_examples(self) -> List[ExampleProgram]:
        """获取所有示例"""
        return list(self.examples.values())
    
    def generate_example_index(self) -> str:
        """
        生成示例索引
        
        Returns:
            索引Markdown文本
        """
        lines = []
        
        lines.append("# 言律语言示例程序索引\n")
        
        # 按分类组织
        for category in ExampleCategory:
            examples = self.get_examples_by_category(category)
            if examples:
                lines.append(f"\n## {category.value}\n")
                for example in examples:
                    lines.append(
                        f"- [{example.title}](#{example.id}) - "
                        f"{example.description} (难度: {example.difficulty})"
                    )
        
        return '\n'.join(lines)


# 全局示例管理器实例
_global_example_manager: Optional[ExampleManager] = None


def get_example_manager() -> ExampleManager:
    """获取全局示例管理器"""
    global _global_example_manager
    if _global_example_manager is None:
        _global_example_manager = ExampleManager()
    return _global_example_manager
