"""
错误消息系统测试

测试ErrorMessageManager的功能
"""

import pytest
from yanlv.error_messages import (
    ErrorMessageManager, 
    get_error_manager,
    format_error
)


class TestErrorMessageManager:
    """ErrorMessageManager测试类"""
    
    def test_manager_initialization(self):
        """测试管理器初始化"""
        manager = ErrorMessageManager()
        assert len(manager.errors) > 0
    
    def test_get_error(self):
        """测试获取错误信息"""
        manager = ErrorMessageManager()
        
        # 测试存在的错误
        error = manager.get_error("YANLV-0001")
        assert error is not None
        assert error.code == "YANLV-0001"
        assert error.message == "括号未闭合"
        assert error.category == "词法错误"
        
        # 测试不存在的错误
        error = manager.get_error("YANLV-9999")
        assert error is None
    
    def test_format_error(self):
        """测试格式化错误消息"""
        manager = ErrorMessageManager()
        
        # 基本格式化
        msg = manager.format_error("YANLV-0001")
        assert "YANLV-0001" in msg
        assert "括号未闭合" in msg
        assert "词法错误" in msg
        
        # 带位置信息
        msg = manager.format_error("YANLV-0001", line=10, column=5)
        assert "第10行" in msg
        assert "第5列" in msg
        
        # 带额外参数
        msg = manager.format_error("YANLV-0200", 变量名="x")
        assert "变量名: x" in msg
    
    def test_get_all_errors(self):
        """测试获取所有错误"""
        manager = ErrorMessageManager()
        
        errors = manager.get_all_errors()
        assert len(errors) > 0
        
        # 检查错误代码格式
        for error in errors:
            assert error.code.startswith("YANLV-")
    
    def test_get_errors_by_category(self):
        """测试按类别获取错误"""
        manager = ErrorMessageManager()
        
        # 词法错误
        lexical_errors = manager.get_errors_by_category("词法错误")
        assert len(lexical_errors) > 0
        assert all(e.category == "词法错误" for e in lexical_errors)
        
        # 语法错误
        syntax_errors = manager.get_errors_by_category("语法错误")
        assert len(syntax_errors) > 0
        assert all(e.category == "语法错误" for e in syntax_errors)
        
        # 语义错误
        semantic_errors = manager.get_errors_by_category("语义错误")
        assert len(semantic_errors) > 0
        assert all(e.category == "语义错误" for e in semantic_errors)
    
    def test_error_severity(self):
        """测试错误严重程度"""
        manager = ErrorMessageManager()
        
        # 错误级别
        error = manager.get_error("YANLV-0001")
        assert error.severity == 1
        
        # 警告级别
        warning = manager.get_error("YANLV-0400")
        assert warning.severity == 2
    
    def test_error_suggestion(self):
        """测试错误建议"""
        manager = ErrorMessageManager()
        
        error = manager.get_error("YANLV-0200")
        assert error.suggestion is not None
        assert len(error.suggestion) > 0
        assert "定义" in error.suggestion
    
    def test_error_example(self):
        """测试错误示例"""
        manager = ErrorMessageManager()
        
        error = manager.get_error("YANLV-0001")
        assert error.example is not None
        assert "正确" in error.example
        assert "错误" in error.example


class TestErrorCategories:
    """错误类别测试"""
    
    def test_lexical_errors(self):
        """测试词法错误"""
        manager = ErrorMessageManager()
        
        # YANLV-0001 ~ YANLV-0099
        lexical_codes = [
            "YANLV-0001",  # 括号未闭合
            "YANLV-0002",  # 引号未闭合
            "YANLV-0003",  # 非法字符
            "YANLV-0004",  # 数字格式错误
        ]
        
        for code in lexical_codes:
            error = manager.get_error(code)
            assert error is not None
            assert error.category == "词法错误"
    
    def test_syntax_errors(self):
        """测试语法错误"""
        manager = ErrorMessageManager()
        
        # YANLV-0100 ~ YANLV-0199
        syntax_codes = [
            "YANLV-0100",  # 缺少关键字
            "YANLV-0101",  # 缺少标识符
            "YANLV-0102",  # 缺少表达式
            "YANLV-0103",  # 无效的语句
            "YANLV-0104",  # 缺少右大括号
        ]
        
        for code in syntax_codes:
            error = manager.get_error(code)
            assert error is not None
            assert error.category == "语法错误"
    
    def test_semantic_errors(self):
        """测试语义错误"""
        manager = ErrorMessageManager()
        
        # YANLV-0200 ~ YANLV-0299
        semantic_codes = [
            "YANLV-0200",  # 未定义的变量
            "YANLV-0201",  # 未定义的函数
            "YANLV-0202",  # 参数数量不匹配
            "YANLV-0203",  # 类型不匹配
            "YANLV-0204",  # 重复定义
        ]
        
        for code in semantic_codes:
            error = manager.get_error(code)
            assert error is not None
            assert error.category == "语义错误"
    
    def test_runtime_errors(self):
        """测试运行时错误"""
        manager = ErrorMessageManager()
        
        # YANLV-0300 ~ YANLV-0399
        runtime_codes = [
            "YANLV-0300",  # 除零错误
            "YANLV-0301",  # 数组索引越界
            "YANLV-0302",  # 空值引用
            "YANLV-0303",  # 文件不存在
        ]
        
        for code in runtime_codes:
            error = manager.get_error(code)
            assert error is not None
            assert error.category == "运行时错误"
    
    def test_warnings(self):
        """测试警告"""
        manager = ErrorMessageManager()
        
        # YANLV-0400 ~ YANLV-0499
        warning_codes = [
            "YANLV-0400",  # 未使用的变量
            "YANLV-0401",  # 代码不可达
            "YANLV-0402",  # 无限循环
        ]
        
        for code in warning_codes:
            error = manager.get_error(code)
            assert error is not None
            assert error.category == "警告"
            assert error.severity == 2


class TestGlobalFunctions:
    """全局函数测试"""
    
    def test_get_error_manager(self):
        """测试获取全局管理器"""
        manager1 = get_error_manager()
        manager2 = get_error_manager()
        
        # 应该是同一个实例
        assert manager1 is manager2
    
    def test_format_error_function(self):
        """测试格式化错误函数"""
        msg = format_error("YANLV-0001", line=5)
        
        assert "YANLV-0001" in msg
        assert "第5行" in msg
        assert "括号未闭合" in msg


class TestErrorMessageQuality:
    """错误消息质量测试"""
    
    def test_all_errors_have_suggestions(self):
        """测试所有错误都有建议"""
        manager = ErrorMessageManager()
        
        for error in manager.get_all_errors():
            assert error.suggestion is not None
            assert len(error.suggestion) > 0
    
    def test_all_errors_have_chinese_messages(self):
        """测试所有错误消息都是中文"""
        manager = ErrorMessageManager()
        
        for error in manager.get_all_errors():
            # 检查是否包含中文字符
            has_chinese = any(
                '\u4e00' <= char <= '\u9fff' 
                for char in error.message
            )
            assert has_chinese, f"错误 {error.code} 的消息不是中文"
    
    def test_error_codes_unique(self):
        """测试错误代码唯一"""
        manager = ErrorMessageManager()
        
        codes = [error.code for error in manager.get_all_errors()]
        assert len(codes) == len(set(codes))  # 无重复


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
