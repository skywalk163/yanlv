"""
Language Server测试

测试YanLvLanguageServer的功能
"""

import pytest
from yanlv.language_server import (
    YanLvLanguageServer, 
    Position, 
    Range, 
    Diagnostic
)


class TestLanguageServer:
    """Language Server测试类"""
    
    def test_server_initialization(self):
        """测试服务器初始化"""
        server = YanLvLanguageServer()
        assert len(server.keywords) > 0
        assert len(server.builtins) > 0
        assert len(server.stdlib) > 0
    
    def test_document_management(self):
        """测试文档管理"""
        server = YanLvLanguageServer()
        
        # 打开文档
        content = "定义 x 为 10"
        server.did_open("test.yanlv", content)
        
        assert "test.yanlv" in server.documents
        assert server.documents["test.yanlv"] == content
        
        # 修改文档
        new_content = "定义 x 为 20"
        server.did_change("test.yanlv", new_content)
        
        assert server.documents["test.yanlv"] == new_content
        
        # 关闭文档
        server.did_close("test.yanlv")
        
        assert "test.yanlv" not in server.documents
    
    def test_diagnostics(self):
        """测试诊断功能"""
        server = YanLvLanguageServer()
        
        # 测试正确的代码
        content1 = "定义 x 为 10"
        server.did_open("test1.yanlv", content1)
        diagnostics1 = server.get_diagnostics("test1.yanlv")
        assert len(diagnostics1) == 0
        
        # 测试未闭合括号
        content2 = "函数 test("
        server.did_open("test2.yanlv", content2)
        diagnostics2 = server.get_diagnostics("test2.yanlv")
        assert len(diagnostics2) > 0
        assert any("括号未闭合" in d.message for d in diagnostics2)
        
        # 测试未闭合引号
        content3 = '定义 s 为 "hello'
        server.did_open("test3.yanlv", content3)
        diagnostics3 = server.get_diagnostics("test3.yanlv")
        assert len(diagnostics3) > 0
        assert any("引号未闭合" in d.message for d in diagnostics3)
    
    def test_completions(self):
        """测试补全功能"""
        server = YanLvLanguageServer()
        
        content = "定义 x 为 10"
        server.did_open("test.yanlv", content)
        
        completions = server.get_completions(
            "test.yanlv", 
            Position(line=0, character=0)
        )
        
        # 应该包含关键字
        assert any(c.label == "定义" for c in completions)
        assert any(c.label == "函数" for c in completions)
        
        # 应该包含内置函数
        assert any(c.label == "打印" for c in completions)
        
        # 应该包含用户定义的变量
        assert any(c.label == "x" for c in completions)
    
    def test_definition(self):
        """测试跳转定义"""
        server = YanLvLanguageServer()
        
        content = """定义 x 为 10
输出 x"""
        server.did_open("test.yanlv", content)
        
        # 在第二行的x处查找定义
        definition = server.get_definition(
            "test.yanlv",
            Position(line=1, character=3)
        )
        
        assert definition is not None
        assert definition.range.start.line == 0
        assert definition.range.start.character == 3  # "定义 x 为 10"中x的位置
    
    def test_function_definition(self):
        """测试函数定义跳转"""
        server = YanLvLanguageServer()
        
        content = """函数 加法(a, b) {
    返回 a + b
}
输出 加法(1, 2)"""
        server.did_open("test.yanlv", content)
        
        # 在第三行的"加法"处查找定义
        definition = server.get_definition(
            "test.yanlv",
            Position(line=3, character=3)
        )
        
        assert definition is not None
        assert definition.range.start.line == 0
    
    def test_references(self):
        """测试查找引用"""
        server = YanLvLanguageServer()
        
        content = """定义 x 为 10
输出 x
设 x 为 20
输出 x"""
        server.did_open("test.yanlv", content)
        
        # 在第一行的x处查找引用
        references = server.get_references(
            "test.yanlv",
            Position(line=0, character=3)
        )
        
        # 应该找到4个引用(定义+3次使用)
        assert len(references) == 4
    
    def test_hover(self):
        """测试悬停提示"""
        server = YanLvLanguageServer()
        
        content = "定义 x 为 10"
        server.did_open("test.yanlv", content)
        
        # 测试关键字悬停
        hover1 = server.get_hover(
            "test.yanlv",
            Position(line=0, character=0)
        )
        assert hover1 is not None
        assert "关键字" in hover1
        
        # 测试用户定义变量悬停
        hover2 = server.get_hover(
            "test.yanlv",
            Position(line=0, character=3)
        )
        assert hover2 is not None
        assert "定义位置" in hover2
    
    def test_builtin_hover(self):
        """测试内置函数悬停"""
        server = YanLvLanguageServer()
        
        content = "打印(123)"
        server.did_open("test.yanlv", content)
        
        hover = server.get_hover(
            "test.yanlv",
            Position(line=0, character=0)
        )
        
        assert hover is not None
        assert "内置函数" in hover
    
    def test_multi_file_symbols(self):
        """测试多文件符号"""
        server = YanLvLanguageServer()
        
        # 文件1
        content1 = "定义 x 为 10"
        server.did_open("file1.yanlv", content1)
        
        # 文件2
        content2 = "定义 y 为 20"
        server.did_open("file2.yanlv", content2)
        
        # 两个文件的符号都应该存在
        assert "x" in server.symbols
        assert "y" in server.symbols
        
        # 关闭文件1
        server.did_close("file1.yanlv")
        
        # x的符号应该被移除
        assert "x" not in server.symbols or len(server.symbols["x"]) == 0


class TestLanguageServerIntegration:
    """Language Server集成测试"""
    
    def test_complete_workflow(self):
        """测试完整工作流"""
        server = YanLvLanguageServer()
        
        # 1. 打开文档
        content = """函数 平方(x) {
    返回 x * x
}

定义 num 为 5
定义 result 为 平方
输出 result"""
        server.did_open("test.yanlv", content)
        
        # 2. 获取诊断
        diagnostics = server.get_diagnostics("test.yanlv")
        assert len(diagnostics) == 0  # 没有语法错误
        
        # 3. 获取补全
        completions = server.get_completions(
            "test.yanlv",
            Position(line=0, character=0)
        )
        assert len(completions) > 0
        
        # 4. 查找函数定义
        definition = server.get_definition(
            "test.yanlv",
            Position(line=5, character=15)  # "平方"的位置
        )
        assert definition is not None
        assert definition.range.start.line == 0
        
        # 5. 查找引用
        references = server.get_references(
            "test.yanlv",
            Position(line=4, character=3)  # "num"的定义位置
        )
        assert len(references) >= 1  # 至少有定义本身
        
        # 6. 获取悬停提示
        hover = server.get_hover(
            "test.yanlv",
            Position(line=0, character=0)  # "函数"关键字
        )
        assert hover is not None


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
