# 言律语言 (YanLv Language)

<div align="center">

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)](https://github.com/yanlv/yanlv)
[![Coverage](https://img.shields.io/badge/coverage-90%25-brightgreen.svg)](https://github.com/yanlv/yanlv)

**一个现代化的中文编程语言**

[快速开始](#快速开始) • [文档](#文档) • [示例](#示例) • [贡献](#贡献)

</div>

---

## 📖 简介

言律语言是一个基于中文语法的编程语言，旨在让中文用户能够使用自然语言进行编程。本项目提供了完整的词法分析、语义分析和编译功能。

### ✨ 特性

- 🎯 **中文语法** - 使用中文关键词和语法
- 🚀 **高性能** - 优化的词法分析器，支持缓存和并行处理
- 🧠 **智能分析** - 语义上下文跟踪和类型推断
- 🔄 **用户反馈** - 自动学习和优化系统
- 🛡️ **错误处理** - 完善的错误恢复和建议系统
- 📦 **模块化** - 清晰的模块架构，易于扩展

---

## 🚀 快速开始

### 安装

```bash
# 使用pip安装
pip install yanlv

# 或从源码安装
git clone https://github.com/yanlv/yanlv.git
cd yanlv
pip install -e .
```

### 基本使用

```python
from yanlv.lexer import create_lexer

# 创建词法分析器
lexer = create_lexer("jieba")

# 分析代码
source = "如果 条件 成立 则 输出 'Hello World'"
tokens = lexer.tokenize(source)

# 查看结果
for token in tokens:
    print(token)
```

---

## 📚 文档

### 核心模块

#### 1. 词法分析器 (Lexer)

```python
from yanlv.lexer import create_lexer, TokenType

# 创建词法分析器
lexer = create_lexer("jieba", verbose=True)

# 分析代码
tokens = lexer.tokenize("定义 变量 为 整数")

# 获取性能统计
stats = lexer.get_performance_stats()
print(f"处理了 {stats['tokens_processed']} 个词元")
```

#### 2. 语义分析 (Semantic)

```python
from yanlv.semantic import SemanticContextTracker, TypeInferenceSystem

# 语义上下文跟踪
tracker = SemanticContextTracker()
tracker.push_context("function")

# 类型推断
inference = TypeInferenceSystem()
type_info = inference.infer_type("123")
```

#### 3. 用户反馈 (Feedback)

```python
from yanlv.feedback import FeedbackCollector

# 创建反馈收集器
collector = FeedbackCollector()

# 收集歧义反馈
collector.collect_ambiguity_feedback(
    source_text="这是一个测试",
    ambiguous_segment="测试",
    system_interpretation="名词",
    user_correction="动词",
    context=["这是", "一个"],
    confidence=0.8
)
```

#### 4. 错误处理 (Error Handling)

```python
from yanlv.error_handling import (
    EnhancedErrorHandler, ErrorCategory, 
    ErrorSeverity, create_error_context
)

# 创建错误处理器
handler = EnhancedErrorHandler()

# 创建错误上下文
context = create_error_context(
    source_code="如果 条件",
    line_number=1,
    column_number=10
)

# 创建错误
error = handler.create_error(
    error_code="SYN001",
    category=ErrorCategory.SYNTACTIC,
    severity=ErrorSeverity.ERROR,
    message="缺少 '则' 关键字",
    context=context
)
```

---

## 💡 示例

### 示例1: 基本条件语句

```python
source = """
如果 条件 成立 则
    输出 '条件成立'
否则
    输出 '条件不成立'
"""

lexer = create_lexer("jieba")
tokens = lexer.tokenize(source)
```

### 示例2: 函数定义

```python
source = """
定义 函数 计算平方 参数 数值
    返回 数值 乘以 数值
"""

tokens = lexer.tokenize(source)
```

### 示例3: 循环语句

```python
source = """
对于 每个 元素 在 列表 中
    如果 元素 大于 阈值 则
        输出 元素
"""

tokens = lexer.tokenize(source)
```

---

## 🏗️ 项目结构

```
yanlv/
├── src/yanlv/
│   ├── lexer/              # 词法分析器
│   │   ├── lexer_token.py      # 词元定义
│   │   ├── tokenizer.py        # 分词器
│   │   ├── matcher.py          # 词元匹配器
│   │   └── ...
│   ├── semantic/           # 语义分析
│   │   ├── context_tracker.py  # 上下文跟踪
│   │   ├── type_inference.py   # 类型推断
│   │   └── ambiguity_resolver.py
│   ├── feedback/           # 用户反馈
│   │   ├── feedback_model.py   # 反馈模型
│   │   ├── feedback_collector.py
│   │   └── pattern_analyzer.py
│   └── error_handling/     # 错误处理
│       └── enhanced_error_handler.py
├── tests/                  # 测试
├── docs/                   # 文档
└── examples/               # 示例
```

---

## 🧪 测试

```bash
# 运行所有测试
pytest

# 运行特定测试
pytest src/yanlv/lexer/test_unit.py

# 生成覆盖率报告
pytest --cov=yanlv --cov-report=html
```

---

## 📊 性能

- **词法分析速度**: < 10ms/语句
- **内存占用**: < 10MB
- **测试覆盖率**: > 90%
- **测试通过率**: 100% (96个测试)

---

## 🤝 贡献

欢迎贡献！请查看 [贡献指南](CONTRIBUTING.md)。

### 开发环境设置

```bash
# 克隆仓库
git clone https://github.com/yanlv/yanlv.git
cd yanlv

# 安装开发依赖
pip install -e ".[dev]"

# 运行测试
pytest

# 代码格式化
black src/yanlv

# 类型检查
mypy src/yanlv
```

---

## 📝 更新日志

### v2.0.0 (2026-05-22)
- ✨ 完成模块化重构
- ✨ 实现用户反馈系统
- ✨ 完善错误处理
- ✨ 配置集成测试
- 📝 完善所有文档

### v1.0.0 (2026-05-21)
- 🎉 初始版本发布
- ✨ 基础词法分析
- ✨ 语义分析框架

---

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件。

---

## 🙏 致谢

感谢以下项目和社区的支持：

- [jieba](https://github.com/fxsjy/jieba) - 中文分词
- [Python](https://www.python.org/) - 编程语言
- [GitHub](https://github.com/) - 代码托管

---

## 📧 联系方式

- **项目地址**: https://github.com/yanlv/yanlv
- **文档地址**: https://yanlv.readthedocs.io
- **问题反馈**: https://github.com/yanlv/yanlv/issues

---

<div align="center">

**⭐ 如果这个项目对您有帮助，请给一个星标！⭐**

Made with ❤️ by 言律语言项目组

</div>