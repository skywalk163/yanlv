# 言律语言 (Yanlv Language)

中文编程语言，让编程更自然、更易学。

## 项目结构

```
yanlv/
├── .github/              # GitHub配置
│   └── workflows/        # CI/CD工作流
├── deploy/               # 部署相关文件
├── docs/                 # 项目文档
│   ├── BUILD.md          # 构建文档
│   ├── PYTHON_STDLIB_COMPLETE_SUMMARY.md  # Python标准库实现总结
│   └── ...               # 其他文档
├── examples/             # 示例代码
│   ├── hello.yan         # Hello World示例
│   ├── quick_start.yan   # 快速开始示例
│   └── simple.yan        # 简单示例
├── libraries/            # 外部库
├── online-ide/           # 在线IDE
├── playground/           # 在线体验平台
│   ├── index.html        # 主页
│   ├── builtins.html     # 内置函数学习页
│   └── stdlib.html       # 标准库学习页
├── racket/               # Racket相关实现
├── src/                  # 源代码
│   └── yanlv/            # 言律语言核心
│       ├── builtins_ext.py      # 内置函数扩展
│       └── stdlib/              # 标准库扩展
│           ├── collections_ext.py
│           ├── itertools_ext.py
│           ├── functools_ext.py
│           ├── pathlib_ext.py
│           ├── datetime_ext.py
│           ├── math_ext.py
│           ├── json_ext.py
│           ├── random_ext.py
│           ├── re_ext.py
│           ├── statistics_ext.py
│           ├── string_ext.py
│           ├── typing_ext.py
│           ├── dataclasses_ext.py
│           ├── enum_ext.py
│           ├── csv_ext.py
│           ├── hashlib_ext.py
│           ├── contextlib_ext.py
│           ├── textwrap_ext.py
│           ├── pprint_ext.py
│           ├── pickle_ext.py
│           ├── copy_ext.py
│           ├── glob_ext.py
│           ├── operator_ext.py
│           ├── tempfile_ext.py
│           ├── shutil_ext.py
│           ├── bisect_ext.py
│           └── heapq_ext.py
├── stdlib/               # 标准库（旧版）
├── tests/                # 测试代码
│   ├── test_builtins_ext.py
│   └── ...               # 其他测试
├── tools/                # 工具脚本
├── vscode-yanlv/         # VSCode插件
├── website/              # 官方网站
├── .gitignore            # Git忽略配置
├── build_unix.sh         # Unix构建脚本
├── build_windows.bat     # Windows构建脚本
├── install.sh            # 安装脚本
├── pyproject.toml        # Python项目配置
├── pytest.ini            # Pytest配置
├── run_yanlv.bat         # Windows运行脚本
└── setup_ubuntu.sh       # Ubuntu安装脚本
```

## 快速开始

### 安装

```bash
# 克隆仓库
git clone https://github.com/yourusername/yanlv.git
cd yanlv

# 安装依赖
pip install -e .
```

### 运行

```bash
# Windows
run_yanlv.bat

# Linux/Mac
python -m yanlv
```

### 示例代码

```yanlv
输出 "你好，言律语言！"
定义 变量 x 为 10
输出 x
```

## 标准库

言律语言提供了完整的Python 3.12标准库中文版本，包括：

### 核心模块（8个）
- collections_ext - 高级数据结构
- itertools_ext - 迭代器工具
- functools_ext - 函数式编程
- pathlib_ext - 路径操作
- datetime_ext - 日期时间
- math_ext - 数学函数
- json_ext - JSON处理
- random_ext - 随机数生成

### 重要模块（8个）
- re_ext - 正则表达式
- statistics_ext - 统计函数
- string_ext - 字符串工具
- typing_ext - 类型提示
- dataclasses_ext - 数据类
- enum_ext - 枚举类型
- csv_ext - CSV处理
- hashlib_ext - 哈希算法

### 实用模块（11个）
- contextlib_ext - 上下文管理器
- textwrap_ext - 文本格式化
- pprint_ext - 美化打印
- pickle_ext - 对象序列化
- copy_ext - 对象复制
- glob_ext - 文件模式匹配
- operator_ext - 操作符函数
- tempfile_ext - 临时文件
- shutil_ext - 高级文件操作
- bisect_ext - 二分查找
- heapq_ext - 堆队列

## 文档

详细文档请查看 [docs](./docs/) 目录。

## 在线体验

访问 [Playground](./playground/) 在线体验言律语言。

## 开发

### 运行测试

```bash
pytest tests/
```

### 构建文档

```bash
cd docs
# 构建文档
```

## 贡献

欢迎贡献代码！请查看 [贡献指南](./docs/CONTRIBUTING.md)。

## 许可证

MIT License

## 联系方式

- GitHub: [yanlv](https://github.com/yourusername/yanlv)
- 文档: [docs](./docs/)
- 问题反馈: [Issues](https://github.com/yourusername/yanlv/issues)
