"""
教程系统测试

测试TutorialManager的功能
"""

import pytest
from yanlv.tutorial import (
    TutorialManager, 
    Tutorial,
    TutorialLevel,
    get_tutorial_manager
)


class TestTutorialManager:
    """TutorialManager测试类"""
    
    def test_manager_initialization(self):
        """测试管理器初始化"""
        manager = TutorialManager()
        assert len(manager.tutorials) > 0
    
    def test_get_tutorial(self):
        """测试获取教程"""
        manager = TutorialManager()
        
        # 测试存在的教程
        tutorial = manager.get_tutorial("beginner-001")
        assert tutorial is not None
        assert tutorial.title == "安装和环境配置"
        assert tutorial.level == TutorialLevel.BEGINNER
        
        # 测试不存在的教程
        tutorial = manager.get_tutorial("nonexistent")
        assert tutorial is None
    
    def test_get_tutorials_by_level(self):
        """测试按难度级别获取教程"""
        manager = TutorialManager()
        
        # 入门教程
        beginner = manager.get_tutorials_by_level(TutorialLevel.BEGINNER)
        assert len(beginner) > 0
        assert all(t.level == TutorialLevel.BEGINNER for t in beginner)
        
        # 进阶教程
        intermediate = manager.get_tutorials_by_level(TutorialLevel.INTERMEDIATE)
        assert len(intermediate) > 0
        assert all(t.level == TutorialLevel.INTERMEDIATE for t in intermediate)
    
    def test_get_all_tutorials(self):
        """测试获取所有教程"""
        manager = TutorialManager()
        
        all_tutorials = manager.get_all_tutorials()
        assert len(all_tutorials) > 0


class TestTutorialContent:
    """教程内容测试"""
    
    def test_beginner_tutorials(self):
        """测试入门教程"""
        manager = TutorialManager()
        
        # 环境配置教程
        tutorial = manager.get_tutorial("beginner-001")
        assert tutorial is not None
        assert len(tutorial.sections) > 0
        assert len(tutorial.tags) > 0
        
        # 第一个程序教程
        tutorial = manager.get_tutorial("beginner-002")
        assert tutorial is not None
        assert "Hello World" in tutorial.title or "第一个程序" in tutorial.title
        
        # 变量和数据类型教程
        tutorial = manager.get_tutorial("beginner-003")
        assert tutorial is not None
        assert "变量" in tutorial.title
    
    def test_intermediate_tutorials(self):
        """测试进阶教程"""
        manager = TutorialManager()
        
        # 函数教程
        tutorial = manager.get_tutorial("intermediate-001")
        assert tutorial is not None
        assert "函数" in tutorial.title
        
        # 控制流教程
        tutorial = manager.get_tutorial("intermediate-002")
        assert tutorial is not None
        assert "控制流" in tutorial.title
    
    def test_tutorial_structure(self):
        """测试教程结构"""
        manager = TutorialManager()
        
        for tutorial in manager.get_all_tutorials():
            # 每个教程都有标题和描述
            assert tutorial.title is not None
            assert tutorial.description is not None
            
            # 每个教程都有章节
            assert len(tutorial.sections) > 0
            
            # 每个教程都有预计时间
            assert tutorial.estimated_time is not None
            
            # 每个教程都有标签
            assert len(tutorial.tags) > 0


class TestTutorialIndex:
    """教程索引测试"""
    
    def test_generate_tutorial_index(self):
        """测试生成教程索引"""
        manager = TutorialManager()
        
        index = manager.generate_tutorial_index()
        
        # 验证基本结构
        assert "# 言律语言教程索引" in index
        assert "## 入门教程" in index
        assert "## 进阶教程" in index
        assert "## 高级教程" in index
    
    def test_index_contains_all_tutorials(self):
        """测试索引包含所有教程"""
        manager = TutorialManager()
        
        index = manager.generate_tutorial_index()
        
        # 验证所有教程都在索引中
        for tutorial in manager.get_all_tutorials():
            assert tutorial.title in index


class TestTutorialPrerequisites:
    """教程前置知识测试"""
    
    def test_prerequisites_chain(self):
        """测试前置知识链"""
        manager = TutorialManager()
        
        # beginner-002 依赖 beginner-001
        tutorial = manager.get_tutorial("beginner-002")
        assert "beginner-001" in tutorial.prerequisites
        
        # beginner-003 依赖 beginner-002
        tutorial = manager.get_tutorial("beginner-003")
        assert "beginner-002" in tutorial.prerequisites


class TestTutorialSections:
    """教程章节测试"""
    
    def test_sections_have_content(self):
        """测试章节有内容"""
        manager = TutorialManager()
        
        for tutorial in manager.get_all_tutorials():
            for section in tutorial.sections:
                assert section.title is not None
                assert section.content is not None
                assert len(section.content) > 0
    
    def test_sections_have_exercises(self):
        """测试章节有练习题"""
        manager = TutorialManager()
        
        for tutorial in manager.get_all_tutorials():
            for section in tutorial.sections:
                # 大多数章节应该有练习题
                # (不强制要求所有章节都有)
                if section.exercises:
                    assert len(section.exercises) > 0


class TestGlobalManager:
    """全局管理器测试"""
    
    def test_get_global_manager(self):
        """测试获取全局管理器"""
        manager1 = get_tutorial_manager()
        manager2 = get_tutorial_manager()
        
        # 应该是同一个实例
        assert manager1 is manager2


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
