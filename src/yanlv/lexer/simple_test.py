#!/usr/bin/env python3
"""
简单测试模块化词法分析器
"""

import sys
import os

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("=" * 60)
print("模块化词法分析器测试")
print("=" * 60)

try:
    # 测试导入
    print("\n1. 测试模块导入...")
    from lexer_token import Token, TokenType
    print("   - lexer_token: OK")
    
    from tokenizer import YanLuTokenizer
    print("   - tokenizer: OK")
    
    from matcher import TokenMatcher
    print("   - matcher: OK")
    
    from error_handler import ErrorHandler
    print("   - error_handler: OK")
    
    from context_manager import ContextManager
    print("   - context_manager: OK")
    
    from pattern_manager import PatternManager
    print("   - pattern_manager: OK")
    
    from performance_optimizer import PerformanceOptimizer
    print("   - performance_optimizer: OK")
    
    from utils import PerformanceMonitor, Logger
    print("   - utils: OK")
    
    from lexer_modular import ModularYanLuLexer, create_lexer
    print("   - lexer_modular: OK")
    
    print("\n2. 测试创建词法分析器...")
    lexer = create_lexer("jieba", verbose=False)
    print(f"   - 创建成功: {lexer}")
    
    print("\n3. 测试分词器...")
    tokenizer = YanLuTokenizer.create("jieba")
    segments = tokenizer.segment("这是一个测试")
    print(f"   - 分词结果: {segments}")
    
    print("\n4. 测试词元匹配器...")
    matcher = TokenMatcher()
    token = matcher.match_token("测试", 0, 1, 1)
    print(f"   - 匹配结果: {token}")
    
    print("\n5. 测试错误处理器...")
    from utils import Position
    from error_handler import ErrorCode
    error_handler = ErrorHandler()
    error_handler.add_error(ErrorCode.LEXER_INVALID_CHAR, "测试错误", Position(line=1, column=1, offset=0))
    print(f"   - 错误数量: {error_handler.get_error_count()}")
    
    print("\n6. 测试上下文管理器...")
    from context_manager import ContextType
    context_manager = ContextManager()
    context = context_manager.push_context(ContextType.FUNCTION, Position(line=1, column=1, offset=0))
    print(f"   - 上下文: {context}")
    
    print("\n7. 测试模式管理器...")
    pattern_manager = PatternManager()
    pattern_count = pattern_manager.get_pattern_count()
    print(f"   - 模式数量: {pattern_count}")
    
    print("\n8. 测试性能优化器...")
    optimizer = PerformanceOptimizer()
    stats = optimizer.get_performance_stats()
    print(f"   - 性能统计: {stats}")
    
    print("\n" + "=" * 60)
    print("所有测试通过！模块化重构成功！")
    print("=" * 60)
    
    # 输出模块统计
    print("\n模块统计:")
    print(f"  - 词元类型: {len(TokenType)}")
    print(f"  - 分词器类型: {len(YanLuTokenizer.get_available_tokenizers())}")
    print(f"  - 模式数量: {pattern_count}")
    print(f"  - 错误数量: {error_handler.get_error_count()}")
    
except Exception as e:
    print(f"\n测试失败: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)