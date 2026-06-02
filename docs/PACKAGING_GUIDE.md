# 言律语言打包和分发指南

## 一、当前状态

### ✅ 已有配置

1. **pyproject.toml** - 现代Python打包配置
   - 支持pip安装
   - 定义了CLI入口点：`yanlv = "yanlv.cli:main"`
   - 包含所有依赖

2. **CLI接口** - `src/yanlv/cli.py`
   - 支持编译、运行、交互模式
   - 完整的命令行参数解析

### ❌ 缺少的功能

- 可执行文件打包（exe/二进制）
- 跨平台分发
- 安装包制作

---

## 二、打包方案

### 方案1：Python包分发（推荐）

**优点：**
- 跨平台支持
- 安装简单
- 依赖自动管理

**步骤：**

```bash
# 1. 构建包
python -m build

# 2. 上传到PyPI（可选）
twine upload dist/*

# 3. 用户安装
pip install yanlv

# 4. 使用
yanlv 编译 hello.yan
yanlv 运行 hello.yan
yanlv 交互
```

**生成的文件：**
- `dist/yanlv-2.0.0-py3-none-any.whl` (wheel包)
- `dist/yanlv-2.0.0.tar.gz` (源码包)

---

### 方案2：PyInstaller可执行文件

**优点：**
- 单文件可执行
- 无需Python环境
- 适合非技术用户

**步骤：**

#### 2.1 安装PyInstaller

```bash
pip install pyinstaller
```

#### 2.2 创建spec文件

创建 `yanlv.spec`:

```python
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['src/yanlv/cli.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('src/yanlv/lexer/*.py', 'yanlv/lexer'),
        ('src/yanlv/semantic/*.py', 'yanlv/semantic'),
        ('src/yanlv/interop/*.py', 'yanlv/interop'),
    ],
    hiddenimports=[
        'yanlv.compiler',
        'yanlv.lexer.lexer_modular',
        'yanlv.interpreter_complete',
        'yanlv.advanced_interpreter',
        'yanlv.semantic.context_tracker',
        'yanlv.semantic.ambiguity_resolver',
        'yanlv.interop',
        'jieba',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='yanlv',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='docs/images/yanlv.ico',  # 如果有图标
)
```

#### 2.3 构建可执行文件

```bash
# Windows
pyinstaller yanlv.spec

# Linux/macOS
pyinstaller yanlv.spec
```

**生成的文件：**
- Windows: `dist/yanlv.exe`
- Linux: `dist/yanlv`
- macOS: `dist/yanlv`

---

### 方案3：Nuitka编译（高性能）

**优点：**
- 编译成真正的机器码
- 性能更好
- 更难反编译

**步骤：**

```bash
# 1. 安装Nuitka
pip install nuitka

# 2. 编译
python -m nuitka \
    --standalone \
    --onefile \
    --enable-plugin=tk-inter \
    --include-data-dir=src/yanlv/lexer=yanlv/lexer \
    --include-data-dir=src/yanlv/semantic=yanlv/semantic \
    --include-data-dir=src/yanlv/interop=yanlv/interop \
    --output-filename=yanlv \
    src/yanlv/cli.py
```

---

## 三、完整打包脚本

### 3.1 Windows打包脚本

创建 `build_windows.bat`:

```batch
@echo off
echo ========================================
echo 言律语言 Windows 打包脚本
echo ========================================

echo.
echo [1/4] 清理旧文件
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist *.spec del *.spec

echo.
echo [2/4] 安装依赖
pip install -e .
pip install pyinstaller

echo.
echo [3/4] 构建可执行文件
pyinstaller --onefile ^
    --name yanlv ^
    --console ^
    --add-data "src/yanlv/lexer;yanlv/lexer" ^
    --add-data "src/yanlv/semantic;yanlv/semantic" ^
    --add-data "src/yanlv/interop;yanlv/interop" ^
    --hidden-import jieba ^
    --hidden-import yanlv.compiler ^
    --hidden-import yanlv.lexer.lexer_modular ^
    --hidden-import yanlv.interpreter_complete ^
    --hidden-import yanlv.advanced_interpreter ^
    src/yanlv/cli.py

echo.
echo [4/4] 测试可执行文件
dist\yanlv.exe --help

echo.
echo ========================================
echo 打包完成！
echo 可执行文件: dist\yanlv.exe
echo ========================================
pause
```

