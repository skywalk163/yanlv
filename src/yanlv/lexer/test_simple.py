"""
简单测试模块化词法分析器
"""
import sys
import os

# 添加src目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

def main():
    print("=" * 60)
    print("模块化词法分析器测试")
    print("=" * 60)
    
    # 测试导入
    print("\n[1] 测试导入...")
    try:
        from yanlv.lexer import Lexer, Token, TokenType
        print("[OK] 导入成功")
    except Exception as e:
        print(f"[FAIL] 导入失败: {e}")
        return 1
    
    # 测试实例化
    print("\n[2] 测试实例化...")
    try:
        lexer = Lexer()
        print("[OK] 实例化成功")
    except Exception as e:
        print(f"[FAIL] 实例化失败: {e}")
        return 1
    
    # 测试基本词法分析
    print("\n[3] 测试基本词法分析...")
    try:
        code = "定义 变量 x 为 整数"
        tokens = lexer.tokenize(code)
        print(f"[OK] 生成了 {len(tokens)} 个词元")
        for i, token in enumerate(tokens):
            print(f"  {i}: {token}")
    except Exception as e:
        print(f"[FAIL] 词法分析失败: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    # 测试多行代码
    print("\n[4] 测试多行代码...")
    try:
        code = '''
定义 变量 x 为 整数
赋值 x 为 10
输出 x
'''
        tokens = lexer.tokenize(code)
        print(f"[OK] 生成了 {len(tokens)} 个词元")
    except Exception as e:
        print(f"[FAIL] 多行代码分析失败: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    # 测试便捷函数
    print("\n[5] 测试便捷函数...")
    try:
        from yanlv.lexer import tokenize, tokenize_with_stats, create_lexer
        
        tokens = tokenize("定义 x 为 整数")
        print(f"[OK] tokenize() 生成了 {len(tokens)} 个词元")
        
        tokens, stats = tokenize_with_stats("定义 x 为 整数")
        print(f"[OK] tokenize_with_stats() 生成了 {len(tokens)} 个词元")
        
        lexer2 = create_lexer()
        print("[OK] create_lexer() 创建成功")
    except Exception as e:
        print(f"[FAIL] 便捷函数测试失败: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    # 测试其他模块
    print("\n[6] 测试其他模块...")
    try:
        from yanlv.lexer import (
            YanLuTokenizer, JiebaTokenizer,
            ErrorHandler, create_error_handler,
            ContextManager, create_context_manager,
            PatternManager, create_pattern_manager,
            PerformanceOptimizer, OptimizationConfig, OptimizationLevel
        )
        
        # 测试分词器
        tokenizer = JiebaTokenizer()
        segments = tokenizer.segment("这是一个测试")
        print(f"[OK] 分词器测试成功: {segments}")
        
        # 测试错误处理器
        error_handler = create_error_handler()
        print("[OK] 错误处理器创建成功")
        
        # 测试上下文管理器
        context_manager = create_context_manager()
        print("[OK] 上下文管理器创建成功")
        
        # 测试模式管理器
        pattern_manager = create_pattern_manager()
        print("[OK] 模式管理器创建成功")
        
        # 测试性能优化器
        config = OptimizationConfig(level=OptimizationLevel.BASIC)
        optimizer = PerformanceOptimizer(config)
        print("[OK] 性能优化器创建成功")
        
    except Exception as e:
        print(f"[FAIL] 其他模块测试失败: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    print("\n" + "=" * 60)
    print("所有测试通过！")
    print("=" * 60)
    return 0


if __name__ == '__main__':
    sys.exit(main())
