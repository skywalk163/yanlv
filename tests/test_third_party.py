"""
第三方库集成测试

测试ThirdPartyIntegration的功能
"""

import pytest
from yanlv.third_party import (
    ThirdPartyLibrary,
    ThirdPartyIntegration,
    NumpyAdapter,
    PandasAdapter,
    RequestsAdapter,
    get_integration
)


class TestThirdPartyLibrary:
    """第三方库测试"""
    
    def test_library_initialization(self):
        """测试库初始化"""
        # 测试存在的库
        lib = ThirdPartyLibrary("json")
        assert lib.is_available()
        
        # 测试不存在的库
        lib = ThirdPartyLibrary("nonexistent_lib_xyz")
        assert not lib.is_available()
    
    def test_get_function(self):
        """测试获取函数"""
        lib = ThirdPartyLibrary("json")
        
        # 测试存在的函数
        func = lib.get_function("dumps")
        assert func is not None
        assert callable(func)
        
        # 测试不存在的函数
        func = lib.get_function("nonexistent_func")
        assert func is None
    
    def test_list_functions(self):
        """测试列出函数"""
        lib = ThirdPartyLibrary("json")
        functions = lib.list_functions()
        
        assert len(functions) > 0
        assert "dumps" in functions
        assert "loads" in functions


class TestThirdPartyIntegration:
    """第三方库集成测试"""
    
    def test_integration_initialization(self):
        """测试集成管理器初始化"""
        integration = ThirdPartyIntegration()
        assert len(integration.libraries) > 0
    
    def test_import_library(self):
        """测试导入库"""
        integration = ThirdPartyIntegration()
        
        # 测试导入存在的库
        result = integration.import_library("json", "j")
        assert result
        
        # 测试导入不存在的库
        result = integration.import_library("nonexistent_lib_xyz")
        assert not result
    
    def test_get_library(self):
        """测试获取库"""
        integration = ThirdPartyIntegration()
        
        # 导入库
        integration.import_library("json", "test_json")
        
        # 获取库
        lib = integration.get_library("test_json")
        assert lib is not None
        assert lib.is_available()
    
    def test_list_available_libraries(self):
        """测试列出可用库"""
        integration = ThirdPartyIntegration()
        
        # 导入一些库
        integration.import_library("json", "j1")
        integration.import_library("os", "o1")
        
        available = integration.list_available_libraries()
        assert "j1" in available
        assert "o1" in available


class TestAdapters:
    """适配器测试"""
    
    def test_numpy_adapter(self):
        """测试NumPy适配器"""
        integration = ThirdPartyIntegration()
        adapter = NumpyAdapter(integration)
        
        # 检查是否可用(取决于是否安装了numpy)
        # 这里只测试适配器创建成功
        assert adapter is not None
    
    def test_pandas_adapter(self):
        """测试Pandas适配器"""
        integration = ThirdPartyIntegration()
        adapter = PandasAdapter(integration)
        
        # 检查适配器创建成功
        assert adapter is not None
    
    def test_requests_adapter(self):
        """测试Requests适配器"""
        integration = ThirdPartyIntegration()
        adapter = RequestsAdapter(integration)
        
        # 检查适配器创建成功
        assert adapter is not None


class TestGlobalIntegration:
    """全局集成管理器测试"""
    
    def test_get_global_integration(self):
        """测试获取全局集成管理器"""
        integration1 = get_integration()
        integration2 = get_integration()
        
        # 应该是同一个实例
        assert integration1 is integration2


class TestLibraryUsage:
    """库使用测试"""
    
    def test_json_library_usage(self):
        """测试JSON库使用"""
        integration = ThirdPartyIntegration()
        
        # 导入json库
        result = integration.import_library("json", "json")
        assert result
        
        # 调用dumps函数
        data = {"name": "张三", "age": 25}
        json_str = integration.call_function("json", "dumps", data, ensure_ascii=False)
        assert "张三" in json_str
        assert "25" in json_str
        
        # 调用loads函数
        parsed = integration.call_function("json", "loads", json_str)
        assert parsed["name"] == "张三"
        assert parsed["age"] == 25
    
    def test_os_library_usage(self):
        """测试OS库使用"""
        integration = ThirdPartyIntegration()
        
        # 导入os库
        result = integration.import_library("os", "os")
        assert result
        
        # 调用getcwd函数
        cwd = integration.call_function("os", "getcwd")
        assert cwd is not None
        assert len(cwd) > 0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
