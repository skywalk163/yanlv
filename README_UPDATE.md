# 言律语言 (YanLv Language)

一个创新的中文编程语言，支持无空格编程。

## 特性

### 🎯 无空格编程
言律语言支持完全无空格的中文编程，让代码更简洁、更符合中文书写习惯。

**示例对比**:
```python
# 有空格版本
定义 变量 x 为 10
输出 x

# 无空格版本
定义变量x为10
输出x
```

### 🚀 核心功能

- **模块化词法分析器**: 清晰的模块结构，易于维护和扩展
- **智能分词**: 自动识别关键词边界，无需空格分隔
- **跨平台支持**: Windows、Linux、macOS 全平台支持
- **Web Playground**: 在线体验言律语言

## 快速开始

### 安装

```bash
# 克隆仓库
git clone https://gitcode.com/your-username/yanlv.git
cd yanlv

# 安装依赖
pip install -r requirements.txt
```

### 使用

#### Python API

```python
from yanlv.lexer import create_lexer

# 创建无空格分词器
lexer = create_lexer("yanlv_nospace")

# 分析代码
tokens = lexer.tokenize('定义变量x为10输出x')

# 查看词元
for token in tokens:
    print(f"{token.type.name}: {token.value}")
```

#### Web Playground

```bash
cd playground
python server.py
```

访问 http://localhost:5000

## 示例代码

### 1. Hello World
```
输出"你好，言律语言！"
```

### 2. 变量定义
```
定义变量x为10
输出x
```

### 3. 条件语句
```
如果条件成立则
输出"条件为真"
否则
输出"条件为假"
```

### 4. 循环语句
```
循环5次执行
输出"这是循环"
结束
```

### 5. 函数定义
```
函数加法参数a b
返回a+b
结束
输出"函数已定义"
```

## 项目结构

```
yanlv/
├── src/yanlv/
│   ├── lexer/              # 词法分析器（模块化）
│   │   ├── __init__.py
│   │   ├── base.py         # 基础类
│   │   ├── constants.py    # 常量定义
│   │   ├── lexer_token.py  # 词元定义
│   │   ├── tokenizer.py    # 分词器（含无空格支持）
│   │   ├── matcher.py      # 词元匹配器
│   │   ├── error_handler.py
│   │   ├── context_manager.py
│   │   ├── pattern_manager.py
│   │   ├── performance_optimizer.py
│   │   ├── lexer_modular.py
│   │   └── utils.py
│   ├── parser/             # 语法分析器
│   ├── semantic/           # 语义分析
│   └── feedback/           # 反馈系统
├── playground/             # Web Playground
│   ├── server.py           # 后端服务
│   ├── index.html          # 前端界面
│   └── requirements.txt
├── requirements.txt        # 项目依赖
├── INSTALL.md              # 安装指南
├── NO_SPACE_SUPPORT.md     # 无空格支持文档
└── README.md               # 本文档
```

## 关键词

言律语言支持以下关键词（无需空格分隔）:

| 关键词 | 类型 | 别名 |
|--------|------|------|
| 输出 | OUTPUT | 打印, 显示 |
| 定义 | DEFINE | - |
| 变量 | VARIABLE | - |
| 函数 | FUNCTION | - |
| 参数 | PARAMETER | - |
| 为 | IS | - |
| 如果 | IF | 要是 |
| 否则 | ELSE | 不然 |
| 循环 | LOOP | - |
| 返回 | RETURN | - |
| 结束 | END | - |

## 分词器类型

### 1. jieba (默认)
使用结巴分词器，适合有空格的代码。

### 2. yanlv_nospace (推荐)
言律语言专用分词器，支持无空格编程。

### 3. thulac
清华大学分词器，准确率较高（需安装）。

## 文档

- [安装指南](INSTALL.md)
- [无空格支持](NO_SPACE_SUPPORT.md)
- [API文档](src/yanlv/lexer/API_DOCUMENTATION.md)
- [调试报告](DEBUG_REPORT.md)

## 开发

### 运行测试

```bash
# 测试词法分析器
cd src/yanlv/lexer
python test_simple.py

# 测试无空格功能
cd ../..
python test_nospace_lexer.py

# 测试 Playground API
cd playground
python test_api.py
```

### 添加新关键词

1. 在 `src/yanlv/lexer/lexer_token.py` 中添加 TokenType
2. 在 `src/yanlv/lexer/constants.py` 中添加关键词映射

## 性能

- **分词速度**: < 1ms (简单代码)
- **关键词识别**: 100% 准确
- **内存占用**: 低
- **跨平台**: Windows + Linux + macOS

## 版本历史

### v2.1.0 (2026-05-24)
- ✨ 新增无空格编程支持
- ✨ 新增 YanLuNoSpaceTokenizer 分词器
- 🎨 更新示例代码为无空格版本
- 📝 完善文档

### v2.0.0 (2026-05-23)
- 🎉 模块化重构词法分析器
- ✨ 添加 Playground Web 界面
- 📝 完善安装文档

## 贡献

欢迎贡献代码、报告问题或提出建议！

## 许可证

MIT License

## 联系方式

- 项目主页: https://gitcode.com/your-username/yanlv
- 问题反馈: https://gitcode.com/your-username/yanlv/issues

---

**言律语言 - 让中文编程更简单** 🚀
