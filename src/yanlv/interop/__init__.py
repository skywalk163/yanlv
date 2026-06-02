"""
言律语言互操作系统 - 实现示例

提供与主流语言（Python、JavaScript、SQL等）的互操作能力
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
import ast
import json


# ============================================================================
# 核心接口
# ============================================================================

class Track(ABC):
    """轨基类 - 定义互操作接口"""

    @abstractmethod
    def execute(self, code: str, context: Dict[str, Any]) -> Any:
        """
        执行代码

        Args:
            code: 外部语言代码
            context: 执行上下文（变量、函数等）

        Returns:
            执行结果
        """
        pass

    @abstractmethod
    def validate(self, code: str) -> Dict[str, Any]:
        """
        验证代码

        Args:
            code: 外部语言代码

        Returns:
            验证结果 {"valid": bool, "errors": List[str]}
        """
        pass

    @abstractmethod
    def get_capabilities(self) -> List[str]:
        """
        获取轨的能力

        Returns:
            能力列表，如 ["async", "modules", "classes"]
        """
        pass

    @abstractmethod
    def convert_type(self, value: Any, target_type: str) -> Any:
        """
        类型转换

        Args:
            value: 值
            target_type: 目标类型

        Returns:
            转换后的值
        """
        pass


# ============================================================================
# 轨管理器
# ============================================================================

class TrackManager:
    """轨管理器 - 管理所有轨实例"""

    def __init__(self):
        self.tracks: Dict[str, Track] = {}
        self.active_track: Optional[str] = None

    def register_track(self, name: str, track: Track) -> None:
        """注册轨"""
        self.tracks[name] = track

    def get_track(self, name: str) -> Optional[Track]:
        """获取轨"""
        return self.tracks.get(name)

    def execute_in_track(self, track_name: str, code: str,
                        context: Dict[str, Any]) -> Any:
        """在指定轨中执行代码"""
        track = self.get_track(track_name)
        if not track:
            raise ValueError(f"未找到轨: {track_name}")

        return track.execute(code, context)

    def list_tracks(self) -> List[str]:
        """列出所有轨"""
        return list(self.tracks.keys())


# ============================================================================
# Python轨实现
# ============================================================================

class PythonTrack(Track):
    """Python轨 - 嵌入Python代码"""

    def __init__(self):
        self.globals: Dict[str, Any] = {}
        self.locals: Dict[str, Any] = {}

    def execute(self, code: str, context: Dict[str, Any]) -> Any:
        """
        执行Python代码

        支持三种模式：
        1. 表达式模式 - 返回表达式值
        2. 语句模式 - 执行语句，返回None
        3. 函数模式 - 执行函数定义，返回函数
        """
        # 合并上下文
        exec_globals = {**self.globals, **context}
        exec_locals = self.locals.copy()

        try:
            # 尝试作为表达式执行
            result = eval(code, exec_globals, exec_locals)
            return result
        except SyntaxError:
            # 作为语句执行
            exec(code, exec_globals, exec_locals)

            # 更新全局和局部变量
            self.globals.update(exec_globals)
            self.locals.update(exec_locals)

            # 检查是否定义了函数
            try:
                tree = ast.parse(code)
                for node in reversed(tree.body):
                    if isinstance(node, ast.FunctionDef):
                        func = exec_locals.get(node.name)
                        if func:
                            # 确保函数能访问到全局变量
                            func.__globals__.update(exec_globals)
                        return func
            except:
                pass

            return None

    def validate(self, code: str) -> Dict[str, Any]:
        """验证Python代码语法"""
        try:
            ast.parse(code)
            return {"valid": True, "errors": []}
        except SyntaxError as e:
            return {
                "valid": False,
                "errors": [f"语法错误 (行{e.lineno}): {e.msg}"]
            }

    def get_capabilities(self) -> List[str]:
        """Python轨能力"""
        return [
            "async",           # 支持异步
            "modules",         # 支持模块导入
            "classes",         # 支持类定义
            "exceptions",      # 支持异常处理
            "generators",      # 支持生成器
            "decorators",      # 支持装饰器
        ]

    def convert_type(self, value: Any, target_type: str) -> Any:
        """类型转换"""
        type_map = {
            "int": int,
            "float": float,
            "str": str,
            "bool": bool,
            "list": list,
            "dict": dict,
        }

        if target_type in type_map:
            try:
                return type_map[target_type](value)
            except:
                return value

        return value


# ============================================================================
# 类型转换系统
# ============================================================================

class TypeConverter:
    """类型转换器"""

    # 言律类型 <-> Python类型 <-> JavaScript类型
    type_mappings = {
        "yanlv": {
            "整数": "int",
            "小数": "float",
            "文本": "str",
            "布尔": "bool",
            "列表": "list",
            "字典": "dict",
        },
        "python": {
            "int": "整数",
            "float": "小数",
            "str": "文本",
            "bool": "布尔",
            "list": "列表",
            "dict": "字典",
        },
        "javascript": {
            "number": "小数",
            "string": "文本",
            "boolean": "布尔",
            "array": "列表",
            "object": "字典",
        }
    }

    @staticmethod
    def convert(value: Any, from_lang: str, to_lang: str) -> Any:
        """跨语言类型转换"""
        # 获取值的类型
        from_type = type(value).__name__

        # 查找映射
        from_mapping = TypeConverter.type_mappings.get(from_lang, {})
        to_mapping = TypeConverter.type_mappings.get(to_lang, {})

        # 转换类型
        common_type = from_mapping.get(from_type, from_type)
        target_type = to_mapping.get(common_type, common_type)

        # 执行转换
        return TypeConverter._convert_value(value, target_type)

    @staticmethod
    def _convert_value(value: Any, target_type: str) -> Any:
        """执行实际的类型转换"""
        converters = {
            "int": int,
            "float": float,
            "str": str,
            "bool": bool,
            "list": list,
            "dict": dict,
        }

        if target_type in converters:
            try:
                return converters[target_type](value)
            except:
                return value

        return value


# ============================================================================
# 错误处理
# ============================================================================

class InteropError(Exception):
    """互操作错误基类"""
    pass


class ExecutionError(InteropError):
    """执行错误"""
    def __init__(self, lang: str, message: str, details: Dict = None):
        self.lang = lang
        self.message = message
        self.details = details or {}
        super().__init__(f"[{lang}] {message}")


class TypeConversionError(InteropError):
    """类型转换错误"""
    def __init__(self, value: Any, from_type: str, to_type: str):
        self.value = value
        self.from_type = from_type
        self.to_type = to_type
        super().__init__(
            f"无法将 {from_type} 类型的值 {value} 转换为 {to_type}"
        )


# ============================================================================
# 使用示例
# ============================================================================

def example_usage():
    """使用示例"""
    print("=" * 60)
    print("言律语言互操作系统 - 使用示例")
    print("=" * 60)

    # 1. 创建轨管理器
    manager = TrackManager()

    # 2. 注册Python轨
    python_track = PythonTrack()
    manager.register_track("python", python_track)

    print("\n已注册的轨:", manager.list_tracks())

    # 3. 执行简单的Python表达式
    print("\n--- 示例1: 简单表达式 ---")
    result = manager.execute_in_track("python", "2 ** 10", {})
    print(f"2 ** 10 = {result}")

    # 4. 执行带上下文的代码
    print("\n--- 示例2: 带上下文执行 ---")
    context = {"x": 10, "y": 20}
    result = manager.execute_in_track("python", "x + y", context)
    print(f"x + y = {result}")

    # 5. 执行Python语句
    print("\n--- 示例3: 执行语句 ---")
    code = """
