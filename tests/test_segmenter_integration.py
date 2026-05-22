"""
分词器集成测试

测试jieba和THULAC分词器的集成
"""

import unittest
import sys
import os

# 添加src目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from yanlv.lexer.lexer import YanLuLexer
from yanlv.lexer.token import TokenType


class TestSegmenterIntegration(unittest.TestCase):
    """分词器集成测试"""
    
    def test_jieba_segmenter(self):
        """测试jieba分词器"""
        print("测试jieba分词器...")
        lexer = YanLuLexer(segmenter="jieba")
        
        # 测试简单句子
        source_code = "温度升高，风扇开启。"
        tokens = lexer.tokenize(source_code)
        
        # 检查分词结果
        token_texts = [token.value for token in tokens]
        expected = ["温度", "升高", "，", "风扇", "开启", "。"]
        self.assertEqual(token_texts, expected)
        
        # 检查词元类型
        expected_types = [
            TokenType.IDENTIFIER,  # 温度
            TokenType.VERB,        # 升高
            TokenType.COMMA,       # ，
            TokenType.IDENTIFIER,  # 风扇
            TokenType.VERB,        # 开启
            TokenType.PERIOD,      # 。
        ]
        
        for i, (token, expected_type) in enumerate(zip(tokens, expected_types)):
            self.assertEqual(token.type, expected_type, 
                           f"位置 {i}: '{token.value}' 应该是 {expected_type}, 但得到 {token.type}")
        
        print("  jieba分词器测试通过")
    
    def test_thulac_segmenter_if_available(self):
        """测试THULAC分词器（如果可用）"""
        try:
            import thulac
            print("测试THULAC分词器...")
            lexer = YanLuLexer(segmenter="thulac")
            
            # 测试简单句子
            source_code = "温度升高，风扇开启。"
            tokens = lexer.tokenize(source_code)
            
            # 检查分词结果
            token_texts = [token.value for token in tokens]
            expected = ["温度", "升高", "，", "风扇", "开启", "。"]
            self.assertEqual(token_texts, expected)
            
            # 检查词元类型
            expected_types = [
                TokenType.IDENTIFIER,  # 温度
                TokenType.VERB,        # 升高
                TokenType.COMMA,       # ，
                TokenType.IDENTIFIER,  # 风扇
                TokenType.VERB,        # 开启
                TokenType.PERIOD,      # 。
            ]
            
            for i, (token, expected_type) in enumerate(zip(tokens, expected_types)):
                self.assertEqual(token.type, expected_type, 
                               f"位置 {i}: '{token.value}' 应该是 {expected_type}, 但得到 {token.type}")
            
            print("  THULAC分词器测试通过")
            
        except ImportError:
            print("  THULAC未安装，跳过测试")
            self.skipTest("THULAC未安装")
    
    def test_complex_sentence_jieba(self):
        """测试jieba分词器处理复杂句子"""
        lexer = YanLuLexer(segmenter="jieba")
        
        source_code = "如果温度超过30度，就开启空调。"
        tokens = lexer.tokenize(source_code)
        
        token_texts = [token.value for token in tokens]
        expected = ["如果", "温度", "超过", "30", "度", "，", "就", "开启", "空调", "。"]
        self.assertEqual(token_texts, expected)
    
    def test_complex_sentence_thulac_if_available(self):
        """测试THULAC分词器处理复杂句子（如果可用）"""
        try:
            import thulac
            lexer = YanLuLexer(segmenter="thulac")
            
            source_code = "如果温度超过30度，就开启空调。"
            tokens = lexer.tokenize(source_code)
            
            token_texts = [token.value for token in tokens]
            expected = ["如果", "温度", "超过", "30", "度", "，", "就", "开启", "空调", "。"]
            self.assertEqual(token_texts, expected)
            
        except ImportError:
            self.skipTest("THULAC未安装")
    
    def test_verb_recognition_jieba(self):
        """测试jieba分词器的动词识别"""
        lexer = YanLuLexer(segmenter="jieba")
        
        test_cases = [
            ("计算总和", ["计算", "总和"], [TokenType.VERB, TokenType.IDENTIFIER]),
            ("打印结果", ["打印", "结果"], [TokenType.VERB, TokenType.IDENTIFIER]),
            ("设置温度", ["设置", "温度"], [TokenType.VERB, TokenType.IDENTIFIER]),
            ("开启设备", ["开启", "设备"], [TokenType.VERB, TokenType.IDENTIFIER]),
        ]
        
        for source_code, expected_tokens, expected_types in test_cases:
            with self.subTest(source_code=source_code):
                tokens = lexer.tokenize(source_code)
                token_texts = [token.value for token in tokens]
                self.assertEqual(token_texts, expected_tokens)
                
                for i, (token, expected_type) in enumerate(zip(tokens, expected_types)):
                    self.assertEqual(token.type, expected_type)
    
    def test_verb_recognition_thulac_if_available(self):
        """测试THULAC分词器的动词识别（如果可用）"""
        try:
            import thulac
            lexer = YanLuLexer(segmenter="thulac")
            
            test_cases = [
                ("计算总和", ["计算", "总和"], [TokenType.VERB, TokenType.IDENTIFIER]),
                ("打印结果", ["打印", "结果"], [TokenType.VERB, TokenType.IDENTIFIER]),
                ("设置温度", ["设置", "温度"], [TokenType.VERB, TokenType.IDENTIFIER]),
                ("开启设备", ["开启", "设备"], [TokenType.VERB, TokenType.IDENTIFIER]),
            ]
            
            for source_code, expected_tokens, expected_types in test_cases:
                with self.subTest(source_code=source_code):
                    tokens = lexer.tokenize(source_code)
                    token_texts = [token.value for token in tokens]
                    self.assertEqual(token_texts, expected_tokens)
                    
                    for i, (token, expected_type) in enumerate(zip(tokens, expected_types)):
                        self.assertEqual(token.type, expected_type)
                        
        except ImportError:
            self.skipTest("THULAC未安装")
    
    def test_segmenter_fallback(self):
        """测试分词器回退机制"""
        # 测试无效的分词器名称
        lexer = YanLuLexer(segmenter="invalid_segmenter")
        # 应该回退到jieba
        self.assertEqual(lexer.segmenter_type, "jieba")
        
        # 测试分词功能
        source_code = "测试分词"
        tokens = lexer.tokenize(source_code)
        self.assertEqual(len(tokens), 2)
        self.assertEqual(tokens[0].value, "测试")
        self.assertEqual(tokens[0].type, TokenType.VERB)
        self.assertEqual(tokens[1].value, "分词")
        self.assertEqual(tokens[1].type, TokenType.IDENTIFIER)
    
    def test_performance_comparison(self):
        """性能比较测试"""
        import time
        
        test_text = "在智能家居系统中，温度传感器检测到高温后，自动开启空调制冷模式，同时风扇也开始工作以加速空气流通。"
        
        # jieba性能
        jieba_lexer = YanLuLexer(segmenter="jieba")
        start_time = time.time()
        for _ in range(100):
            jieba_lexer.tokenize(test_text)
        jieba_time = time.time() - start_time
        
        # THULAC性能（如果可用）
        try:
            import thulac
            thulac_lexer = YanLuLexer(segmenter="thulac")
            start_time = time.time()
            for _ in range(100):
                thulac_lexer.tokenize(test_text)
            thulac_time = time.time() - start_time
            
            print(f"\n性能比较:")
            print(f"  jieba: {jieba_time:.4f}秒 (100次)")
            print(f"  THULAC: {thulac_time:.4f}秒 (100次)")
            print(f"  速度比: {jieba_time/thulac_time:.2f}x")
            
            # THULAC应该更快
            self.assertLess(thulac_time, jieba_time * 2, "THULAC不应该比jieba慢太多")
            
        except ImportError:
            print(f"\n性能测试 (仅jieba):")
            print(f"  jieba: {jieba_time:.4f}秒 (100次)")
            self.skipTest("THULAC未安装")


def run_integration_tests():
    """运行集成测试"""
    print("分词器集成测试")
    print("=" * 60)
    
    # 创建测试套件
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # 添加测试类
    suite.addTests(loader.loadTestsFromTestCase(TestSegmenterIntegration))
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # 输出统计信息
    print("\n" + "=" * 60)
    print("分词器集成测试结果统计:")
    print(f"  运行测试: {result.testsRun}")
    print(f"  通过测试: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"  失败测试: {len(result.failures)}")
    print(f"  错误测试: {len(result.errors)}")
    print(f"  跳过测试: {len(result.skipped)}")
    
    if result.failures:
        print("\n失败测试:")
        for test, traceback in result.failures:
            print(f"  {test}:")
            for line in traceback.split('\n')[-3:]:
                print(f"    {line}")
    
    if result.errors:
        print("\n错误测试:")
        for test, traceback in result.errors:
            print(f"  {test}:")
            for line in traceback.split('\n')[-3:]:
                print(f"    {line}")
    
    print("=" * 60)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_integration_tests()
    
    if success:
        print("\n✅ 所有集成测试通过!")
    else:
        print("\n❌ 有测试失败!")
    
    sys.exit(0 if success else 1)