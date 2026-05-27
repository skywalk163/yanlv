"""
类型注解测试

测试TypeAnnotation的功能
"""

import pytest
from yanlv.type_annotation import (
    YanLvType,
    TypeAnnotation,
    TypeChecker,
    TypeInferrer,
    TypeAnnotationParser,
    type_hint,
    get_type_checker
)


class TestTypeAnnotation:
    """类型注解测试"""
    
    def test_basic_type(self):
        """测试基本类型"""
        annotation = TypeAnnotation(base_type=YanLvType.整数)
        
        assert annotation.base_type == YanLvType.整数
        assert str(annotation) == "整数"
    
    def test_optional_type(self):
        """测试可选类型"""
        annotation = TypeAnnotation(base_type=YanLvType.整数, is_optional=True)
        
        assert annotation.is_optional
        assert str(annotation) == "整数?"
    
    def test_generic_type(self):
        """测试泛型类型"""
        element_type = TypeAnnotation(base_type=YanLvType.整数)
        annotation = TypeAnnotation(
            base_type=YanLvType.列表,
            generic_args=[element_type]
        )
        
        assert annotation.generic_args is not None
        assert str(annotation) == "列表[整数]"
    
    def test_custom_type(self):
        """测试自定义类型"""
        annotation = TypeAnnotation(
            base_type=YanLvType.任意,
            custom_type="用户"
        )
        
        assert annotation.custom_type == "用户"
        assert str(annotation) == "用户"


class TestTypeChecker:
    """类型检查器测试"""
    
    def test_checker_initialization(self):
        """测试检查器初始化"""
        checker = TypeChecker()
        assert len(checker.type_map) == 0
        assert len(checker.errors) == 0
    
    def test_register_type(self):
        """测试注册类型"""
        checker = TypeChecker()
        
        annotation = TypeAnnotation(base_type=YanLvType.整数)
        checker.register_type("x", annotation)
        
        assert "x" in checker.type_map
    
    def test_get_type(self):
        """测试获取类型"""
        checker = TypeChecker()
        
        annotation = TypeAnnotation(base_type=YanLvType.字符串)
        checker.register_type("name", annotation)
        
        result = checker.get_type("name")
        assert result is not None
        assert result.base_type == YanLvType.字符串
    
    def test_check_integer(self):
        """测试整数类型检查"""
        checker = TypeChecker()
        
        annotation = TypeAnnotation(base_type=YanLvType.整数)
        checker.register_type("x", annotation)
        
        assert checker.check_type("x", 42)
        assert not checker.check_type("x", 3.14)
        assert not checker.check_type("x", "hello")
    
    def test_check_string(self):
        """测试字符串类型检查"""
        checker = TypeChecker()
        
        annotation = TypeAnnotation(base_type=YanLvType.字符串)
        checker.register_type("name", annotation)
        
        assert checker.check_type("name", "张三")
        assert not checker.check_type("name", 42)
    
    def test_check_list(self):
        """测试列表类型检查"""
        checker = TypeChecker()
        
        element_type = TypeAnnotation(base_type=YanLvType.整数)
        annotation = TypeAnnotation(
            base_type=YanLvType.列表,
            generic_args=[element_type]
        )
        checker.register_type("numbers", annotation)
        
        assert checker.check_type("numbers", [1, 2, 3])
        assert not checker.check_type("numbers", [1, "two", 3])
    
    def test_check_optional(self):
        """测试可选类型检查"""
        checker = TypeChecker()
        
        annotation = TypeAnnotation(base_type=YanLvType.整数, is_optional=True)
        checker.register_type("x", annotation)
        
        assert checker.check_type("x", 42)
        assert checker.check_type("x", None)


class TestTypeInferrer:
    """类型推断器测试"""
    
    def test_infer_integer(self):
        """测试推断整数类型"""
        annotation = TypeInferrer.infer_type(42)
        
        assert annotation.base_type == YanLvType.整数
    
    def test_infer_float(self):
        """测试推断浮点数类型"""
        annotation = TypeInferrer.infer_type(3.14)
        
        assert annotation.base_type == YanLvType.浮点数
    
    def test_infer_string(self):
        """测试推断字符串类型"""
        annotation = TypeInferrer.infer_type("hello")
        
        assert annotation.base_type == YanLvType.字符串
    
    def test_infer_boolean(self):
        """测试推断布尔类型"""
        annotation = TypeInferrer.infer_type(True)
        
        assert annotation.base_type == YanLvType.布尔
    
    def test_infer_list(self):
        """测试推断列表类型"""
        annotation = TypeInferrer.infer_type([1, 2, 3])
        
        assert annotation.base_type == YanLvType.列表
        assert annotation.generic_args is not None
        assert annotation.generic_args[0].base_type == YanLvType.整数
    
    def test_infer_dict(self):
        """测试推断字典类型"""
        annotation = TypeInferrer.infer_type({"a": 1, "b": 2})
        
        assert annotation.base_type == YanLvType.字典
        assert annotation.generic_args is not None
        assert len(annotation.generic_args) == 2


class TestTypeAnnotationParser:
    """类型注解解析器测试"""
    
    def test_parse_basic_type(self):
        """测试解析基本类型"""
        annotation = TypeAnnotationParser.parse("整数")
        
        assert annotation.base_type == YanLvType.整数
    
    def test_parse_optional_type(self):
        """测试解析可选类型"""
        annotation = TypeAnnotationParser.parse("整数?")
        
        assert annotation.base_type == YanLvType.整数
        assert annotation.is_optional
    
    def test_parse_generic_type(self):
        """测试解析泛型类型"""
        annotation = TypeAnnotationParser.parse("列表[整数]")
        
        assert annotation.base_type == YanLvType.列表
        assert annotation.generic_args is not None
        assert annotation.generic_args[0].base_type == YanLvType.整数
    
    def test_parse_dict_type(self):
        """测试解析字典类型"""
        annotation = TypeAnnotationParser.parse("字典[字符串, 整数]")
        
        assert annotation.base_type == YanLvType.字典
        assert annotation.generic_args is not None
        assert len(annotation.generic_args) == 2


class TestTypeHintDecorator:
    """类型注解装饰器测试"""
    
    def test_type_hint_decorator(self):
        """测试类型注解装饰器"""
        @type_hint(x="整数", y="字符串")
        def func(x, y):
            return f"{x}: {y}"
        
        assert hasattr(func, '_type_hints')
        assert func._type_hints['x'] == "整数"
        assert func._type_hints['y'] == "字符串"


class TestGlobalChecker:
    """全局检查器测试"""
    
    def test_get_global_checker(self):
        """测试获取全局检查器"""
        checker1 = get_type_checker()
        checker2 = get_type_checker()
        
        # 应该是同一个实例
        assert checker1 is checker2


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
