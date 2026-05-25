"""
言律语言扩展数学函数集成测试
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from yanlv.lexer import create_lexer
from yanlv.interpreter import create_interpreter


def test_trigonometric_functions():
    """测试三角函数"""
    print("\n=== 测试三角函数 ===")
    
    lexer = create_lexer("yanlv_nospace")
    interpreter = create_interpreter()
    
    # 测试正弦
    code1 = '''
定义变量角度为1.5708
正弦 角度
'''
    tokens1 = lexer.tokenize(code1)
    output1 = interpreter.execute(tokens1)
    print(f"测试1 - 正弦(π/2): {output1}")
    assert "1.0" in output1[0] or "0.999" in output1[0]
    
    # 测试余弦
    code2 = '''
余弦 0
'''
    tokens2 = lexer.tokenize(code2)
    output2 = interpreter.execute(tokens2)
    print(f"测试2 - 余弦(0): {output2}")
    assert "1.0" in output2[0]
    
    # 测试正切
    code3 = '''
正切 0.785398
'''
    tokens3 = lexer.tokenize(code3)
    output3 = interpreter.execute(tokens3)
    print(f"测试3 - 正切(π/4): {output3}")
    assert "0.999" in output3[0] or "1.0" in output3[0]
    
    print("[PASS] 三角函数测试通过")


def test_logarithmic_functions():
    """测试对数函数"""
    print("\n=== 测试对数函数 ===")
    
    lexer = create_lexer("yanlv_nospace")
    interpreter = create_interpreter()
    
    # 测试自然对数
    code1 = '''
定义变量数值为2.71828
自然对数 数值
'''
    tokens1 = lexer.tokenize(code1)
    output1 = interpreter.execute(tokens1)
    print(f"测试1 - 自然对数(e): {output1}")
    assert "1.0" in output1[0] or "0.999" in output1[0]
    
    # 测试常用对数
    code2 = '''
常用对数 100
'''
    tokens2 = lexer.tokenize(code2)
    output2 = interpreter.execute(tokens2)
    print(f"测试2 - 常用对数(100): {output2}")
    assert "2.0" in output2[0]
    
    # 测试指数
    code3 = '''
指数 1
'''
    tokens3 = lexer.tokenize(code3)
    output3 = interpreter.execute(tokens3)
    print(f"测试3 - 指数(1): {output3}")
    assert "2.718" in output3[0]
    
    print("[PASS] 对数函数测试通过")


def test_rounding_functions():
    """测试取整函数"""
    print("\n=== 测试取整函数 ===")
    
    lexer = create_lexer("yanlv_nospace")
    interpreter = create_interpreter()
    
    # 测试向上取整
    code1 = '''
向上取整 3.2
'''
    tokens1 = lexer.tokenize(code1)
    output1 = interpreter.execute(tokens1)
    print(f"测试1 - 向上取整(3.2): {output1}")
    assert "4" in output1[0]
    
    # 测试向下取整
    code2 = '''
向下取整 3.8
'''
    tokens2 = lexer.tokenize(code2)
    output2 = interpreter.execute(tokens2)
    print(f"测试2 - 向下取整(3.8): {output2}")
    assert "3" in output2[0]
    
    # 测试四舍五入
    code3 = '''
四舍五入 3.5
'''
    tokens3 = lexer.tokenize(code3)
    output3 = interpreter.execute(tokens3)
    print(f"测试3 - 四舍五入(3.5): {output3}")
    assert "4" in output3[0]
    
    print("[PASS] 取整函数测试通过")


def test_factorial():
    """测试阶乘函数"""
    print("\n=== 测试阶乘函数 ===")
    
    lexer = create_lexer("yanlv_nospace")
    interpreter = create_interpreter()
    
    # 测试阶乘
    code1 = '''
阶乘 5
'''
    tokens1 = lexer.tokenize(code1)
    output1 = interpreter.execute(tokens1)
    print(f"测试1 - 阶乘(5): {output1}")
    assert "120" in output1[0]
    
    # 测试0的阶乘
    code2 = '''
阶乘 0
'''
    tokens2 = lexer.tokenize(code2)
    output2 = interpreter.execute(tokens2)
    print(f"测试2 - 阶乘(0): {output2}")
    assert "1" in output2[0]
    
    print("[PASS] 阶乘函数测试通过")


def run_all_tests():
    """运行所有测试"""
    print("\n" + "="*50)
    print("言律语言扩展数学函数集成测试")
    print("="*50)
    
    try:
        test_trigonometric_functions()
        test_logarithmic_functions()
        test_rounding_functions()
        test_factorial()
        
        print("\n" + "="*50)
        print("[PASS] 所有集成测试通过！")
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
