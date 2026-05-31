"""
言律语言扩展数学函数测试

测试新增的10个数学函数：
- 三角函数：sin, cos, tan
- 对数函数：log, log10, exp
- 取整函数：ceil, floor, round
- 阶乘：factorial
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from yanlv.lexer.lexer_token import TokenType
from yanlv.lexer.constants import KEYWORDS


def test_token_types():
    """测试新增的TokenType是否正确定义"""
    print("\n=== 测试TokenType定义 ===")
    
    # 检查三角函数
    assert hasattr(TokenType, 'SIN'), "SIN TokenType未定义"
    assert hasattr(TokenType, 'COS'), "COS TokenType未定义"
    assert hasattr(TokenType, 'TAN'), "TAN TokenType未定义"
    
    # 检查对数函数
    assert hasattr(TokenType, 'LOG'), "LOG TokenType未定义"
    assert hasattr(TokenType, 'LOG10'), "LOG10 TokenType未定义"
    assert hasattr(TokenType, 'EXP'), "EXP TokenType未定义"
    
    # 检查取整函数
    assert hasattr(TokenType, 'CEIL'), "CEIL TokenType未定义"
    assert hasattr(TokenType, 'FLOOR'), "FLOOR TokenType未定义"
    assert hasattr(TokenType, 'ROUND'), "ROUND TokenType未定义"
    
    # 检查阶乘
    assert hasattr(TokenType, 'FACTORIAL'), "FACTORIAL TokenType未定义"
    
    print("[PASS] 所有TokenType定义正确")


def test_keywords():
    """测试新增的中文关键词映射"""
    print("\n=== 测试关键词映射 ===")
    
    # 检查三角函数关键词
    assert '正弦' in KEYWORDS, "正弦 关键词未映射"
    assert KEYWORDS['正弦'] == TokenType.SIN, "正弦 映射错误"
    
    assert '余弦' in KEYWORDS, "余弦 关键词未映射"
    assert KEYWORDS['余弦'] == TokenType.COS, "余弦 映射错误"
    
    assert '正切' in KEYWORDS, "正切 关键词未映射"
    assert KEYWORDS['正切'] == TokenType.TAN, "正切 映射错误"
    
    # 检查对数函数关键词
    assert '自然对数' in KEYWORDS, "自然对数 关键词未映射"
    assert KEYWORDS['自然对数'] == TokenType.LOG, "自然对数 映射错误"
    
    assert '常用对数' in KEYWORDS, "常用对数 关键词未映射"
    assert KEYWORDS['常用对数'] == TokenType.LOG10, "常用对数 映射错误"
    
    assert '指数' in KEYWORDS, "指数 关键词未映射"
    assert KEYWORDS['指数'] == TokenType.EXP, "指数 映射错误"
    
    # 检查取整函数关键词
    assert '向上取整' in KEYWORDS, "向上取整 关键词未映射"
    assert KEYWORDS['向上取整'] == TokenType.CEIL, "向上取整 映射错误"
    
    assert '向下取整' in KEYWORDS, "向下取整 关键词未映射"
    assert KEYWORDS['向下取整'] == TokenType.FLOOR, "向下取整 映射错误"
    
    assert '四舍五入' in KEYWORDS, "四舍五入 关键词未映射"
    assert KEYWORDS['四舍五入'] == TokenType.ROUND, "四舍五入 映射错误"
    
    # 检查阶乘关键词
    assert '阶乘' in KEYWORDS, "阶乘 关键词未映射"
    assert KEYWORDS['阶乘'] == TokenType.FACTORIAL, "阶乘 映射错误"
    
    print("[PASS] 所有关键词映射正确")


def test_token_values():
    """测试TokenType的值"""
    print("\n=== 测试TokenType值 ===")
    
    assert TokenType.SIN.value == "SIN"
    assert TokenType.COS.value == "COS"
    assert TokenType.TAN.value == "TAN"
    assert TokenType.LOG.value == "LOG"
    assert TokenType.LOG10.value == "LOG10"
    assert TokenType.EXP.value == "EXP"
    assert TokenType.CEIL.value == "CEIL"
    assert TokenType.FLOOR.value == "FLOOR"
    assert TokenType.ROUND.value == "ROUND"
    assert TokenType.FACTORIAL.value == "FACTORIAL"
    
    print("[PASS] 所有TokenType值正确")


def run_all_tests():
    """运行所有测试"""
    print("\n" + "="*50)
    print("言律语言扩展数学函数测试")
    print("="*50)
    
    try:
        test_token_types()
        test_keywords()
        test_token_values()
        
        print("\n" + "="*50)
        print("[PASS] 所有测试通过！")
        print("="*50)
        print("\n新增的10个数学函数：")
        print("  三角函数：正弦、余弦、正切")
        print("  对数函数：自然对数、常用对数、指数")
        print("  取整函数：向上取整、向下取整、四舍五入")
        print("  其他：阶乘")
        return True
    except Exception as e:
        print(f"\n[FAIL] 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
