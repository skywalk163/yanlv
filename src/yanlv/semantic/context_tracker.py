"""
语义上下文跟踪器

实现语义关系图和类型系统，用于跟踪代码中的语义关系
"""

from enum import Enum
from typing import Dict, List, Set, Optional, Any, Tuple
from dataclasses import dataclass, field
from collections import defaultdict


class SemanticRelation(Enum):
    """语义关系枚举"""
    SUBJECT_OF = "SUBJECT_OF"          # 主语关系
    OBJECT_OF = "OBJECT_OF"            # 宾语关系
    MODIFIES = "MODIFIES"              # 修饰关系
    IS_A = "IS_A"                      # 是关系
    HAS_A = "HAS_A"                    # 有/包含关系
    PART_OF = "PART_OF"                # 部分关系
    CAUSES = "CAUSES"                  # 因果关系
    PRECEDES = "PRECEDES"              # 先后关系
    SIMILAR_TO = "SIMILAR_TO"          # 相似关系
    OPPOSITE_OF = "OPPOSITE_OF"        # 相反关系


class SemanticType(Enum):
    """语义类型枚举"""
    ENTITY = "ENTITY"                  # 实体
    ACTION = "ACTION"                  # 动作
    STATE = "STATE"                    # 状态
    PROPERTY = "PROPERTY"              # 属性
    RELATION = "RELATION"              # 关系
    EVENT = "EVENT"                    # 事件
    CONCEPT = "CONCEPT"                # 概念


@dataclass
class SemanticNode:
    """语义图节点"""
    
    id: str                           # 节点ID
    name: str                         # 节点名称
    semantic_type: SemanticType       # 语义类型
    attributes: Dict[str, Any] = field(default_factory=dict)  # 属性
    position: Optional[Tuple[int, int]] = None  # 位置(行,列)


@dataclass
class SemanticEdge:
    """语义图边"""
    
    source_id: str                    # 源节点ID
    target_id: str                    # 目标节点ID
    relation: SemanticRelation        # 关系类型
    weight: float = 1.0               # 关系权重
    attributes: Dict[str, Any] = field(default_factory=dict)  # 边属性


