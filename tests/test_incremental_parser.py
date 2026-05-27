"""
增量解析器测试

测试IncrementalParser的功能
"""

import pytest
from yanlv.incremental_parser import (
    TextChange,
    ASTNode,
    ASTDiff,
    IncrementalParser,
    ChangeAnalyzer,
    ChangeType
)


class TestASTNode:
    """AST节点测试"""
    
    def test_node_creation(self):
        """测试节点创建"""
        node = ASTNode(
            node_type="Function",
            start_line=1,
            start_column=0,
            end_line=5,
            end_column=10,
            children=[]
        )
        
        assert node.node_type == "Function"
        assert node.start_line == 1
        assert node.end_line == 5
    
    def test_contains(self):
        """测试位置包含检查"""
        node = ASTNode(
            node_type="Function",
            start_line=1,
            start_column=0,
            end_line=5,
            end_column=10,
            children=[]
        )
        
        # 在范围内
        assert node.contains(2, 5)
        assert node.contains(1, 0)
        assert node.contains(5, 10)
        
        # 不在范围内
        assert not node.contains(0, 0)
        assert not node.contains(6, 0)
    
    def test_overlaps(self):
        """测试范围重叠检查"""
        node = ASTNode(
            node_type="Function",
            start_line=2,
            start_column=0,
            end_line=4,
            end_column=10,
            children=[]
        )
        
        # 重叠
        assert node.overlaps(1, 0, 3, 0)
        assert node.overlaps(3, 0, 5, 0)
        
        # 不重叠
        assert not node.overlaps(0, 0, 1, 0)
        assert not node.overlaps(5, 0, 6, 0)


class TestASTDiff:
    """AST差异测试"""
    
    def test_compute_diff_identical(self):
        """测试相同AST的差异"""
        ast1 = ASTNode(
            node_type="Program",
            start_line=1,
            start_column=0,
            end_line=1,
            end_column=10,
            children=[]
        )
        
        ast2 = ASTNode(
            node_type="Program",
            start_line=1,
            start_column=0,
            end_line=1,
            end_column=10,
            children=[]
        )
        
        diff = ASTDiff.compute_diff(ast1, ast2)
        
        assert len(diff["added"]) == 0
        assert len(diff["removed"]) == 0
        assert len(diff["modified"]) == 0
    
    def test_compute_diff_added(self):
        """测试新增节点"""
        ast1 = ASTNode(
            node_type="Program",
            start_line=1,
            start_column=0,
            end_line=1,
            end_column=10,
            children=[]
        )
        
        child = ASTNode(
            node_type="Function",
            start_line=1,
            start_column=0,
            end_line=1,
            end_column=10,
            children=[]
        )
        
        ast2 = ASTNode(
            node_type="Program",
            start_line=1,
            start_column=0,
            end_line=1,
            end_column=10,
            children=[child]
        )
        
        diff = ASTDiff.compute_diff(ast1, ast2)
        
        assert len(diff["added"]) > 0


class TestIncrementalParser:
    """增量解析器测试"""
    
    def test_parser_initialization(self):
        """测试解析器初始化"""
        parser = IncrementalParser()
        assert len(parser.ast_cache) == 0
        assert len(parser.last_parse_time) == 0
    
    def test_parse_incremental_no_old_ast(self):
        """测试没有旧AST时的增量解析"""
        parser = IncrementalParser()
        
        result = parser.parse_incremental("test.yl", None, [])
        
        assert result is not None
        assert result.node_type == "Program"
    
    def test_parse_incremental_with_changes(self):
        """测试有变更时的增量解析"""
        parser = IncrementalParser()
        
        old_ast = ASTNode(
            node_type="Program",
            start_line=1,
            start_column=0,
            end_line=10,
            end_column=0,
            children=[]
        )
        
        changes = [
            TextChange(
                start_line=5,
                start_column=0,
                end_line=5,
                end_column=10,
                change_type=ChangeType.MODIFY,
                old_text="旧代码",
                new_text="新代码"
            )
        ]
        
        result = parser.parse_incremental("test.yl", old_ast, changes)
        
        assert result is not None
    
    def test_invalidate_cache(self):
        """测试缓存失效"""
        parser = IncrementalParser()
        
        # 添加缓存
        parser.ast_cache["test.yl"] = ASTNode(
            node_type="Program",
            start_line=1,
            start_column=0,
            end_line=1,
            end_column=0,
            children=[]
        )
        
        # 使缓存失效
        parser.invalidate_cache("test.yl")
        
        assert "test.yl" not in parser.ast_cache


class TestChangeAnalyzer:
    """变更分析器测试"""
    
    def test_analyze_changes_no_change(self):
        """测试无变更"""
        text = "第一行\n第二行\n第三行"
        
        changes = ChangeAnalyzer.analyze_changes(text, text)
        
        assert len(changes) == 0
    
    def test_analyze_changes_insert(self):
        """测试插入行"""
        old_text = "第一行\n第二行"
        new_text = "第一行\n第二行\n第三行"
        
        changes = ChangeAnalyzer.analyze_changes(old_text, new_text)
        
        assert len(changes) > 0
        assert any(c.change_type == ChangeType.INSERT for c in changes)
    
    def test_analyze_changes_delete(self):
        """测试删除行"""
        old_text = "第一行\n第二行\n第三行"
        new_text = "第一行\n第二行"
        
        changes = ChangeAnalyzer.analyze_changes(old_text, new_text)
        
        assert len(changes) > 0
        assert any(c.change_type == ChangeType.DELETE for c in changes)
    
    def test_analyze_changes_modify(self):
        """测试修改行"""
        old_text = "第一行\n旧第二行\n第三行"
        new_text = "第一行\n新第二行\n第三行"
        
        changes = ChangeAnalyzer.analyze_changes(old_text, new_text)
        
        assert len(changes) > 0
        assert any(c.change_type == ChangeType.MODIFY for c in changes)


class TestTextChange:
    """文本变更测试"""
    
    def test_change_creation(self):
        """测试变更创建"""
        change = TextChange(
            start_line=1,
            start_column=0,
            end_line=1,
            end_column=10,
            change_type=ChangeType.MODIFY,
            old_text="旧文本",
            new_text="新文本"
        )
        
        assert change.start_line == 1
        assert change.change_type == ChangeType.MODIFY
        assert change.old_text == "旧文本"
        assert change.new_text == "新文本"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
