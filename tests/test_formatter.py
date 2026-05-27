"""
代码格式化工具测试

测试CodeFormatter的功能
"""

import pytest
from yanlv.formatter import (
    CodeFormatter, 
    get_global_formatter,
    format_code
)


class TestCodeFormatter:
    """CodeFormatter测试类"""
    
    def test_formatter_initialization(self):
        """测试格式化器初始化"""
        formatter = CodeFormatter()
        assert formatter.indent_size == 4
    
    def test_format_simple_code(self):
        """测试格式化简单代码"""
        formatter = CodeFormatter()
        
        code = "定义 x 为 10"
        formatted = formatter.format(code)
        
        assert formatted == "定义 x 为 10"
    
    def test_format_indentation(self):
        """测试格式化缩进"""
        formatter = CodeFormatter()
        
        code = """函数 test() {
定义 x 为 10
}"""
        
        formatted = formatter.format(code)
        lines = formatted.split('\n')
        
        # 函数定义行
        assert lines[0] == "函数 test() {"
        # 函数体应该缩进
        assert lines[1].startswith("    ")
        # 右大括号不缩进
        assert lines[2] == "}"
    
    def test_format_trailing_whitespace(self):
        """测试去除行尾空白"""
        formatter = CodeFormatter()
        
        code = "定义 x 为 10   \n定义 y 为 20  "
        formatted = formatter.format(code)
        
        assert "  " not in formatted
        assert formatted == "定义 x 为 10\n定义 y 为 20"
    
    def test_format_operators(self):
        """测试格式化运算符"""
        formatter = CodeFormatter()
        
        code = "定义 x 为 1+2*3"
        formatted = formatter.format(code)
        
        # 运算符两边应该有空格
        assert "1 + 2 * 3" in formatted
    
    def test_format_commas(self):
        """测试格式化逗号"""
        formatter = CodeFormatter()
        
        code = "函数 test(a,b,c) {"
        formatted = formatter.format(code)
        
        # 逗号后应该有空格
        assert "a, b, c" in formatted
    
    def test_format_blank_lines(self):
        """测试添加空行"""
        formatter = CodeFormatter()
        
        code = """函数 test() {
定义 x 为 10
}
定义 y 为 20"""
        
        formatted = formatter.format(code)
        lines = formatted.split('\n')
        
        # 右大括号后应该有空行
        assert any(line == '' for line in lines)
    
    def test_format_nested_blocks(self):
        """测试格式化嵌套代码块"""
        formatter = CodeFormatter()
        
        code = """函数 outer() {
函数 inner() {
定义 x 为 10
}
}"""
        
        formatted = formatter.format(code)
        lines = formatted.split('\n')
        
        # 第一层缩进
        assert lines[1].startswith("    函数 inner()")
        # 第二层缩进
        assert lines[2].startswith("        定义 x 为 10")
    
    def test_check_format_correct(self):
        """测试检查格式正确的代码"""
        formatter = CodeFormatter()
        
        code = "定义 x 为 10"
        is_correct, diffs = formatter.check_format(code)
        
        assert is_correct
        assert len(diffs) == 0
    
    def test_check_format_incorrect(self):
        """测试检查格式不正确的代码"""
        formatter = CodeFormatter()
        
        code = "定义 x 为 1+2"
        is_correct, diffs = formatter.check_format(code)
        
        assert not is_correct
        assert len(diffs) > 0


class TestFormatterFeatures:
    """格式化器特性测试"""
    
    def test_preserve_strings(self):
        """测试保留字符串内容"""
        formatter = CodeFormatter()
        
        code = '定义 s 为 "hello,world"'
        formatted = formatter.format(code)
        
        # 字符串内的逗号不应该被格式化
        assert '"hello,world"' in formatted
    
    def test_multiple_operators(self):
        """测试多个运算符"""
        formatter = CodeFormatter()
        
        code = "定义 x 为 a+b*c-d/e"
        formatted = formatter.format(code)
        
        # 所有运算符都应该有空格
        assert "a + b * c - d / e" in formatted
    
    def test_comparison_operators(self):
        """测试比较运算符"""
        formatter = CodeFormatter()
        
        code = "若 x>y 则 {"
        formatted = formatter.format(code)
        
        assert "x > y" in formatted
    
    def test_logical_operators(self):
        """测试逻辑运算符"""
        formatter = CodeFormatter()
        
        code = "若 x>0且y>0 则 {"
        formatted = formatter.format(code)
        
        assert "x > 0 且 y > 0" in formatted


class TestGlobalFormatter:
    """全局格式化器测试"""
    
    def test_get_global_formatter(self):
        """测试获取全局格式化器"""
        formatter1 = get_global_formatter()
        formatter2 = get_global_formatter()
        
        # 应该是同一个实例
        assert formatter1 is formatter2
    
    def test_format_code_function(self):
        """测试格式化代码函数"""
        code = "定义 x 为 1+2"
        formatted = format_code(code)
        
        assert "1 + 2" in formatted


class TestFormatterEdgeCases:
    """格式化器边界情况测试"""
    
    def test_empty_code(self):
        """测试空代码"""
        formatter = CodeFormatter()
        
        formatted = formatter.format("")
        assert formatted == ""
    
    def test_only_whitespace(self):
        """测试只有空白"""
        formatter = CodeFormatter()
        
        formatted = formatter.format("   \n   \n   ")
        assert formatted.strip() == ""
    
    def test_multiple_blank_lines(self):
        """测试多个空行"""
        formatter = CodeFormatter()
        
        code = "定义 x 为 10\n\n\n\n定义 y 为 20"
        formatted = formatter.format(code)
        
        # 应该保留合理的空行
        assert "定义 x 为 10" in formatted
        assert "定义 y 为 20" in formatted
    
    def test_complex_expression(self):
        """测试复杂表达式"""
        formatter = CodeFormatter()
        
        code = "定义 result 为 (a+b)*(c-d)/e"
        formatted = formatter.format(code)
        
        # 应该正确格式化
        assert "result" in formatted


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
