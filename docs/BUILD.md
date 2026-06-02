# 言律语言打包说明

## ✅ 当前状态

**源码可以编译成可执行文件！**

测试结果：
- ✓ 基本功能测试通过
- ✓ CLI功能测试通过
- ✓ 编译器正常工作

---

## 🚀 快速开始

### 方式1：直接运行（开发模式）

```bash
# 交互模式
python src/yanlv/cli.py 交互

# 编译文件
python src/yanlv/cli.py 编译 hello.yan

# 查看帮助
python src/yanlv/cli.py --help
```

### 方式2：安装后使用

```bash
# 安装（开发模式）
pip install -e .

# 使用
yanlv 交互
yanlv 编译 hello.yan
yanlv --help
```

### 方式3：打包成可执行文件

#### Windows:
```bash
# 运行打包脚本
build_windows.bat

# 生成的文件
dist\yanlv.exe
```

#### Linux/macOS:
```bash
# 添加执行权限
chmod +x build_unix.sh

# 运行打包脚本
./build_unix.sh

# 生成的文件
dist/yanlv
```

---

## 📦 打包选项

### 选项1：Python包（推荐开发者）

```bash
# 安装构建工具
pip install build

# 构建
python -m build

# 生成的文件
dist/yanlv-2.0.0-py3-none-any.whl
dist/yanlv-2.0.0.tar.gz

# 安装
pip install dist/yanlv-2.0.0-py3-none-any.whl
```

### 选项2：PyInstaller可执行文件（推荐普通用户）

**优点：**
- 单文件，无需Python环境
- 跨平台支持
- 简单易用

**Windows打包：**
```bash
pip install pyinstaller
pyinstaller --onefile --name yanlv --console src\yanlv\cli.py
```

**Linux/macOS打包：**
```bash
pip install pyinstaller
pyinstaller --onefile --name yanlv --console src/yanlv/cli.py
```

### 选项3：Nuitka编译（高性能）

```bash
pip install nuitka
python -m nuitka --standalone --onefile src/yanlv/cli.py
```

---

## 🎯 使用示例

### 交互模式

```bash
yanlv 交互
```

```
言律语言交互式解释器 v0.1.0
输入 '退出' 或 'exit' 退出
输入 '帮助' 或 'help' 查看帮助

言律> 输出 "你好世界"
你好世界

言律> 定义变量 x 为 10
言律> 输出 x
10

言律> 退出
再见!
```

### 编译文件

创建 `hello.yan`:
```
# 这是注释
输出 "你好，言律语言！"

定义变量 x 为 10
定义变量 y 为 20
定义变量 z 为 x 加 y

输出 "计算结果："
输出 z
```

运行：
```bash
yanlv 编译 hello.yan
yanlv 运行 hello.yan
```

---

## 📊 打包大小

| 方式 | 大小 | 说明 |
|------|------|------|
| Python包 | ~100KB | 需要Python环境 |
| PyInstaller | ~15-20MB | 包含Python运行时 |
| Nuitka | ~10-15MB | 编译成机器码 |

---

## 🔧 系统要求

### 运行要求：
- Python 3.8+
- jieba >= 0.42.1

### 打包要求：
- PyInstaller 或 Nuitka
- 各平台对应的编译器（C/C++轨需要）

---

## 📝 完整打包流程

### 1. 测试系统
```bash
python test_system.py
```

### 2. 构建Python包
```bash
pip install build
python -m build
```

### 3. 打包可执行文件

**Windows:**
```bash
build_windows.bat
```

**Linux/macOS:**
```bash
./build_unix.sh
```

### 4. 测试可执行文件

**Windows:**
```bash
dist\yanlv.exe 交互
```

**Linux/macOS:**
```bash
./dist/yanlv 交互
```

---

## 🎉 总结

**当前源码完全支持编译成可执行文件！**

推荐方案：
- **开发者** → 使用 `pip install -e .`
- **普通用户** → 下载打包好的exe/二进制文件
- **分发** → 使用PyInstaller打包各平台版本

立即开始：
```bash
# 测试
python test_system.py

# 使用
python src/yanlv/cli.py 交互

# 打包
build_windows.bat  # Windows
./build_unix.sh    # Linux/macOS
```
