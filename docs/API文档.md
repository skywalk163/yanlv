# 言律编程语言 API 文档

## 目录

1. [词法分析器](#词法分析器)
2. [语法分析器](#语法分析器)
3. [解释器](#解释器)
4. [编译器](#编译器)
5. [标准库](#标准库)
6. [多轨制](#多轨制)
7. [性能优化](#性能优化)

---

## 词法分析器

### Lexer

主词法分析器类。

```python
from yanlv.lexer import Lexer

lexer = Lexer()
tokens = lexer.tokenize(source_code)
```

#### 方法

##### `tokenize(source: str) -> List[Token]`

将源代码转换为Token列表。

**参数：**
- `source`: 源代码字符串

**返回：**
- Token列表

**示例：**
```python
source = "定义变量x为10"
tokens = lexer.tokenize(source)
# 返回: [Token(DEFINE), Token(VARIABLE), Token(IDENTIFIER, 'x'), ...]
```

### Token

Token类，表示词法单元。

```python
from yanlv.lexer.lexer_token import Token, TokenType

token = Token(TokenType.NUMBER, 42, 1, 1, '42')
```

#### 属性

- `type`: TokenType - Token类型
- `value`: Any - Token值
- `line`: int - 行号
- `column`: int - 列号
- `literal`: str - 字面量

---

## 语法分析器

### Parser

主语法分析器类。

```python
from yanlv.parser import Parser

parser = Parser(tokens)
ast = parser.parse()
```

#### 方法

##### `parse() -> Program`

解析Token序列，生成AST。

**返回：**
- Program节点（AST根节点）

**示例：**
```python
tokens = lexer.tokenize(source)
ast = parser.parse(tokens)
# 返回: Program(statements=[...])
```

### AST节点类型

#### Program

程序节点，AST的根节点。

```python
from yanlv.ast_nodes import Program

program = Program(statements=[
    VariableDeclaration('x', Literal(10, 'number'))
])
```

#### VariableDeclaration

变量声明节点。

```python
from yanlv.ast_nodes import VariableDeclaration

var_decl = VariableDeclaration('x', Literal(10, 'number'))
```

#### FunctionDeclaration

函数声明节点。

```python
from yanlv.ast_nodes import FunctionDeclaration

func_decl = FunctionDeclaration(
    name='add',
    parameters=['a', 'b'],
    body=[...]
)
```

#### IfStatement

条件语句节点。

```python
from yanlv.ast_nodes import IfStatement

if_stmt = IfStatement(
    condition=BinaryExpression('>', Identifier('x'), Literal(10, 'number')),
    consequent=[...],
    alternate=[...]
)
```

---

## 解释器

### YanLuInterpreter

言律语言解释器。

```python
from yanlv.interpreter import YanLuInterpreter

interpreter = YanLuInterpreter()
output = interpreter.execute(tokens)
```

#### 方法

##### `execute(tokens: List[Token]) -> List[str]`

执行Token序列。

**参数：**
- `tokens`: Token列表

**返回：**
- 输出列表

**示例：**
```python
source = """
定义变量x为10
输出x
"""
tokens = lexer.tokenize(source)
output = interpreter.execute(tokens)
# 返回: ['=> 10']
```

---

## 编译器

### PythonCodeGenerator

Python代码生成器。

```python
from yanlv.code_generator import PythonCodeGenerator

generator = PythonCodeGenerator()
python_code = generator.generate(ast)
```

#### 方法

##### `generate(node: ASTNode) -> str`

生成Python代码。

**参数：**
- `node`: AST节点

**返回：**
- Python代码字符串

**示例：**
```python
ast = parser.parse(tokens)
code = generator.generate(ast)
# 返回: "x = 10\nprint(x)"
```

### JavaScriptCodeGenerator

JavaScript代码生成器。

```python
from yanlv.js_generator import JavaScriptCodeGenerator

js_generator = JavaScriptCodeGenerator()
js_code = js_generator.generate(ast)
```

---

## 标准库

### 数学函数

```python
from yanlv.stdlib import 加, 减, 乘, 除, 幂, 开方

# 加法
result = 加(10, 20)  # 30

# 减法
result = 减(30, 10)  # 20

# 乘法
result = 乘(5, 6)  # 30

# 除法
result = 除(20, 4)  # 5.0

# 幂运算
result = 幂(2, 10)  # 1024

# 开方
result = 开方(16)  # 4.0
```

### 数组函数

```python
from yanlv.stdlib import 长度, 添加, 删除, 排序, 求和, 平均值

arr = [1, 2, 3, 4, 5]

# 长度
n = 长度(arr)  # 5

# 添加
添加(arr, 6)  # [1, 2, 3, 4, 5, 6]

# 排序
sorted_arr = 排序([3, 1, 2])  # [1, 2, 3]

# 求和
total = 求和(arr)  # 15

# 平均值
avg = 平均值(arr)  # 3.0
```

### 字符串函数

```python
from yanlv.stdlib import 分割, 替换, 去空格, 转大写, 转小写

# 分割
parts = 分割("a,b,c", ",")  # ["a", "b", "c"]

# 替换
text = 替换("hello world", "world", "python")  # "hello python"

# 去空格
text = 去空格("  hello  ")  # "hello"

# 转大写
text = 转大写("hello")  # "HELLO"
```

### 文件函数

```python
from yanlv.stdlib import 读取文件, 写入文件, 文件存在

# 读取文件
content = 读取文件("data.txt")

# 写入文件
写入文件("output.txt", "Hello World")

# 检查文件存在
exists = 文件存在("data.txt")  # True/False
```

### JSON函数

```python
from yanlv.stdlib import 解析JSON, 生成JSON

# 解析JSON
data = 解析JSON('{"name":"张三","age":25}')

# 生成JSON
json_str = 生成JSON({"name": "张三", "age": 25})
```

### 时间函数

```python
from yanlv.stdlib import 当前时间, 当前日期, 时间戳

# 当前时间
now = 当前时间()  # "2026-05-26 12:00:00"

# 当前日期
today = 当前日期()  # "2026-05-26"

# 时间戳
ts = 时间戳()  # 1716700800.0
```

---

## 多轨制

### MultiTrackParser

多轨解析器。

```python
from yanlv.multi_track import MultiTrackParser

parser = MultiTrackParser()
program = parser.parse(source)
```

#### 使用示例

```yan
# Python轨
Python轨
x = 10
y = 20
结束Python轨

# JavaScript轨
JavaScript轨
let z = x + y;
结束JavaScript轨

# SQL轨
SQL轨
SELECT * FROM users
WHERE age > 18
结束SQL轨
```

### MultiTrackExecutor

多轨执行器。

```python
from yanlv.multi_track import MultiTrackExecutor

executor = MultiTrackExecutor()
results = executor.execute(program)
```

---

## 性能优化

### PerformanceMonitor

性能监控器。

```python
from yanlv.performance import PerformanceMonitor

monitor = PerformanceMonitor()

with monitor.measure('operation') as ctx:
    ctx.set_input_size(100)
    # 执行操作

summary = monitor.get_summary()
```

### OptimizedLexer

优化的词法分析器。

```python
from yanlv.performance import OptimizedLexer

lexer = OptimizedLexer()
tokens = lexer.tokenize_optimized(source)
```

### 缓存装饰器

```python
from yanlv.performance import cached, memoize

# LRU缓存
@cached(maxsize=128)
def expensive_function(x):
    return x * 2

# 记忆化
@memoize
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
```

---

## 完整示例

### 示例1：基本使用

```python
from yanlv.lexer import Lexer
from yanlv.parser import Parser
from yanlv.interpreter import YanLuInterpreter

# 源代码
source = """
定义变量x为10
定义变量y为20
输出x加y
"""

# 词法分析
lexer = Lexer()
tokens = lexer.tokenize(source)

# 语法分析
parser = Parser(tokens)
ast = parser.parse()

# 解释执行
interpreter = YanLuInterpreter()
output = interpreter.execute(tokens)

print(output)  # ['=> 30']
```

### 示例2：编译到Python

```python
from yanlv.lexer import Lexer
from yanlv.parser import Parser
from yanlv.code_generator import PythonCodeGenerator

source = """
定义变量x为10
定义变量y为20
输出x加y
"""

# 编译流程
tokens = Lexer().tokenize(source)
ast = Parser(tokens).parse()
python_code = PythonCodeGenerator().generate(ast)

print(python_code)
# 输出:
# x = 10
# y = 20
# print((x + y))
```

### 示例3：编译到JavaScript

```python
from yanlv.lexer import Lexer
from yanlv.parser import Parser
from yanlv.js_generator import JavaScriptCodeGenerator

source = """
定义变量x为10
定义变量y为20
输出x加y
"""

# 编译流程
tokens = Lexer().tokenize(source)
ast = Parser(tokens).parse()
js_code = JavaScriptCodeGenerator().generate(ast)

print(js_code)
# 输出:
# let x = 10;
# let y = 20;
# console.log((x + y));
```

---

## 错误处理

### 常见错误

1. **词法错误**
```python
# 未闭合的字符串
source = '定义变量x为"hello'
# 错误: 未闭合的字符串
```

2. **语法错误**
```python
# 未闭合的块
source = """
如果x大于10则
  输出x
# 缺少"结束"
"""
# 错误: 未闭合的如果块
```

3. **运行时错误**
```python
# 未定义的变量
source = "输出x"
# 错误: 变量x未定义
```

---

## 性能建议

1. **使用缓存**
```python
from yanlv.performance import OptimizedLexer

lexer = OptimizedLexer()
# 自动缓存结果
tokens = lexer.tokenize_optimized(source)
```

2. **批处理**
```python
from yanlv.performance import BatchProcessor

processor = BatchProcessor(batch_size=100)
results = processor.process_batch(items, process_function)
```

3. **性能监控**
```python
from yanlv.performance import PerformanceMonitor

monitor = PerformanceMonitor()
# 监控关键操作
with monitor.measure('tokenize'):
    tokens = lexer.tokenize(source)
```

---

**版本：** 0.1.0  
**更新时间：** 2026-05-26
