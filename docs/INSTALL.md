# 言律语言 - 安装指南

## 系统要求

- Python 3.8 或更高版本
- 支持 Windows、Linux、macOS

## 快速安装

### Windows (Python 3.12)

```powershell
# 进入项目目录
cd g:\dumategithub\yanlv

# 安装依赖
pip install -r requirements.txt

# 或只安装核心依赖
pip install jieba typing-extensions
```

### Ubuntu/Linux (Python 3.11)

```bash
# 进入项目目录
cd ~/github/yanlv

# 方法1：使用安装脚本（推荐）
chmod +x setup_ubuntu.sh
./setup_ubuntu.sh

# 方法2：手动安装
pip3 install --user jieba typing-extensions flask flask-cors

# 方法3：使用 requirements.txt
pip3 install --user -r requirements.txt
pip3 install --user -r playground/requirements.txt
```

## 验证安装

### Windows

```powershell
# 测试 jieba
python -c "import jieba; print('jieba OK')"

# 测试词法分析器
cd src\yanlv\lexer
python test_simple.py
```

### Ubuntu/Linux

```bash
# 测试 jieba
python3 -c "import jieba; print('jieba OK')"

# 测试词法分析器
cd src/yanlv/lexer
python3 test_simple.py
```

## 启动 Playground

### Windows

```powershell
cd playground
python server.py
```

访问: http://localhost:5000

### Ubuntu/Linux

```bash
cd playground
python3 server.py
```

访问: http://localhost:5000

## 依赖说明

### 核心依赖（必需）

| 包名 | 版本 | 用途 |
|------|------|------|
| jieba | >= 0.42.1 | 中文分词 |
| typing-extensions | >= 4.0.0 | 类型支持 |

### Playground 依赖

| 包名 | 版本 | 用途 |
|------|------|------|
| flask | >= 2.0.0 | Web 框架 |
| flask-cors | >= 3.0.0 | 跨域支持 |

### 可选依赖

| 包名 | 版本 | 用途 |
|------|------|------|
| thulac | >= 0.2.0 | 另一个分词器 |

## Python 版本兼容性

| Python 版本 | 状态 | 说明 |
|-------------|------|------|
| 3.8 | ✅ | 最低支持版本 |
| 3.9 | ✅ | 完全支持 |
| 3.10 | ✅ | 完全支持 |
| 3.11 | ✅ | Ubuntu 默认，完全支持 |
| 3.12 | ✅ | Windows 测试版本，完全支持 |

**jieba 支持所有 Python 3.6+ 版本，版本差异不是问题！**

## 常见问题

### 1. ModuleNotFoundError: No module named 'jieba'

**原因**: 缺少 jieba 包

**解决**:
```bash
# Ubuntu/Linux
pip3 install --user jieba

# Windows
pip install jieba
```

### 2. pip/pip3 命令不存在

**Ubuntu/Linux**:
```bash
sudo apt update
sudo apt install python3-pip
```

**Windows**: Python 安装时已包含 pip

### 3. 权限不足

**Ubuntu/Linux**:
```bash
# 使用 --user 参数
pip3 install --user jieba
```

**Windows**: 以管理员身份运行 PowerShell

### 4. 网络问题

使用国内镜像：
```bash
# 清华镜像
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple jieba

# 阿里镜像
pip install -i https://mirrors.aliyun.com/pypi/simple jieba
```

## 开发环境设置

### 安装开发依赖

```bash
# Ubuntu/Linux
pip3 install --user -r requirements.txt

# Windows
pip install -r requirements.txt
```

这会安装：
- pytest: 测试框架
- flake8: 代码检查
- black: 代码格式化
- mypy: 类型检查

### 运行测试

```bash
cd src/yanlv/lexer
python3 test_simple.py  # Linux
python test_simple.py   # Windows
```

## 项目结构

```
yanlv/
├── src/yanlv/
│   ├── lexer/          # 词法分析器（模块化）
│   ├── parser/         # 语法分析器
│   ├── semantic/       # 语义分析
│   └── ...
├── playground/         # Web Playground
│   ├── server.py       # 后端服务
│   └── requirements.txt
├── requirements.txt    # 项目依赖
├── setup_ubuntu.sh     # Ubuntu 安装脚本
└── INSTALL.md          # 本文档
```

## 下一步

1. ✅ 安装依赖
2. ✅ 验证安装
3. ✅ 启动 Playground
4. 📖 阅读 API 文档: `src/yanlv/lexer/API_DOCUMENTATION.md`
5. 🎯 开始使用言律语言！

## 获取帮助

- 查看 `QUICK_FIX_UBUNTU.md` - Ubuntu 快速修复
- 查看 `INSTALL_UBUNTU.md` - Ubuntu 详细指南
- 查看 `src/yanlv/lexer/REFACTORING_SUMMARY.md` - 模块化说明
