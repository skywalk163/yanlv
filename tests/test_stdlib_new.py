"""
扩展标准库测试

测试新增的实用函数
"""

import pytest
from yanlv.stdlib_new import (
    datetime_funcs,
    json_funcs,
    regex_funcs,
    crypto_funcs,
    random_funcs,
    string_funcs
)


class TestDateTimeFunctions:
    """日期时间函数测试"""
    
    def test_当前时间(self):
        """测试获取当前时间"""
        result = datetime_funcs.当前时间()
        assert result is not None
        assert len(result) > 0
        # 格式: YYYY-MM-DD HH:MM:SS
        assert len(result) == 19
    
    def test_当前日期(self):
        """测试获取当前日期"""
        result = datetime_funcs.当前日期()
        assert result is not None
        # 格式: YYYY-MM-DD
        assert len(result) == 10
    
    def test_格式化时间(self):
        """测试格式化时间"""
        timestamp = "2024-01-15 10:30:00"
        result = datetime_funcs.格式化时间(timestamp, "%Y年%m月%d日")
        assert result == "2024年01月15日"
    
    def test_时间差(self):
        """测试计算时间差"""
        start = "2024-01-15 10:00:00"
        end = "2024-01-15 10:05:30"
        result = datetime_funcs.时间差(start, end)
        assert result == 330  # 5分30秒 = 330秒


class TestJSONFunctions:
    """JSON函数测试"""
    
    def test_解析JSON(self):
        """测试解析JSON"""
        json_str = '{"name": "张三", "age": 25}'
        result = json_funcs.解析JSON(json_str)
        assert result is not None
        assert result["name"] == "张三"
        assert result["age"] == 25
    
    def test_生成JSON(self):
        """测试生成JSON"""
        obj = {"name": "李四", "age": 30}
        result = json_funcs.生成JSON(obj)
        assert "李四" in result
        assert "30" in result
    
    def test_美化JSON(self):
        """测试美化JSON"""
        json_str = '{"name":"王五","age":35}'
        result = json_funcs.美化JSON(json_str)
        assert "王五" in result
        assert "\n" in result  # 美化后应该有换行


class TestRegexFunctions:
    """正则表达式函数测试"""
    
    def test_匹配(self):
        """测试匹配"""
        text = "我的电话是13812345678"
        pattern = r"\d{11}"
        result = regex_funcs.匹配(text, pattern)
        assert result is True
    
    def test_查找所有(self):
        """测试查找所有"""
        text = "电话: 13812345678, 13987654321"
        pattern = r"\d{11}"
        result = regex_funcs.查找所有(text, pattern)
        assert len(result) == 2
        assert "13812345678" in result
        assert "13987654321" in result
    
    def test_替换(self):
        """测试替换"""
        text = "价格: 100元"
        pattern = r"\d+"
        replacement = "XXX"
        result = regex_funcs.替换(text, pattern, replacement)
        assert result == "价格: XXX元"
    
    def test_分割(self):
        """测试分割"""
        text = "苹果,香蕉,橙子"
        pattern = r","
        result = regex_funcs.分割(text, pattern)
        assert len(result) == 3
        assert "苹果" in result


class TestCryptoFunctions:
    """加密函数测试"""
    
    def test_MD5哈希(self):
        """测试MD5哈希"""
        text = "hello"
        result = crypto_funcs.MD5哈希(text)
        assert len(result) == 32  # MD5哈希长度为32
        assert result == "5d41402abc4b2a76b9719d911017c592"
    
    def test_SHA256哈希(self):
        """测试SHA256哈希"""
        text = "hello"
        result = crypto_funcs.SHA256哈希(text)
        assert len(result) == 64  # SHA256哈希长度为64
    
    def test_哈希一致性(self):
        """测试哈希一致性"""
        text = "test"
        hash1 = crypto_funcs.MD5哈希(text)
        hash2 = crypto_funcs.MD5哈希(text)
        assert hash1 == hash2


class TestRandomFunctions:
    """随机数函数测试"""
    
    def test_随机整数(self):
        """测试随机整数"""
        for _ in range(10):
            result = random_funcs.随机整数(1, 100)
            assert 1 <= result <= 100
    
    def test_随机浮点数(self):
        """测试随机浮点数"""
        for _ in range(10):
            result = random_funcs.随机浮点数(0.0, 1.0)
            assert 0.0 <= result <= 1.0
    
    def test_随机选择(self):
        """测试随机选择"""
        items = ["苹果", "香蕉", "橙子"]
        for _ in range(10):
            result = random_funcs.随机选择(items)
            assert result in items
    
    def test_打乱顺序(self):
        """测试打乱顺序"""
        items = [1, 2, 3, 4, 5]
        result = random_funcs.打乱顺序(items)
        assert len(result) == 5
        assert set(result) == set(items)  # 元素相同,顺序可能不同


class TestStringFunctions:
    """字符串函数测试"""
    
    def test_去除空白(self):
        """测试去除空白"""
        text = "  hello  "
        result = string_funcs.去除空白(text)
        assert result == "hello"
    
    def test_转大写(self):
        """测试转大写"""
        text = "hello"
        result = string_funcs.转大写(text)
        assert result == "HELLO"
    
    def test_转小写(self):
        """测试转小写"""
        text = "HELLO"
        result = string_funcs.转小写(text)
        assert result == "hello"
    
    def test_首字母大写(self):
        """测试首字母大写"""
        text = "hello"
        result = string_funcs.首字母大写(text)
        assert result == "Hello"
    
    def test_是否包含(self):
        """测试是否包含"""
        text = "hello world"
        assert string_funcs.是否包含(text, "hello") == True
        assert string_funcs.是否包含(text, "xyz") == False
    
    def test_统计出现(self):
        """测试统计出现"""
        text = "hello hello hello"
        result = string_funcs.统计出现(text, "hello")
        assert result == 3


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
