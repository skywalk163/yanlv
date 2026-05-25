"""
言律语言内置数学函数测试
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from yanlv.lexer import create_lexer
from yanlv.interpreter import create_interpreter


def test_abs():
    """测试绝对值函数"""
    print("\n=== 测试绝对值函数 ===")
    
    lexer = create_lexer("yanlv_nospace")
    interpreter = create_interpreter()
    
    # 测试1：正数绝对值
    code1 = '''
定义变量数字为10
绝对值 数字
'''
    tokens1 = lexer.tokenize(code1)
    output1 = interpreter.execute(tokens1)
    print(f"测试1 - 正数绝对值: {output1}")
    assert "10" in output1[0]
    
    # 测试2：负数绝对值
    code2 = '''
定义变量数字为-5
绝对值 数字
'''
    tokens2 = lexer.tokenize(code2)
    output2 = interpreter.execute(tokens2)
    print(f"测试2 - 负数绝对值: {output2}")
    assert "5" in output2[0]
    
    # 测试3：直接使用数字
    code3 = '''
绝对值 -8
'''
    tokens3 = lexer.tokenize(code3)
    output3 = interpreter.execute(tokens3)
    print(f"测试3 - 直接使用数字: {output3}")
    assert "8" in output3[0]
    
    print("[PASS] 绝对值函数测试通过")


def test_sqrt():
    """测试平方根函数"""
    print("\n=== 测试平方根函数 ===")
    
    lexer = create_lexer("yanlv_nospace")
    interpreter = create_interpreter()
    
    # 测试1：整数平方根
    code1 = '''
定义变量数字为16
平方根 数字
'''
    tokens1 = lexer.tokenize(code1)
    output1 = interpreter.execute(tokens1)
    print(f"测试1 - 整数平方根: {output1}")
    assert "4" in output1[0]
    
    # 测试2：浮点数平方根
    code2 = '''
平方根 2
'''
    tokens2 = lexer.tokenize(code2)
    output2 = interpreter.execute(tokens2)
    print(f"测试2 - 浮点数平方根: {output2}")
    assert "1.414" in output2[0]
    
    print("[PASS] 平方根函数测试通过")


def test_pow():
    """测试幂函数"""
    print("\n=== 测试幂函数 ===")
    
    lexer = create_lexer("yanlv_nospace")
    interpreter = create_interpreter()
    
    # 测试1：整数幂
    code1 = '''
定义变量底数为2
定义变量指数为3
幂 底数 指数
'''
    tokens1 = lexer.tokenize(code1)
    output1 = interpreter.execute(tokens1)
    print(f"测试1 - 整数幂: {output1}")
    assert "8" in output1[0]
    
    # 测试2：直接使用数字
    code2 = '''
幂 3 2
'''
    tokens2 = lexer.tokenize(code2)
    output2 = interpreter.execute(tokens2)
    print(f"测试2 - 直接使用数字: {output2}")
    assert "9" in output2[0]
    
    print("[PASS] 幂函数测试通过")


def test_int():
    """测试取整函数"""
    print("\n=== 测试取整函数 ===")
    
    lexer = create_lexer("yanlv_nospace")
    interpreter = create_interpreter()
    
    # 测试1：浮点数取整
    code1 = '''
定义变量数字为3.7
取整 数字
'''
    tokens1 = lexer.tokenize(code1)
    output1 = interpreter.execute(tokens1)
    print(f"测试1 - 浮点数取整: {output1}")
    assert "3" in output1[0]
    
    # 测试2：负数取整
    code2 = '''
取整 -2.8
'''
    tokens2 = lexer.tokenize(code2)
    output2 = interpreter.execute(tokens2)
    print(f"测试2 - 负数取整: {output2}")
    assert "-2" in output2[0]
    
    print("[PASS] 取整函数测试通过")


def test_random():
    """测试随机数函数"""
    print("\n=== 测试随机数函数 ===")
    
    lexer = create_lexer("yanlv_nospace")
    interpreter = create_interpreter()
    
    # 测试：生成随机数
    code = '''
随机数
'''
    tokens = lexer.tokenize(code)
    output = interpreter.execute(tokens)
    print(f"测试 - 生成随机数: {output}")
    # 验证输出是一个数字
    assert "=>" in output[0]
    
    print("[PASS] 随机数函数测试通过")


def run_all_tests():
    """运行所有测试"""
    print("\n" + "="*50)
    print("言律语言内置数学函数测试")
    print("="*50)
    
    try:
        test_abs()
        test_sqrt()
        test_pow()
        test_int()
        test_random()
        
        print("\n" + "="*50)
        print("[PASS] 所有数学函数测试通过！")
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
