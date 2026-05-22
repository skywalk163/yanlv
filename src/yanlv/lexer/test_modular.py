#!/usr/bin/env python3
"""
测试模块化词法分析器
"""

import sys
import os

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    # 测试导入
    from lexer_modular import ModularYanLuLexer, create_lexer, tokenize
    from lexer_token import Token, TokenType
    from tokenizer import YanLuTokenizer
    from matcher import TokenMatcher
    from error_handler import ErrorHandler
    from context_manager import ContextManager
    from pattern_manager import PatternManager
    from performance_optimizer import PerformanceOptimizer
    from utils import PerformanceMonitor, Logger, Position
    
    print("✅ 所有模块导入成功！")
    
    # 测试创建词法分析器
    lexer = create_lexer("jieba", verbose=True)
    print(f"✅ 创建词法分析器: {lexer}")
    
    # 测试配置
    config = lexer.get_config()
    print(f"✅ 获取配置: {config}")
    
    # 测试分词器
    tokenizer = YanLuTokenizer.create("jieba")
    segments = tokenizer.segment("这是一个测试")
    print(f"✅ 分词测试: {segments}")
    
    # 测试词元匹配器
    matcher = TokenMatcher()
    token = matcher.match_token("测试", 0, 1, 1)
    print(f"✅ 词元匹配测试: {token}")
    
    # 测试错误处理器
    error_handler = ErrorHandler()
    error_handler.add_error("TEST001", "测试错误", Position(line=1, column=1, offset=0))
    print(f"✅ 错误处理器测试: {error_handler.get_error_count()} 个错误")
    
    # 测试上下文管理器
    context_manager = ContextManager()
    context = context_manager.push_context("function", Position(line=1, column=1, offset=0))
    print(f"✅ 上下文管理器测试: {context}")
    
    # 测试模式管理器
    pattern_manager = PatternManager()
    pattern_count = pattern_manager.get_pattern_count()
    print(f"✅ 模式管理器测试: {pattern_count} 个模式")
    
    # 测试性能优化器
    optimizer = PerformanceOptimizer()
    stats = optimizer.get_performance_stats()
    print(f"✅ 性能优化器测试: {stats}")
    
    # 测试工具模块
    monitor = PerformanceMonitor()
    monitor.start()
    monitor.stop()
    print(f"✅ 性能监控器测试: {monitor.get_stats()}")
    
    logger = Logger("test")
    logger.info("测试日志")
    print("✅ 日志测试完成")
    
    # 测试词法分析
    source_code = "如果 条件 成立 则 输出 'Hello World'"
    tokens = tokenize(source_code)
    print(f"✅ 词法分析测试: {len(tokens)} 个词元")
    for i, token in enumerate(tokens[:5]):  # 只显示前5个
        print(f"  {i+1}. {token}")
    
    print("\n🎉 所有测试通过！模块化重构成功！")
    
except ImportError as e:
    print(f"❌ 导入失败: {e}")
    import traceback
    traceback.print_exc()
except Exception as e:
    print(f"❌ 测试失败: {e}")
    import traceback
    traceback.print_exc()