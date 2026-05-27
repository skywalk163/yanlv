"""
言律语言类型注解支持

提供类型注解、类型检查和类型提示功能
"""

from typing import Any, Dict, List, Optional, Union
from dataclasses import dataclass
from enum import Enum


class YanLvType(Enum):
    """言律语言基本类型"""
    整数 = "整数"
    浮点数 = "浮点数"
    字符串 = "字符串"
    布尔 = "布尔"
    列表 = "列表"
    字典 = "字典"
    空 = "空"
    任意 = "任意"


@dataclass
class TypeAnnotation:
    """类型注解"""
    base_type: YanLvType              # 基本类型
    generic_args: Optional[List['TypeAnnotation']] = None  # 泛型参数
    is_optional: bool = False         # 是否可选(可为空)
    custom_type: Optional[str] = None # 自定义类型名
    
    def __str__(self) -> str:
        """转换为字符串表示"""
        if self.custom_type:
            type_str = self.custom_type
        else:
            type_str = self.base_type.value
        
        if self.generic_args:
            args_str = ", ".join(str(arg) for arg in self.generic_args)
            type_str = f"{type_str}[{args_str}]"
        
        if self.is_optional:
            type_str = f"{type_str}?"
        
        return type_str


class TypeChecker:
    """类型检查器"""
    
    def __init__(self):
        """初始化类型检查器"""
        self.type_map: Dict[str, TypeAnnotation] = {}
        self.errors: List[str] = []
    
    def register_type(self, name: str, type_annotation: TypeAnnotation) -> None:
        """
        注册变量类型
        
        Args:
            name: 变量名
            type_annotation: 类型注解
        """
        self.type_map[name] = type_annotation
    
    def get_type(self, name: str) -> Optional[TypeAnnotation]:
        """
        获取变量类型
        
        Args:
            name: 变量名
            
        Returns:
            类型注解
        """
        return self.type_map.get(name)
    
    def check_type(self, name: str, value: Any) -> bool:
        """
        检查值是否符合类型
        
        Args:
            name: 变量名
            value: 值
            
        Returns:
            是否符合类型
        """
        type_annotation = self.get_type(name)
        if type_annotation is None:
            return True  # 没有类型注解,默认通过
        
        return self._check_value_type(value, type_annotation)
    
    def _check_value_type(self, value: Any, type_annotation: TypeAnnotation) -> bool:
        """
        检查值类型
        
        Args:
            value: 值
            type_annotation: 类型注解
            
        Returns:
            是否符合类型
        """
        # 检查可选类型
        if type_annotation.is_optional and value is None:
            return True
        
        # 检查自定义类型
        if type_annotation.custom_type:
            # 简化实现:假设自定义类型总是匹配
            return True
        
        # 检查基本类型
        base_type = type_annotation.base_type
        
        if base_type == YanLvType.整数:
            return isinstance(value, int) and not isinstance(value, bool)
        elif base_type == YanLvType.浮点数:
            return isinstance(value, (int, float)) and not isinstance(value, bool)
        elif base_type == YanLvType.字符串:
            return isinstance(value, str)
        elif base_type == YanLvType.布尔:
            return isinstance(value, bool)
        elif base_type == YanLvType.列表:
            if not isinstance(value, list):
                return False
            # 检查泛型参数
            if type_annotation.generic_args:
                element_type = type_annotation.generic_args[0]
                return all(self._check_value_type(item, element_type) for item in value)
            return True
        elif base_type == YanLvType.字典:
            if not isinstance(value, dict):
                return False
            # 检查泛型参数
            if type_annotation.generic_args and len(type_annotation.generic_args) == 2:
                key_type = type_annotation.generic_args[0]
                value_type = type_annotation.generic_args[1]
                return all(
                    self._check_value_type(k, key_type) and self._check_value_type(v, value_type)
                    for k, v in value.items()
                )
            return True
        elif base_type == YanLvType.空:
            return value is None
        elif base_type == YanLvType.任意:
            return True
        
        return False
    
    def add_error(self, error: str) -> None:
        """
        添加类型错误
        
        Args:
            error: 错误信息
        """
        self.errors.append(error)
    
    def get_errors(self) -> List[str]:
        """获取所有类型错误"""
        return self.errors.copy()
    
    def clear_errors(self) -> None:
        """清空错误列表"""
        self.errors.clear()


