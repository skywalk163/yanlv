"""
词法分析器Token缓存性能测试

测试Token缓存对词法分析器性能的提升效果
"""

import pytest
import time
from yanlv.lexer.lexer_modular import create_lexer
from yanlv.lexer.token_cache import get_global_cache


class TestLexerCachePerformance:
"""词法分析器缓存性能测试"""

def test_cache_speedup(self):
"""测试缓存加速效果"""
# 创建启用缓存的词法分析器
lexer = create_lexer(enable_cache=True, verbose=False)

# 测试代码
code = """
定义 变量 甲 为 10
定义 变量 乙 为 20
定义 函数 加法(参数 甲, 参数 乙) 为
返回 甲 加 乙

定义 变量 结果 为 加法(甲, 乙)
输出 结果
""" * 10  # 重复10次以增加处理时间

# 第一次编译(缓存未命中)
start1 = time.time()
tokens1 = lexer.tokenize(code)
time1 = (time.time() - start1) * 1000  # 转换为毫秒

stats1 = lexer.get_performance_stats()

# 第二次编译(缓存命中)
start2 = time.time()
tokens2 = lexer.tokenize(code)
time2 = (time.time() - start2) * 1000  # 转换为毫秒

stats2 = lexer.get_performance_stats()

# 验证结果相同
assert len(tokens1) == len(tokens2)
assert tokens1 == tokens2

# 验证缓存命中
assert stats2.get('cache_hits', 0) >= 1

# 验证缓存加速效果(第二次应该快得多)
# 由于缓存命中,第二次编译时间应该显著减少
print(f"\n第一次编译时间: {time1:.2f}ms")
print(f"第二次编译时间: {time2:.2f}ms")
print(f"加速比: {time1/time2 if time2 > 0 else float('inf'):.2f}x")

# 缓存命中时,时间应该减少至少50%
if time1 > 0:
speedup = time1 / time2 if time2 > 0 else float('inf')
assert speedup > 1.5, f"缓存加速效果不明显: {speedup:.2f}x"

def test_cache_statistics(self):
"""测试缓存统计信息"""
# 清空全局缓存
cache = get_global_cache()
cache.clear()

# 创建词法分析器
lexer = create_lexer(enable_cache=True)

# 不同的代码片段
codes = [
"定义 变量 甲 为 10",
"定义 变量 乙 为 20",
"定义 变量 甲 为 10",  # 重复
"输出 甲",
"定义 变量 甲 为 10",  # 再次重复
]

# 编译所有代码
for code in codes:
lexer.tokenize(code)

# 获取缓存统计
stats = lexer.get_performance_stats()
cache_stats = stats.get('token_cache', {})

# 验证缓存统计
assert 'hits' in cache_stats
assert 'misses' in cache_stats
assert cache_stats['hits'] >= 2  # 至少2次命中
assert cache_stats['misses'] >= 3  # 至少3次未命中

print(f"\n缓存命中次数: {cache_stats['hits']}")
print(f"缓存未命中次数: {cache_stats['misses']}")
print(f"命中率: {cache_stats.get('hit_rate', '0%')}")

def test_cache_disabled(self):
"""测试禁用缓存"""
# 创建禁用缓存的词法分析器
lexer = create_lexer(enable_cache=False)

code = "定义 变量 甲 为 10"

# 编译两次
tokens1 = lexer.tokenize(code)
tokens2 = lexer.tokenize(code)

# 验证结果相同
assert tokens1 == tokens2

# 验证没有缓存统计
stats = lexer.get_performance_stats()
assert 'token_cache' not in stats or stats['token_cache'] is None

def test_large_code_caching(self):
"""测试大型代码缓存"""
lexer = create_lexer(enable_cache=True)

# 生成大型代码
code_lines = []
for i in range(100):
code_lines.append(f"定义 变量 变量{i} 为 {i}")

code = "\n".join(code_lines)

# 第一次编译
start1 = time.time()
tokens1 = lexer.tokenize(code)
time1 = (time.time() - start1) * 1000

# 第二次编译
start2 = time.time()
tokens2 = lexer.tokenize(code)
time2 = (time.time() - start2) * 1000

# 验证结果相同
assert tokens1 == tokens2

# 验证缓存加速
if time1 > 0 and time2 > 0:
speedup = time1 / time2
print(f"\n大型代码编译:")
print(f"第一次: {time1:.2f}ms")
print(f"第二次: {time2:.2f}ms")
print(f"加速比: {speedup:.2f}x")

# 大型代码的加速效果应该更明显
assert speedup > 2.0, f"大型代码缓存加速效果不明显: {speedup:.2f}x"

def test_cache_with_different_codes(self):
"""测试不同代码的缓存"""
lexer = create_lexer(enable_cache=True)

# 不同的代码
codes = {
'code1': "定义 变量 甲 为 10",
'code2': "定义 变量 乙 为 20",
'code3': "输出 甲",
}

# 第一次编译所有代码
results1 = {}
for name, code in codes.items():
results1[name] = lexer.tokenize(code)

# 第二次编译所有代码(应该从缓存获取)
results2 = {}
for name, code in codes.items():
results2[name] = lexer.tokenize(code)

# 验证结果相同
for name in codes:
assert results1[name] == results2[name]

# 验证缓存统计
stats = lexer.get_performance_stats()
cache_stats = stats.get('token_cache', {})

# 应该有3次缓存命中
assert cache_stats['hits'] >= 3

def test_cache_memory_efficiency(self):
"""测试缓存内存效率"""
cache = get_global_cache()
cache.clear()

lexer = create_lexer(enable_cache=True, cache_size=100)

# 编译多个不同的代码
for i in range(150):  # 超过缓存大小
code = f"定义 变量 变量{i} 为 {i}"
lexer.tokenize(code)

# 获取缓存统计
cache_stats = cache.get_stats()

# 验证缓存大小不超过最大值
assert cache_stats.size <= 100

# 验证有淘汰发生
assert cache_stats.evictions > 0

print(f"\n缓存大小: {cache_stats.size}/{cache_stats.max_size}")
print(f"淘汰次数: {cache_stats.evictions}")


if __name__ == '__main__':
pytest.main([__file__, '-v', '-s'])
