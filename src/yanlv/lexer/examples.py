#!/usr/bin/env python3
"""
言律语言词法分析器 - 使用示例

展示各种使用场景和最佳实践
"""

import sys
import os

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lexer_modular import create_lexer, tokenize, tokenize_with_stats
from lexer_token import TokenType
from tokenizer import YanLuTokenizer
from matcher import TokenMatcher
from error_handler import ErrorHandler, ErrorCode
from performance_optimizer import PerformanceOptimizer, OptimizationLevel
from utils import Position


def example_basic_usage():
    """基本使用示例"""
    print("\n" + "="*60)
    print("示例1: 基本使用")
    print("="*60)
    
    # 创建词法分析器
    lexer = create_lexer("jieba")
    
    # 分析源代码
    source_code = "如果 条件 成立 则 输出 'Hello World'"
    tokens = lexer.tokenize(source_code)
    
    # 显示结果
    print(f"源代码: {source_code}")
    print(f"词元数量: {len(tokens)}")
    print("\n词元列表:")
    for i, token in enumerate(tokens[:10], 1):  # 只显示前10个
        print(f"  {i}. {token}")


def example_different_tokenizers():
    """使用不同分词器"""
    print("\n" + "="*60)
    print("示例2: 使用不同分词器")
    print("="*60)
    
    source_code = "这是一个中文分词测试"
    
    # 使用jieba分词器
    print("\n使用jieba分词器:")
    lexer_jieba = create_lexer("jieba")
    tokens_jieba = lexer_jieba.tokenize(source_code)
    print(f"  词元数量: {len(tokens_jieba)}")
    
    # 检查THULAC是否可用
    available = YanLuTokenizer.get_available_tokenizers()
    if "thulac" in available:
        print("\n使用THULAC分词器:")
        lexer_thulac = create_lexer("thulac")
        tokens_thulac = lexer_thulac.tokenize(source_code)
        print(f"  词元数量: {len(tokens_thulac)}")
    else:
        print("\nTHULAC分词器不可用（需要安装: pip install thulac）")


def example_error_handling():
    """错误处理示例"""
    print("\n" + "="*60)
    print("示例3: 错误处理")
    print("="*60)
    
    # 创建错误处理器
    handler = ErrorHandler(max_errors=10)
    
    # 添加一些错误
    position1 = Position(line=1, column=5, offset=10)
    handler.add_error(
        code=ErrorCode.LEXER_INVALID_CHAR,
        message="无效字符: '@'",
        position=position1,
        suggestion="请使用有效的标识符字符"
    )
    
    position2 = Position(line=2, column=10, offset=50)
    handler.add_warning(
        code=ErrorCode.LEXER_INVALID_CHAR,
        message="潜在问题: 连续的空格",
        position=position2,
        suggestion="建议使用单个空格"
    )
    
    # 显示错误信息
    print(f"错误数量: {handler.get_error_count()}")
    print(f"警告数量: {handler.get_warning_count()}")
    
    print("\n错误列表:")
    for error in handler.get_all_errors():
        print(f"  {error}")
    
    print("\n警告列表:")
    for warning in handler.get_all_warnings():
        print(f"  {warning}")


def example_performance_optimization():
    """性能优化示例"""
    print("\n" + "="*60)
    print("示例4: 性能优化")
    print("="*60)
    
    # 创建不同优化级别的词法分析器
    source_code = "如果 条件 成立 则 输出 'Hello World'" * 100
    
    # 基础优化
    print("\n基础优化:")
    lexer_basic = create_lexer("jieba", optimization_level="basic")
    tokens_basic = lexer_basic.tokenize(source_code)
    stats_basic = lexer_basic.get_performance_stats()
    print(f"  词元数量: {len(tokens_basic)}")
    print(f"  处理时间: {stats_basic['total_time']:.6f}秒")
    
    # 高级优化
    print("\n高级优化:")
    lexer_advanced = create_lexer("jieba", optimization_level="advanced")
    tokens_advanced = lexer_advanced.tokenize(source_code)
    stats_advanced = lexer_advanced.get_performance_stats()
    print(f"  词元数量: {len(tokens_advanced)}")
    print(f"  处理时间: {stats_advanced['total_time']:.6f}秒")


def example_custom_patterns():
    """自定义模式示例"""
    print("\n" + "="*60)
    print("示例5: 自定义模式")
    print("="*60)
    
    from pattern_manager import PatternManager, PatternType
    
    # 创建模式管理器
    manager = PatternManager()
    
    # 添加自定义模式
    manager.add_pattern(
        name="phone_number",
        pattern=r"^1[3-9]\d{9}$",
        token_type=TokenType.IDENTIFIER,
        pattern_type=PatternType.CUSTOM,
        priority=150,
        description="手机号码",
        examples=["13812345678", "15987654321"]
    )
    
    # 测试匹配
    test_cases = ["13812345678", "123", "变量"]
    print("\n模式匹配测试:")
    for test in test_cases:
        result = manager.match(test)
        if result:
            print(f"  '{test}' -> {result[0]}")
        else:
            print(f"  '{test}' -> 无匹配")


