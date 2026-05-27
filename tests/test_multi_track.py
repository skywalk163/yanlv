"""
言律语言多轨制支持测试
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from yanlv.multi_track import (
MultiTrackParser, MultiTrackExecutor, MultiTrackCodeGenerator,
TrackType, create_multi_track_parser
)


class TestMultiTrackParser(unittest.TestCase):
"""测试多轨解析器"""

def setUp(self):
self.parser = create_multi_track_parser()

def test_parse_yanlv_code(self):
"""测试言律代码解析"""
source = "定义变量x为10"
program = self.parser.parse(source)

self.assertEqual(len(program.blocks), 1)
self.assertEqual(program.blocks[0].track_type, TrackType.YANLV)

def test_parse_python_track(self):
"""测试Python轨解析"""
source = """
Python轨
x = 10
y = 20
结束Python轨
"""
program = self.parser.parse(source)

# 找到Python轨块
python_blocks = [b for b in program.blocks if b.track_type == TrackType.PYTHON]
self.assertEqual(len(python_blocks), 1)
self.assertIn('x = 10', python_blocks[0].code)

def test_parse_javascript_track(self):
"""测试JavaScript轨解析"""
source = """
JavaScript轨
let x = 10;
let y = 20;
结束JavaScript轨
"""
program = self.parser.parse(source)

js_blocks = [b for b in program.blocks if b.track_type == TrackType.JAVASCRIPT]
self.assertEqual(len(js_blocks), 1)
self.assertIn('let x = 10;', js_blocks[0].code)

def test_parse_sql_track(self):
"""测试SQL轨解析"""
source = """
SQL轨
SELECT * FROM users
WHERE age > 18
结束SQL轨
"""
program = self.parser.parse(source)

sql_blocks = [b for b in program.blocks if b.track_type == TrackType.SQL]
self.assertEqual(len(sql_blocks), 1)
self.assertIn('SELECT * FROM users', sql_blocks[0].code)

def test_parse_multi_track_program(self):
"""测试多轨程序解析"""
source = """
定义变量x为10

Python轨
y = x * 2
结束Python轨

JavaScript轨
let z = y + 5;
结束JavaScript轨
"""
program = self.parser.parse(source)

# 应该有3个块
self.assertGreaterEqual(len(program.blocks), 2)


class TestMultiTrackExecutor(unittest.TestCase):
"""测试多轨执行器"""

def setUp(self):
self.executor = MultiTrackExecutor()
self.parser = create_multi_track_parser()

def test_execute_python_code(self):
"""测试Python代码执行"""
source = """
Python轨
x = 10
y = 20
结束Python轨
"""
program = self.parser.parse(source)
results = self.executor.execute(program)

# 检查执行结果
self.assertGreater(len(results), 0)


class TestMultiTrackCodeGenerator(unittest.TestCase):
"""测试多轨代码生成器"""

def setUp(self):
self.generator = MultiTrackCodeGenerator()
self.parser = create_multi_track_parser()

def test_generate_python_code(self):
"""测试Python代码生成"""
source = """
Python轨
x = 10
y = 20
结束Python轨
"""
program = self.parser.parse(source)
code = self.generator.generate(program, TrackType.PYTHON)

self.assertIn('x = 10', code)

def test_generate_javascript_code(self):
"""测试JavaScript代码生成"""
source = """
JavaScript轨
let x = 10;
let y = 20;
结束JavaScript轨
"""
program = self.parser.parse(source)
code = self.generator.generate(program, TrackType.JAVASCRIPT)

self.assertIn('let x = 10;', code)


class TestTrackTypes(unittest.TestCase):
"""测试轨类型"""

def test_track_type_values(self):
"""测试轨类型值"""
self.assertEqual(TrackType.YANLV.value, "yanlv")
self.assertEqual(TrackType.PYTHON.value, "python")
self.assertEqual(TrackType.JAVASCRIPT.value, "javascript")
self.assertEqual(TrackType.SQL.value, "sql")


if __name__ == '__main__':
unittest.main()