import math
radius = 5
area = math.pi * radius ** 2
"""
    manager.execute_in_track("python", code, {})
    result = manager.execute_in_track("python", "area", {})
    print(f"圆面积 (r=5) = {result:.2f}")

    # 6. 定义和调用函数
    print("\n--- 示例4: 定义函数 ---")
    func_code = """
def square(x):
    return x * x

def add(a, b):
    return a + b
"""
    manager.execute_in_track("python", func_code, {})
    square_func = manager.execute_in_track("python", "square", {})
    add_func = manager.execute_in_track("python", "add", {})

    result1 = square_func(5)
    result2 = add_func(3, 7)
    print(f"square(5) = {result1}")
    print(f"add(3, 7) = {result2}")

    # 7. 使用Python库
    print("\n--- 示例5: 使用Python库 ---")
    stats_code = """
import statistics
data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
mean = statistics.mean(data)
median = statistics.median(data)
stdev = statistics.stdev(data)
result = {"mean": mean, "median": median, "stdev": stdev}
"""
    manager.execute_in_track("python", stats_code, {})
    result = manager.execute_in_track("python", "result", {})
    print(f"统计结果: {result}")

    # 8. 验证代码
    print("\n--- 示例6: 代码验证 ---")
    valid_code = "x = 10"
    invalid_code = "x = "

    valid_result = python_track.validate(valid_code)
    print(f"验证 '{valid_code}': {valid_result}")

    invalid_result = python_track.validate(invalid_code)
    print(f"验证 '{invalid_code}': {invalid_result}")

    # 9. 类型转换
    print("\n--- 示例7: 类型转换 ---")
    converter = TypeConverter()

    # Python int -> 言律整数
    value = 42
    converted = converter.convert(value, "python", "yanlv")
    print(f"Python {value} ({type(value).__name__}) -> 言律 {converted}")

    # Python list -> 言律列表
    value = [1, 2, 3, 4, 5]
    converted = converter.convert(value, "python", "yanlv")
    print(f"Python {value} -> 言律列表 {converted}")

    # 10. 查看轨的能力
    print("\n--- 示例8: 轨的能力 ---")
    capabilities = python_track.get_capabilities()
    print(f"Python轨能力: {capabilities}")

    print("\n" + "=" * 60)
    print("示例完成")
    print("=" * 60)


if __name__ == "__main__":
    example_usage()