def example_token_matching():
    """词元匹配示例"""
    print("\n" + "="*60)
    print("示例6: 词元匹配")
    print("="*60)
    
    # 创建词元匹配器
    matcher = TokenMatcher()
    
    # 测试不同类型的词元
    test_cases = [
        "123",           # 数字
        "3.14",          # 浮点数
        "变量",          # 标识符
        "如果",          # 关键词
        "。",            # 标点
        "输出",          # 动词
    ]
    
    print("\n词元匹配测试:")
    for test in test_cases:
        token = matcher.match_token(test, 0, 1, 1)
        if token:
            print(f"  '{test}' -> {token.type}")
        else:
            print(f"  '{test}' -> 无法识别")


def example_context_management():
    """上下文管理示例"""
    print("\n" + "="*60)
    print("示例7: 上下文管理")
    print("="*60)
    
    from context_manager import ContextManager, ContextType
    
    # 创建上下文管理器
    manager = ContextManager()
    
    # 进入函数上下文
    pos1 = Position(line=1, column=1, offset=0)
    func_context = manager.push_context(ContextType.FUNCTION, pos1)
    print(f"进入函数上下文: {func_context}")
    print(f"当前深度: {manager.get_context_depth()}")
    
    # 添加符号
    manager.add_symbol("参数1", 10, "parameter")
    manager.add_symbol("局部变量", 20, "variable")
    print(f"符号表: {manager.get_symbol_table()}")
    
    # 进入循环上下文
    pos2 = Position(line=5, column=1, offset=100)
    loop_context = manager.push_context(ContextType.LOOP, pos2)
    print(f"\n进入循环上下文: {loop_context}")
    print(f"当前深度: {manager.get_context_depth()}")
    
    # 退出循环上下文
    pos3 = Position(line=10, column=1, offset=200)
    manager.pop_context(pos3)
    print(f"\n退出循环上下文")
    print(f"当前深度: {manager.get_context_depth()}")
    
    # 退出函数上下文
    pos4 = Position(line=15, column=1, offset=300)
    manager.pop_context(pos4)
    print(f"\n退出函数上下文")
    print(f"当前深度: {manager.get_context_depth()}")


def example_convenience_functions():
    """便捷函数示例"""
    print("\n" + "="*60)
    print("示例8: 便捷函数")
    print("="*60)
    
    # 使用tokenize函数
    source_code = "如果 条件 成立 则 输出 'Hello World'"
    tokens = tokenize(source_code)
    print(f"tokenize函数: 处理了 {len(tokens)} 个词元")
    
    # 使用tokenize_with_stats函数
    tokens, stats = tokenize_with_stats(source_code)
    print(f"\ntokenize_with_stats函数:")
    print(f"  词元数量: {len(tokens)}")
    print(f"  处理时间: {stats['total_time']:.6f}秒")
    print(f"  词元统计: {stats['tokens_processed']}")


def example_performance_monitoring():
    """性能监控示例"""
    print("\n" + "="*60)
    print("示例9: 性能监控")
    print("="*60)
    
    # 创建词法分析器
    lexer = create_lexer("jieba", verbose=False)
    
    # 分析大量代码
    source_code = "\n".join([
        "如果 条件1 成立 则 输出 '结果1'",
        "否则如果 条件2 成立 则 输出 '结果2'",
        "否则 输出 '结果3'",
    ] * 100)
    
    tokens = lexer.tokenize(source_code)
    
    # 获取性能统计
    stats = lexer.get_performance_stats()
    
    print(f"性能统计:")
    print(f"  总词元数: {stats['tokens_processed']}")
    print(f"  总行数: {stats['lines_processed']}")
    print(f"  处理时间: {stats['total_time']:.6f}秒")
    print(f"  错误数: {stats['errors']}")
    print(f"  警告数: {stats['warnings']}")
    
    # 缓存统计
    if 'tokenization_hit_rate' in stats:
        print(f"  缓存命中率: {stats['tokenization_hit_rate']:.2%}")


def example_batch_processing():
    """批量处理示例"""
    print("\n" + "="*60)
    print("示例10: 批量处理")
    print("="*60)
    
    # 创建词法分析器
    lexer = create_lexer("jieba")
    
    # 批量处理多个文件
    source_codes = [
        "如果 条件 成立 则 输出 '结果'",
        "对于 每个 元素 在 列表 中 执行 操作",
        "定义 函数 参数 返回 结果",
    ]
    
    print(f"批量处理 {len(source_codes)} 个代码片段:")
    for i, source_code in enumerate(source_codes, 1):
        tokens = lexer.tokenize(source_code)
        print(f"  {i}. '{source_code[:30]}...' -> {len(tokens)} 个词元")


def main():
    """主函数"""
    print("="*60)
    print("言律语言词法分析器 - 使用示例")
    print("="*60)
    
    # 运行所有示例
    example_basic_usage()
    example_different_tokenizers()
    example_error_handling()
    example_performance_optimization()
    example_custom_patterns()
    example_token_matching()
    example_context_management()
    example_convenience_functions()
    example_performance_monitoring()
    example_batch_processing()
    
    print("\n" + "="*60)
    print("所有示例运行完成！")
    print("="*60)


if __name__ == "__main__":
    main()