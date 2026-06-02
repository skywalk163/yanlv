"""
测试歧义消解增强功能

测试新增的功能：
1. 消解历史记录
2. 统计信息收集
3. 动词歧义消解
4. 优化的置信度算法
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from yanlv.semantic.context_tracker import SemanticContextTracker, SemanticType
from yanlv.semantic.type_inference import TypeInferenceSystem
from yanlv.semantic.ambiguity_resolver import AmbiguityResolver, AmbiguityType
from yanlv.lexer.verb_categories import resolve_verb_ambiguity, VerbCategory


def test_ambiguity_history():
    """测试消解历史记录功能"""
    print("\n" + "=" * 60)
    print("测试1: 消解历史记录功能")
    print("=" * 60)

    # 创建消解器
    context = SemanticContextTracker()
    type_inference = TypeInferenceSystem(context)
    resolver = AmbiguityResolver(context, type_inference)

    # 设置上下文
    context.set_topic("温度控制")
    context.add_context({
        "sentence": "温度是25度。",
        "entities": ["温度"],
        "subject": "温度",
    })

    # 测试多个表达式
    test_expressions = [
        "温度变为30度后，风扇开启。",
        "三个用户和五个订单，计算折扣。",
        "变为开启状态。",
        "它需要调整。",
    ]

    for expr in test_expressions:
        print(f"\n处理表达式: {expr}")
        ambiguities = resolver.detect_ambiguity(expr)
        if ambiguities:
            for amb in ambiguities:
                resolution = resolver.resolve_ambiguity(expr, amb)
                print(f"  - 歧义类型: {amb['type'].value}")
                print(f"    消解结果: {resolution['interpretation']}")
                print(f"    置信度: {resolution['confidence']:.2f}")

    # 检查历史记录
    resolutions = context.get_ambiguity_resolutions()
    print(f"\n历史记录数量: {len(resolutions)}")
    assert len(resolutions) > 0, "历史记录应该不为空"

    # 测试按类型过滤
    time_resolutions = context.get_ambiguity_resolutions(
        ambiguity_type="time_expression"
    )
    print(f"时间表达式歧义记录: {len(time_resolutions)}")

    print("[PASS] 消解历史记录功能测试通过")


def test_statistics():
    """测试统计信息收集功能"""
    print("\n" + "=" * 60)
    print("测试2: 统计信息收集功能")
    print("=" * 60)

    # 创建消解器
    context = SemanticContextTracker()
    type_inference = TypeInferenceSystem(context)
    resolver = AmbiguityResolver(context, type_inference)

    # 处理多个表达式
    expressions = [
        "温度大于28，开启空调制冷。",
        "三个苹果和五个香蕉。",
        "变为开启状态。",
        "它需要调整。",
        "张三、李四和王五，发送消息。",
    ]

    for expr in expressions:
        ambiguities = resolver.detect_ambiguity(expr)
        for amb in ambiguities:
            resolver.resolve_ambiguity(expr, amb)

    # 获取统计信息
    stats = resolver.get_resolution_statistics()

    print(f"\n统计信息:")
    print(f"  总消解数: {stats['total_resolutions']}")
    print(f"  平均置信度: {stats['average_confidence']:.2f}")
    print(f"  成功率: {stats['success_rate']:.2%}")
    print(f"  高置信度数量: {stats['high_confidence_count']}")
    print(f"  低置信度数量: {stats['low_confidence_count']}")

    print(f"\n按类型统计:")
    for type_name, count in stats['by_type'].items():
        print(f"  {type_name}: {count}")

    print(f"\n按策略统计:")
    for strategy, count in stats['by_strategy'].items():
        print(f"  {strategy}: {count}")

    assert stats['total_resolutions'] > 0, "应该有消解记录"
    assert 0 <= stats['average_confidence'] <= 1, "置信度应在0-1之间"
    assert 0 <= stats['success_rate'] <= 1, "成功率应在0-1之间"

    print("[PASS] 统计信息收集功能测试通过")


def test_verb_ambiguity():
    """测试动词歧义消解"""
    print("\n" + "=" * 60)
    print("测试3: 动词歧义消解")
    print("=" * 60)

    # 测试用例
    test_cases = [
        ("打", {"text": "计算数学题"}, "calculate"),
        ("打", {"text": "打电话联系"}, "call"),
        ("打", {"text": "打开文件"}, "open"),
        ("打", {"text": "打印输出"}, "print"),
        ("打", {"text": "打球运动"}, "hit"),
        ("行", {"text": "行走移动"}, "walk"),
        ("行", {"text": "行为做法"}, "behavior"),
        ("行", {"text": "表格行列"}, "row"),
        ("发", {"text": "发现找到"}, "discover"),
        ("发", {"text": "发送消息"}, "send"),
        ("发", {"text": "开发发展"}, "develop"),
        ("开", {"text": "开启启动"}, "open"),
        ("开", {"text": "开始启动"}, "start"),
        ("关", {"text": "关闭文件"}, "close"),
        ("关", {"text": "关联相关"}, "relate"),
        ("设", {"text": "设置配置"}, "set"),
        ("设", {"text": "定义设定"}, "define"),
    ]

    for verb, context, expected_meaning in test_cases:
        result = resolve_verb_ambiguity(verb, context)
        resolved = result.get("resolved_meaning", "")
        confidence = result.get("confidence", 0)

        print(f"\n动词: {verb}")
        print(f"  上下文: {context['text']}")
        print(f"  消解结果: {resolved}")
        print(f"  期望结果: {expected_meaning}")
        print(f"  置信度: {confidence:.2f}")

        # 验证结果
        if expected_meaning:
            assert resolved == expected_meaning, f"消解结果应为 {expected_meaning}"
        assert 0 <= confidence <= 1, "置信度应在0-1之间"

    print("\n[PASS] 动词歧义消解测试通过")


def test_confidence_algorithm():
    """测试优化的置信度算法"""
    print("\n" + "=" * 60)
    print("测试4: 优化的置信度算法")
    print("=" * 60)

    # 创建消解器
    context = SemanticContextTracker()
    type_inference = TypeInferenceSystem(context)
    resolver = AmbiguityResolver(context, type_inference)

    # 设置丰富的上下文
    context.set_topic("智能家居控制")
    context.add_context({
        "sentence": "温度传感器检测到温度变化。",
        "entities": ["温度", "传感器"],
        "subject": "温度",
        "topic": "温度",
    })
    context.add_context({
        "sentence": "空调系统准备就绪。",
        "entities": ["空调", "系统"],
        "subject": "空调",
        "topic": "空调",
    })

    # 测试表达式
    expression = "温度大于28度，空调开启制冷模式。"
    print(f"\n表达式: {expression}")
    print(f"当前主题: {context.get_topic()}")

    # 检测和消解歧义
    ambiguities = resolver.detect_ambiguity(expression)

    print(f"\n检测到 {len(ambiguities)} 个歧义:")
    for i, amb in enumerate(ambiguities, 1):
        print(f"\n{i}. 歧义类型: {amb['type'].value}")
        print(f"   匹配文本: {amb['match']}")
        print(f"   位置: {amb['start']}-{amb['end']}")
        print(f"   初始置信度: {amb['confidence']:.2f}")

        # 消解歧义
        resolution = resolver.resolve_ambiguity(expression, amb)
        print(f"   消解结果: {resolution['interpretation']}")
        print(f"   最终置信度: {resolution['confidence']:.2f}")
        print(f"   使用策略: {', '.join(resolution['strategies'])}")

        # 验证置信度在合理范围
        assert 0 < resolution['confidence'] < 1, "置信度应在0-1之间"

    # 添加用户反馈并重新测试
    print("\n添加用户反馈...")
    if ambiguities:
        first_amb = ambiguities[0]
        resolver.add_user_feedback(
            first_amb['type'],
            first_amb['match'],
            resolver.resolve_ambiguity(expression, first_amb),
            0.9  # 高置信度反馈
        )

        # 重新检测，置信度应该提高
        new_ambiguities = resolver.detect_ambiguity(expression)
        if new_ambiguities:
            new_first = new_ambiguities[0]
            print(f"反馈后置信度: {new_first['confidence']:.2f}")

    print("\n[PASS] 优化的置信度算法测试通过")


def test_integration():
    """集成测试"""
    print("\n" + "=" * 60)
    print("测试5: 集成测试")
    print("=" * 60)

    # 创建完整的消解系统
    context = SemanticContextTracker(max_history=20)
    type_inference = TypeInferenceSystem(context)
    resolver = AmbiguityResolver(context, type_inference)

    # 模拟实际使用场景
    scenarios = [
        {
            "topic": "订单处理",
            "context": {
                "sentence": "用户提交了订单。",
                "entities": ["用户", "订单"],
                "subject": "用户",
            },
            "expressions": [
                "订单状态变为已付款，准备发货。",
                "三个商品和五个赠品。",
                "它需要处理。",
            ]
        },
        {
            "topic": "设备控制",
            "context": {
                "sentence": "智能设备已连接。",
                "entities": ["设备"],
                "subject": "设备",
            },
            "expressions": [
                "温度大于28，开启空调。",
                "湿度小于30，开启加湿器。",
                "变为自动模式。",
            ]
        },
    ]

    for scenario in scenarios:
        print(f"\n场景: {scenario['topic']}")
        context.set_topic(scenario['topic'])
        context.add_context(scenario['context'])

        for expr in scenario['expressions']:
            print(f"\n  表达式: {expr}")
            ambiguities = resolver.detect_ambiguity(expr)

            for amb in ambiguities:
                resolution = resolver.resolve_ambiguity(expr, amb)
                print(f"    - {amb['type'].value}: {resolution['interpretation']} "
                      f"(置信度: {resolution['confidence']:.2f})")

    # 最终统计
    stats = resolver.get_resolution_statistics()
    print(f"\n最终统计:")
    print(f"  总消解数: {stats['total_resolutions']}")
    print(f"  平均置信度: {stats['average_confidence']:.2f}")
    print(f"  成功率: {stats['success_rate']:.2%}")

    # 验证统计数据的合理性
    assert stats['total_resolutions'] > 0, "应该有消解记录"
    assert stats['average_confidence'] > 0.5, "平均置信度应该较高"

    print("\n[PASS] 集成测试通过")


def main():
    """运行所有测试"""
    print("\n" + "=" * 60)
    print("歧义消解增强功能测试")
    print("=" * 60)

    try:
        test_ambiguity_history()
        test_statistics()
        test_verb_ambiguity()
        test_confidence_algorithm()
        test_integration()

        print("\n" + "=" * 60)
        print("[PASS] 所有测试通过！")
        print("=" * 60)

    except AssertionError as e:
        print(f"\n[FAIL] 测试失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] 测试出错: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
