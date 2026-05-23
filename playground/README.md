# 言律语言交互环境使用指南

## 概述

言律语言提供了两种交互环境：
1. **命令行交互环境 (REPL)** - 适合快速测试和学习
2. **Web Playground** - 适合在线体验和演示

---

## 1. 命令行交互环境 (REPL)

### 启动REPL

```bash
# 方式1：直接运行
python src/yanlv/repl.py

# 方式2：作为模块运行
python -m yanlv.repl
```

### REPL功能

#### 基本命令

| 命令 | 说明 |
|------|------|
| `帮助` | 显示帮助信息 |
| `退出` / `exit` | 退出交互环境 |
| `清空` / `clear` | 清空屏幕 |
| `历史` / `history` | 显示命令历史 |
| `统计` / `stats` | 显示性能统计 |
| `变量` / `vars` | 显示所有变量 |
| `重置` / `reset` | 重置环境 |

#### 编程示例

```言律
# 输出语句
言律> 输出 'Hello World'
=> Hello World

# 变量定义
言律> 定义 变量 x 为 10
=> 定义变量 x = 10

# 条件语句
言律> 如果 条件 成立 则 输出 '条件为真'
=> [条件语句]

# 循环语句
言律> 循环 5 次 执行 输出 '测试'
=> [循环语句]
```

#### 特殊命令

```言律
# 分析代码结构
言律> 分析 输出 '测试'

代码分析:
  源代码: 输出 '测试'
  词元数量: 3

  词元列表:
    1. OUTPUT: '输出'
    2. STRING: '测试'
    3. EOF: ''

# 测试代码执行
言律> 测试 输出 'Hello'

测试执行:
  [输出] Hello

# 提交反馈
言律> 反馈 测试 名词 动词
反馈已提交，ID: xxx
```

### REPL特性

- ✅ **历史记录** - 使用上下箭头浏览历史命令
- ✅ **自动补全** - Tab键自动补全（计划中）
- ✅ **多行输入** - 支持多行代码输入
- ✅ **错误处理** - 友好的错误提示
- ✅ **性能统计** - 实时查看执行统计

---

## 2. Web Playground

### 启动Playground

```bash
# 方式1：使用启动脚本
cd playground
python start.py

# 方式2：直接启动后端
cd playground
python server.py

# 然后在浏览器中打开
# http://localhost:5000
```

### Playground功能

#### 界面布局

```
┌─────────────────────────────────────────┐
│        言律语言 Playground              │
├──────────────────┬──────────────────────┤
│   代码编辑器      │    输出结果          │
│                  │                      │
│  [输入代码]       │  [显示结果]          │
│                  │                      │
│  [运行] [清空]    │  [执行统计]          │
│                  │                      │
│  [快速示例]       │                      │
└──────────────────┴──────────────────────┘
```

#### 功能特点

1. **代码编辑器**
   - 语法高亮（计划中）
   - 行号显示
   - 自动缩进

2. **快速示例**
   - 输出语句
   - 变量定义
   - 条件语句
   - 循环语句

3. **执行统计**
   - 词元数量
   - 执行时间
   - 代码行数

4. **API接口**
   - POST /api/run - 运行代码
   - POST /api/analyze - 分析代码
   - POST /api/feedback - 提交反馈
   - GET /api/stats - 获取统计
   - GET /api/examples - 获取示例

### 使用示例

#### 示例1：输出语句

```言律
输出 'Hello, 言律语言！'
输出 '这是一个中文编程语言'
```

输出：
```
=> Hello, 言律语言！
=> 这是一个中文编程语言
```

#### 示例2：变量定义

```言律
定义 变量 x 为 10
定义 变量 y 为 20
输出 x
输出 y
```

输出：
```
=> 定义变量 x = 10
=> 定义变量 y = 20
=> 10
=> 20
```

#### 示例3：条件语句

```言律
如果 条件 成立 则 输出 '条件为真'
如果 条件 不成立 则 输出 '条件为假'
```

