# 言律语言词法分析器 API 文档

## 概述

言律语言词法分析器是一个模块化的中文编程语言词法分析器，支持jieba和THULAC两种分词器，提供完善的错误处理和性能优化功能。

## 主要模块

### 1. 词元定义 (lexer_token)

#### TokenType
词元类型枚举，定义了59种词元类型。

```python
from yanlv.lexer import TokenType

# 词元类型
TokenType.IDENTIFIER  # 标识符
TokenType.NUMBER      # 数字
TokenType.STRING      # 字符串
TokenType.IF          # 如果
TokenType.ELSE        # 否则
TokenType.VERB        # 动词
# ... 更多类型
```

#### Token
词元类，表示一个词法单元。

```python
from yanlv.lexer import Token, TokenType

# 创建词元
token = Token(
    type=TokenType.IDENTIFIER,
    value="变量",
    line=1,
    column=1,
    literal="变量"
)

# 词元方法
token.is_identifier()  # 检查是否为标识符
token.is_number()      # 检查是否为数字
token.is_keyword()     # 检查是否为关键词
token.to_dict()        # 转换为字典
```

### 2. 分词器 (tokenizer)

#### YanLuTokenizer
分词器工厂类。

```python
from yanlv.lexer import YanLuTokenizer

# 创建分词器
tokenizer = YanLuTokenizer.create("jieba")

# 分词
segments = tokenizer.segment("这是一个测试")
# 结果: ['这是', '一个', '测试']

# 获取可用分词器
tokenizers = YanLuTokenizer.get_available_tokenizers()
# 结果: ['jieba', 'thulac']

# 获取分词器信息
info = YanLuTokenizer.get_tokenizer_info("jieba")
```

#### JiebaTokenizer
jieba分词器实现。

```python
from yanlv.lexer import JiebaTokenizer

tokenizer = JiebaTokenizer(
    enable_cache=True,
    cache_size=1000
)

# 分词
segments = tokenizer.segment("中文分词测试")

# 获取统计信息
stats = tokenizer.get_statistics()
```

#### ThulacTokenizer
THULAC分词器实现。

```python
from yanlv.lexer import ThulacTokenizer

tokenizer = ThulacTokenizer(
    seg_only=True,
    enable_cache=True
)

# 分词
segments = tokenizer.segment("中文分词测试")
```

### 3. 词元匹配器 (matcher)

#### TokenMatcher
词元匹配器，用于识别和匹配不同类型的词元。

```python
from yanlv.lexer import TokenMatcher

matcher = TokenMatcher()

# 匹配词元
token = matcher.match_token("123", 0, 1, 1)
# 结果: Token(NUMBER, '123', line=1, col=1)

# 获取词元类型
token_type = matcher.get_token_type("变量")
# 结果: TokenType.IDENTIFIER

# 检查方法
matcher.is_chinese_character('中')  # True
matcher.is_chinese_punctuation('。')  # True
matcher.is_keyword('如果')  # True
```

#### AdvancedTokenMatcher
高级词元匹配器，支持更多特性。

```python
from yanlv.lexer import AdvancedTokenMatcher

matcher = AdvancedTokenMatcher()

# 添加自定义词元类型
matcher.add_custom_token_type(
    pattern=r"^自定义$",
    token_type=TokenType.IDENTIFIER
)

# 添加自定义验证函数
def custom_validator(segment):
    if segment.startswith("自定义"):
        return TokenType.IDENTIFIER
    return None

matcher.add_custom_validator(custom_validator)
```

### 4. 模式管理器 (pattern_manager)

#### PatternManager
模式管理器，管理正则表达式模式。

```python
from yanlv.lexer import PatternManager, PatternType, TokenType

manager = PatternManager()

# 添加模式
manager.add_pattern(
    name="custom_number",
    pattern=r"^\d+$",
    token_type=TokenType.NUMBER,
    pattern_type=PatternType.LITERAL,
    priority=100,
    description="自定义数字模式",
    examples=["123", "456"]
)

# 匹配文本
result = manager.match("123")
# 结果: (TokenType.NUMBER, '123')

# 查找所有匹配
matches = manager.find_all_matches("123 456 789")

# 获取模式
pattern = manager.get_pattern("custom_number")

# 移除模式
manager.remove_pattern("custom_number")

# 获取模式数量
count = manager.get_pattern_count()
```

### 5. 错误处理 (error_handler)

#### ErrorHandler
错误处理器。

