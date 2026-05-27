"""
言律语言增量解析器

支持在代码变更时只重新解析受影响的部分
"""

from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum


class ChangeType(Enum):
    """变更类型"""
    INSERT = "插入"
    DELETE = "删除"
    MODIFY = "修改"


@dataclass
class TextChange:
    """文本变更"""
    start_line: int          # 起始行
    start_column: int        # 起始列
    end_line: int            # 结束行
    end_column: int          # 结束列
    change_type: ChangeType  # 变更类型
    old_text: str            # 旧文本
    new_text: str            # 新文本


@dataclass
class ASTNode:
    """AST节点(简化版)"""
    node_type: str           # 节点类型
    start_line: int          # 起始行
    start_column: int        # 起始列
    end_line: int            # 结束行
    end_column: int          # 结束列
    children: List['ASTNode'] # 子节点
    parent: Optional['ASTNode'] = None  # 父节点
    
    def contains(self, line: int, column: int) -> bool:
        """检查位置是否在节点范围内"""
        if line < self.start_line or line > self.end_line:
            return False
        if line == self.start_line and column < self.start_column:
            return False
        if line == self.end_line and column > self.end_column:
            return False
        return True
    
    def overlaps(self, start_line: int, start_col: int, end_line: int, end_col: int) -> bool:
        """检查是否与范围重叠"""
        # 检查范围是否在节点之前
        if end_line < self.start_line:
            return False
        if end_line == self.start_line and end_col < self.start_column:
            return False
        
        # 检查范围是否在节点之后
        if start_line > self.end_line:
            return False
        if start_line == self.end_line and start_col > self.end_column:
            return False
        
        return True


class ASTDiff:
    """AST差异计算器"""
    
    @staticmethod
    def compute_diff(old_ast: ASTNode, new_ast: ASTNode) -> Dict[str, Any]:
        """
        计算AST差异
        
        Args:
            old_ast: 旧AST
            new_ast: 新AST
            
        Returns:
            差异信息
        """
        diff = {
            "added": [],      # 新增节点
            "removed": [],    # 删除节点
            "modified": []    # 修改节点
        }
        
        # 收集所有节点
        old_nodes = ASTDiff._collect_nodes(old_ast)
        new_nodes = ASTDiff._collect_nodes(new_ast)
        
        # 找出新增的节点
        for node in new_nodes:
            if not ASTDiff._find_matching_node(node, old_nodes):
                diff["added"].append(node)
        
        # 找出删除的节点
        for node in old_nodes:
            if not ASTDiff._find_matching_node(node, new_nodes):
                diff["removed"].append(node)
        
        # 找出修改的节点
        for new_node in new_nodes:
            old_node = ASTDiff._find_matching_node(new_node, old_nodes)
            if old_node and ASTDiff._is_modified(old_node, new_node):
                diff["modified"].append({
                    "old": old_node,
                    "new": new_node
                })
        
        return diff
    
    @staticmethod
    def _collect_nodes(node: ASTNode) -> List[ASTNode]:
        """收集所有节点"""
        nodes = [node]
        for child in node.children:
            nodes.extend(ASTDiff._collect_nodes(child))
        return nodes
    
    @staticmethod
    def _find_matching_node(target: ASTNode, nodes: List[ASTNode]) -> Optional[ASTNode]:
        """查找匹配的节点"""
        for node in nodes:
            if (node.node_type == target.node_type and
                node.start_line == target.start_line and
                node.start_column == target.start_column):
                return node
        return None
    
    @staticmethod
    def _is_modified(old_node: ASTNode, new_node: ASTNode) -> bool:
        """检查节点是否被修改"""
        return (old_node.end_line != new_node.end_line or
                old_node.end_column != new_node.end_column)


