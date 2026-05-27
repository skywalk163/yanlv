"""
模块系统测试

测试ModuleManager的功能
"""

import pytest
import os
import tempfile
from yanlv.module_system import (
    Module,
    ModuleManager,
    ModuleBuilder,
    get_module_manager
)


class TestModule:
    """模块测试"""
    
    def test_module_initialization(self):
        """测试模块初始化"""
        module = Module("test_module")
        assert module.name == "test_module"
        assert module.path is None
        assert len(module.exports) == 0
        assert len(module.imports) == 0
        assert not module.loaded
    
    def test_add_export(self):
        """测试添加导出项"""
        module = Module("test_module")
        
        module.add_export("func1", lambda x: x * 2)
        module.add_export("var1", 42)
        
        assert "func1" in module.exports
        assert "var1" in module.exports
        assert module.exports["var1"] == 42
    
    def test_get_export(self):
        """测试获取导出项"""
        module = Module("test_module")
        module.add_export("value", 100)
        
        result = module.get_export("value")
        assert result == 100
        
        # 测试不存在的导出项
        result = module.get_export("nonexistent")
        assert result is None
    
    def test_list_exports(self):
        """测试列出导出项"""
        module = Module("test_module")
        module.add_export("a", 1)
        module.add_export("b", 2)
        module.add_export("c", 3)
        
        exports = module.list_exports()
        assert len(exports) == 3
        assert "a" in exports
        assert "b" in exports
        assert "c" in exports
    
    def test_add_import(self):
        """测试添加导入"""
        module1 = Module("module1")
        module2 = Module("module2")
        
        module1.add_import("m2", module2)
        
        assert "m2" in module1.imports
        assert module1.imports["m2"] is module2


class TestModuleManager:
    """模块管理器测试"""
    
    def test_manager_initialization(self):
        """测试管理器初始化"""
        manager = ModuleManager()
        assert len(manager.modules) == 0
        assert len(manager.search_paths) > 0
    
    def test_add_search_path(self):
        """测试添加搜索路径"""
        manager = ModuleManager()
        
        test_path = "/test/path"
        manager.add_search_path(test_path)
        
        assert test_path in manager.search_paths
    
    def test_create_module(self):
        """测试创建模块"""
        manager = ModuleManager()
        
        module = manager.create_module("test_module")
        
        assert module is not None
        assert module.name == "test_module"
        assert "test_module" in manager.modules
    
    def test_get_module(self):
        """测试获取模块"""
        manager = ModuleManager()
        
        # 创建模块
        manager.create_module("test_module")
        
        # 获取模块
        module = manager.get_module("test_module")
        assert module is not None
        
        # 测试不存在的模块
        module = manager.get_module("nonexistent")
        assert module is None
    
    def test_import_module(self):
        """测试导入模块"""
        manager = ModuleManager()
        
        # 导入json模块(Python标准库)
        module = manager.import_module("json")
        assert module is not None
        assert module.loaded
        
        # 测试别名导入
        module = manager.import_module("os", "myos")
        assert module is not None
        assert "myos" in manager.modules
    
    def test_import_from(self):
        """测试从模块导入"""
        manager = ModuleManager()
        
        # 从json模块导入dumps和loads
        imports = manager.import_from("json", ["dumps", "loads"])
        
        assert "dumps" in imports
        assert "loads" in imports
        assert callable(imports["dumps"])
    
    def test_export_all(self):
        """测试导出所有内容"""
        manager = ModuleManager()
        
        # 导入模块
        manager.import_module("json")
        
        # 导出所有内容
        exports = manager.export_all("json")
        
        assert len(exports) > 0
        assert "dumps" in exports
        assert "loads" in exports
    
    def test_list_modules(self):
        """测试列出模块"""
        manager = ModuleManager()
        
        # 创建几个模块
        manager.create_module("module1")
        manager.create_module("module2")
        manager.create_module("module3")
        
        modules = manager.list_modules()
        
        assert len(modules) == 3
        assert "module1" in modules
        assert "module2" in modules
        assert "module3" in modules


class TestModuleBuilder:
    """模块构建器测试"""
    
    def test_build_module(self):
        """测试构建模块"""
        manager = ModuleManager()
        builder = ModuleBuilder(manager)
        
        exports = {
            "func1": lambda x: x * 2,
            "var1": 42,
            "var2": "hello"
        }
        
        module = builder.build_module("custom_module", exports)
        
        assert module is not None
        assert module.loaded
        assert "func1" in module.exports
        assert "var1" in module.exports
        assert module.exports["var1"] == 42
    
    def test_build_from_file(self):
        """测试从文件构建模块"""
        manager = ModuleManager()
        builder = ModuleBuilder(manager)
        
        # 创建临时Python文件
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write("""
def test_func():
    return 42

test_var = "hello"
""")
            temp_path = f.name
        
        try:
            module = builder.build_from_file("temp_module", temp_path)
            
            assert module is not None
            assert module.loaded
            assert "test_func" in module.exports
            assert "test_var" in module.exports
        finally:
            os.unlink(temp_path)


class TestGlobalManager:
    """全局管理器测试"""
    
    def test_get_global_manager(self):
        """测试获取全局管理器"""
        manager1 = get_module_manager()
        manager2 = get_module_manager()
        
        # 应该是同一个实例
        assert manager1 is manager2


class TestModuleUsage:
    """模块使用测试"""
    
    def test_module_import_usage(self):
        """测试模块导入使用"""
        manager = ModuleManager()
        
        # 导入json模块
        json_module = manager.import_module("json")
        
        # 使用导出的函数
        dumps = json_module.get_export("dumps")
        loads = json_module.get_export("loads")
        
        # 测试功能
        data = {"name": "张三", "age": 25}
        json_str = dumps(data, ensure_ascii=False)
        parsed = loads(json_str)
        
        assert parsed["name"] == "张三"
        assert parsed["age"] == 25
    
    def test_module_chain_import(self):
        """测试模块链式导入"""
        manager = ModuleManager()
        
        # 创建主模块
        main_module = manager.create_module("main")
        
        # 导入其他模块
        json_module = manager.import_module("json")
        os_module = manager.import_module("os")
        
        # 添加导入关系
        main_module.add_import("json", json_module)
        main_module.add_import("os", os_module)
        
        # 验证导入关系
        assert main_module.get_import("json") is json_module
        assert main_module.get_import("os") is os_module


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