```python
from yanlv.lexer import ErrorHandler, ErrorCode, ErrorSeverity
from yanlv.lexer.utils import Position

handler = ErrorHandler(max_errors=100, max_warnings=1000)

# 添加错误
position = Position(line=1, column=5, offset=10)
handler.add_error(
    code=ErrorCode.LEXER_INVALID_CHAR,
    message="无效字符",
    position=position,
    severity=ErrorSeverity.ERROR,
    suggestion="请检查字符是否有效"
)

# 添加警告
handler.add_warning(
    code=ErrorCode.LEXER_INVALID_CHAR,
    message="潜在问题",
    position=position
)

# 检查错误
has_errors = handler.has_errors()
error_count = handler.get_error_count()
warning_count = handler.get_warning_count()

# 获取错误列表
errors = handler.get_all_errors()
warnings = handler.get_all_warnings()

# 格式化输出
output = handler.format_messages()
```

### 6. 上下文管理 (context_manager)

#### ContextManager
上下文管理器。

```python
from yanlv.lexer import ContextManager, ContextType
from yanlv.lexer.utils import Position

manager = ContextManager()

# 推入上下文
position = Position(line=1, column=1, offset=0)
context = manager.push_context(ContextType.FUNCTION, position)

# 弹出上下文
end_position = Position(line=10, column=1, offset=100)
context = manager.pop_context(end_position)

# 获取当前上下文
current = manager.get_current_context()

# 获取上下文深度
depth = manager.get_context_depth()

# 符号表操作
manager.add_symbol("变量", 123, "variable")
value = manager.get_symbol("变量")
has_symbol = manager.has_symbol("变量")

# 统计信息
stats = manager.get_statistics()
```

### 7. 性能优化器 (performance_optimizer)

#### PerformanceOptimizer
性能优化器。

```python
from yanlv.lexer import PerformanceOptimizer, OptimizationConfig, OptimizationLevel

# 创建优化器
config = OptimizationConfig(
    level=OptimizationLevel.ADVANCED,
    enable_cache=True,
    cache_size=2000,
    enable_profiling=True
)
optimizer = PerformanceOptimizer(config)

# 优化分词
segments = optimizer.optimize_tokenization("这是一个测试")

# 优化匹配
result = optimizer.optimize_matching(
    segment="测试",
    matcher_func=lambda s: Token(TokenType.IDENTIFIER, s, 1, 1, s)
)

# 获取统计信息
cache_stats = optimizer.get_cache_stats()
performance_stats = optimizer.get_performance_stats()

# 清空缓存
optimizer.clear_caches()

# 重置性能数据
optimizer.reset_performance_data()
```

### 8. 工具模块 (utils)

#### Position
位置信息。

```python
from yanlv.lexer.utils import Position

position = Position(line=1, column=5, offset=10)
print(position)  # (1:5)
```

#### Range
范围信息。

```python
from yanlv.lexer.utils import Range, Position

start = Position(line=1, column=1, offset=0)
end = Position(line=1, column=10, offset=10)
range_obj = Range(start=start, end=end)
print(range_obj)  # (1:1)-(1:10)
```

#### Cache
缓存实现。

```python
from yanlv.lexer.utils import Cache

cache = Cache(max_size=100)

# 设置缓存
cache.set("key", "value")

# 获取缓存
value = cache.get("key")

# 清空缓存
cache.clear()

# 获取大小
size = cache.size()
```

#### PerformanceMonitor
性能监控器。

```python
from yanlv.lexer.utils import PerformanceMonitor

monitor = PerformanceMonitor()

# 开始监控
monitor.start()

# ... 执行操作 ...

# 停止监控
monitor.stop()

# 获取统计
stats = monitor.get_stats()
```

### 9. 模块化词法分析器 (lexer_modular)

#### ModularYanLuLexer
模块化词法分析器主类。

```python
from yanlv.lexer import ModularYanLuLexer

lexer = ModularYanLuLexer(
    segmenter="jieba",
    verbose=True,
    enable_cache=True,
    cache_size=1000
)

# 分析源代码
tokens = lexer.tokenize("如果 条件 成立 则 输出 'Hello World'")

# 获取错误
errors = lexer.get_errors()
warnings = lexer.get_warnings()

# 检查错误
has_errors = lexer.has_errors()

# 获取性能统计
stats = lexer.get_performance_stats()

# 获取配置
config = lexer.get_config()

# 重置
lexer.reset()
```

## 工厂函数

### create_lexer
创建词法分析器。

