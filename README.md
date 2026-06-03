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
│   ├── stdlib.html       # 标准库学习页
│   ├── server.py         # Web 服务器
│   └── requirements.txt  # Playground 依赖
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

### 新手入门三步走

**第一步：安装**
```bash
# 克隆仓库
git clone https://github.com/yourusername/yanlv.git
cd yanlv

# 安装依赖
pip install -e .
```

**第二步：运行示例**
```powershell
# Windows PowerShell（推荐）
python -m yanlv 运行 examples\hello.yan

# Linux/Mac
python -m yanlv 运行 examples/hello.yan
```

**第三步：启动 Playground（可选）**
```bash
cd playground
pip install -r requirements.txt  # 安装 Playground 依赖
python server.py
# 然后在浏览器打开 http://localhost:5000
```

### 安装

```bash
# 克隆仓库
git clone https://github.com/skywalk163/yanlv.git
cd yanlv

# 安装依赖
pip install -e .
```

### 运行

#### Windows 系统

**推荐方式：使用 PowerShell 直接运行**
```powershell
# 设置 UTF-8 编码（如果遇到中文显示问题）
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# 运行示例文件
python -m yanlv 运行 examples\hello.yan
```

**使用批处理文件**
```powershell
# 注意：批处理文件可能存在中文编码问题
.\run_yanlv.bat examples\hello.yan
```

> **注意**：Windows 批处理文件（.bat）在处理中文字符时可能存在编码问题。如果遇到 `'p' is not recognized` 等错误，请使用 PowerShell 直接运行的方式。

#### Linux/Mac 系统

```bash
python -m yanlv 运行 examples/hello.yan
```

#### 交互模式

```bash
python -m yanlv 交互
```

### 示例代码

```yanlv
输出 "你好，言律语言！"
定义 变量 x 为 10
输出 x
```

### 查看所有可用命令

```bash
# 查看帮助信息
python -m yanlv 帮助

# 查看可用命令
python -m yanlv --help
```

言律语言支持以下命令：
- `运行` - 运行指定的 .yan 文件
- `编译` - 编译代码（如果支持）
- `交互` - 启动交互式 REPL 环境
- `帮助` - 显示帮助信息

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

## 常见问题

### Windows 下批处理文件运行失败

**问题现象**：
```
'p' is not recognized as an internal or external command
'o' is not recognized as an internal or external command
```

**原因**：Windows 批处理文件（.bat）在处理中文字符时存在编码问题，导致命令无法正确解析。

**解决方案**：
使用 PowerShell 直接运行，而不是使用批处理文件：
```powershell
# 设置 UTF-8 编码
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# 运行程序
python -m yanlv 运行 examples\hello.yan
```

### 中文显示乱码

如果遇到中文显示乱码，请在 PowerShell 中设置编码：
```powershell
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$PSDefaultParameterValues['*:Encoding'] = 'utf8'
```

### Playground 无法启动

**问题现象 1：缺少依赖模块**
```
ModuleNotFoundError: No module named 'flask_cors'
```

**解决方案**：
安装 Playground 所需的依赖：
```bash
cd playground
pip install -r requirements.txt

# 或者手动安装
pip install flask flask-cors jieba
```

**问题现象 2：无法连接**
```
curl: (7) Failed to connect to 127.0.0.1 port 5000
```

**解决方案**：
1. 检查端口是否被占用：
   ```powershell
   # Windows
   netstat -ano | findstr :5000
   
   # Linux/Mac
   lsof -i :5000
   ```

2. 如果端口被占用，停止占用进程或修改 `playground/server.py` 中的端口号

3. 确保已安装所需依赖：
   ```bash
   pip install flask flask-cors jieba
   ```

4. 启动后等待 2-3 秒再访问，服务需要初始化时间

## 文档

详细文档请查看 [docs](./docs/) 目录。

## 在线体验

### Playground Web 界面

Playground 提供了一个 Web 界面，可以在浏览器中交互式地编写和运行言律语言代码。

#### 启动 Playground

**重要：安装 Playground 依赖**

在启动 Playground 之前，需要先安装所需的依赖包：

```bash
# 进入 playground 目录
cd playground

# 安装 Playground 依赖
pip install -r requirements.txt

# 或者手动安装依赖
pip install flask flask-cors jieba
```

**Windows 系统：**
```powershell
# 方式1：使用批处理脚本（推荐）
.\start_server.bat

# 方式2：直接启动
python server.py
```

**Linux/Mac 系统：**
```bash
# 启动服务器
python server.py
```

#### 访问 Playground

启动服务器后，在浏览器中打开：
- **主页**：http://localhost:5000
- **内置函数学习**：http://localhost:5000/builtins.html
- **标准库学习**：http://localhost:5000/stdlib.html
- **示例代码**：http://localhost:5000/examples.html

#### Playground 功能

1. **代码编辑器**：编写言律语言代码
2. **运行代码**：点击"运行"按钮执行代码
3. **查看结果**：在右侧查看输出结果
4. **快速示例**：选择预设示例快速学习
5. **执行统计**：查看词元数量、执行时间等信息

#### 示例操作

在 Playground 中输入以下代码并点击"运行"：

```yanlv
输出 "你好，言律语言！"
定义 变量 x 为 10
输出 x
```

### 命令行交互环境 (REPL)

除了 Web 界面，还可以使用命令行交互环境：

```bash
# 启动交互环境
python -m yanlv 交互

# 或使用 REPL 模块
python -m yanlv.repl
```

**REPL 常用命令：**
- `帮助` - 显示帮助信息
- `退出` 或 `exit` - 退出交互环境
- `清空` 或 `clear` - 清空屏幕
- `变量` 或 `vars` - 显示所有变量

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

- GitHub: [yanlv](https://github.com/skywalk163/yanlv)
- 文档: [docs](./docs/)
- 问题反馈: [Issues](https://github.com/skywalk163/yanlv/issues)
