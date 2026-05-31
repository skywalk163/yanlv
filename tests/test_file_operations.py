"""
言律语言文件操作功能测试
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from yanlv.lexer import create_lexer
from yanlv.interpreter import create_interpreter


def test_file_write_read():
    """测试文件写入和读取"""
    print("\n=== 测试文件写入和读取 ===")
    
    lexer = create_lexer("yanlv_nospace")
    interpreter = create_interpreter()
    
    # 测试写入文件
    code1 = '''
写入文件 "test_file.txt" "你好，世界！"
'''
    tokens1 = lexer.tokenize(code1)
    output1 = interpreter.execute(tokens1)
    print(f"测试1 - 写入文件: {output1}")
    assert "文件已写入" in output1[0]
    
    # 测试读取文件
    code2 = '''
读取文件 "test_file.txt" 为 内容
输出 内容
'''
    tokens2 = lexer.tokenize(code2)
    output2 = interpreter.execute(tokens2)
    print(f"测试2 - 读取文件: {output2}")
    # 检查文件内容被输出
    assert len(output2) > 0
    
    # 清理测试文件
    if os.path.exists("test_file.txt"):
        os.remove("test_file.txt")
    
    print("[PASS] 文件写入和读取测试通过")


def test_file_exists():
    """测试文件存在检查"""
    print("\n=== 测试文件存在检查 ===")
    
    lexer = create_lexer("yanlv_nospace")
    interpreter = create_interpreter()
    
    # 创建测试文件
    with open("test_exists.txt", "w", encoding="utf-8") as f:
        f.write("test")
    
    # 测试文件存在
    code1 = '''
文件存在 "test_exists.txt"
'''
    tokens1 = lexer.tokenize(code1)
    output1 = interpreter.execute(tokens1)
    print(f"测试1 - 文件存在: {output1}")
    assert "真" in output1[0]
    
    # 测试文件不存在
    code2 = '''
文件存在 "not_exists.txt"
'''
    tokens2 = lexer.tokenize(code2)
    output2 = interpreter.execute(tokens2)
    print(f"测试2 - 文件不存在: {output2}")
    assert "假" in output2[0]
    
    # 清理测试文件
    if os.path.exists("test_exists.txt"):
        os.remove("test_exists.txt")
    
    print("[PASS] 文件存在检查测试通过")


def test_file_size():
    """测试文件大小"""
    print("\n=== 测试文件大小 ===")
    
    lexer = create_lexer("yanlv_nospace")
    interpreter = create_interpreter()
    
    # 创建测试文件
    with open("test_size.txt", "w", encoding="utf-8") as f:
        f.write("12345")
    
    # 测试文件大小
    code = '''
文件大小 "test_size.txt"
'''
    tokens = lexer.tokenize(code)
    output = interpreter.execute(tokens)
    print(f"测试 - 文件大小: {output}")
    assert "5" in output[0]
    
    # 清理测试文件
    if os.path.exists("test_size.txt"):
        os.remove("test_size.txt")
    
    print("[PASS] 文件大小测试通过")


def test_path_operations():
    """测试路径操作"""
    print("\n=== 测试路径操作 ===")
    
    lexer = create_lexer("yanlv_nospace")
    interpreter = create_interpreter()
    
    # 测试获取文件名
    code1 = '''
文件名 "C:/Users/test/data.txt"
'''
    tokens1 = lexer.tokenize(code1)
    output1 = interpreter.execute(tokens1)
    print(f"测试1 - 文件名: {output1}")
    assert "data.txt" in output1[0]
    
    # 测试获取目录名
    code2 = '''
目录名 "C:/Users/test/data.txt"
'''
    tokens2 = lexer.tokenize(code2)
    output2 = interpreter.execute(tokens2)
    print(f"测试2 - 目录名: {output2}")
    assert "C:/Users/test" in output2[0] or "C:\\Users\\test" in output2[0]
    
    print("[PASS] 路径操作测试通过")


def run_all_tests():
    """运行所有测试"""
    print("\n" + "="*50)
    print("言律语言文件操作功能测试")
    print("="*50)
    
    try:
        test_file_write_read()
        test_file_exists()
        test_file_size()
        test_path_operations()
        
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