class TypeInferrer:
    """类型推断器"""
    
    @staticmethod
    def infer_type(value: Any) -> TypeAnnotation:
        """
        推断值的类型
        
        Args:
            value: 值
            
        Returns:
            类型注解
        """
        if value is None:
            return TypeAnnotation(base_type=YanLvType.空)
        elif isinstance(value, bool):
            return TypeAnnotation(base_type=YanLvType.布尔)
        elif isinstance(value, int):
            return TypeAnnotation(base_type=YanLvType.整数)
        elif isinstance(value, float):
            return TypeAnnotation(base_type=YanLvType.浮点数)
        elif isinstance(value, str):
            return TypeAnnotation(base_type=YanLvType.字符串)
        elif isinstance(value, list):
            # 推断列表元素类型
            if value:
                element_type = TypeInferrer.infer_type(value[0])
                return TypeAnnotation(
                    base_type=YanLvType.列表,
                    generic_args=[element_type]
                )
            return TypeAnnotation(base_type=YanLvType.列表)
        elif isinstance(value, dict):
            # 推断字典键值类型
            if value:
                first_key = next(iter(value))
                key_type = TypeInferrer.infer_type(first_key)
                value_type = TypeInferrer.infer_type(value[first_key])
                return TypeAnnotation(
                    base_type=YanLvType.字典,
                    generic_args=[key_type, value_type]
                )
            return TypeAnnotation(base_type=YanLvType.字典)
        else:
            return TypeAnnotation(base_type=YanLvType.任意)


class TypeAnnotationParser:
    """类型注解解析器"""
    
    @staticmethod
    def parse(type_str: str) -> TypeAnnotation:
        """
        解析类型字符串
        
        Args:
            type_str: 类型字符串
            
        Returns:
            类型注解
        """
        # 去除空白
        type_str = type_str.strip()
        
        # 检查是否可选
        is_optional = type_str.endswith("?")
        if is_optional:
            type_str = type_str[:-1].strip()
        
        # 检查泛型参数
        if "[" in type_str and "]" in type_str:
            base_str = type_str[:type_str.index("[")].strip()
            args_str = type_str[type_str.index("[")+1:type_str.rindex("]")].strip()
            
            # 解析泛型参数
            generic_args = TypeAnnotationParser._parse_generic_args(args_str)
            
            # 解析基本类型
            base_type = TypeAnnotationParser._parse_base_type(base_str)
            
            return TypeAnnotation(
                base_type=base_type,
                generic_args=generic_args,
                is_optional=is_optional
            )
        else:
            # 解析基本类型
            base_type = TypeAnnotationParser._parse_base_type(type_str)
            
            return TypeAnnotation(
                base_type=base_type,
                is_optional=is_optional
            )
    
    @staticmethod
    def _parse_base_type(type_str: str) -> YanLvType:
        """解析基本类型"""
        type_map = {
            "整数": YanLvType.整数,
            "浮点数": YanLvType.浮点数,
            "字符串": YanLvType.字符串,
            "布尔": YanLvType.布尔,
            "列表": YanLvType.列表,
            "字典": YanLvType.字典,
            "空": YanLvType.空,
            "任意": YanLvType.任意
        }
        
        return type_map.get(type_str, YanLvType.任意)
    
    @staticmethod
    def _parse_generic_args(args_str: str) -> List[TypeAnnotation]:
        """解析泛型参数"""
        # 简化实现:按逗号分割
        args = []
        current_arg = ""
        bracket_count = 0
        
        for char in args_str:
            if char == "[":
                bracket_count += 1
                current_arg += char
            elif char == "]":
                bracket_count -= 1
                current_arg += char
            elif char == "," and bracket_count == 0:
                if current_arg.strip():
                    args.append(TypeAnnotationParser.parse(current_arg.strip()))
                current_arg = ""
            else:
                current_arg += char
        
        if current_arg.strip():
            args.append(TypeAnnotationParser.parse(current_arg.strip()))
        
        return args


# 类型注解装饰器
def type_hint(**kwargs):
    """
    类型注解装饰器
    
    Args:
        kwargs: 参数类型映射
        
    Returns:
        装饰器函数
    """
    def decorator(func):
        func._type_hints = kwargs
        return func
    return decorator


# 全局类型检查器实例
_global_type_checker: Optional[TypeChecker] = None


def get_type_checker() -> TypeChecker:
    """获取全局类型检查器"""
    global _global_type_checker
    if _global_type_checker is None:
        _global_type_checker = TypeChecker()
    return _global_type_checker