class SemanticContextTracker:
    """语义上下文跟踪器"""
    
    def __init__(self, max_history: int = 10):
        """
        初始化语义上下文跟踪器
        
        Args:
            max_history: 最大历史记录数
        """
        self.nodes: Dict[str, SemanticNode] = {}
        self.edges: List[SemanticEdge] = []
        self.context_history: List[Dict[str, Any]] = []
        self.max_history = max_history
        
        # 主题链跟踪
        self.topic_chain: List[str] = []
        self.current_topic: Optional[str] = None
        
        # 变量类型推断
        self.variable_types: Dict[str, SemanticType] = {}
        
        # 函数签名
        self.function_signatures: Dict[str, Dict[str, Any]] = {}
        
        # 状态跟踪
        self.states: Dict[str, Any] = {}
        
    def add_node(self, node: SemanticNode) -> None:
        """添加语义节点"""
        self.nodes[node.id] = node
        
    def add_edge(self, edge: SemanticEdge) -> None:
        """添加语义边"""
        self.edges.append(edge)
        
    def get_node(self, node_id: str) -> Optional[SemanticNode]:
        """获取语义节点"""
        return self.nodes.get(node_id)
    
    def get_edges(self, node_id: str, relation: Optional[SemanticRelation] = None) -> List[SemanticEdge]:
        """获取与节点相关的边"""
        result = []
        for edge in self.edges:
            if edge.source_id == node_id or edge.target_id == node_id:
                if relation is None or edge.relation == relation:
                    result.append(edge)
        return result
    
    def add_context(self, context: Dict[str, Any]) -> None:
        """添加上下文记录"""
        self.context_history.append(context)
        if len(self.context_history) > self.max_history:
            self.context_history.pop(0)
    
    def get_recent_context(self, n: int = 5) -> List[Dict[str, Any]]:
        """获取最近的上下文记录"""
        return self.context_history[-n:] if self.context_history else []
    
    def set_topic(self, topic: str) -> None:
        """设置当前主题"""
        self.current_topic = topic
        self.topic_chain.append(topic)
        
    def get_topic(self) -> Optional[str]:
        """获取当前主题"""
        return self.current_topic
    
    def get_topic_chain(self) -> List[str]:
        """获取主题链"""
        return self.topic_chain.copy()
    
    def infer_variable_type(self, variable_name: str, value: Any) -> SemanticType:
        """推断变量类型"""
        if isinstance(value, bool):
            var_type = SemanticType.STATE
        elif isinstance(value, (int, float)):
            var_type = SemanticType.PROPERTY
        elif isinstance(value, str):
            # 根据内容推断类型
            if value.endswith("状态"):
                var_type = SemanticType.STATE
            elif value.endswith("动作"):
                var_type = SemanticType.ACTION
            elif value.endswith("属性"):
                var_type = SemanticType.PROPERTY
            else:
                var_type = SemanticType.ENTITY
        elif isinstance(value, list):
            var_type = SemanticType.RELATION
        elif isinstance(value, dict):
            var_type = SemanticType.CONCEPT
        else:
            var_type = SemanticType.ENTITY
            
        self.variable_types[variable_name] = var_type
        return var_type
    
    def get_variable_type(self, variable_name: str) -> Optional[SemanticType]:
        """获取变量类型"""
        return self.variable_types.get(variable_name)
    
    def register_function(self, func_name: str, params: List[str], return_type: SemanticType) -> None:
        """注册函数签名"""
        self.function_signatures[func_name] = {
            "params": params,
            "return_type": return_type
        }
    
    def get_function_signature(self, func_name: str) -> Optional[Dict[str, Any]]:
        """获取函数签名"""
        return self.function_signatures.get(func_name)
    
    def update_state(self, state_name: str, value: Any) -> None:
        """更新状态"""
        self.states[state_name] = value
    
    def get_state(self, state_name: str) -> Any:
        """获取状态"""
        return self.states.get(state_name)
    
    def find_semantic_relations(self, node_id: str, depth: int = 2) -> Dict[str, List[Tuple[str, SemanticRelation]]]:
        """
        查找节点的语义关系
        
        Args:
            node_id: 节点ID
            depth: 搜索深度
            
        Returns:
            字典: {关系类型: [(相关节点ID, 关系)]}
        """
        result = defaultdict(list)
        visited = set()
        
        def dfs(current_id: str, current_depth: int, relation_path: List[Tuple[str, SemanticRelation]]):
            if current_depth > depth or current_id in visited:
                return
                
            visited.add(current_id)
            
            for edge in self.get_edges(current_id):
                if edge.source_id == current_id:
                    neighbor_id = edge.target_id
                else:
                    neighbor_id = edge.source_id
                    
                result[edge.relation.value].append((neighbor_id, edge.relation))
                
                if current_depth < depth:
                    dfs(neighbor_id, current_depth + 1, relation_path + [(neighbor_id, edge.relation)])
        
        dfs(node_id, 0, [])
        return dict(result)
    
    def analyze_sentence(self, sentence: str, position: Tuple[int, int]) -> Dict[str, Any]:
        """
        分析句子的语义
        
        Args:
            sentence: 句子文本
            position: 位置(行,列)
            
        Returns:
            语义分析结果
        """
        # 这里实现句子语义分析逻辑
        # 实际实现需要结合分词和语法分析
        
        analysis = {
            "sentence": sentence,
            "position": position,
            "entities": [],
            "actions": [],
            "relations": [],
            "topic": None,
            "type": None
        }
        
        # 简单关键词匹配
        if "变为" in sentence or "变成" in sentence:
            analysis["type"] = "STATE_TRANSITION"
        elif "等于" in sentence or "是" in sentence:
            analysis["type"] = "ASSIGNMENT"
        elif "印" in sentence or "显示" in sentence:
            analysis["type"] = "OUTPUT"
        elif "如果" in sentence or "要是" in sentence:
            analysis["type"] = "CONDITIONAL"
        elif "对于" in sentence:
            analysis["type"] = "LOOP"
        else:
            analysis["type"] = "STATEMENT"
        
        # 提取主题（第一个名词）
        words = sentence.replace("，", " ").replace("。", " ").split()
        if words:
            analysis["topic"] = words[0]
            
        return analysis
    
    def clear(self) -> None:
        """清除所有上下文"""
        self.nodes.clear()
        self.edges.clear()
        self.context_history.clear()
        self.topic_chain.clear()
        self.current_topic = None
        self.variable_types.clear()
        self.function_signatures.clear()
        self.states.clear()
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典表示"""
        return {
            "nodes": {k: {
                "id": v.id,
                "name": v.name,
                "type": v.semantic_type.value,
                "attributes": v.attributes,
                "position": v.position
            } for k, v in self.nodes.items()},
            "edges": [{
                "source": e.source_id,
                "target": e.target_id,
                "relation": e.relation.value,
                "weight": e.weight,
                "attributes": e.attributes
            } for e in self.edges],
            "topic_chain": self.topic_chain,
            "current_topic": self.current_topic,
            "variable_types": {k: v.value for k, v in self.variable_types.items()},
            "function_signatures": self.function_signatures,
            "states": self.states,
            "context_history": self.context_history[-self.max_history:]
        }


# 测试函数
def test_semantic_context_tracker():
    """测试语义上下文跟踪器"""
    print("语义上下文跟踪器测试")
    print("=" * 50)
    
    tracker = SemanticContextTracker(max_history=5)
    
    # 测试1: 添加节点和边
    node1 = SemanticNode("n1", "温度", SemanticType.ENTITY, {"value": 25})
    node2 = SemanticNode("n2", "升高", SemanticType.ACTION)
    node3 = SemanticNode("n3", "风扇", SemanticType.ENTITY)
    node4 = SemanticNode("n4", "开启", SemanticType.ACTION)
    
    tracker.add_node(node1)
    tracker.add_node(node2)
    tracker.add_node(node3)
    tracker.add_node(node4)
    
    edge1 = SemanticEdge("n1", "n2", SemanticRelation.SUBJECT_OF)
    edge2 = SemanticEdge("n2", "n3", SemanticRelation.CAUSES)
    edge3 = SemanticEdge("n3", "n4", SemanticRelation.SUBJECT_OF)
    
    tracker.add_edge(edge1)
    tracker.add_edge(edge2)
    tracker.add_edge(edge3)
    
    print("测试1: 节点和边添加")
    print(f"节点数量: {len(tracker.nodes)}")
    print(f"边数量: {len(tracker.edges)}")
    print()
    
    # 测试2: 获取节点和边
    print("测试2: 获取节点和边")
    node = tracker.get_node("n1")
    if node:
        print(f"节点n1: {node.name} ({node.semantic_type.value})")
    
    edges = tracker.get_edges("n2")
    print(f"节点n2的边: {len(edges)}条")
    for e in edges:
        print(f"  {e.source_id} -> {e.target_id} ({e.relation.value})")
    print()
    
    # 测试3: 上下文历史
    print("测试3: 上下文历史")
    tracker.add_context({"sentence": "温度升高", "type": "STATE_CHANGE"})
    tracker.add_context({"sentence": "风扇开启", "type": "ACTION"})
    
    recent = tracker.get_recent_context(2)
    print(f"最近2个上下文: {len(recent)}个")
    for ctx in recent:
        print(f"  {ctx}")
    print()
    
    # 测试4: 主题链
    print("测试4: 主题链")
    tracker.set_topic("温度控制")
    tracker.set_topic("风扇控制")
    
    print(f"当前主题: {tracker.get_topic()}")
    print(f"主题链: {tracker.get_topic_chain()}")
    print()
    
    # 测试5: 变量类型推断
    print("测试5: 变量类型推断")
    var_type1 = tracker.infer_variable_type("温度值", 25)
    var_type2 = tracker.infer_variable_type("开关状态", True)
    var_type3 = tracker.infer_variable_type("设备名称", "风扇")
    
    print(f"温度值 类型: {var_type1.value}")
    print(f"开关状态 类型: {var_type2.value}")
    print(f"设备名称 类型: {var_type3.value}")
    print()
    
    # 测试6: 函数注册
    print("测试6: 函数注册")
    tracker.register_function("计算温度", ["当前温度", "目标温度"], SemanticType.PROPERTY)
    
    func_sig = tracker.get_function_signature("计算温度")
    if func_sig:
        print(f"函数签名: {func_sig}")
    print()
    
    # 测试7: 状态管理
    print("测试7: 状态管理")
    tracker.update_state("系统状态", "运行中")
    tracker.update_state("温度", 28)
    
    print(f"系统状态: {tracker.get_state('系统状态')}")
    print(f"温度: {tracker.get_state('温度')}")
    print()
    
    # 测试8: 语义关系查找
    print("测试8: 语义关系查找")
    relations = tracker.find_semantic_relations("n1", depth=2)
    print(f"节点n1的语义关系:")
    for rel_type, rel_list in relations.items():
        print(f"  {rel_type}: {len(rel_list)}个关系")
    print()
    
    # 测试9: 句子分析
    print("测试9: 句子分析")
    analysis = tracker.analyze_sentence("温度升高，风扇开启。", (1, 1))
    print(f"句子分析结果: {analysis}")
    print()
    
    # 测试10: 转换为字典
    print("测试10: 转换为字典")
    data = tracker.to_dict()
    print(f"数据结构键: {list(data.keys())}")
    print(f"节点数量: {len(data['nodes'])}")
    print(f"边数量: {len(data['edges'])}")
    
    print("=" * 50)
    print("测试完成")


if __name__ == "__main__":
    test_semantic_context_tracker()