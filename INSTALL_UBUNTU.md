# Ubuntu 系统安装指南

## 问题诊断

错误信息：
```
ModuleNotFoundError: No module named 'jieba'
```

这表示系统缺少 jieba 包，与 Python 版本无关。

## 解决方案

### 方案1：安装核心依赖（推荐）

在 Ubuntu 系统上执行：

```bash
# 进入项目根目录
cd ~/github/yanlv

# 安装核心依赖
pip3 install jieba typing-extensions

# 或者安装所有依赖
pip3 install -r requirements.txt
```

### 方案2：使用虚拟环境（推荐）

```bash
# 创建虚拟环境
cd ~/github/yanlv
python3 -m venv venv

# 激活虚拟环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 运行服务器
cd playground
python3 server.py
```

### 方案3：用户级安装

```bash
# 安装到用户目录
pip3 install --user jieba typing-extensions
```

## 验证安装

```bash
# 检查 jieba 是否安装成功
python3 -c "import jieba; print('jieba version:', jieba.__version__)"

# 运行测试
cd ~/github/yanlv/src/yanlv/lexer
python3 test_simple.py
```

## Python 版本兼容性

- ✅ Python 3.11 (Ubuntu) - 完全支持
- ✅ Python 3.12 (Windows) - 完全支持
- ✅ Python 3.8+ - 都支持

jieba 支持所有 Python 3.x 版本，版本差异不是问题。

## 常见问题

### Q1: pip3 命令不存在

```bash
# Ubuntu 安装 pip3
sudo apt update
sudo apt install python3-pip
```

### Q2: 权限不足

```bash
# 使用 --user 参数
pip3 install --user jieba

# 或使用 sudo（不推荐）
sudo pip3 install jieba
```

### Q3: 网络问题

```bash
# 使用国内镜像
pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple jieba
```

## 完整安装步骤

```bash
# 1. 进入项目目录
cd ~/github/yanlv

# 2. 检查 Python 版本
python3 --version  # 应该显示 Python 3.11.x

# 3. 安装依赖
pip3 install jieba typing-extensions

# 4. 验证安装
python3 -c "import jieba; print('OK')"

# 5. 运行服务器
cd playground
python3 server.py
```

## 依赖列表

核心依赖（必需）：
- jieba >= 0.42.1
- typing-extensions >= 4.0.0

可选依赖：
- thulac >= 0.2.0 (另一个分词器)

开发依赖：
- pytest, flake8, black, mypy 等
