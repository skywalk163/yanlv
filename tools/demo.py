#!/usr/bin/env python3
"""
言律(Yán Lǜ)语言演示脚本

展示词法分析、语义分析和歧义消解功能
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from yanlv.lexer import YanLuLexer
from yanlv.semantic import SemanticContextTracker, TypeInferenceSystem, AmbiguityResolver
from yanlv.lexer.verb_categories import VERB_CATEGORIES, get_verb_category, get_verb_arity


def demo_lexer():
    """演示词法分析器"""
    print("=" * 60)
    print("词法分析器演示")
    print("=" * 60)
    
    lexer = YanLuLexer()
    
    # 示例代码
    examples = [
        "定温度是25。",
        "如果温度大30就开启风扇。",
        "对于i在1到10：印i。",
        "温度变为30度。",
        "张三、李四，计算折扣。",
        "'你好，世界'",
        "真且假",
        "定x等于十加五。",
    ]
    
    for i, code in enumerate(examples, 1):
        print(f"\n示例 {i}: {code}")
        print("-" * 40)
        
        tokens = lexer.tokenize(code)
        
        # 只显示非换行符的词法单元
        for token in tokens:
            if token.type.value != "NEWLINE" and token.type.value != "EOF":
                value_str = str(token.value)
                if len(value_str) > 15:
                    value_str = value_str[:12] + "..."
                
                lexeme_str = token.lexeme
                if len(lexeme_str) > 15:
                    lexeme_str = lexeme_str[:12] + "..."
                
                print(f"  {token.type.value:<15} {value_str:<15} {lexeme_str}")


def demo_verb_categories():
    """演示动词分类词典"""
    print("\n" + "=" * 60)
    print("动词分类词典演示")
    print("=" * 60)
    
    # 显示动词类别统计
    print(f"动词类别数量: {len(VERB_CATEGORIES)}")
    print(f"动词总数: {sum(len(cat['verbs']) for cat in VERB_CATEGORIES.values())}")
    
    # 显示每个类别的动词
    print("\n动词类别详情:")
    for category_name, category_info in VERB_CATEGORIES.items():
        verbs = category_info["verbs"]
        semantic_role = category_info.get("semantic_role", "UNKNOWN")
        print(f"\n{category_name}:")
        print(f"  语义角色: {semantic_role}")
        print(f"  动词数量: {len(verbs)}")
        print(f"  示例动词: {', '.join(verbs[:5])}")
        if len(verbs) > 5:
            print(f"  ... 还有{len(verbs)-5}个")
    
    # 测试动词查询
    print("\n动词查询示例:")
    test_verbs = ["变为", "开启", "计算", "移动", "创建", "删除", "查询", "修改", "发送", "比较"]
    
    for verb in test_verbs:
        category_name, category_info = get_verb_category(verb)
        arity = get_verb_arity(verb)
        
        if category_info:
            semantic_role = category_info.get("semantic_role", "UNKNOWN")
            print(f"  {verb:5} -> 类别: {category_name:20} 语义角色: {semantic_role:20} 元数: {arity}")
        else:
            print(f"  {verb:5} -> 未找到")


def demo_semantic_analysis():
    """演示语义分析"""
    print("\n" + "=" * 60)
    print("语义分析演示")
    print("=" * 60)
    
    # 创建语义上下文和类型推断系统
    context = SemanticContextTracker()
    inference = TypeInferenceSystem(context)
    
    # 设置主题
    context.set_topic("温度控制")
    
    # 添加一些上下文
    context.add_context({
        "sentence": "温度是25度。",
        "entities": ["温度"],
        "subject": "温度",
        "type": "ASSIGNMENT"
    })
    
    context.add_context({
        "sentence": "风扇状态是关闭。",
        "entities": ["风扇"],
        "subject": "风扇",
        "type": "STATE"
    })
    
    # 演示类型推断
    print("类型推断示例:")
    expressions = [
        ("温度", "变量"),
        ("25", "数字字面量"),
        ("真", "布尔字面量"),
        ("温度大30", "比较表达式"),
        ("开启风扇", "动作表达式"),
        ("'高温警告'", "字符串字面量"),
    ]
    
    for expr, desc in expressions:
        result = inference.infer_expression_type(expr)
        print(f"  {desc:15} '{expr:20}' -> 类型: {result['type']:15} 置信度: {result['confidence']:.2f}")
        
        if "suggestions" in result and result["suggestions"]:
            print(f"    建议: {', '.join([s['type'] for s in result['suggestions'][:2]])}")
    
    # 演示语义关系
    print("\n语义关系示例:")
    
    # 添加语义节点
    from yanlv.semantic.context_tracker import SemanticNode, SemanticType
    
    node1 = SemanticNode("n1", "温度", SemanticType.ENTITY, {"value": 25})
    node2 = SemanticNode("n2", "升高", SemanticType.ACTION)
    node3 = SemanticNode("n3", "风扇", SemanticType.ENTITY)
    node4 = SemanticNode("n4", "开启", SemanticType.ACTION)
    
    context.add_node(node1)
    context.add_node(node2)
    context.add_node(node3)
    context.add_node(node4)
    
    # 添加语义边
    from yanlv.semantic.context_tracker import SemanticEdge, SemanticRelation
    
    edge1 = SemanticEdge(node1.id, node2.id, SemanticRelation.SUBJECT_OF)
    edge2 = SemanticEdge(node2.id, node3.id, SemanticRelation.CAUSES)
    edge3 = SemanticEdge(node3.id, node4.id, SemanticRelation.SUBJECT_OF)
    
    context.add_edge(edge1)
    context.add_edge(edge2)
    context.add_edge(edge3)
    
    # 查找关系
    relations = context.find_semantic_relations(node2.id, depth=2)
    print(f"节点'{node2.name}'的关系:")
    for rel_type, rel_list in relations.items():
        print(f"  {rel_type}: {len(rel_list)}个关系")
        for target_id, rel in rel_list[:2]:  # 只显示前2个
            target_node = context.get_node(target_id)
            if target_node:
                print(f"    -> {target_node.name}")


def demo_ambiguity_resolution():
    """演示歧义消解"""
    print("\n" + "=" * 60)
    print("歧义消解演示")
    print("=" * 60)
    
    # 创建语义上下文、类型推断和歧义消解器
    context = SemanticContextTracker()
    inference = TypeInferenceSystem(context)
    resolver = AmbiguityResolver(context, inference)
    
    # 设置上下文
    context.set_topic("智能家居控制")
    context.add_context({
        "sentence": "温度传感器检测到高温。",
        "entities": ["温度传感器", "高温"],
        "subject": "温度传感器",
    })
    context.add_context({
        "sentence": "空调设置为制冷模式。",
        "entities": ["空调", "制冷模式"],
        "subject": "空调",
    })
    
    # 歧义示例
    ambiguous_sentences = [
        ("温度升高，风扇开启。", "时间表达式歧义"),
        ("三个用户和五个订单，计算折扣。", "量词歧义"),
        ("变为开启状态。", "主语省略歧义"),
        ("它需要调整。", "上下文依赖歧义"),
        ("张三、李四和王五，发送消息。", "并列结构歧义"),
        ("快速地运行程序。", "修饰语附着歧义"),
        ("打开发送文件。", "多义歧义"),
        ("自己完成任务。", "代词指代歧义"),
        ("苹果、香蕉……等等。", "省略歧义"),
    ]
    
    for sentence, desc in ambiguous_sentences:
        print(f"\n{desc}:")
        print(f"  句子: {sentence}")
        
        # 检测歧义
        ambiguities = resolver.detect_ambiguity(sentence)
        
        if ambiguities:
            print(f"  检测到 {len(ambiguities)} 个歧义:")
            for i, ambiguity in enumerate(ambiguities[:2], 1):  # 只显示前2个
                print(f"    {i}. 类型: {ambiguity['type'].value}")
                print(f"       匹配: '{ambiguity['match']}'")
                print(f"       置信度: {ambiguity['confidence']:.2f}")
                
                # 消解歧义
                resolution = resolver.resolve_ambiguity(sentence, ambiguity)
                print(f"       消解: {resolution['interpretation']}")
                print(f"       消解置信度: {resolution['confidence']:.2f}")
                
                if resolution.get("strategies"):
                    print(f"       使用策略: {', '.join(resolution['strategies'])}")
        else:
            print("  未检测到歧义")
    
    # 显示统计信息
    stats = resolver.get_resolution_statistics()
    print(f"\n歧义消解统计:")
    print(f"  总消解数: {stats['total_resolutions']}")
    print(f"  平均置信度: {stats['average_confidence']:.2f}")
    print(f"  成功率: {stats['success_rate']:.2%}")


def demo_complete_pipeline():
    """演示完整处理流程"""
    print("\n" + "=" * 60)
    print("完整处理流程演示")
    print("=" * 60)
    
    # 示例代码
    code = """
    定温度是25。
    如果温度大30就开启风扇。
    对于i在1到10：印i。
    温度、湿度，计算舒适度。
    """
    
    print("源代码:")
    print(code)
    
    # 1. 词法分析
    print("\n1. 词法分析:")
    lexer = YanLuLexer()
    tokens = lexer.tokenize(code)
    
    verb_count = 0
    for token in tokens:
        if token.type.value.startswith("VERB_"):
            verb_count += 1
            print(f"  动词: {token.lexeme} ({token.type.value})")
    
    print(f"  总共识别到 {verb_count} 个动词")
    
    # 2. 语义分析
    print("\n2. 语义分析:")
    context = SemanticContextTracker()
    inference = TypeInferenceSystem(context)
    
    # 设置主题
    context.set_topic("环境控制")
    
    # 分析每行代码
    lines = [line.strip() for line in code.strip().split('\n') if line.strip()]
    for line in lines:
        print(f"  分析: {line}")
        
        # 类型推断
        result = inference.infer_expression_type(line)
        if result["type"]:
            print(f"    类型: {result['type']} (置信度: {result['confidence']:.2f})")
        
        # 添加到上下文
        context.add_context({
            "sentence": line,
            "type": result["type"] if result["type"] else "UNKNOWN",
            "confidence": result["confidence"]
        })
    
    # 3. 歧义检测和消解
    print("\n3. 歧义检测和消解:")
    resolver = AmbiguityResolver(context, inference)
    
    ambiguous_lines = [
        "温度、湿度，计算舒适度。",  # 并列结构歧义
        "变为30度后，开启。",        # 主语省略歧义
    ]
    
    for line in ambiguous_lines:
        print(f"  检测: {line}")
        ambiguities = resolver.detect_ambiguity(line)
        
        if ambiguities:
            for amb in ambiguities[:1]:  # 只处理第一个歧义
                resolution = resolver.resolve_ambiguity(line, amb)
                print(f"    歧义: {amb['type'].value}")
                print(f"    消解: {resolution['interpretation']}")
                print(f"    置信度: {resolution['confidence']:.2f}")
        else:
            print("    未检测到歧义")
    
    # 4. 显示语义图
    print("\n4. 语义关系图:")
    nodes = context.get_all_nodes()
    print(f"  节点数量: {len(nodes)}")
    
    for node in nodes[:5]:  # 只显示前5个节点
        print(f"    节点: {node.name} ({node.semantic_type.value})")
        edges = context.get_edges(node.id)
        if edges:
            for edge in edges[:2]:  # 只显示前2个关系
                target = context.get_node(edge.target_id)
                if target:
                    print(f"      关系: {edge.relation.value} -> {target.name}")


def main():
    """主函数"""
    print("言律(Yán Lǜ)语言演示")
    print("=" * 60)
    print("一个基于认知科学的中文原生编程语言")
    print()
    
    # 运行各个演示
    demo_lexer()
    demo_verb_categories()
    demo_semantic_analysis()
    demo_ambiguity_resolution()
    demo_complete_pipeline()
    
    print("\n" + "=" * 60)
    print("演示完成!")
    print("=" * 60)
    
    # 显示项目信息
    print("\n项目组件:")
    print("  ✓ 词法分析器 (支持中文分词和动词分类)")
    print("  ✓ 语义上下文跟踪器 (语义关系图)")
    print("  ✓ 类型推断系统 (6种推断规则)")
    print("  ✓ 歧义消解器 (10种歧义类型)")
    print("  ✓ 动词分类词典 (13个类别，119个动词)")
    print("  ✓ 测试套件 (31个测试用例)")
    
    print("\n核心特性:")
    print("  • 因果链语法")
    print("  • 上下文省略")
    print("  • 状态流")
    print("  • 多轨设计")
    print("  • 元数驱动解析")
    print("  • 百家姓变量命名")
    
    print("\n下一步:")
    print("  1. 实现解析器 (将词法单元转换为AST)")
    print("  2. 实现代码生成器 (生成目标代码)")
    print("  3. 添加标准库和工具链")
    print("  4. 开发IDE插件和文档")


if __name__ == "__main__":
    main()