"""
API文档生成器测试

测试APIDocGenerator的功能
"""

import pytest
from yanlv.api_doc import (
    APIDocGenerator, 
    APIFunction,
    APIParameter,
    get_api_doc_generator
)


class TestAPIDocGenerator:
    """APIDocGenerator测试类"""
    
    def test_generator_initialization(self):
        """测试生成器初始化"""
        generator = APIDocGenerator()
        assert len(generator.functions) > 0
        assert len(generator.categories) > 0
    
    def test_get_function(self):
        """测试获取函数文档"""
        generator = APIDocGenerator()
        
        # 测试存在的函数
        func = generator.get_function("取整")
        assert func is not None
        assert func.name == "取整"
        assert func.category == "数学函数"
        
        # 测试不存在的函数
        func = generator.get_function("不存在的函数")
        assert func is None
    
    def test_get_functions_by_category(self):
        """测试按分类获取函数"""
        generator = APIDocGenerator()
        
        # 数学函数
        math_funcs = generator.get_functions_by_category("数学函数")
        assert len(math_funcs) > 0
        assert all(f.category == "数学函数" for f in math_funcs)
        
        # 字符串函数
        string_funcs = generator.get_functions_by_category("字符串函数")
        assert len(string_funcs) > 0
        assert all(f.category == "字符串函数" for f in string_funcs)
    
    def test_add_function(self):
        """测试添加函数"""
        generator = APIDocGenerator()
        
        new_func = APIFunction(
            name="测试函数",
            description="这是一个测试函数",
            parameters=[
                APIParameter("x", "整数", "参数x")
            ],
            return_type="整数",
            return_description="返回值",
            examples=["测试函数(1)"],
            category="测试分类"
        )
        
        generator.add_function(new_func)
        
        # 验证添加成功
        func = generator.get_function("测试函数")
        assert func is not None
        assert func.name == "测试函数"
        
        # 验证分类添加
        test_funcs = generator.get_functions_by_category("测试分类")
        assert len(test_funcs) == 1


class TestDocumentGeneration:
    """文档生成测试"""
    
    def test_generate_markdown(self):
        """测试生成Markdown文档"""
        generator = APIDocGenerator()
        
        markdown = generator.generate_markdown()
        
        # 验证基本结构
        assert "# 言律语言标准库API文档" in markdown
        assert "## 数学函数" in markdown
        assert "### 取整" in markdown
        assert "**参数:**" in markdown
        assert "**返回值:**" in markdown
        assert "**示例:**" in markdown
    
    def test_generate_html(self):
        """测试生成HTML文档"""
        generator = APIDocGenerator()
        
        html = generator.generate_html()
        
        # 验证基本结构
        assert "<!DOCTYPE html>" in html
        assert "<html" in html
        assert "<title>言律语言API文档</title>" in html
        assert "<h1>言律语言标准库API文档</h1>" in html
        assert "<h2>数学函数</h2>" in html
        assert "<h3>取整</h3>" in html
    
    def test_markdown_contains_all_functions(self):
        """测试Markdown包含所有函数"""
        generator = APIDocGenerator()
        
        markdown = generator.generate_markdown()
        
        # 验证所有函数都在文档中
        for func_name in generator.functions:
            assert f"### {func_name}" in markdown
    
    def test_html_contains_all_functions(self):
        """测试HTML包含所有函数"""
        generator = APIDocGenerator()
        
        html = generator.generate_html()
        
        # 验证所有函数都在文档中
        for func_name in generator.functions:
            assert f"<h3>{func_name}</h3>" in html


class TestFunctionDocumentation:
    """函数文档测试"""
    
    def test_math_functions(self):
        """测试数学函数文档"""
        generator = APIDocGenerator()
        
        # 取整函数
        func = generator.get_function("取整")
        assert func is not None
        assert len(func.parameters) == 1
        assert func.parameters[0].name == "x"
        assert len(func.examples) > 0
        
        # 幂函数
        func = generator.get_function("幂")
        assert func is not None
        assert len(func.parameters) == 2
    
    def test_string_functions(self):
        """测试字符串函数文档"""
        generator = APIDocGenerator()
        
        # 长度函数
        func = generator.get_function("长度")
        assert func is not None
        assert func.category == "字符串函数"
        
        # 查找函数
        func = generator.get_function("查找")
        assert func is not None
        assert len(func.parameters) == 2
    
    def test_array_functions(self):
        """测试数组函数文档"""
        generator = APIDocGenerator()
        
        # 添加函数
        func = generator.get_function("添加")
        assert func is not None
        assert func.category == "数组函数"
        
        # 删除函数
        func = generator.get_function("删除")
        assert func is not None
    
    def test_io_functions(self):
        """测试输入输出函数文档"""
        generator = APIDocGenerator()
        
        # 输出函数
        func = generator.get_function("输出")
        assert func is not None
        assert func.category == "输入输出"
        
        # 输入函数
        func = generator.get_function("输入")
        assert func is not None


class TestGlobalGenerator:
    """全局生成器测试"""
    
    def test_get_global_generator(self):
        """测试获取全局生成器"""
        generator1 = get_api_doc_generator()
        generator2 = get_api_doc_generator()
        
        # 应该是同一个实例
        assert generator1 is generator2


class TestDocumentationQuality:
    """文档质量测试"""
    
    def test_all_functions_have_descriptions(self):
        """测试所有函数都有描述"""
        generator = APIDocGenerator()
        
        for func in generator.functions.values():
            assert func.description is not None
            assert len(func.description) > 0
    
    def test_all_functions_have_examples(self):
        """测试所有函数都有示例"""
        generator = APIDocGenerator()
        
        for func in generator.functions.values():
            assert len(func.examples) > 0
    
    def test_all_parameters_have_descriptions(self):
        """测试所有参数都有描述"""
        generator = APIDocGenerator()
        
        for func in generator.functions.values():
            for param in func.parameters:
                assert param.description is not None
                assert len(param.description) > 0
    
    def test_all_functions_have_return_info(self):
        """测试所有函数都有返回值信息"""
        generator = APIDocGenerator()
        
        for func in generator.functions.values():
            assert func.return_type is not None
            assert func.return_description is not None


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
