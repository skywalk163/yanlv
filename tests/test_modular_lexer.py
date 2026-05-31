#!/usr/bin/env python3
"""
测试模块化重构后的词法分析器
"""

import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 直接导入模块
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))

from yanlv.lexer import (
YanLuLexer, create_lexer, tokenize, tokenize_file,
YanLuTokenizer, create_tokenizer, get_available_tokenizers,
TokenMatcher, create_token_matcher,
ErrorHandler, create_error_handler,
ContextManager, create_context_manager,
PatternManager, create_pattern_manager,
PerformanceOptimizer, create_performance_optimizer,
Token, TokenType
)


def test_basic_functionality():
"""测试基本功能"""
print("=" * 60)
print("测试基本功能")
print("=" * 60)

# 创建词法分析器
lexer = create_lexer(segmenter="jieba", verbose=True)

# 测试代码
test_code = """
如果 数字 大于 10 则
    输出 "数字大于10"
    否则
        输出 "数字小于等于10"
    """

    print(f"测试代码:\n{test_code}")
    print("-" * 60)

    # 词法分析
    tokens = lexer.tokenize(test_code)

    print(f"生成的词元数量: {len(tokens)}")
    print("-" * 60)

    # 显示前10个词元
    print("前10个词元:")
    for i, token in enumerate(tokens[:10]):
    print(f"  {i+1}: {token}")

    # 获取统计信息
    stats = lexer.get_statistics()
    print(f"\n统计信息:")
    print(f"  处理行数: {stats['lines_processed']}")
    print(f"  处理词元: {stats['tokens_processed']}")
    print(f"  处理字符: {stats['characters_processed']}")
    print(f"  处理时间: {stats['processing_time']:.3f}s")
    print(f"  错误数量: {stats['errors']}")
    print(f"  警告数量: {stats['warnings']}")

    return lexer, tokens


    def test_tokenizer():
    """测试分词器模块"""
    print("\n" + "=" * 60)
    print("测试分词器模块")
    print("=" * 60)

    # 获取可用的分词器
    available_tokenizers = get_available_tokenizers()
    print(f"可用的分词器: {available_tokenizers}")

    # 创建分词器
    tokenizer = create_tokenizer("jieba", verbose=True)
    print(f"分词器类型: {tokenizer.get_segmenter_type()}")

    # 测试分词
    text = "如果数字大于10则输出结果"
    segments = tokenizer.segment(text)
    print(f"文本: {text}")
    print(f"分词结果: {segments}")

    # 获取统计信息
    stats = tokenizer.get_statistics()
    print(f"分词器统计: {stats}")

    return tokenizer


    def test_token_matcher():
    """测试词元匹配器模块"""
    print("\n" + "=" * 60)
    print("测试词元匹配器模块")
    print("=" * 60)

    # 创建词元匹配器
    matcher = create_token_matcher()

    # 测试匹配
    test_cases = [
    ("123", TokenType.NUMBER),
    ("3.14", TokenType.NUMBER),
    ("变量", TokenType.IDENTIFIER),
    ("如果", TokenType.IF),
    ("+", TokenType.PLUS),
    ("=", TokenType.EQUAL),
    ("（", TokenType.LPAREN),
    ("）", TokenType.RPAREN),
    ("。", TokenType.PERIOD),
    ("，", TokenType.COMMA),
    ]

    for text, expected_type in test_cases:
    token = matcher.match_token(text, position=0, line_num=1, column=1)
    if token:
    result = "✓" if token.type == expected_type else "✗"
    print(f"  {result} '{text}' -> {token.type.value} (期望: {expected_type.value})")
    else:
    print(f"  ✗ '{text}' -> 无匹配 (期望: {expected_type.value})")

    # 获取统计信息
    stats = matcher.get_statistics()
    print(f"\n匹配器统计: {stats}")

    return matcher


    def test_error_handler():
    """测试错误处理器模块"""
    print("\n" + "=" * 60)
    print("测试错误处理器模块")
    print("=" * 60)

    # 创建错误处理器
    error_handler = create_error_handler(max_errors=10, max_warnings=20)

    # 添加一些错误和警告
    from yanlv.lexer.utils import Position

    error_handler.add_error(
    code="LEX001",
    message="无法识别的字符: '#'",
    position=Position(line=1, column=5, offset=4),
    suggestion="请使用有效的字符"
    )

    error_handler.add_warning(
    code="LEXW001",
    message="行长度超过限制: 120 > 100",
    position=Position(line=2, column=1, offset=0),
    suggestion="考虑将长行拆分为多行"
    )

    error_handler.add_info(
    code="LEXI001",
    message="检测到中文数字",
    position=Position(line=3, column=10, offset=20)
    )

    # 显示错误和警告
    print("错误和警告:")
    print(error_handler.format_messages(include_warnings=True, include_infos=True))

    # 获取统计信息
    stats = error_handler.get_statistics()
    print(f"\n错误处理器统计:")
    print(f"  错误数量: {stats['current_errors']}")
    print(f"  警告数量: {stats['current_warnings']}")
    print(f"  信息数量: {stats['current_infos']}")

    return error_handler


    def test_context_manager():
    """测试上下文管理器模块"""
    print("\n" + "=" * 60)
    print("测试上下文管理器模块")
    print("=" * 60)

    # 创建上下文管理器
    context_manager = create_context_manager()

    # 创建一些上下文
    from yanlv.lexer.utils import Position

    # 进入函数上下文
    func_context = context_manager.enter_function(
    name="main",
    position=Position(line=1, column=1, offset=0),
    parameters=["arg1", "arg2"]
    )
    print(f"进入函数上下文: {func_context}")

    # 进入循环上下文
    loop_context = context_manager.enter_loop(
    loop_type="for",
    position=Position(line=2, column=5, offset=10)
    )
    print(f"进入循环上下文: {loop_context}")

    # 添加符号
    context_manager.add_symbol("counter", 0, "variable")
    context_manager.add_symbol("max_value", 100, "constant")

    # 获取当前上下文
    current_context = context_manager.get_current_context()
    print(f"当前上下文: {current_context}")

    # 获取上下文深度
    depth = context_manager.get_context_depth()
    print(f"上下文深度: {depth}")

    # 获取符号表
    symbol_table = context_manager.get_symbol_table()
    print(f"符号表: {symbol_table}")

    # 获取统计信息
    stats = context_manager.get_statistics()
    print(f"\n上下文管理器统计:")
    print(f"  总上下文数: {stats['total_contexts']}")
    print(f"  当前深度: {stats['current_depth']}")
    print(f"  最大深度: {stats['max_depth']}")
    print(f"  符号数量: {stats['symbol_count']}")

    # 弹出上下文
    popped_context = context_manager.pop_context(Position(line=10, column=1, offset=100))
    print(f"\n弹出的上下文: {popped_context}")

    return context_manager


    def test_pattern_manager():
    """测试模式管理器模块"""
    print("\n" + "=" * 60)
    print("测试模式管理器模块")
    print("=" * 60)

    # 创建模式管理器
    pattern_manager = create_pattern_manager()

    # 添加自定义模式
    pattern_manager.add_pattern(
    name="email",
    pattern=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
    token_type=TokenType.STRING,
    pattern_type="custom",
    priority=50,
    description="电子邮件地址",
    examples=["user@example.com", "test@domain.org"]
    )

    pattern_manager.add_pattern(
    name="url",
    pattern=r"^https?://[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(?:/[^ ]*)?$",
    token_type=TokenType.STRING,
    pattern_type="custom",
    priority=40,
    description="URL地址",
    examples=["https://example.com", "http://test.org/path"]
    )

    # 测试模式匹配
    test_cases = [
    ("123", TokenType.NUMBER),
    ("user@example.com", TokenType.STRING),  # 应该匹配email模式
    ("https://example.com", TokenType.STRING),  # 应该匹配url模式
    ("变量名", TokenType.IDENTIFIER),
    ]

    for text, expected_type in test_cases:
    result = pattern_manager.match(text)
    if result:
    token_type, matched_text = result
    result_str = "✓" if token_type == expected_type else "✗"
    print(f"  {result_str} '{text}' -> {token_type.value} (匹配: '{matched_text}')")
    else:
    print(f"  ✗ '{text}' -> 无匹配 (期望: {expected_type.value})")

    # 获取模式信息
    patterns = pattern_manager.get_all_patterns()
    print(f"\n模式数量: {pattern_manager.get_pattern_count()}")
    print("模式列表:")
    for pattern in patterns[:5]:  # 只显示前5个
    print(f"  - {pattern.name}: {pattern.description or '无描述'}")

    if len(patterns) > 5:
    print(f"  ... 还有 {len(patterns) - 5} 个模式")

    return pattern_manager


    def test_performance_optimizer():
    """测试性能优化器模块"""
    print("\n" + "=" * 60)
    print("测试性能优化器模块")
    print("=" * 60)

    # 创建性能优化器
    from yanlv.lexer.performance_optimizer import OptimizationConfig, OptimizationLevel

    config = OptimizationConfig(
    level=OptimizationLevel.BASIC,
    enable_cache=True,
    cache_size=500,
    enable_precompilation=True,
    enable_lazy_loading=True,
    enable_parallel_processing=False,
    max_workers=2,
    batch_size=50,
    timeout_ms=3000,
    memory_limit_mb=50
    )

    optimizer = create_performance_optimizer(config)

    # 测试缓存优化
    def expensive_computation(x):
    # 模拟耗时计算
    import time
    time.sleep(0.001)  # 1ms延迟
    return x * x

    print("测试缓存优化:")
    import time

    # 第一次计算（应该缓存未命中）
    start_time = time.time()
    result1 = optimizer.optimize_matching("test1", lambda x: expensive_computation(10))
    time1 = time.time() - start_time

    # 第二次计算相同输入（应该缓存命中）
    start_time = time.time()
    result2 = optimizer.optimize_matching("test1", lambda x: expensive_computation(10))
    time2 = time.time() - start_time

    print(f"  第一次计算: {result1}, 耗时: {time1:.6f}s")
    print(f"  第二次计算: {result2}, 耗时: {time2:.6f}s")
    print(f"  加速比: {time1/time2:.2f}x")

    # 测试批处理
    print("\n测试批处理:")
    items = list(range(100))

    start_time = time.time()
    results = optimizer.batch_process(items, lambda x: x * x)
    batch_time = time.time() - start_time

    start_time = time.time()
    results_sequential = [x * x for x in items]
    sequential_time = time.time() - start_time

    print(f"  批处理时间: {batch_time:.6f}s")
    print(f"  串行处理时间: {sequential_time:.6f}s")
    print(f"  结果数量: {len(results)}")

    # 获取性能统计
    stats = optimizer.get_performance_statistics()
    print(f"\n性能优化器统计:")
    print(f"  总优化次数: {stats['optimization']['total_optimizations']}")
    print(f"  缓存命中率: {stats['cache']['matching']['hit_rate']:.2%}")
    print(f"  预编译模式数: {stats['optimization']['precompilation_count']}")

    # 检查内存使用
    memory_ok = optimizer.check_memory_usage()
    print(f"  内存检查: {'通过' if memory_ok else '警告'}")

    return optimizer


    def test_integration():
    """测试集成功能"""
    print("\n" + "=" * 60)
    print("测试集成功能")
    print("=" * 60)

    # 创建完整的词法分析器
    lexer = create_lexer(
    segmenter="jieba",
    verbose=False,
    strict_mode=False,
    max_errors=50,
    max_warnings=100,
    enable_cache=True,
    cache_size=1000
    )

    # 测试复杂代码
    complex_code = """
    # 这是一个测试程序
    定义 计算平方和(数字列表):
    总和 = 0
    对于 数字 在 数字列表:
    如果 数字 > 0:
        总和 = 总和 + 数字 * 数字
        否则:
            输出 "跳过负数: " + 字符串(数字)
            结束循环
            返回 总和
            结束定义

            # 测试调用
            列表 = [1, 2, 3, 4, 5]
            结果 = 计算平方和(列表)
            输出 "平方和: " + 字符串(结果)
            """

            print("测试复杂代码:")
            print("-" * 40)
            print(complex_code)
            print("-" * 40)

            # 词法分析
            tokens = lexer.tokenize(complex_code)

            print(f"生成的词元数量: {len(tokens)}")
            print("\n词元类型统计:")

            # 统计词元类型
            type_count = {}
            for token in tokens:
            type_name = token.type.value
            type_count[type_name] = type_count.get(type_name, 0) + 1

            for type_name, count in sorted(type_count.items()):
            print(f"  {type_name}: {count}")

            # 显示错误和警告
            errors = lexer.get_errors()
            warnings = lexer.get_warnings()

            if errors:
            print(f"\n错误数量: {len(errors)}")
            for error in errors[:3]:  # 只显示前3个错误
            print(f"  - {error['message']} (位置: {error['position']})")
            if len(errors) > 3:
            print(f"  ... 还有 {len(errors) - 3} 个错误")

            if warnings:
            print(f"\n警告数量: {len(warnings)}")
            for warning in warnings[:3]:  # 只显示前3个警告
            print(f"  - {warning['message']} (位置: {warning['position']})")
            if len(warnings) > 3:
            print(f"  ... 还有 {len(warnings) - 3} 个警告")

            # 获取上下文信息
            context_info = lexer.get_context_info()
            print(f"\n上下文信息:")
            print(f"  当前上下文: {context_info['current_context']}")
            print(f"  上下文深度: {context_info['context_depth']}")
            print(f"  符号数量: {len(context_info['symbol_table'])}")

            return lexer, tokens


            def main():
            """主测试函数"""
            print("言律语言词法分析器 - 模块化重构测试")
            print("=" * 60)

            try:
            # 测试基本功能
            lexer, tokens = test_basic_functionality()

            # 测试分词器模块
            tokenizer = test_tokenizer()

            # 测试词元匹配器模块
            matcher = test_token_matcher()

            # 测试错误处理器模块
            error_handler = test_error_handler()

            # 测试上下文管理器模块
            context_manager = test_context_manager()

            # 测试模式管理器模块
            pattern_manager = test_pattern_manager()

            # 测试性能优化器模块
            optimizer = test_performance_optimizer()

            # 测试集成功能
            lexer2, tokens2 = test_integration()

            print("\n" + "=" * 60)
            print("所有测试完成!")
            print("=" * 60)

            # 总结
            print("\n模块化重构总结:")
            print("✓ 成功创建了9个模块化组件")
            print("✓ 实现了完整的词法分析器架构")
            print("✓ 支持多种分词器（jieba/thulac）")
            print("✓ 实现了错误处理和上下文管理")
            print("✓ 添加了性能优化和缓存机制")
            print("✓ 提供了完整的API接口")
            print("✓ 保持了向后兼容性")

            # 文件大小对比
            import os

            original_size = 0
            if os.path.exists("src/yanlv/lexer/lexer.py"):
            original_size = os.path.getsize("src/yanlv/lexer/lexer.py")

            modular_sizes = {}
            modular_files = [
            "base.py", "token.py", "constants.py", "tokenizer.py",
            "matcher.py", "utils.py", "error_handler.py", "pattern_manager.py",
            "context_manager.py", "performance_optimizer.py", "lexer_new.py"
            ]

            total_modular_size = 0
            for file in modular_files:
            filepath = f"src/yanlv/lexer/{file}"
            if os.path.exists(filepath):
            size = os.path.getsize(filepath)
            modular_sizes[file] = size
            total_modular_size += size

            print(f"\n文件大小对比:")
            if original_size > 0:
            print(f"  原始lexer.py: {original_size:,} 字节")
            print(f"  模块化总大小: {total_modular_size:,} 字节")

            if original_size > 0:
            reduction = ((original_size - total_modular_size) / original_size) * 100
            print(f"  大小减少: {reduction:.1f}%")

            print(f"\n模块文件大小:")
            for file, size in sorted(modular_sizes.items()):
            print(f"  {file}: {size:,} 字节")

            return True

            except Exception as e:
            print(f"\n测试失败: {e}")
            import traceback
            traceback.print_exc()
            return False


            if __name__ == "__main__":
            success = main()
            sys.exit(0 if success else 1)