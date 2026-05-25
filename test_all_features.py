"""
言律语言功能测试 - 简化版
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from yanlv.lexer import create_lexer
from yanlv.interpreter import create_interpreter


def test_basic_operations():
    """测试基本操作"""
    print("\n=== 测试基本操作 ===")
    
    lexer = create_lexer("yanlv_nospace")
    interpreter = create_interpreter()
    
    # 测试变量定义
    code = '''
定义变量x为 10
输出 x
'''
    tokens = lexer.tokenize(code)
    output = interpreter.execute(tokens)
    print(f"测试 - 变量定义: {output}")
    assert "10" in output[0]
    
    print("[PASS] 基本操作测试通过")


def test_math_functions():
    """测试数学函数"""
    print("\n=== 测试数学函数 ===")
    
    lexer = create_lexer("yanlv_nospace")
    interpreter = create_interpreter()
    
    # 测试绝对值
    code = '''
定义变量x为 -5
绝对值 x
'''
    tokens = lexer.tokenize(code)
    output = interpreter.execute(tokens)
    print(f"测试 - 绝对值: {output}")
    assert "5" in output[0]
    
    print("[PASS] 数学函数测试通过")


def test_file_operations():
    """测试文件操作"""
    print("\n=== 测试文件操作 ===")
    
    lexer = create_lexer("yanlv_nospace")
    interpreter = create_interpreter()
    
    # 测试文件存在检查
    code = '''
文件存在 "test.txt"
'''
    tokens = lexer.tokenize(code)
    output = interpreter.execute(tokens)
    print(f"测试 - 文件存在: {output}")
    assert "真" in output[0] or "假" in output[0]
    
    print("[PASS] 文件操作测试通过")


def test_exception_handling():
    """测试异常处理"""
    print("\n=== 测试异常处理 ===")
    
    lexer = create_lexer("yanlv_nospace")
    interpreter = create_interpreter()
    
    # 测试抛出异常
    code = '''
抛出 "测试异常"
'''
    tokens = lexer.tokenize(code)
    output = interpreter.execute(tokens)
    print(f"测试 - 抛出异常: {output}")
    assert "异常" in output[0]
    
    print("[PASS] 异常处理测试通过")


def run_all_tests():
    """运行所有测试"""
    print("\n" + "="*50)
    print("言律语言功能测试")
    print("="*50)
    
    try:
        test_basic_operations()
        test_math_functions()
        test_file_operations()
        test_exception_handling()
        
        print("\n" + "="*50)
        print("[PASS] 所有测试通过！")
        print("="*50)
        return True
    except Exception as e:
        print(f"\n[FAIL] 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
