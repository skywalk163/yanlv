"""
言律语言教程体系

提供从入门到进阶的完整教程
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum


class TutorialLevel(Enum):
    """教程难度级别"""
    BEGINNER = "入门"      # 入门级
    INTERMEDIATE = "进阶"  # 进阶级
    ADVANCED = "高级"      # 高级


@dataclass
class TutorialSection:
    """教程章节"""
    title: str           # 章节标题
    content: str         # 章节内容
    code_examples: List[str]  # 代码示例
    exercises: List[str]      # 练习题


@dataclass
class Tutorial:
    """教程"""
    id: str                    # 教程ID
    title: str                 # 教程标题
    description: str           # 教程描述
    level: TutorialLevel       # 难度级别
    sections: List[TutorialSection]  # 章节列表
    prerequisites: List[str]   # 前置知识
    estimated_time: str        # 预计时间
    tags: List[str]            # 标签


class TutorialManager:
    """
    教程管理器
    
    管理所有教程内容
    """
    
    def __init__(self):
        """初始化教程管理器"""
        self.tutorials: Dict[str, Tutorial] = {}
        self._init_tutorials()
    
    def _init_tutorials(self) -> None:
        """初始化教程"""
        
        # 入门教程1: 环境配置
        self.add_tutorial(Tutorial(
            id="beginner-001",
            title="安装和环境配置",
            description="学习如何安装和配置言律编程语言开发环境",
            level=TutorialLevel.BEGINNER,
            sections=[
                TutorialSection(
                    title="安装言律语言",
                    content="""
言律语言可以通过以下方式安装:

1. 使用pip安装:
   ```
   pip install yanlv
   ```

2. 从源码安装:
   ```
   git clone https://github.com/yanlv/yanlv.git
   cd yanlv
   python setup.py install
   ```

3. 验证安装:
   ```
   yanlv --version
   ```
""",
                    code_examples=[
                        "# 验证安装",
                        "导入 yanlv",
                        "输出(\"言律语言安装成功!\")"
                    ],
                    exercises=[
                        "练习1: 安装言律语言并验证版本",
                        "练习2: 查看言律语言的帮助信息"
                    ]
                ),
                TutorialSection(
                    title="配置开发环境",
                    content="""
推荐使用VS Code作为开发环境:

1. 安装VS Code
2. 安装言律语言扩展
3. 配置语法高亮
4. 配置代码格式化
""",
                    code_examples=[],
                    exercises=[
                        "练习1: 安装VS Code和言律语言扩展",
                        "练习2: 创建第一个言律语言文件"
                    ]
                )
            ],
            prerequisites=[],
            estimated_time="30分钟",
            tags=["安装", "环境", "入门"]
        ))
        
        # 入门教程2: 第一个程序
        self.add_tutorial(Tutorial(
            id="beginner-002",
            title="第一个程序",
            description="编写并运行你的第一个言律语言程序",
            level=TutorialLevel.BEGINNER,
            sections=[
                TutorialSection(
                    title="Hello World",
                    content="""
让我们编写第一个言律语言程序 - Hello World:

```yanlv
输出("Hello, World!")
```

这个程序会输出 "Hello, World!" 到控制台。
""",
                    code_examples=[
                        "# 第一个程序",
                        '输出("Hello, World!")',
                        "",
                        "# 也可以输出中文",
                        '输出("你好,世界!")'
                    ],
                    exercises=[
                        "练习1: 编写并运行Hello World程序",
                        "练习2: 修改程序输出你的名字"
                    ]
                ),
                TutorialSection(
                    title="运行程序",
                    content="""
有两种方式运行言律语言程序:

1. 直接运行:
   ```
   yanlv run hello.yanlv
   ```

2. 交互式运行:
   ```
   yanlv repl
   >>> 输出("Hello")
   Hello
   ```
