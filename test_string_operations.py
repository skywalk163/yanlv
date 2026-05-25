"""
言律语言字符串操作增强功能测试
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from yanlv.lexer import create_lexer
from yanlv.interpreter import create_interpreter


def test_string_concat():
    """测试字符串连接功能"""
    print("\n=== 测试字符串连接 ===")
    
    lexer = create_lexer("yanlv_nospace")
    interpreter = create_interpreter()
    
    # 测试1：基本字符串连接
    code1 = '''
定义变量问候为"你好"
定义变量世界为"世界"
连接 问候 世界
'''
    tokens1 = lexer.tokenize(code1)
    output1 = interpreter.execute(tokens1)
    print(f"测试1 - 基本连接: {output1}")
    assert "你好世界" in output1[0]
    
    # 测试2：字符串与数字连接
    code2 = '''
定义变量数字为123
连接 "数字：" 数字
'''
    tokens2 = lexer.tokenize(code2)
    output2 = interpreter.execute(tokens2)
    print(f"测试2 - 字符串与数字: {output2}")
    assert "数字：123" in output2[0]
    
    # 测试3：多元素连接并赋值
    code3 = '''
定义变量问候为"你好"
定义变量世界为"世界"
连接 问候 " " 世界 为 结果
输出 结果
'''
    tokens3 = lexer.tokenize(code3)
    output3 = interpreter.execute(tokens3)
    print(f"测试3 - 多元素连接并赋值: {output3}")
    assert "你好 世界" in output3[0]
    
    print("[PASS] 字符串连接测试通过")


def test_string_slice():
    """测试字符串切片功能"""
    print("\n=== 测试字符串切片 ===")
    
    lexer = create_lexer("yanlv_nospace")
    interpreter = create_interpreter()
    
    # 测试1：基本切片
    code1 = '''
定义变量文本为"你好世界"
切片 文本 0 2
'''
    tokens1 = lexer.tokenize(code1)
    output1 = interpreter.execute(tokens1)
    print(f"测试1 - 基本切片: {output1}")
    assert "你好" in output1[0]
    
    # 测试2：负索引
    code2 = '''
定义变量文本为"你好世界"
切片 文本 -2
'''
    tokens2 = lexer.tokenize(code2)
    output2 = interpreter.execute(tokens2)
    print(f"测试2 - 负索引: {output2}")
    assert "世界" in output2[0]
    
    # 测试3：带步长
    code3 = '''
定义变量文本为"你好世界"
切片 文本 0 4 2
'''
    tokens3 = lexer.tokenize(code3)
    output3 = interpreter.execute(tokens3)
    print(f"测试3 - 带步长: {output3}")
    assert "你世" in output3[0]
    
    print("[PASS] 字符串切片测试通过")


def test_find_all():
    """测试查找全部功能"""
    print("\n=== 测试查找全部 ===")
    
    lexer = create_lexer("yanlv_nospace")
    interpreter = create_interpreter()
    
    # 测试1：查找多个位置
    code1 = '''
定义变量文本为"你好世界你好"
查找全部 文本 "你好"
'''
    tokens1 = lexer.tokenize(code1)
    output1 = interpreter.execute(tokens1)
    print(f"测试1 - 查找多个位置: {output1}")
    assert "[0, 4]" in output1[0]
    
    # 测试2：未找到
    code2 = '''
定义变量文本为"你好世界"
查找全部 文本 "不存在"
'''
    tokens2 = lexer.tokenize(code2)
    output2 = interpreter.execute(tokens2)
    print(f"测试2 - 未找到: {output2}")
    assert "[]" in output2[0]
    
    print("[PASS] 查找全部测试通过")


def test_replace_once():
    """测试单次替换功能"""
    print("\n=== 测试单次替换 ===")
    
    lexer = create_lexer("yanlv_nospace")
    interpreter = create_interpreter()
    
    # 测试：单次替换
    code = '''
定义变量文本为"你好世界你好"
替换一次 文本 "你好" "您好"
'''
    tokens = lexer.tokenize(code)
    output = interpreter.execute(tokens)
    print(f"测试 - 单次替换: {output}")
    assert "您好世界你好" in output[0]
    
    print("[PASS] 单次替换测试通过")


def test_upper_lower():
    """测试大小写转换功能"""
    print("\n=== 测试大小写转换 ===")
    
    lexer = create_lexer("yanlv_nospace")
    interpreter = create_interpreter()
    
    # 测试1：大写转换
    code1 = '''
定义变量文本为"Hello世界"
大写 文本
'''
    tokens1 = lexer.tokenize(code1)
    output1 = interpreter.execute(tokens1)
    print(f"测试1 - 大写转换: {output1}")
    assert "HELLO世界" in output1[0]
    
    # 测试2：小写转换
    code2 = '''
定义变量文本为"HELLO世界"
小写 文本
'''
    tokens2 = lexer.tokenize(code2)
    output2 = interpreter.execute(tokens2)
    print(f"测试2 - 小写转换: {output2}")
    assert "hello世界" in output2[0]
    
    print("[PASS] 大小写转换测试通过")


def test_trim():
    """测试去空格功能"""
    print("\n=== 测试去空格 ===")
    
    lexer = create_lexer("yanlv_nospace")
    interpreter = create_interpreter()
    
    # 测试1：去除首尾空格
    code1 = '''
定义变量文本为"  你好 世界  "
去空格 文本
'''
    tokens1 = lexer.tokenize(code1)
    output1 = interpreter.execute(tokens1)
    print(f"测试1 - 去除首尾空格: {output1}")
    assert "你好 世界" in output1[0]
    
    # 测试2：去除所有空格
    code2 = '''
定义变量文本为"  你好 世界  "
去全部空格 文本
'''
    tokens2 = lexer.tokenize(code2)
    output2 = interpreter.execute(tokens2)
    print(f"测试2 - 去除所有空格: {output2}")
    assert "你好世界" in output2[0]
    
    print("[PASS] 去空格测试通过")


def test_for_each_char():
    """测试字符遍历功能"""
    print("\n=== 测试字符遍历 ===")
    
    lexer = create_lexer("yanlv_nospace")
    interpreter = create_interpreter()
    
    # 测试：遍历字符
    code = '''
定义变量文本为"你好"
遍历字符 文本 字符
    输出 字符
结束
'''
    tokens = lexer.tokenize(code)
    output = interpreter.execute(tokens)
    print(f"测试 - 字符遍历: {output}")
    assert len(output) == 2
    assert "你" in output[0]
    assert "好" in output[1]
    
    print("[PASS] 字符遍历测试通过")


def run_all_tests():
    """运行所有测试"""
    print("\n" + "="*50)
    print("言律语言字符串操作增强功能测试")
    print("="*50)
    
    try:
        test_string_concat()
        test_string_slice()
        test_find_all()
        test_replace_once()
        test_upper_lower()
        test_trim()
        test_for_each_char()
        
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
