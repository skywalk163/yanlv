"""
示例程序测试

测试ExampleManager的功能
"""

import pytest
from yanlv.examples import (
    ExampleManager, 
    ExampleProgram,
    ExampleCategory,
    get_example_manager
)


class TestExampleManager:
    """ExampleManager测试类"""
    
    def test_manager_initialization(self):
        """测试管理器初始化"""
        manager = ExampleManager()
        assert len(manager.examples) > 0
    
    def test_get_example(self):
        """测试获取示例"""
        manager = ExampleManager()
        
        # 测试存在的示例
        example = manager.get_example("basic-001")
        assert example is not None
        assert example.title == "Hello World"
        assert example.category == ExampleCategory.BASIC
        
        # 测试不存在的示例
        example = manager.get_example("nonexistent")
        assert example is None
    
    def test_get_examples_by_category(self):
        """测试按分类获取示例"""
        manager = ExampleManager()
        
        # 基础示例
        basic = manager.get_examples_by_category(ExampleCategory.BASIC)
        assert len(basic) > 0
        assert all(e.category == ExampleCategory.BASIC for e in basic)
        
        # 算法示例
        algo = manager.get_examples_by_category(ExampleCategory.ALGORITHM)
        assert len(algo) > 0
        assert all(e.category == ExampleCategory.ALGORITHM for e in algo)
    
    def test_get_all_examples(self):
        """测试获取所有示例"""
        manager = ExampleManager()
        
        all_examples = manager.get_all_examples()
        assert len(all_examples) > 0


class TestExampleContent:
    """示例内容测试"""
    
    def test_basic_examples(self):
        """测试基础示例"""
        manager = ExampleManager()
        
        # Hello World
        example = manager.get_example("basic-001")
        assert example is not None
        assert "Hello" in example.code
        assert len(example.output) > 0
        
        # 变量和运算
        example = manager.get_example("basic-002")
        assert example is not None
        assert "定义" in example.code
        
        # 条件判断
        example = manager.get_example("basic-003")
        assert example is not None
        assert "若" in example.code
        
        # 循环语句
        example = manager.get_example("basic-004")
        assert example is not None
        assert "当" in example.code
    
    def test_algorithm_examples(self):
        """测试算法示例"""
        manager = ExampleManager()
        
        # 阶乘
        example = manager.get_example("algo-001")
        assert example is not None
        assert "阶乘" in example.title
        assert example.difficulty == "中等"
        
        # 斐波那契
        example = manager.get_example("algo-002")
        assert example is not None
        assert "斐波那契" in example.title
        
        # 冒泡排序
        example = manager.get_example("algo-003")
        assert example is not None
        assert "排序" in example.title
    
    def test_practical_examples(self):
        """测试实用程序示例"""
        manager = ExampleManager()
        
        # 计算器
        example = manager.get_example("practical-001")
        assert example is not None
        assert "计算器" in example.title
        
        # 猜数字游戏
        example = manager.get_example("practical-002")
        assert example is not None
        assert "游戏" in example.category.value
    
    def test_example_structure(self):
        """测试示例结构"""
        manager = ExampleManager()
        
        for example in manager.get_all_examples():
            # 每个示例都有标题和描述
            assert example.title is not None
            assert example.description is not None
            
            # 每个示例都有代码和输出
            assert len(example.code) > 0
            assert len(example.output) > 0
            
            # 每个示例都有解释
            assert len(example.explanation) > 0
            
            # 每个示例都有难度
            assert example.difficulty in ["简单", "中等", "困难"]
            
            # 每个示例都有标签
            assert len(example.tags) > 0


class TestExampleIndex:
    """示例索引测试"""
    
    def test_generate_example_index(self):
        """测试生成示例索引"""
        manager = ExampleManager()
        
        index = manager.generate_example_index()
        
        # 验证基本结构
        assert "# 言律语言示例程序索引" in index
        assert "## 基础示例" in index
        assert "## 算法示例" in index
    
    def test_index_contains_all_examples(self):
        """测试索引包含所有示例"""
        manager = ExampleManager()
        
        index = manager.generate_example_index()
        
        # 验证所有示例都在索引中
        for example in manager.get_all_examples():
            assert example.title in index


class TestExampleCode:
    """示例代码测试"""
    
    def test_code_has_chinese_keywords(self):
        """测试代码包含中文关键字"""
        manager = ExampleManager()
        
        chinese_keywords = ["定义", "函数", "若", "则", "否则", "当", "执行", "输出", "返回"]
        
        for example in manager.get_all_examples():
            # 至少包含一个中文关键字
            has_keyword = any(kw in example.code for kw in chinese_keywords)
            assert has_keyword, f"示例 {example.id} 缺少中文关键字"
    
    def test_code_quality(self):
        """测试代码质量"""
        manager = ExampleManager()
        
        for example in manager.get_all_examples():
            # 代码不应该为空
            assert len(example.code.strip()) > 0
            
            # 输出不应该为空
            assert len(example.output.strip()) > 0


class TestGlobalManager:
    """全局管理器测试"""
    
    def test_get_global_manager(self):
        """测试获取全局管理器"""
        manager1 = get_example_manager()
        manager2 = get_example_manager()
        
        # 应该是同一个实例
        assert manager1 is manager2


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