输出：
```
=> [条件语句]
=> [条件语句]
```

---

## 3. API使用

### Python API

```python
from yanlv.lexer import create_lexer

# 创建词法分析器
lexer = create_lexer("jieba")

# 分析代码
tokens = lexer.tokenize("输出 'Hello World'")

# 查看结果
for token in tokens:
    print(f"{token.type.name}: {token.value}")
```

### REST API

#### 运行代码

```bash
curl -X POST http://localhost:5000/api/run \
  -H "Content-Type: application/json" \
  -d '{"code": "输出 \"Hello World\""}'
```

响应：
```json
{
  "success": true,
  "output": "=> Hello World",
  "stats": {
    "tokens": 3,
    "lines": 1,
    "exec_time": 0.5,
    "variables": 0
  }
}
```

#### 分析代码

```bash
curl -X POST http://localhost:5000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"code": "输出 \"测试\""}'
```

响应：
```json
{
  "success": true,
  "tokens": [
    {"type": "OUTPUT", "value": "输出", "line": 1, "column": 1},
    {"type": "STRING", "value": "测试", "line": 1, "column": 4},
    {"type": "EOF", "value": "", "line": 1, "column": 8}
  ],
  "total_tokens": 3
}
```

---

## 4. 高级功能

### 自定义配置

```python
from yanlv.lexer import create_lexer

# 使用不同的分词器
lexer_jieba = create_lexer("jieba")
lexer_thulac = create_lexer("thulac")

# 自定义配置
config = {
    'enable_cache': True,
    'max_cache_size': 1000,
    'enable_parallel': True
}
lexer = create_lexer("jieba", config)
```

### 反馈系统

```python
from yanlv.feedback import FeedbackCollector

collector = FeedbackCollector()

# 收集反馈
feedback_id = collector.collect_ambiguity_feedback(
    source_text="测试代码",
    ambiguous_segment="测试",
    system_interpretation="名词",
    user_correction="动词",
    context=["这是", "一个"],
    confidence=0.8
)

# 查看统计
stats = collector.get_statistics()
print(stats)
```

---

## 5. 故障排除

### 常见问题

#### Q: REPL无法启动？

A: 检查Python版本和依赖：
```bash
python --version  # 需要3.8+
pip install jieba
```

#### Q: Playground无法访问？

A: 检查端口是否被占用：
```bash
# Windows
netstat -ano | findstr :5000

# Linux/Mac
lsof -i :5000
```

#### Q: 分词结果不正确？

A: 尝试不同的分词器：
```python
lexer = create_lexer("thulac")  # 使用THULAC
```

---

## 6. 性能优化

### 缓存优化

```python
# 启用缓存
lexer = create_lexer("jieba", {'enable_cache': True})

# 查看缓存效果
stats = lexer.get_performance_stats()
print(f"缓存命中率: {stats['cache_hit_rate']}")
```

### 并行处理

```python
# 启用并行处理
lexer = create_lexer("jieba", {'enable_parallel': True})

# 处理大量代码
codes = ["代码1", "代码2", "代码3", ...]
results = lexer.tokenize_batch(codes)
```

---

## 7. 扩展开发

### 添加新的词元类型

```python
from yanlv.lexer import TokenType

# 定义新的词元类型
class MyTokenType(TokenType):
    MY_TOKEN = auto()

# 使用新的词元类型
# ...
```

### 自定义分词器

```python
from yanlv.lexer import YanLuTokenizer

class MyTokenizer(YanLuTokenizer):
    def tokenize(self, text):
        # 自定义分词逻辑
        # ...
        return tokens
```

---

## 8. 更多资源

- **项目主页**: https://gitcode.com/skywalk163/yanlv
- **API文档**: API_DOCUMENTATION.md
- **示例代码**: examples/
- **问题反馈**: https://gitcode.com/skywalk163/yanlv/issues

---

**享受使用言律语言编程！** 🎉
