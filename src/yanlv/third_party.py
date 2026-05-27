"""
言律语言第三方库集成机制

支持调用numpy、pandas等Python第三方库
"""

from typing import Any, Dict, List, Optional, Callable
import importlib
import sys


class ThirdPartyLibrary:
    """第三方库包装类"""
    
    def __init__(self, module_name: str, alias: Optional[str] = None):
        """
        初始化第三方库
        
        Args:
            module_name: Python模块名
            alias: 别名
        """
        self.module_name = module_name
        self.alias = alias or module_name
        self.module = None
        self._functions: Dict[str, Callable] = {}
        
        # 尝试导入模块
        try:
            self.module = importlib.import_module(module_name)
        except ImportError:
            pass
    
    def is_available(self) -> bool:
        """检查库是否可用"""
        return self.module is not None
    
    def get_function(self, func_name: str) -> Optional[Callable]:
        """
        获取函数
        
        Args:
            func_name: 函数名
            
        Returns:
            函数对象
        """
        if not self.is_available():
            return None
        
        # 从缓存获取
        if func_name in self._functions:
            return self._functions[func_name]
        
        # 从模块获取
        if hasattr(self.module, func_name):
            func = getattr(self.module, func_name)
            self._functions[func_name] = func
            return func
        
        return None
    
    def call_function(self, func_name: str, *args, **kwargs) -> Any:
        """
        调用函数
        
        Args:
            func_name: 函数名
            args: 位置参数
            kwargs: 关键字参数
            
        Returns:
            函数返回值
        """
        func = self.get_function(func_name)
        if func is None:
            raise AttributeError(f"模块 {self.module_name} 没有函数 {func_name}")
        
        return func(*args, **kwargs)
    
    def list_functions(self) -> List[str]:
        """列出所有可用函数"""
        if not self.is_available():
            return []
        
        functions = []
        for name in dir(self.module):
            if not name.startswith('_'):
                attr = getattr(self.module, name)
                if callable(attr):
                    functions.append(name)
        
        return functions


class ThirdPartyIntegration:
    """
    第三方库集成管理器
    
    管理所有第三方库的导入和调用
    """
    
    def __init__(self):
        """初始化集成管理器"""
        self.libraries: Dict[str, ThirdPartyLibrary] = {}
        self._init_common_libraries()
    
    def _init_common_libraries(self) -> None:
        """初始化常用库"""
        # 预定义常用库
        common_libs = [
            ("numpy", "np"),
            ("pandas", "pd"),
            ("requests", "req"),
            ("matplotlib.pyplot", "plt"),
            ("scipy", "sp"),
            ("sklearn", "sk"),
        ]
        
        for module_name, alias in common_libs:
            self.libraries[alias] = ThirdPartyLibrary(module_name, alias)
    
    def import_library(self, module_name: str, alias: Optional[str] = None) -> bool:
        """
        导入第三方库
        
        Args:
            module_name: Python模块名
            alias: 别名
            
        Returns:
            是否成功
        """
        lib = ThirdPartyLibrary(module_name, alias)
        
        if not lib.is_available():
            return False
        
        key = alias or module_name
        self.libraries[key] = lib
        return True
    
    def get_library(self, alias: str) -> Optional[ThirdPartyLibrary]:
        """
        获取库
        
        Args:
            alias: 别名
            
        Returns:
            第三方库对象
        """
        return self.libraries.get(alias)
    
    def call_function(self, lib_alias: str, func_name: str, *args, **kwargs) -> Any:
        """
        调用第三方库函数
        
        Args:
            lib_alias: 库别名
            func_name: 函数名
            args: 位置参数
            kwargs: 关键字参数
            
        Returns:
            函数返回值
        """
        lib = self.get_library(lib_alias)
        if lib is None:
            raise ImportError(f"未导入库: {lib_alias}")
        
        return lib.call_function(func_name, *args, **kwargs)
    
    def list_available_libraries(self) -> List[str]:
        """列出所有可用的库"""
        return [
            alias for alias, lib in self.libraries.items()
            if lib.is_available()
        ]
    
    def list_library_functions(self, alias: str) -> List[str]:
        """
        列出库的所有函数
        
        Args:
            alias: 库别名
            
        Returns:
            函数名列表
        """
        lib = self.get_library(alias)
        if lib is None:
            return []
        
        return lib.list_functions()


