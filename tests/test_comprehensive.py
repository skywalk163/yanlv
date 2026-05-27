"""
言律语言综合测试套件

提升测试覆盖率到80%
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from yanlv.lexer.lexer_token import Token, TokenType
from yanlv.parser import Parser, parse_tokens
from yanlv.ast_nodes import (
Program, VariableDeclaration, FunctionDeclaration,
IfStatement, WhileStatement, BinaryExpression,
Identifier, Literal, ArrayLiteral
)
from yanlv.code_generator import PythonCodeGenerator
from yanlv.js_generator import JavaScriptCodeGenerator
from yanlv.stdlib import (
加, 减, 乘, 除, 幂, 开方, 绝对值,
长度, 添加, 删除, 排序, 反转, 求和, 平均值,
分割, 替换, 去空格, 转大写, 转小写,
当前时间, 当前日期
    )
    from yanlv.multi_track import (
    MultiTrackParser, MultiTrackExecutor, TrackType
    )
    from yanlv.performance import (
    PerformanceMonitor, OptimizedLexer, BatchProcessor
    )


    class TestLexerComprehensive(unittest.TestCase):
    """词法分析器综合测试"""

    def test_token_creation(self):
    """测试Token创建"""
    token = Token(TokenType.NUMBER, 42, 1, 1, '42')
    self.assertEqual(token.type, TokenType.NUMBER)
    self.assertEqual(token.value, 42)
    self.assertEqual(token.line, 1)
    self.assertEqual(token.column, 1)

    def test_token_string_representation(self):
    """测试Token字符串表示"""
    token = Token(TokenType.IDENTIFIER, 'x', 1, 1, 'x')
    str_repr = str(token)
    self.assertIn('IDENTIFIER', str_repr)
    self.assertIn('x', str_repr)

    def test_multiple_token_types(self):
    """测试多种Token类型"""
    types = [
    TokenType.NUMBER, TokenType.STRING, TokenType.BOOLEAN,
    TokenType.IF, TokenType.ELSE, TokenType.WHILE,
    TokenType.DEFINE, TokenType.FUNCTION, TokenType.OUTPUT
    ]

    for token_type in types:
    token = Token(token_type, 'test', 1, 1, 'test')
    self.assertEqual(token.type, token_type)


    class TestParserComprehensive(unittest.TestCase):
    """语法分析器综合测试"""

    def test_empty_program(self):
    """测试空程序"""
    tokens = []
    program = parse_tokens(tokens)
    self.assertIsInstance(program, Program)
    self.assertEqual(len(program.statements), 0)

    def test_variable_declarations(self):
    """测试多个变量声明"""
    tokens = [
    Token(TokenType.DEFINE, '定义', 1, 1, '定义'),
    Token(TokenType.VARIABLE, '变量', 1, 3, '变量'),
    Token(TokenType.IDENTIFIER, 'x', 1, 5, 'x'),
    Token(TokenType.IS, '为', 1, 7, '为'),
    Token(TokenType.NUMBER, 10, 1, 9, '10'),
    Token(TokenType.DEFINE, '定义', 2, 1, '定义'),
    Token(TokenType.VARIABLE, '变量', 2, 3, '变量'),
    Token(TokenType.IDENTIFIER, 'y', 2, 5, 'y'),
    Token(TokenType.IS, '为', 2, 7, '为'),
    Token(TokenType.NUMBER, 20, 2, 9, '20'),
    ]

    program = parse_tokens(tokens)
    self.assertEqual(len(program.statements), 2)

    def test_nested_expressions(self):
    """测试嵌套表达式"""
    tokens = [
    Token(TokenType.NUMBER, 2, 1, 1, '2'),
    Token(TokenType.PLUS, '+', 1, 3, '+'),
    Token(TokenType.LPAREN, '(', 1, 5, '('),
    Token(TokenType.NUMBER, 3, 1, 6, '3'),
    Token(TokenType.MULTIPLY, '*', 1, 8, '*'),
    Token(TokenType.NUMBER, 4, 1, 10, '4'),
    Token(TokenType.RPAREN, ')', 1, 11, ')'),
    ]

    parser = Parser(tokens)
    expr = parser._parse_expression()
    self.assertIsInstance(expr, BinaryExpression)


    class TestCodeGeneratorComprehensive(unittest.TestCase):
    """代码生成器综合测试"""

    def test_python_generator_basic(self):
    """测试Python代码生成器基础功能"""
    generator = PythonCodeGenerator()

    # 测试数字字面量
    lit = Literal(42, 'number')
    code = generator.generate(lit)
    self.assertEqual(code, '42')

    # 测试字符串字面量
    lit = Literal('hello', 'string')
    code = generator.generate(lit)
    self.assertEqual(code, '"hello"')

    def test_javascript_generator_basic(self):
    """测试JavaScript代码生成器基础功能"""
    generator = JavaScriptCodeGenerator()

    # 测试数字字面量
    lit = Literal(42, 'number')
    code = generator.generate(lit)
    self.assertEqual(code, '42')

    # 测试布尔字面量
    lit = Literal(True, 'boolean')
    code = generator.generate(lit)
    self.assertEqual(code, 'true')

    def test_complex_program_generation(self):
    """测试复杂程序生成"""
    program = Program([
    VariableDeclaration('x', Literal(10, 'number')),
    VariableDeclaration('y', Literal(20, 'number')),
    ])

    py_gen = PythonCodeGenerator()
    py_code = py_gen.generate(program)

    self.assertIn('x', py_code)
    self.assertIn('y', py_code)

    js_gen = JavaScriptCodeGenerator()
    js_code = js_gen.generate(program)

    self.assertIn('let x', js_code)
    self.assertIn('let y', js_code)


    class TestStdlibComprehensive(unittest.TestCase):
    """标准库综合测试"""

    def test_math_operations(self):
    """测试数学运算"""
    self.assertEqual(加(1, 2), 3)
    self.assertEqual(减(5, 3), 2)
    self.assertEqual(乘(4, 5), 20)
    self.assertEqual(除(10, 2), 5.0)
    self.assertEqual(幂(2, 3), 8)
    self.assertEqual(开方(16), 4.0)
    self.assertEqual(绝对值(-5), 5)

    def test_array_operations(self):
    """测试数组操作"""
    arr = [1, 2, 3, 4, 5]

    self.assertEqual(长度(arr), 5)
    self.assertEqual(求和(arr), 15)
    self.assertEqual(平均值(arr), 3.0)
    self.assertEqual(最大值(arr), 5)
    self.assertEqual(最小值(arr), 1)

    sorted_arr = 排序([3, 1, 2])
    self.assertEqual(sorted_arr, [1, 2, 3])

    reversed_arr = 反转([1, 2, 3])
    self.assertEqual(reversed_arr, [3, 2, 1])

    def test_string_operations(self):
    """测试字符串操作"""
    self.assertEqual(去空格("  hello  "), "hello")
    self.assertEqual(转大写("hello"), "HELLO")
    self.assertEqual(转小写("HELLO"), "hello")
    self.assertEqual(替换("hello world", "world", "python"), "hello python")
    self.assertEqual(分割("a,b,c", ","), ["a", "b", "c"])

    def test_time_functions(self):
    """测试时间函数"""
    now = 当前时间()
    self.assertIsInstance(now, str)
    self.assertIn('-', now)

    today = 当前日期()
    self.assertIsInstance(today, str)
    self.assertIn('-', today)


    class TestMultiTrackComprehensive(unittest.TestCase):
    """多轨制综合测试"""

    def test_parse_multiple_tracks(self):
    """测试解析多个轨"""
    source = """
    Python轨
    x = 10
    结束Python轨

    JavaScript轨
    let y = 20;
    结束JavaScript轨
    """
    parser = MultiTrackParser()
    program = parser.parse(source)

    python_blocks = [b for b in program.blocks if b.track_type == TrackType.PYTHON]
    js_blocks = [b for b in program.blocks if b.track_type == TrackType.JAVASCRIPT]

    self.assertEqual(len(python_blocks), 1)
    self.assertEqual(len(js_blocks), 1)

    def test_track_execution(self):
    """测试轨执行"""
    source = """
    Python轨
    x = 10
    y = 20
    结束Python轨
    """
    parser = MultiTrackParser()
    program = parser.parse(source)

    executor = MultiTrackExecutor()
    results = executor.execute(program)

    self.assertGreater(len(results), 0)


    class TestPerformanceComprehensive(unittest.TestCase):
    """性能优化综合测试"""

    def test_performance_monitor(self):
    """测试性能监控"""
    monitor = PerformanceMonitor()

    # 测量多个操作
    for i in range(3):
    with monitor.measure('test_op') as ctx:
    ctx.set_input_size(100 * (i + 1))

    summary = monitor.get_summary()
    self.assertIn('test_op', summary)
    self.assertEqual(summary['test_op']['count'], 3)

    def test_optimized_lexer(self):
    """测试优化词法分析器"""
    lexer = OptimizedLexer()

    source = "定义变量x为10"
    tokens1 = lexer.tokenize_optimized(source)
    tokens2 = lexer.tokenize_optimized(source)  # 应该从缓存获取

    self.assertEqual(len(tokens1), len(tokens2))

    def test_batch_processor(self):
    """测试批处理器"""
    processor = BatchProcessor(batch_size=10)
    items = list(range(25))

    results = processor.process_batch(items, lambda x: x * 2)

    self.assertEqual(len(results), 25)
    self.assertEqual(results[0], 0)
    self.assertEqual(results[24], 48)


    class TestIntegration(unittest.TestCase):
    """集成测试"""

    def test_full_pipeline(self):
    """测试完整流水线"""
    # 1. 创建Token
    tokens = [
    Token(TokenType.DEFINE, '定义', 1, 1, '定义'),
    Token(TokenType.VARIABLE, '变量', 1, 3, '变量'),
    Token(TokenType.IDENTIFIER, 'x', 1, 5, 'x'),
    Token(TokenType.IS, '为', 1, 7, '为'),
    Token(TokenType.NUMBER, 10, 1, 9, '10'),
    ]

    # 2. 解析为AST
    program = parse_tokens(tokens)
    self.assertIsInstance(program, Program)

    # 3. 生成Python代码
    py_gen = PythonCodeGenerator()
    py_code = py_gen.generate(program)
    self.assertIn('x', py_code)

    # 4. 生成JavaScript代码
    js_gen = JavaScriptCodeGenerator()
    js_code = js_gen.generate(program)
    self.assertIn('let x', js_code)

    def test_stdlib_integration(self):
    """测试标准库集成"""
    # 使用标准库函数
    arr = [1, 2, 3, 4, 5]

    # 链式操作
    result = 求和(arr)
    avg = 平均值(arr)

    self.assertEqual(result, 15)
    self.assertEqual(avg, 3.0)


    class TestEdgeCases(unittest.TestCase):
    """边界情况测试"""

    def test_empty_input(self):
    """测试空输入"""
    tokens = []
    program = parse_tokens(tokens)
    self.assertEqual(len(program.statements), 0)

    def test_single_token(self):
    """测试单个Token"""
    token = Token(TokenType.NUMBER, 42, 1, 1, '42')
    self.assertEqual(token.value, 42)

    def test_large_numbers(self):
    """测试大数字"""
    result = 加(1000000, 2000000)
    self.assertEqual(result, 3000000)

    def test_special_characters(self):
    """测试特殊字符"""
    text = "你好，世界！"
    result = 长度(text)
    self.assertEqual(result, 6)


    # 导入需要的函数
    from yanlv.stdlib import 最大值, 最小值


    if __name__ == '__main__':
    unittest.main()