""",
                    code_examples=[
                        "# 在REPL中运行",
                        '输出("交互模式测试")',
                        "定义 x 为 10",
                        "输出(x)"
                    ],
                    exercises=[
                        "练习1: 使用命令行运行程序",
                        "练习2: 使用REPL交互模式"
                    ]
                )
            ],
            prerequisites=["beginner-001"],
            estimated_time="20分钟",
            tags=["Hello World", "运行", "入门"]
        ))
        
        # 入门教程3: 变量和数据类型
        self.add_tutorial(Tutorial(
            id="beginner-003",
            title="变量和数据类型",
            description="学习言律语言的变量定义和基本数据类型",
            level=TutorialLevel.BEGINNER,
            sections=[
                TutorialSection(
                    title="定义变量",
                    content="""
使用"定义"关键字定义变量:

```yanlv
定义 x 为 10        # 整数
定义 y 为 3.14      # 浮点数
定义 name 为 "张三"  # 字符串
定义 flag 为 真     # 布尔值
```
""",
                    code_examples=[
                        "# 定义不同类型的变量",
                        "定义 age 为 25",
                        "定义 price 为 99.9",
                        '定义 name 为 "李四"',
                        "定义 is_student 为 真",
                        "",
                        "# 输出变量",
                        "输出(age)",
                        "输出(name)"
                    ],
                    exercises=[
                        "练习1: 定义不同类型的变量",
                        "练习2: 输出变量的值"
                    ]
                ),
                TutorialSection(
                    title="数据类型",
                    content="""
言律语言支持以下基本数据类型:

- 整数: 1, 2, 3, -1, -2
- 浮点数: 3.14, 2.718, -1.5
- 字符串: "hello", 'world'
- 布尔值: 真, 假
- 数组: [1, 2, 3], ["a", "b", "c"]
""",
                    code_examples=[
                        "# 整数",
                        "定义 int_num 为 42",
                        "",
                        "# 浮点数",
                        "定义 float_num 为 3.14159",
                        "",
                        "# 字符串",
                        '定义 str_val 为 "言律语言"',
                        "",
                        "# 布尔值",
                        "定义 bool_val 为 真",
                        "",
                        "# 数组",
                        "定义 arr 为 [1, 2, 3, 4, 5]"
                    ],
                    exercises=[
                        "练习1: 创建各种类型的变量",
                        "练习2: 使用数组存储多个值"
                    ]
                )
            ],
            prerequisites=["beginner-002"],
            estimated_time="40分钟",
            tags=["变量", "数据类型", "入门"]
        ))
        
        # 进阶教程1: 函数
        self.add_tutorial(Tutorial(
            id="intermediate-001",
            title="函数定义和调用",
            description="学习如何定义和调用函数",
            level=TutorialLevel.INTERMEDIATE,
            sections=[
                TutorialSection(
                    title="定义函数",
                    content="""
使用"函数"关键字定义函数:

```yanlv
函数 加法(a, b) {
    返回 a + b
}
```
""",
                    code_examples=[
                        "# 定义简单函数",
                        "函数 问候(name) {",
                        '    输出("你好, " + name)',
                        "}",
                        "",
                        "# 调用函数",
                        '问候("张三")',
                        "",
                        "# 带返回值的函数",
                        "函数 平方(x) {",
                        "    返回 x * x",
                        "}",
                        "",
                        "定义 result 为 平方(5)",
                        "输出(result)  # 输出 25"
                    ],
                    exercises=[
                        "练习1: 定义一个计算两数之和的函数",
                        "练习2: 定义一个判断奇偶的函数"
                    ]
                )
            ],
            prerequisites=["beginner-003"],
            estimated_time="60分钟",
            tags=["函数", "进阶"]
        ))
        
        # 进阶教程2: 控制流
        self.add_tutorial(Tutorial(
            id="intermediate-002",
            title="控制流语句",
            description="学习条件判断和循环语句",
            level=TutorialLevel.INTERMEDIATE,
            sections=[
                TutorialSection(
                    title="条件判断",
                    content="""
使用"若...则...否则"进行条件判断:

