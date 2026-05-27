"""
言律语言意合式函数调用处理器

实现参数推断、链式调用和语义关联
"""

from typing import List, Dict, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum


class ParameterType(Enum):
    """参数类型"""
    NUMBER = "NUMBER"
    STRING = "STRING"
    BOOLEAN = "BOOLEAN"
    ARRAY = "ARRAY"
    OBJECT = "OBJECT"
    FUNCTION = "FUNCTION"
    ANY = "ANY"


@dataclass
class Parameter:
    """参数定义"""
    name: str
    param_type: ParameterType = ParameterType.ANY
    default_value: Optional[Any] = None
    is_optional: bool = False


@dataclass
class FunctionSignature:
    """函数签名"""
    name: str
    parameters: List[Parameter] = field(default_factory=list)
    return_type: ParameterType = ParameterType.ANY
    description: str = ""


@dataclass
class CallContext:
    """调用上下文"""
    available_variables: Dict[str, Any] = field(default_factory=dict)
    recent_values: List[Any] = field(default_factory=list)
    type_hints: Dict[str, ParameterType] = field(default_factory=dict)


class ImplicitCallResolver:
    """意合式调用解析器"""
    
    def __init__(self):
        """初始化解析器"""
        self.function_signatures: Dict[str, FunctionSignature] = {}
        self.call_context = CallContext()
        
        # 注册内置函数签名
        self._register_builtin_functions()
    
    def _register_builtin_functions(self):
        """注册内置函数签名"""
        # 数学函数
        self.function_signatures['加'] = FunctionSignature(
            name='加',
            parameters=[
                Parameter('a', ParameterType.NUMBER),
                Parameter('b', ParameterType.NUMBER)
            ],
            return_type=ParameterType.NUMBER
        )
        
        self.function_signatures['减'] = FunctionSignature(
            name='减',
            parameters=[
                Parameter('a', ParameterType.NUMBER),
                Parameter('b', ParameterType.NUMBER)
            ],
            return_type=ParameterType.NUMBER
        )
        
        self.function_signatures['乘'] = FunctionSignature(
            name='乘',
            parameters=[
                Parameter('a', ParameterType.NUMBER),
                Parameter('b', ParameterType.NUMBER)
            ],
            return_type=ParameterType.NUMBER
        )
        
        self.function_signatures['除'] = FunctionSignature(
            name='除',
            parameters=[
                Parameter('a', ParameterType.NUMBER),
                Parameter('b', ParameterType.NUMBER)
            ],
            return_type=ParameterType.NUMBER
        )
        
        # 数组函数
        self.function_signatures['映射'] = FunctionSignature(
            name='映射',
            parameters=[
                Parameter('array', ParameterType.ARRAY),
                Parameter('func', ParameterType.FUNCTION)
            ],
            return_type=ParameterType.ARRAY
        )
        
        self.function_signatures['过滤'] = FunctionSignature(
            name='过滤',
            parameters=[
                Parameter('array', ParameterType.ARRAY),
                Parameter('condition', ParameterType.FUNCTION)
            ],
            return_type=ParameterType.ARRAY
        )
        
        self.function_signatures['归约'] = FunctionSignature(
            name='归约',
            parameters=[
                Parameter('array', ParameterType.ARRAY),
                Parameter('func', ParameterType.FUNCTION),
                Parameter('initial', ParameterType.ANY)
            ],
            return_type=ParameterType.ANY
        )
        
        # 字符串函数
        self.function_signatures['连接'] = FunctionSignature(
            name='连接',
            parameters=[
                Parameter('str1', ParameterType.STRING),
                Parameter('str2', ParameterType.STRING)
            ],
            return_type=ParameterType.STRING
        )
        
        self.function_signatures['分割'] = FunctionSignature(
            name='分割',
            parameters=[
                Parameter('str', ParameterType.STRING),
                Parameter('separator', ParameterType.STRING)
            ],
            return_type=ParameterType.ARRAY
        )
    
    def infer_parameters(self, func_name: str, 
                        provided_args: List[Any],
                        context: CallContext) -> List[Any]:
        """
        推断参数
        
        Args:
            func_name: 函数名
            provided_args: 提供的参数
            context: 调用上下文
            
        Returns:
            完整的参数列表
        """
        if func_name not in self.function_signatures:
            return provided_args
        
        signature = self.function_signatures[func_name]
        expected_params = signature.parameters
        
        # 如果参数数量匹配，直接返回
        if len(provided_args) == len(expected_params):
            return provided_args
        
        # 如果参数不足，尝试推断
        inferred_args = list(provided_args)
        
        for i in range(len(provided_args), len(expected_params)):
            param = expected_params[i]
            
            # 尝试从上下文推断
            inferred_value = self._infer_from_context(param, context)
            
            if inferred_value is not None:
                inferred_args.append(inferred_value)
            elif param.default_value is not None:
                inferred_args.append(param.default_value)
            elif param.is_optional:
                # 可选参数，跳过
                pass
            else:
                # 无法推断，使用默认值
                inferred_args.append(self._get_default_for_type(param.param_type))
        
        return inferred_args
    
    def _infer_from_context(self, param: Parameter, 
                           context: CallContext) -> Optional[Any]:
        """从上下文推断参数值"""
        # 检查最近的值
        if context.recent_values:
            for value in reversed(context.recent_values):
                if self._type_matches(value, param.param_type):
                    return value
        
        # 检查可用变量
        for var_name, var_value in context.available_variables.items():
            if self._type_matches(var_value, param.param_type):
                return var_value
        
        return None
    
    def _type_matches(self, value: Any, param_type: ParameterType) -> bool:
        """检查类型是否匹配"""
        if param_type == ParameterType.ANY:
            return True
        
        type_checks = {
            ParameterType.NUMBER: lambda v: isinstance(v, (int, float)),
            ParameterType.STRING: lambda v: isinstance(v, str),
            ParameterType.BOOLEAN: lambda v: isinstance(v, bool),
            ParameterType.ARRAY: lambda v: isinstance(v, list),
            ParameterType.OBJECT: lambda v: isinstance(v, dict),
            ParameterType.FUNCTION: lambda v: callable(v),
        }
        
        return type_checks.get(param_type, lambda v: True)(value)
    
    def _get_default_for_type(self, param_type: ParameterType) -> Any:
        """获取类型的默认值"""
        defaults = {
            ParameterType.NUMBER: 0,
            ParameterType.STRING: "",
            ParameterType.BOOLEAN: False,
            ParameterType.ARRAY: [],
            ParameterType.OBJECT: {},
            ParameterType.FUNCTION: lambda x: x,
            ParameterType.ANY: None,
        }
        return defaults.get(param_type, None)
    
    def resolve_chain_call(self, calls: List[Tuple[str, List[Any]]],
                          initial_value: Any,
                          context: CallContext) -> Any:
        """
        解析链式调用
        
        Args:
            calls: 调用列表 [(函数名, 参数列表), ...]
            initial_value: 初始值
            context: 调用上下文
            
        Returns:
            最终结果
        """
        result = initial_value
        
        for func_name, args in calls:
            # 将前一个结果作为第一个参数
            full_args = [result] + args
            
            # 推断参数
            inferred_args = self.infer_parameters(func_name, full_args, context)
            
            # 执行函数（这里返回模拟结果）
            result = self._execute_function(func_name, inferred_args)
            
            # 更新上下文
            context.recent_values.append(result)
        
        return result
    
    def _execute_function(self, func_name: str, args: List[Any]) -> Any:
        """执行函数（模拟）"""
        # 这里返回一个模拟结果
        # 实际实现会调用真实的函数
        if func_name in ['加', '减', '乘', '除']:
            if len(args) >= 2:
                if func_name == '加':
                    return args[0] + args[1]
                elif func_name == '减':
                    return args[0] - args[1]
                elif func_name == '乘':
                    return args[0] * args[1]
                elif func_name == '除':
                    return args[0] / args[1] if args[1] != 0 else 0
        
        return args[0] if args else None
    
    def parse_implicit_call(self, text: str) -> Tuple[str, List[Any]]:
        """
        解析意合式调用文本
        
        Args:
            text: 调用文本
            
        Returns:
            (函数名, 参数列表)
        """
        # 简化实现：分割空格
        parts = text.split()
        
        if not parts:
            return ('', [])
        
        func_name = parts[0]
        args = []
        
        for part in parts[1:]:
            # 尝试解析为数字
            try:
                args.append(float(part))
            except ValueError:
                # 作为字符串或变量名
                args.append(part)
        
        return (func_name, args)