class NumpyAdapter:
    """NumPy适配器"""
    
    def __init__(self, integration: ThirdPartyIntegration):
        """
        初始化适配器
        
        Args:
            integration: 第三方库集成管理器
        """
        self.integration = integration
        self.np = integration.get_library("np")
    
    def is_available(self) -> bool:
        """检查NumPy是否可用"""
        return self.np is not None and self.np.is_available()
    
    def array(self, data: List) -> Any:
        """创建数组"""
        if not self.is_available():
            raise ImportError("NumPy未安装")
        return self.np.call_function("array", data)
    
    def zeros(self, shape: tuple) -> Any:
        """创建零数组"""
        if not self.is_available():
            raise ImportError("NumPy未安装")
        return self.np.call_function("zeros", shape)
    
    def ones(self, shape: tuple) -> Any:
        """创建全1数组"""
        if not self.is_available():
            raise ImportError("NumPy未安装")
        return self.np.call_function("ones", shape)
    
    def mean(self, arr: Any) -> float:
        """计算均值"""
        if not self.is_available():
            raise ImportError("NumPy未安装")
        return self.np.call_function("mean", arr)
    
    def sum(self, arr: Any) -> float:
        """计算总和"""
        if not self.is_available():
            raise ImportError("NumPy未安装")
        return self.np.call_function("sum", arr)


class PandasAdapter:
    """Pandas适配器"""
    
    def __init__(self, integration: ThirdPartyIntegration):
        """
        初始化适配器
        
        Args:
            integration: 第三方库集成管理器
        """
        self.integration = integration
        self.pd = integration.get_library("pd")
    
    def is_available(self) -> bool:
        """检查Pandas是否可用"""
        return self.pd is not None and self.pd.is_available()
    
    def DataFrame(self, data: Dict) -> Any:
        """创建DataFrame"""
        if not self.is_available():
            raise ImportError("Pandas未安装")
        return self.pd.call_function("DataFrame", data)
    
    def read_csv(self, filepath: str) -> Any:
        """读取CSV文件"""
        if not self.is_available():
            raise ImportError("Pandas未安装")
        return self.pd.call_function("read_csv", filepath)
    
    def read_json(self, filepath: str) -> Any:
        """读取JSON文件"""
        if not self.is_available():
            raise ImportError("Pandas未安装")
        return self.pd.call_function("read_json", filepath)


class RequestsAdapter:
    """Requests适配器"""
    
    def __init__(self, integration: ThirdPartyIntegration):
        """
        初始化适配器
        
        Args:
            integration: 第三方库集成管理器
        """
        self.integration = integration
        self.req = integration.get_library("req")
    
    def is_available(self) -> bool:
        """检查Requests是否可用"""
        return self.req is not None and self.req.is_available()
    
    def get(self, url: str, **kwargs) -> Any:
        """GET请求"""
        if not self.is_available():
            raise ImportError("Requests未安装")
        return self.req.call_function("get", url, **kwargs)
    
    def post(self, url: str, **kwargs) -> Any:
        """POST请求"""
        if not self.is_available():
            raise ImportError("Requests未安装")
        return self.req.call_function("post", url, **kwargs)


# 全局集成管理器实例
_global_integration: Optional[ThirdPartyIntegration] = None


def get_integration() -> ThirdPartyIntegration:
    """获取全局集成管理器"""
    global _global_integration
    if _global_integration is None:
        _global_integration = ThirdPartyIntegration()
    return _global_integration