```python
from yanlv.lexer import create_lexer

lexer = create_lexer(
    segmenter="jieba",
    verbose=True,
    enable_cache=True
)
```

### create_tokenizer
创建分词器。

```python
from yanlv.lexer import create_tokenizer

tokenizer = create_tokenizer("jieba", enable_cache=True)
```

### create_token_matcher
创建词元匹配器。

```python
from yanlv.lexer import create_token_matcher

matcher = create_token_matcher(advanced=False)
```

### create_pattern_manager
创建模式管理器。

```python
from yanlv.lexer import create_pattern_manager

manager = create_pattern_manager()
```

### create_error_handler
创建错误处理器。

```python
from yanlv.lexer import create_error_handler

handler = create_error_handler(max_errors=100)
```

### create_context_manager
创建上下文管理器。

```python
from yanlv.lexer import create_context_manager

manager = create_context_manager()
```

### create_performance_optimizer
创建性能优化器。

```python
from yanlv.lexer import create_performance_optimizer, OptimizationConfig

config = OptimizationConfig(level=OptimizationLevel.ADVANCED)
optimizer = create_performance_optimizer(config)
```

## 便捷函数

### tokenize
便捷函数：将源代码转换为词法单元列表。

```python
from yanlv.lexer import tokenize

tokens = tokenize("如果 条件 成立", segmenter="jieba")
```

### tokenize_with_stats
便捷函数：将源代码转换为词法单元列表并返回统计信息。

```python
from yanlv.lexer import tokenize_with_stats

tokens, stats = tokenize_with_stats("如果 条件 成立", segmenter="jieba")
print(f"处理了 {stats['tokens_processed']} 个词元")
```

## 配置选项

### 优化级别

```python
from yanlv.lexer import OptimizationLevel

OptimizationLevel.NONE       # 无优化
OptimizationLevel.BASIC      # 基础优化
OptimizationLevel.ADVANCED   # 高级优化
OptimizationLevel.AGGRESSIVE # 激进优化
```

### 错误代码

```python
from yanlv.lexer import ErrorCode

# 词法错误
ErrorCode.LEXER_INVALID_CHAR      # 无效字符
ErrorCode.LEXER_UNEXPECTED_TOKEN  # 意外词元
ErrorCode.LEXER_UNTERMINATED_STRING  # 未终止字符串

# 语法错误
ErrorCode.SYNTAX_UNEXPECTED_TOKEN  # 意外词元
ErrorCode.SYNTAX_MISSING_TOKEN     # 缺失词元

# 语义错误
ErrorCode.SEMANTIC_UNDEFINED_VARIABLE  # 未定义变量
ErrorCode.SEMANTIC_TYPE_MISMATCH       # 类型不匹配
```

### 上下文类型

```python
from yanlv.lexer import ContextType

ContextType.GLOBAL       # 全局上下文
ContextType.FUNCTION     # 函数上下文
ContextType.LOOP         # 循环上下文
ContextType.CONDITIONAL  # 条件上下文
ContextType.BLOCK        # 块上下文
```

## 性能调优

### 缓存配置

```python
# 增加缓存大小
lexer = create_lexer("jieba", cache_size=5000)

# 禁用缓存
lexer = create_lexer("jieba", enable_cache=False)
```

### 优化级别配置

```python
from yanlv.lexer import OptimizationLevel

# 使用高级优化
lexer = create_lexer("jieba", optimization_level="advanced")

# 使用激进优化
lexer = create_lexer("jieba", optimization_level="aggressive")
```

### 性能监控

```python
lexer = create_lexer("jieba")
tokens = lexer.tokenize(source_code)

stats = lexer.get_performance_stats()
print(f"总时间: {stats['total_time']:.3f}秒")
print(f"词元数量: {stats['tokens_processed']}")
print(f"缓存命中率: {stats['tokenization_hit_rate']:.2%}")
```

## 错误处理最佳实践

```python
from yanlv.lexer import create_lexer

lexer = create_lexer("jieba", max_errors=100)
tokens = lexer.tokenize(source_code)

# 检查错误
if lexer.has_errors():
    errors = lexer.get_errors()
    for error in errors:
        print(error)
    
    # 获取警告
    warnings = lexer.get_warnings()
    for warning in warnings:
        print(warning)
```

## 版本信息

```python
import yanlv.lexer

print(yanlv.lexer.__version__)  # 2.0.0
print(yanlv.lexer.__author__)   # 言律语言项目组
print(yanlv.lexer.__description__)  # 模块化词法分析器
```