class ChainCallBuilder:
    """链式调用构建器"""
    
    def __init__(self, resolver: ImplicitCallResolver):
        """初始化构建器"""
        self.resolver = resolver
        self.calls: List[Tuple[str, List[Any]]] = []
        self.initial_value: Any = None
    
    def with_value(self, value: Any) -> 'ChainCallBuilder':
        """设置初始值"""
        self.initial_value = value
        return self
    
    def then(self, func_name: str, *args) -> 'ChainCallBuilder':
        """添加调用"""
        self.calls.append((func_name, list(args)))
        return self
    
    def execute(self, context: CallContext = None) -> Any:
        """执行链式调用"""
        if context is None:
            context = CallContext()
        
        return self.resolver.resolve_chain_call(
            self.calls,
            self.initial_value,
            context
        )


# ============================================================================
# 辅助函数
# ============================================================================

def create_implicit_call_resolver() -> ImplicitCallResolver:
    """创建意合式调用解析器"""
    return ImplicitCallResolver()


def create_chain_builder(resolver: ImplicitCallResolver = None) -> ChainCallBuilder:
    """创建链式调用构建器"""
    if resolver is None:
        resolver = create_implicit_call_resolver()
    return ChainCallBuilder(resolver)


# ============================================================================
# 导出
# ============================================================================

__all__ = [
    'ParameterType',
    'Parameter',
    'FunctionSignature',
    'CallContext',
    'ImplicitCallResolver',
    'ChainCallBuilder',
    'create_implicit_call_resolver',
    'create_chain_builder',
]
