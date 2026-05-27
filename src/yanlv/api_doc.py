"""
言律语言API文档生成器

自动生成标准库API文档
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import inspect


@dataclass
class APIParameter:
    """API参数"""
    name: str           # 参数名
    type: str           # 类型
    description: str    # 描述
    default: Any = None # 默认值
    required: bool = True  # 是否必需


@dataclass
class APIFunction:
    """API函数"""
    name: str                   # 函数名
    description: str            # 描述
    parameters: List[APIParameter]  # 参数列表
    return_type: str            # 返回类型
    return_description: str     # 返回值描述
    examples: List[str]         # 示例代码
    category: str               # 分类
    version: str = "1.0"        # 版本


class APIDocGenerator:
    """
    API文档生成器
    
    自动提取和生成API文档
    """
    
    def __init__(self):
        """初始化文档生成器"""
        self.functions: Dict[str, APIFunction] = {}
        self.categories: Dict[str, List[str]] = {}
        
        # 初始化标准库函数文档
        self._init_stdlib_docs()
    
    def _init_stdlib_docs(self) -> None:
        """初始化标准库文档"""
        
        # 数学函数
        self.add_function(APIFunction(
            name="取整",
            description="将数字向下取整到最接近的整数",
            parameters=[
                APIParameter("x", "数字", "要取整的数字", required=True)
            ],
            return_type="整数",
            return_description="取整后的整数",
            examples=[
                "定义 result 为 取整(3.7)  # result = 3",
                "定义 result 为 取整(-2.3)  # result = -3"
            ],
            category="数学函数"
        ))
        
        self.add_function(APIFunction(
            name="取余",
            description="计算两个数相除的余数",
            parameters=[
                APIParameter("a", "数字", "被除数", required=True),
                APIParameter("b", "数字", "除数", required=True)
            ],
            return_type="数字",
            return_description="余数",
            examples=[
                "定义 result 为 取余(10, 3)  # result = 1",
                "定义 result 为 取余(7, 2)   # result = 1"
            ],
            category="数学函数"
        ))
        
        self.add_function(APIFunction(
            name="绝对值",
            description="计算数字的绝对值",
            parameters=[
                APIParameter("x", "数字", "要计算绝对值的数字", required=True)
            ],
            return_type="数字",
            return_description="绝对值",
            examples=[
                "定义 result 为 绝对值(-5)   # result = 5",
                "定义 result 为 绝对值(3.14) # result = 3.14"
            ],
            category="数学函数"
        ))
        
        self.add_function(APIFunction(
            name="平方根",
            description="计算数字的平方根",
            parameters=[
                APIParameter("x", "数字", "要计算平方根的数字(必须≥0)", required=True)
            ],
            return_type="数字",
            return_description="平方根",
            examples=[
                "定义 result 为 平方根(16)  # result = 4",
                "定义 result 为 平方根(2)   # result = 1.414..."
            ],
            category="数学函数"
        ))
        
        self.add_function(APIFunction(
            name="幂",
            description="计算x的y次幂",
            parameters=[
                APIParameter("x", "数字", "底数", required=True),
                APIParameter("y", "数字", "指数", required=True)
            ],
            return_type="数字",
            return_description="x的y次幂",
            examples=[
                "定义 result 为 幂(2, 3)   # result = 8",
                "定义 result 为 幂(10, 2)  # result = 100"
            ],
            category="数学函数"
        ))
        
        # 字符串函数
        self.add_function(APIFunction(
            name="长度",
            description="获取字符串或数组的长度",
            parameters=[
                APIParameter("obj", "字符串或数组", "要计算长度的对象", required=True)
            ],
            return_type="整数",
            return_description="长度",
            examples=[
                "定义 len 为 长度(\"hello\")     # len = 5",
                "定义 len 为 长度([1, 2, 3])    # len = 3"
            ],
            category="字符串函数"
        ))
        
        self.add_function(APIFunction(
            name="查找",
            description="在字符串中查找子串的位置",
            parameters=[
                APIParameter("string", "字符串", "要搜索的字符串", required=True),
                APIParameter("substring", "字符串", "要查找的子串", required=True)
            ],
            return_type="整数",
            return_description="子串位置(未找到返回-1)",
            examples=[
                "定义 pos 为 查找(\"hello world\", \"world\")  # pos = 6",
                "定义 pos 为 查找(\"hello\", \"xyz\")         # pos = -1"
            ],
            category="字符串函数"
        ))
        
        self.add_function(APIFunction(
            name="替换",
            description="替换字符串中的子串",
            parameters=[
                APIParameter("string", "字符串", "原字符串", required=True),
                APIParameter("old", "字符串", "要替换的子串", required=True),
                APIParameter("new", "字符串", "替换后的子串", required=True)
            ],
            return_type="字符串",
            return_description="替换后的字符串",
            examples=[
                "定义 result 为 替换(\"hello world\", \"world\", \"yanlv\")",
                "# result = \"hello yanlv\""
            ],
            category="字符串函数"
        ))
        
        self.add_function(APIFunction(
            name="分割",
            description="按分隔符分割字符串",
            parameters=[
                APIParameter("string", "字符串", "要分割的字符串", required=True),
                APIParameter("separator", "字符串", "分隔符", required=True)
            ],
            return_type="数组",
            return_description="分割后的字符串数组",
            examples=[
                "定义 parts 为 分割(\"a,b,c\", \",\")",
                "# parts = [\"a\", \"b\", \"c\"]"
            ],
            category="字符串函数"
        ))
        
        # 数组函数
        self.add_function(APIFunction(
            name="添加",
            description="向数组添加元素",
            parameters=[
                APIParameter("array", "数组", "要添加元素的数组", required=True),
                APIParameter("element", "任意", "要添加的元素", required=True)
            ],
            return_type="数组",
            return_description="添加元素后的数组",
            examples=[
                "定义 arr 为 [1, 2, 3]",
                "添加(arr, 4)  # arr = [1, 2, 3, 4]"
            ],
            category="数组函数"
        ))
        
        self.add_function(APIFunction(
            name="删除",
            description="从数组删除元素",
            parameters=[
                APIParameter("array", "数组", "要删除元素的数组", required=True),
                APIParameter("index", "整数", "要删除的索引", required=True)
            ],
            return_type="数组",
            return_description="删除元素后的数组",
            examples=[
                "定义 arr 为 [1, 2, 3]",
                "删除(arr, 1)  # arr = [1, 3]"
            ],
            category="数组函数"
        ))
        
        # 输入输出函数
        self.add_function(APIFunction(
            name="输出",
            description="输出内容到控制台",
            parameters=[
                APIParameter("content", "任意", "要输出的内容", required=True)
            ],
            return_type="空",
            return_description="无返回值",
            examples=[
                "输出(\"Hello, World!\")",
                "输出(123)",
                "输出(变量)"
            ],
            category="输入输出"
        ))
        
        self.add_function(APIFunction(
            name="输入",
            description="从控制台读取用户输入",
            parameters=[
                APIParameter("prompt", "字符串", "提示信息", default="", required=False)
            ],
            return_type="字符串",
            return_description="用户输入的内容",
            examples=[
                "定义 name 为 输入(\"请输入姓名: \")",
                "定义 age 为 输入()"
            ],
            category="输入输出"
        ))
    
    def add_function(self, func: APIFunction) -> None:
        """
        添加函数文档
        
        Args:
            func: 函数文档对象
        """
        self.functions[func.name] = func
        
        if func.category not in self.categories:
            self.categories[func.category] = []
        
        self.categories[func.category].append(func.name)
    
    def get_function(self, name: str) -> Optional[APIFunction]:
        """
        获取函数文档
        
        Args:
            name: 函数名
            
        Returns:
            函数文档对象
        """
        return self.functions.get(name)
    
    def get_functions_by_category(self, category: str) -> List[APIFunction]:
        """
        按分类获取函数
        
        Args:
            category: 分类名
            
        Returns:
            函数列表
        """
        if category not in self.categories:
            return []
        
        return [
            self.functions[name] 
            for name in self.categories[category]
        ]
    
    def generate_markdown(self) -> str:
        """
        生成Markdown格式文档
        
        Returns:
            Markdown文档
        """
        lines = []
        
        lines.append("# 言律语言标准库API文档\n")
        lines.append("本文档提供言律语言标准库函数的详细说明和使用示例。\n")
        
        # 按分类生成
        for category in sorted(self.categories.keys()):
            lines.append(f"\n## {category}\n")
            
            for func_name in self.categories[category]:
                func = self.functions[func_name]
                
                # 函数名和描述
                lines.append(f"\n### {func.name}\n")
                lines.append(f"{func.description}\n")
                
                # 参数
                if func.parameters:
                    lines.append("\n**参数:**\n")
                    lines.append("| 参数名 | 类型 | 描述 | 必需 |")
                    lines.append("|--------|------|------|------|")
                    
                    for param in func.parameters:
                        required = "是" if param.required else "否"
                        lines.append(
                            f"| {param.name} | {param.type} | "
                            f"{param.description} | {required} |"
                        )
                
                # 返回值
                lines.append(f"\n**返回值:** {func.return_type}\n")
                lines.append(f"{func.return_description}\n")
                
                # 示例
                if func.examples:
                    lines.append("\n**示例:**\n")
                    lines.append("```yanlv")
                    for example in func.examples:
                        lines.append(example)
                    lines.append("```\n")
        
        return '\n'.join(lines)
    
    def generate_html(self) -> str:
        """
        生成HTML格式文档
        
        Returns:
            HTML文档
        """
        lines = []
        
        lines.append("<!DOCTYPE html>")
        lines.append("<html lang='zh-CN'>")
        lines.append("<head>")
        lines.append("<meta charset='UTF-8'>")
        lines.append("<title>言律语言API文档</title>")
        lines.append("<style>")
        lines.append("body { font-family: Arial, sans-serif; margin: 20px; }")
        lines.append("h1 { color: #333; }")
        lines.append("h2 { color: #666; margin-top: 30px; }")
        lines.append("h3 { color: #999; }")
        lines.append("table { border-collapse: collapse; width: 100%; }")
        lines.append("th, td { border: 1px solid #ddd; padding: 8px; }")
        lines.append("th { background-color: #f2f2f2; }")
        lines.append("code { background-color: #f4f4f4; padding: 2px; }")
        lines.append("pre { background-color: #f4f4f4; padding: 10px; }")
        lines.append("</style>")
        lines.append("</head>")
        lines.append("<body>")
        
        lines.append("<h1>言律语言标准库API文档</h1>")
        lines.append("<p>本文档提供言律语言标准库函数的详细说明和使用示例。</p>")
        
        # 按分类生成
        for category in sorted(self.categories.keys()):
            lines.append(f"<h2>{category}</h2>")
            
            for func_name in self.categories[category]:
                func = self.functions[func_name]
                
                # 函数名和描述
                lines.append(f"<h3>{func.name}</h3>")
                lines.append(f"<p>{func.description}</p>")
                
                # 参数
                if func.parameters:
                    lines.append("<h4>参数</h4>")
                    lines.append("<table>")
                    lines.append("<tr><th>参数名</th><th>类型</th><th>描述</th><th>必需</th></tr>")
                    
                    for param in func.parameters:
                        required = "是" if param.required else "否"
                        lines.append(
                            f"<tr><td>{param.name}</td><td>{param.type}</td>"
                            f"<td>{param.description}</td><td>{required}</td></tr>"
                        )
                    
                    lines.append("</table>")
                
                # 返回值
                lines.append(f"<h4>返回值</h4>")
                lines.append(f"<p><strong>类型:</strong> {func.return_type}</p>")
                lines.append(f"<p>{func.return_description}</p>")
                
                # 示例
                if func.examples:
                    lines.append("<h4>示例</h4>")
                    lines.append("<pre><code>")
                    for example in func.examples:
                        lines.append(example)
                    lines.append("</code></pre>")
        
        lines.append("</body>")
        lines.append("</html>")
        
        return '\n'.join(lines)


# 全局文档生成器实例
_global_generator: Optional[APIDocGenerator] = None


def get_api_doc_generator() -> APIDocGenerator:
    """获取全局文档生成器"""
    global _global_generator
    if _global_generator is None:
        _global_generator = APIDocGenerator()
    return _global_generator
