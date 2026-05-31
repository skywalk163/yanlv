# Ubuntu 快速修复指南

## 问题
```
ModuleNotFoundError: No module named 'jieba'
```

## 原因
Ubuntu 系统缺少 jieba 依赖包（与 Python 3.11/3.12 版本无关）

## 快速解决方案

### 方法1：一键安装（推荐）

```bash
cd ~/github/yanlv
chmod +x setup_ubuntu.sh
./setup_ubuntu.sh
```

### 方法2：手动安装核心依赖

```bash
# 安装 jieba 和 typing-extensions
pip3 install --user jieba typing-extensions

# 安装 Flask（playground 需要）
pip3 install --user flask flask-cors
```

### 方法3：使用 requirements.txt

```bash
# 安装核心依赖
pip3 install --user -r requirements.txt

# 安装 playground 依赖
pip3 install --user -r playground/requirements.txt
```

## 验证安装

```bash
# 测试 jieba
python3 -c "import jieba; print('jieba OK')"

# 测试言律语言模块
cd ~/github/yanlv
python3 -c "import sys; sys.path.insert(0, 'src'); from yanlv.lexer import create_lexer; print('Lexer OK')"
```

## 启动服务器

```bash
cd ~/github/yanlv/playground
python3 server.py
```

## Python 版本说明

- ✅ Python 3.11 (Ubuntu) - 完全支持
- ✅ Python 3.12 (Windows) - 完全支持
- ✅ jieba 支持所有 Python 3.6+ 版本

**版本差异不是问题，只需安装依赖即可！**

## 常见问题

### Q: pip3 命令不存在
```bash
sudo apt update
sudo apt install python3-pip
```

### Q: 权限不足
```bash
# 使用 --user 参数安装到用户目录
pip3 install --user jieba
```

### Q: 网络慢
```bash
# 使用清华镜像
pip3 install --user -i https://pypi.tuna.tsinghua.edu.cn/simple jieba
```

## 完整依赖列表

核心依赖：
- jieba >= 0.42.1
- typing-extensions >= 4.0.0

Playground 依赖：
- flask >= 2.0.0
- flask-cors >= 3.0.0

## 安装后测试

```bash
# 运行测试脚本
cd ~/github/yanlv/src/yanlv/lexer
python3 test_simple.py
```

应该看到：
```
============================================================
所有测试通过！
============================================================
```