### 3.2 Linux/macOS打包脚本

创建 `build_unix.sh`:

```bash
#!/bin/bash

echo "========================================"
echo "言律语言 Unix 打包脚本"
echo "========================================"

echo
echo "[1/4] 清理旧文件"
rm -rf build dist *.spec

echo
echo "[2/4] 安装依赖"
pip install -e .
pip install pyinstaller

echo
echo "[3/4] 构建可执行文件"
pyinstaller --onefile \
    --name yanlv \
    --console \
    --add-data "src/yanlv/lexer:yanlv/lexer" \
    --add-data "src/yanlv/semantic:yanlv/semantic" \
    --add-data "src/yanlv/interop:yanlv/interop" \
    --hidden-import jieba \
    --hidden-import yanlv.compiler \
    --hidden-import yanlv.lexer.lexer_modular \
    --hidden-import yanlv.interpreter_complete \
    --hidden-import yanlv.advanced_interpreter \
    src/yanlv/cli.py

echo
echo "[4/4] 测试可执行文件"
./dist/yanlv --help

echo
echo "========================================"
echo "打包完成！"
echo "可执行文件: dist/yanlv"
echo "========================================"
```

---

## 四、分发渠道

### 4.1 PyPI（Python包索引）

```bash
# 构建
python -m build

# 上传到TestPyPI（测试）
twine upload --repository testpypi dist/*

# 上传到PyPI（正式）
twine upload dist/*
```

用户安装：
```bash
pip install yanlv
```

### 4.2 GitHub Releases

1. 构建各平台可执行文件
2. 创建GitHub Release
3. 上传文件：
   - `yanlv-windows-x64.exe`
   - `yanlv-linux-x64`
   - `yanlv-macos-x64`

### 4.3 包管理器

**Homebrew (macOS):**
```ruby
class Yanlv < Formula
  desc "言律语言 - 中文编程语言"
  homepage "https://github.com/yanlv/yanlv"
  url "https://github.com/yanlv/yanlv/archive/v2.0.0.tar.gz"
  sha256 "..."

  depends_on "python@3.11"

  def install
    system "pip", "install", *std_pip_args, "."
  end
end
```

**Scoop (Windows):**
```json
{
    "version": "2.0.0",
    "url": "https://github.com/yanlv/yanlv/releases/download/v2.0.0/yanlv-windows-x64.exe",
    "bin": "yanlv.exe"
}
```

---

## 五、快速开始

### 立即可用的方式

**方式1：开发模式安装**
```bash
cd yanlv
pip install -e .
yanlv 交互
```

**方式2：直接运行**
```bash
python src/yanlv/cli.py 交互
```

**方式3：构建可执行文件**
```bash
pip install pyinstaller
pyinstaller --onefile src/yanlv/cli.py
./dist/cli  # Linux/macOS
dist\cli.exe  # Windows
```

---

## 六、推荐方案

### 对于开发者
✅ **使用方案1（Python包）**
- `pip install -e .` 开发模式
- `pip install yanlv` 正式安装

### 对于普通用户
✅ **使用方案2（PyInstaller）**
- 下载对应平台的可执行文件
- 无需安装Python
- 双击运行

### 对于高性能需求
✅ **使用方案3（Nuitka）**
- 编译成机器码
- 性能最优

---

## 七、下一步行动

### 立即可做：

1. **测试当前安装**
```bash
pip install -e .
yanlv --help
yanlv 交互
```

2. **构建Python包**
```bash
python -m build
```

3. **创建可执行文件**
```bash
pip install pyinstaller
pyinstaller --onefile src/yanlv/cli.py
```

### 需要添加：

1. ✅ 构建脚本（已提供）
2. ⬜ CI/CD自动化构建
3. ⬜ GitHub Actions配置
4. ⬜ 版本发布流程

---

**总结：当前源码可以编译成可执行文件！推荐使用PyInstaller快速打包。**