class IncrementalParser:
    """
    增量解析器
    
    支持增量解析,只重新解析受影响的部分
    """
    
    def __init__(self):
        """初始化增量解析器"""
        self.ast_cache: Dict[str, ASTNode] = {}
        self.last_parse_time: Dict[str, float] = {}
    
    def parse_incremental(
        self,
        file_path: str,
        old_ast: Optional[ASTNode],
        changes: List[TextChange]
    ) -> ASTNode:
        """
        增量解析
        
        Args:
            file_path: 文件路径
            old_ast: 旧AST
            changes: 变更列表
            
        Returns:
            新AST
        """
        if old_ast is None:
            # 没有旧AST,进行全量解析
            return self._parse_full(file_path)
        
        # 计算受影响的范围
        affected_ranges = self._compute_affected_ranges(old_ast, changes)
        
        # 如果影响范围太大,进行全量解析
        if self._should_full_parse(affected_ranges, old_ast):
            return self._parse_full(file_path)
        
        # 增量解析受影响的部分
        return self._parse_affected(file_path, old_ast, affected_ranges)
    
    def _compute_affected_ranges(
        self,
        ast: ASTNode,
        changes: List[TextChange]
    ) -> List[Tuple[int, int, int, int]]:
        """
        计算受影响的范围
        
        Args:
            ast: AST
            changes: 变更列表
            
        Returns:
            受影响的范围列表[(start_line, start_col, end_line, end_col)]
        """
        affected = []
        
        for change in changes:
            # 找到包含变更的最小节点
            affected_node = self._find_affected_node(ast, change)
            
            if affected_node:
                # 扩展到语句边界
                range_start = self._find_statement_start(ast, affected_node)
                range_end = self._find_statement_end(ast, affected_node)
                
                affected.append((
                    range_start.start_line,
                    range_start.start_column,
                    range_end.end_line,
                    range_end.end_column
                ))
        
        return affected
    
    def _find_affected_node(self, ast: ASTNode, change: TextChange) -> Optional[ASTNode]:
        """找到受变更影响的节点"""
        # 从根节点开始查找
        current = ast
        
        while current:
            # 检查变更是否在当前节点范围内
            if current.contains(change.start_line, change.start_column):
                # 检查子节点
                found_in_child = False
                for child in current.children:
                    if child.contains(change.start_line, change.start_column):
                        current = child
                        found_in_child = True
                        break
                
                # 如果没有子节点包含变更,返回当前节点
                if not found_in_child:
                    return current
            else:
                break
        
        return current
    
    def _find_statement_start(self, ast: ASTNode, node: ASTNode) -> ASTNode:
        """找到语句的起始节点"""
        # 向上查找,直到找到语句级别的节点
        current = node
        while current.parent:
            parent = current.parent
            # 如果父节点是块级节点,返回当前节点
            if parent.node_type in ["Block", "Program", "Function"]:
                return current
            current = parent
        return current
    
    def _find_statement_end(self, ast: ASTNode, node: ASTNode) -> ASTNode:
        """找到语句的结束节点"""
        # 简化实现:返回节点本身
        return node
    
    def _should_full_parse(
        self,
        affected_ranges: List[Tuple[int, int, int, int]],
        ast: ASTNode
    ) -> bool:
        """
        判断是否应该进行全量解析
        
        Args:
            affected_ranges: 受影响的范围
            ast: AST
            
        Returns:
            是否进行全量解析
        """
        if not affected_ranges:
            return False
        
        # 计算受影响的总行数
        total_affected_lines = sum(
            end_line - start_line + 1
            for start_line, start_col, end_line, end_col in affected_ranges
        )
        
        # 计算AST的总行数
        total_lines = ast.end_line - ast.start_line + 1
        
        # 如果受影响的行数超过30%,进行全量解析
        return total_affected_lines > total_lines * 0.3
    
    def _parse_full(self, file_path: str) -> ASTNode:
        """
        全量解析
        
        Args:
            file_path: 文件路径
            
        Returns:
            AST
        """
        # 简化实现:创建一个基本的AST
        # 实际实现应该调用完整的解析器
        return ASTNode(
            node_type="Program",
            start_line=1,
            start_column=0,
            end_line=1,
            end_column=0,
            children=[]
        )
    
    def _parse_affected(
        self,
        file_path: str,
        old_ast: ASTNode,
        affected_ranges: List[Tuple[int, int, int, int]]
    ) -> ASTNode:
        """
        解析受影响的部分
        
        Args:
            file_path: 文件路径
            old_ast: 旧AST
            affected_ranges: 受影响的范围
            
        Returns:
            新AST
        """
        # 简化实现:返回旧AST
        # 实际实现应该只重新解析受影响的部分
        return old_ast
    
    def invalidate_cache(self, file_path: str) -> None:
        """
        使缓存失效
        
        Args:
            file_path: 文件路径
        """
        if file_path in self.ast_cache:
            del self.ast_cache[file_path]
        if file_path in self.last_parse_time:
            del self.last_parse_time[file_path]


class ChangeAnalyzer:
    """变更分析器"""
    
    @staticmethod
    def analyze_changes(
        old_text: str,
        new_text: str
    ) -> List[TextChange]:
        """
        分析文本变更
        
        Args:
            old_text: 旧文本
            new_text: 新文本
            
        Returns:
            变更列表
        """
        changes = []
        
        old_lines = old_text.split('\n')
        new_lines = new_text.split('\n')
        
        # 简化实现:比较每一行
        max_lines = max(len(old_lines), len(new_lines))
        
        for i in range(max_lines):
            old_line = old_lines[i] if i < len(old_lines) else ""
            new_line = new_lines[i] if i < len(new_lines) else ""
            
            if old_line != new_line:
                if i >= len(old_lines):
                    # 新增行
                    changes.append(TextChange(
                        start_line=i + 1,
                        start_column=0,
                        end_line=i + 1,
                        end_column=len(new_line),
                        change_type=ChangeType.INSERT,
                        old_text="",
                        new_text=new_line
                    ))
                elif i >= len(new_lines):
                    # 删除行
                    changes.append(TextChange(
                        start_line=i + 1,
                        start_column=0,
                        end_line=i + 1,
                        end_column=len(old_line),
                        change_type=ChangeType.DELETE,
                        old_text=old_line,
                        new_text=""
                    ))
                else:
                    # 修改行
                    changes.append(TextChange(
                        start_line=i + 1,
                        start_column=0,
                        end_line=i + 1,
                        end_column=max(len(old_line), len(new_line)),
                        change_type=ChangeType.MODIFY,
                        old_text=old_line,
                        new_text=new_line
                    ))
        
        return changes