```yanlv
若 x > 0 则 {
    输出("正数")
} 否则 {
    输出("非正数")
}
```
""",
                    code_examples=[
                        "# 条件判断示例",
                        "定义 score 为 85",
                        "",
                        "若 score >= 90 则 {",
                        '    输出("优秀")',
                        "} 否则 若 score >= 60 则 {",
                        '    输出("及格")',
                        "} 否则 {",
                        '    输出("不及格")',
                        "}"
                    ],
                    exercises=[
                        "练习1: 编写判断闰年的程序",
                        "练习2: 编写成绩等级判断程序"
                    ]
                ),
                TutorialSection(
                    title="循环语句",
                    content="""
使用"当"和"执行"进行循环:

```yanlv
定义 i 为 0
当 i < 10 执行 {
    输出(i)
    设 i 为 i + 1
}
```
""",
                    code_examples=[
                        "# while循环",
                        "定义 i 为 1",
                        "当 i <= 5 执行 {",
                        "    输出(i)",
                        "    设 i 为 i + 1",
                        "}",
                        "",
                        "# 计算阶乘",
                        "函数 阶乘(n) {",
                        "    定义 result 为 1",
                        "    定义 i 为 1",
                        "    当 i <= n 执行 {",
                        "        设 result 为 result * i",
                        "        设 i 为 i + 1",
                        "    }",
                        "    返回 result",
                        "}",
                        "",
                        "输出(阶乘(5))  # 输出 120"
                    ],
                    exercises=[
                        "练习1: 编写计算1到100之和的程序",
                        "练习2: 编写打印九九乘法表的程序"
                    ]
                )
            ],
            prerequisites=["intermediate-001"],
            estimated_time="90分钟",
            tags=["控制流", "条件", "循环", "进阶"]
        ))
    
    def add_tutorial(self, tutorial: Tutorial) -> None:
        """
        添加教程
        
        Args:
            tutorial: 教程对象
        """
        self.tutorials[tutorial.id] = tutorial
    
    def get_tutorial(self, tutorial_id: str) -> Optional[Tutorial]:
        """
        获取教程
        
        Args:
            tutorial_id: 教程ID
            
        Returns:
            教程对象
        """
        return self.tutorials.get(tutorial_id)
    
    def get_tutorials_by_level(self, level: TutorialLevel) -> List[Tutorial]:
        """
        按难度级别获取教程
        
        Args:
            level: 难度级别
            
        Returns:
            教程列表
        """
        return [
            tutorial for tutorial in self.tutorials.values()
            if tutorial.level == level
        ]
    
    def get_all_tutorials(self) -> List[Tutorial]:
        """获取所有教程"""
        return list(self.tutorials.values())
    
    def generate_tutorial_index(self) -> str:
        """
        生成教程索引
        
        Returns:
            索引Markdown文本
        """
        lines = []
        
        lines.append("# 言律语言教程索引\n")
        
        # 入门教程
        lines.append("## 入门教程\n")
        beginner_tutorials = self.get_tutorials_by_level(TutorialLevel.BEGINNER)
        for tutorial in beginner_tutorials:
            lines.append(f"- [{tutorial.title}](#{tutorial.id}) - {tutorial.description} ({tutorial.estimated_time})")
        
        # 进阶教程
        lines.append("\n## 进阶教程\n")
        intermediate_tutorials = self.get_tutorials_by_level(TutorialLevel.INTERMEDIATE)
        for tutorial in intermediate_tutorials:
            lines.append(f"- [{tutorial.title}](#{tutorial.id}) - {tutorial.description} ({tutorial.estimated_time})")
        
        # 高级教程
        lines.append("\n## 高级教程\n")
        advanced_tutorials = self.get_tutorials_by_level(TutorialLevel.ADVANCED)
        if advanced_tutorials:
            for tutorial in advanced_tutorials:
                lines.append(f"- [{tutorial.title}](#{tutorial.id}) - {tutorial.description} ({tutorial.estimated_time})")
        else:
            lines.append("*敬请期待...*")
        
        return '\n'.join(lines)


# 全局教程管理器实例
_global_tutorial_manager: Optional[TutorialManager] = None


def get_tutorial_manager() -> TutorialManager:
    """获取全局教程管理器"""
    global _global_tutorial_manager
    if _global_tutorial_manager is None:
        _global_tutorial_manager = TutorialManager()
    return _global_tutorial_manager
