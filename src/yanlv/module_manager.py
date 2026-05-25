"""
言律语言模块管理器
支持模块导入、导出和命名空间管理
"""
import os
from typing import Dict, List, Any, Optional
from .lexer.lexer_token import Token, TokenType


class Module:
    """模块对象"""
    
    def __init__(self, name: str):
        self.name = name              # 模块名
        self.functions: Dict[str, Any] = {}    # 函数
        self.variables: Dict[str, Any] = {}    # 变量
        self.exports: List[str] = []           # 导出列表
        self.path: Optional[str] = None        # 模块路径
    
    def add_function(self, name: str, func: Any):
        """添加函数"""
        self.functions[name] = func
    
    def add_variable(self, name: str, value: Any):
        """添加变量"""
        self.variables[name] = value
    
    def export_item(self, name: str):
        """导出项目"""
        if name not in self.exports:
            self.exports.append(name)
    
    def get_export(self, name: str) -> Optional[Any]:
        """获取导出项目"""
        if name in self.exports:
            if name in self.functions:
                return self.functions[name]
            elif name in self.variables:
                return self.variables[name]
        return None


class Namespace:
    """命名空间"""
    
    def __init__(self, name: str, parent: Optional['Namespace'] = None):
        self.name = name              # 命名空间名
        self.symbols: Dict[str, Any] = {}      # 符号表
        self.parent = parent          # 父命名空间
    
    def add_symbol(self, name: str, value: Any):
        """添加符号"""
        self.symbols[name] = value
    
    def get_symbol(self, name: str) -> Optional[Any]:
        """获取符号"""
        if name in self.symbols:
            return self.symbols[name]
        elif self.parent:
            return self.parent.get_symbol(name)
        return None
    
    def has_symbol(self, name: str) -> bool:
        """检查符号是否存在"""
        if name in self.symbols:
            return True
        elif self.parent:
            return self.parent.has_symbol(name)
        return False


class ModuleManager:
    """模块管理器"""
    
    def __init__(self, stdlib_path: Optional[str] = None):
        self.modules: Dict[str, Module] = {}           # 已加载模块
        self.namespaces: Dict[str, Namespace] = {}     # 命名空间
        self.stdlib_path = stdlib_path                 # 标准库路径
        self.current_module: Optional[Module] = None   # 当前模块
        self.global_namespace = Namespace("global")    # 全局命名空间
    
    def set_stdlib_path(self, path: str):
        """设置标准库路径"""
        self.stdlib_path = path
    
    def create_module(self, name: str) -> Module:
        """创建模块"""
        module = Module(name)
        self.modules[name] = module
        self.current_module = module
        return module
    
    def get_module(self, name: str) -> Optional[Module]:
        """获取模块"""
        return self.modules.get(name)
    
    def has_module(self, name: str) -> bool:
        """检查模块是否存在"""
        return name in self.modules
    
    def load_module_from_file(self, filepath: str) -> Optional[Module]:
        """从文件加载模块"""
        if not os.path.exists(filepath):
            return None
        
        # 读取文件内容
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 提取模块名
        module_name = os.path.basename(filepath).replace('.yan', '')
        
        # 创建模块
        module = self.create_module(module_name)
        module.path = filepath
        
        return module
    
    def import_module(self, module_name: str, alias: Optional[str] = None) -> bool:
        """导入模块"""
        # 检查是否已加载
        if module_name in self.modules:
            module = self.modules[module_name]
        else:
            # 尝试从文件加载
            filepath = self._find_module_file(module_name)
            if filepath:
                module = self.load_module_from_file(filepath)
                if not module:
                    return False
            else:
                return False
        
        # 创建命名空间
        ns_name = alias if alias else module_name
        namespace = Namespace(ns_name, self.global_namespace)
        
        # 将导出的项目添加到命名空间
        for export_name in module.exports:
            export_value = module.get_export(export_name)
            if export_value is not None:
                namespace.add_symbol(export_name, export_value)
        
        self.namespaces[ns_name] = namespace
        
        return True
    
    def import_from_module(self, module_name: str, items: List[str], 
                          aliases: Optional[Dict[str, str]] = None) -> bool:
        """从模块导入特定项目"""
        # 检查模块是否存在
        if module_name not in self.modules:
            # 尝试加载模块
            filepath = self._find_module_file(module_name)
            if filepath:
                module = self.load_module_from_file(filepath)
                if not module:
                    return False
            else:
                return False
        else:
            module = self.modules[module_name]
        
        # 导入项目到全局命名空间
        for item in items:
            export_value = module.get_export(item)
            if export_value is not None:
                # 使用别名或原名
                name = aliases.get(item, item) if aliases else item
                self.global_namespace.add_symbol(name, export_value)
        
        return True
    
    def export_from_current_module(self, items: List[str]) -> bool:
        """从当前模块导出"""
        if not self.current_module:
            return False
        
        for item in items:
            self.current_module.export_item(item)
        
        return True
    
    def _find_module_file(self, module_name: str) -> Optional[str]:
        """查找模块文件"""
        # 处理标准库路径
        if module_name.startswith("标准库/"):
            if self.stdlib_path:
                module_name = module_name.replace("标准库/", "")
                filepath = os.path.join(self.stdlib_path, f"{module_name}.yan")
                if os.path.exists(filepath):
                    return filepath
        
        # 查找当前目录
        filepath = f"{module_name}.yan"
        if os.path.exists(filepath):
            return filepath
        
        # 查找modules目录
        filepath = os.path.join("modules", f"{module_name}.yan")
        if os.path.exists(filepath):
            return filepath
        
        return None
    
    def get_symbol(self, name: str, namespace_name: Optional[str] = None) -> Optional[Any]:
        """获取符号"""
        if namespace_name:
            # 从指定命名空间获取
            if namespace_name in self.namespaces:
                return self.namespaces[namespace_name].get_symbol(name)
            return None
        else:
            # 从全局命名空间获取
            return self.global_namespace.get_symbol(name)
    
    def add_to_global(self, name: str, value: Any):
        """添加到全局命名空间"""
        self.global_namespace.add_symbol(name, value)


def create_module_manager(stdlib_path: Optional[str] = None) -> ModuleManager:
    """创建模块管理器实例"""
    return ModuleManager(stdlib_path)
