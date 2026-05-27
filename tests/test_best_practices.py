"""
最佳实践指南测试

测试BestPracticesGuide的功能
"""

import pytest
from yanlv.best_practices import (
    BestPracticesGuide,
    BestPractice,
    PracticeCategory,
    get_best_practices_guide
)


class TestBestPracticesGuide:
    """最佳实践指南测试"""
    
    def test_guide_initialization(self):
        """测试指南初始化"""
        guide = BestPracticesGuide()
        assert len(guide.practices) > 0
    
    def test_get_practice(self):
        """测试获取最佳实践"""
        guide = BestPracticesGuide()
        
        # 测试存在的实践
        practice = guide.get_practice("style-001")
        assert practice is not None
        assert practice.title == "使用有意义的变量名"
        
        # 测试不存在的实践
        practice = guide.get_practice("nonexistent")
        assert practice is None
    
    def test_get_practices_by_category(self):
        """测试按分类获取最佳实践"""
        guide = BestPracticesGuide()
        
        # 代码风格
        practices = guide.get_practices_by_category(PracticeCategory.CODE_STYLE)
        assert len(practices) > 0
        assert all(p.category == PracticeCategory.CODE_STYLE for p in practices)
        
        # 性能优化
        practices = guide.get_practices_by_category(PracticeCategory.PERFORMANCE)
        assert len(practices) > 0
        assert all(p.category == PracticeCategory.PERFORMANCE for p in practices)
    
    def test_get_all_practices(self):
        """测试获取所有最佳实践"""
        guide = BestPracticesGuide()
        
        all_practices = guide.get_all_practices()
        assert len(all_practices) > 0


class TestPracticeContent:
    """最佳实践内容测试"""
    
    def test_code_style_practices(self):
        """测试代码风格实践"""
        guide = BestPracticesGuide()
        
        # 变量命名
        practice = guide.get_practice("style-001")
        assert practice is not None
        assert "变量名" in practice.title
        assert len(practice.good_example) > 0
        assert len(practice.bad_example) > 0
        
        # 函数单一职责
        practice = guide.get_practice("style-002")
        assert practice is not None
        assert "函数" in practice.title
        
        # 注释规范
        practice = guide.get_practice("style-003")
        assert practice is not None
        assert "注释" in practice.title
    
    def test_performance_practices(self):
        """测试性能优化实践"""
        guide = BestPracticesGuide()
        
        # 循环优化
        practice = guide.get_practice("perf-001")
        assert practice is not None
        assert "循环" in practice.title
        
        # 缓存使用
        practice = guide.get_practice("perf-002")
        assert practice is not None
        assert "缓存" in practice.title
    
    def test_project_structure_practices(self):
        """测试项目结构实践"""
        guide = BestPracticesGuide()
        
        practice = guide.get_practice("struct-001")
        assert practice is not None
        assert "目录" in practice.title or "结构" in practice.title
    
    def test_debugging_practices(self):
        """测试调试技巧实践"""
        guide = BestPracticesGuide()
        
        practice = guide.get_practice("debug-001")
        assert practice is not None
        assert "断点" in practice.title or "调试" in practice.title
    
    def test_security_practices(self):
        """测试安全编码实践"""
        guide = BestPracticesGuide()
        
        practice = guide.get_practice("security-001")
        assert practice is not None
        assert "验证" in practice.title or "输入" in practice.title


class TestPracticeStructure:
    """最佳实践结构测试"""
    
    def test_practice_structure(self):
        """测试实践结构"""
        guide = BestPracticesGuide()
        
        for practice in guide.get_all_practices():
            # 每个实践都有标题和描述
            assert practice.title is not None
            assert practice.description is not None
            
            # 每个实践都有好和坏的示例
            assert len(practice.good_example) > 0
            assert len(practice.bad_example) > 0
            
            # 每个实践都有解释说明
            assert len(practice.explanation) > 0
            
            # 每个实践都有分类
            assert practice.category in PracticeCategory


class TestGuideGeneration:
    """指南生成测试"""
    
    def test_generate_guide(self):
        """测试生成指南文档"""
        guide = BestPracticesGuide()
        
        guide_text = guide.generate_guide()
        
        # 验证基本结构
        assert "# 言律语言最佳实践指南" in guide_text
        assert "## 代码风格" in guide_text
        assert "## 性能优化" in guide_text
    
    def test_guide_contains_all_practices(self):
        """测试指南包含所有实践"""
        guide = BestPracticesGuide()
        
        guide_text = guide.generate_guide()
        
        # 验证所有实践都在指南中
        for practice in guide.get_all_practices():
            assert practice.title in guide_text


class TestGlobalGuide:
    """全局指南测试"""
    
    def test_get_global_guide(self):
        """测试获取全局指南"""
        guide1 = get_best_practices_guide()
        guide2 = get_best_practices_guide()
        
        # 应该是同一个实例
        assert guide1 is guide2


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
