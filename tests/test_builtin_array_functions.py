"""
言律语言内置数组函数测试
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from yanlv.lexer import create_lexer
from yanlv.interpreter import create_interpreter


def test_sort():
    """测试排序函数"""
    print("\n=== 测试排序函数 ===")
    
    lexer = create_lexer("yanlv_nospace")
    interpreter = create_interpreter()
    
    # 测试1：数字数组排序
    code1 = '''
定义变量数组为[3, 1, 4, 1, 5, 9, 2, 6]
排序 数组
'''
    tokens1 = lexer.tokenize(code1)
    output1 = interpreter.execute(tokens1)
    print(f"测试1 - 数字数组排序: {output1}")
    assert "[1.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 9.0]" in output1[0]
    
    # 测试2：已排序数组
    code2 = '''
定义变量有序数组为[1, 2, 3, 4, 5]
排序 有序数组
'''
    tokens2 = lexer.tokenize(code2)
    output2 = interpreter.execute(tokens2)
    print(f"测试2 - 已排序数组: {output2}")
    assert "[1.0, 2.0, 3.0, 4.0, 5.0]" in output2[0]
    
    print("[PASS] 排序函数测试通过")


def test_reverse():
    """测试反转函数"""
    print("\n=== 测试反转函数 ===")
    
    lexer = create_lexer("yanlv_nospace")
    interpreter = create_interpreter()
    
    # 测试1：数字数组反转
    code1 = '''
定义变量数组为[1, 2, 3, 4, 5]
反转 数组
'''
    tokens1 = lexer.tokenize(code1)
    output1 = interpreter.execute(tokens1)
    print(f"测试1 - 数字数组反转: {output1}")
    assert "[5.0, 4.0, 3.0, 2.0, 1.0]" in output1[0]
    
    # 测试2：字符串数组反转
    code2 = '''
定义变量文本数组为["你", "好", "世", "界"]
反转 文本数组
'''
    tokens2 = lexer.tokenize(code2)
    output2 = interpreter.execute(tokens2)
    print(f"测试2 - 字符串数组反转: {output2}")
    assert "界" in output2[0]
    
    print("[PASS] 反转函数测试通过")


def test_max():
    """测试最大值函数"""
    print("\n=== 测试最大值函数 ===")
    
    lexer = create_lexer("yanlv_nospace")
    interpreter = create_interpreter()
    
    # 测试1：数字数组最大值
    code1 = '''
定义变量数组为[3, 1, 4, 1, 5, 9, 2, 6]
最大值 数组
'''
    tokens1 = lexer.tokenize(code1)
    output1 = interpreter.execute(tokens1)
    print(f"测试1 - 数字数组最大值: {output1}")
    assert "9" in output1[0]
    
    # 测试2：负数数组最大值
    code2 = '''
定义变量负数数组为[-5, -2, -8, -1]
最大值 负数数组
'''
    tokens2 = lexer.tokenize(code2)
    output2 = interpreter.execute(tokens2)
    print(f"测试2 - 负数数组最大值: {output2}")
    assert "-1" in output2[0]
    
    print("[PASS] 最大值函数测试通过")


def test_min():
    """测试最小值函数"""
    print("\n=== 测试最小值函数 ===")
    
    lexer = create_lexer("yanlv_nospace")
    interpreter = create_interpreter()
    
    # 测试1：数字数组最小值
    code1 = '''
定义变量数组为[3, 1, 4, 1, 5, 9, 2, 6]
最小值 数组
'''
    tokens1 = lexer.tokenize(code1)
    output1 = interpreter.execute(tokens1)
    print(f"测试1 - 数字数组最小值: {output1}")
    assert "1" in output1[0]
    
    # 测试2：负数数组最小值
    code2 = '''
定义变量负数数组为[-5, -2, -8, -1]
最小值 负数数组
'''
    tokens2 = lexer.tokenize(code2)
    output2 = interpreter.execute(tokens2)
    print(f"测试2 - 负数数组最小值: {output2}")
    assert "-8" in output2[0]
    
    print("[PASS] 最小值函数测试通过")


def test_sum():
    """测试求和函数"""
    print("\n=== 测试求和函数 ===")
    
    lexer = create_lexer("yanlv_nospace")
    interpreter = create_interpreter()
    
    # 测试1：数字数组求和
    code1 = '''
定义变量数组为[1, 2, 3, 4, 5]
求和 数组
'''
    tokens1 = lexer.tokenize(code1)
    output1 = interpreter.execute(tokens1)
    print(f"测试1 - 数字数组求和: {output1}")
    assert "15" in output1[0]
    
    # 测试2：包含负数的数组求和
    code2 = '''
定义变量混合数组为[1, -2, 3, -4, 5]
求和 混合数组
'''
    tokens2 = lexer.tokenize(code2)
    output2 = interpreter.execute(tokens2)
    print(f"测试2 - 包含负数的数组求和: {output2}")
    assert "3" in output2[0]
    
    print("[PASS] 求和函数测试通过")


def run_all_tests():
    """运行所有测试"""
    print("\n" + "="*50)
    print("言律语言内置数组函数测试")
    print("="*50)
    
    try:
        test_sort()
        test_reverse()
        test_max()
        test_min()
        test_sum()
        
        print("\n" + "="*50)
        print("[PASS] 所有数组函数测试通过！")
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
