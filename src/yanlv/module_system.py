"""
言律语言模块系统

实现模块导入、导出和管理
"""

from typing import Any, Dict, List, Optional
import os
import sys
import importlib.util


class Module:
    """模块类"""
    
    def __init__(self, name: str, path: Optional[str] = None):
        """
        初始化模块
        
        Args:
            name: 模块名
            path: 模块路径
        """
        self.name = name
        self.path = path
        self.exports: Dict[str, Any] = {}
        self.imports: Dict[str, 'Module'] = {}
        self.loaded = False
    
    def add_export(self, name: str, value: Any) -> None:
        """
        添加导出项
        
        Args:
            name: 名称
            value: 值
        """
        self.exports[name] = value
    
    def get_export(self, name: str) -> Optional[Any]:
        """
        获取导出项
        
        Args:
            name: 名称
            
        Returns:
            导出的值
        """
        return self.exports.get(name)
    
    def list_exports(self) -> List[str]:
        """列出所有导出项"""
        return list(self.exports.keys())
    
    def add_import(self, alias: str, module: 'Module') -> None:
        """
        添加导入模块
        
        Args:
            alias: 别名
            module: 模块对象
        """
        self.imports[alias] = module
    
    def get_import(self, alias: str) -> Optional['Module']:
        """
        获取导入模块
        
        Args:
            alias: 别名
            
        Returns:
            模块对象
        """
        return self.imports.get(alias)


class ModuleManager:
    """
    模块管理器
    
    管理所有模块的导入和导出
    """
    
    def __init__(self):
        """初始化模块管理器"""
        self.modules: Dict[str, Module] = {}
        self.search_paths: List[str] = []
        self._init_search_paths()
    
    def _init_search_paths(self) -> None:
        """初始化搜索路径"""
        # 添加当前目录
        self.search_paths.append(os.getcwd())
        
        # 添加Python路径
        for path in sys.path:
            if path and path not in self.search_paths:
                self.search_paths.append(path)
    
    def add_search_path(self, path: str) -> None:
        """
        添加搜索路径
        
        Args:
            path: 路径
        """
        if path not in self.search_paths:
            self.search_paths.append(path)
    
    def find_module(self, name: str) -> Optional[str]:
        """
        查找模块文件
        
        Args:
            name: 模块名
            
        Returns:
            模块文件路径
        """
        # 尝试不同的文件名
        filenames = [
            f"{name}.yl",      # 言律语言文件
            f"{name}.py",      # Python文件
            f"{name}/__init__.yl",  # 言律语言包
            f"{name}/__init__.py",  # Python包
        ]
        
        for search_path in self.search_paths:
            for filename in filenames:
                filepath = os.path.join(search_path, filename)
                if os.path.exists(filepath):
                    return filepath
        
        return None
    
    def create_module(self, name: str, path: Optional[str] = None) -> Module:
        """
        创建模块
        
        Args:
            name: 模块名
            path: 模块路径
            
        Returns:
            模块对象
        """
        module = Module(name, path)
        self.modules[name] = module
        return module
    
    def get_module(self, name: str) -> Optional[Module]:
        """
        获取模块
        
        Args:
            name: 模块名
            
        Returns:
            模块对象
        """
        return self.modules.get(name)
    
    def load_module(self, name: str) -> Optional[Module]:
        """
        加载模块
        
        Args:
            name: 模块名
            
        Returns:
            模块对象
        """
        # 检查是否已加载
        if name in self.modules:
            return self.modules[name]
        
        # 查找模块文件
        path = self.find_module(name)
        if path is None:
            return None
        
        # 创建模块
        module = self.create_module(name, path)
        
        # 根据文件类型加载
        if path.endswith('.py'):
            self._load_python_module(module, path)
        elif path.endswith('.yl'):
            self._load_yanlv_module(module, path)
        
        module.loaded = True
        return module
    
    def _load_python_module(self, module: Module, path: str) -> None:
        """
        加载Python模块
        
        Args:
            module: 模块对象
            path: 文件路径
        """
        # 使用Python的导入机制
        spec = importlib.util.spec_from_file_location(module.name, path)
        if spec and spec.loader:
            py_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(py_module)
            
            # 导出所有非私有成员
            for name in dir(py_module):
                if not name.startswith('_'):
                    module.add_export(name, getattr(py_module, name))
    
    def _load_yanlv_module(self, module: Module, path: str) -> None:
        """
        加载言律模块
        
        Args:
            module: 模块对象
            path: 文件路径
        """
        # 读取文件内容
        try:
            with open(path, 'r', encoding='utf-8') as f:
                code = f.read()
            
            # 这里应该调用言律编译器来编译代码
            # 简化实现:直接存储代码
            module.add_export('__code__', code)
        except Exception as e:
            print(f"加载模块失败: {e}")
    
    def import_module(self, name: str, alias: Optional[str] = None) -> Optional[Module]:
        """
        导入模块
        
        Args:
            name: 模块名
            alias: 别名
            
        Returns:
            模块对象
        """
        module = self.load_module(name)
        if module is None:
            return None
        
        # 如果有别名,注册别名
        if alias:
            self.modules[alias] = module
        
        return module
    
    def import_from(self, module_name: str, names: List[str]) -> Dict[str, Any]:
        """
        从模块导入指定项
        
        Args:
            module_name: 模块名
            names: 要导入的名称列表
            
        Returns:
            导入项字典
        """
        module = self.load_module(module_name)
        if module is None:
            return {}
        
        result = {}
        for name in names:
            value = module.get_export(name)
            if value is not None:
                result[name] = value
        
        return result
    
    def export_all(self, module_name: str) -> Dict[str, Any]:
        """
        导出模块所有内容
        
        Args:
            module_name: 模块名
            
        Returns:
            所有导出项
        """
        module = self.get_module(module_name)
        if module is None:
            return {}
        
        return module.exports.copy()
    
    def list_modules(self) -> List[str]:
        """列出所有已加载模块"""
        return list(self.modules.keys())


class ModuleBuilder:
    """模块构建器"""
    
    def __init__(self, manager: ModuleManager):
        """
        初始化构建器
        
        Args:
            manager: 模块管理器
        """
        self.manager = manager
    
    def build_module(self, name: str, exports: Dict[str, Any]) -> Module:
        """
        构建模块
        
        Args:
            name: 模块名
            exports: 导出项
            
        Returns:
            模块对象
        """
        module = self.manager.create_module(name)
        
        for export_name, value in exports.items():
            module.add_export(export_name, value)
        
        module.loaded = True
        return module
    
    def build_from_file(self, name: str, path: str) -> Optional[Module]:
        """
        从文件构建模块
        
        Args:
            name: 模块名
            path: 文件路径
            
        Returns:
            模块对象
        """
        module = self.manager.create_module(name, path)
        
        if path.endswith('.py'):
            self.manager._load_python_module(module, path)
        elif path.endswith('.yl'):
            self.manager._load_yanlv_module(module, path)
        
        module.loaded = True
        return module


# 全局模块管理器实例
_global_module_manager: Optional[ModuleManager] = None


def get_module_manager() -> ModuleManager:
    """获取全局模块管理器"""
    global _global_module_manager
    if _global_module_manager is None:
        _global_module_manager = ModuleManager()
    return _global_module_manager
