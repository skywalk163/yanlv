#!/bin/bash

echo "========================================"
echo "言律语言 Unix 打包脚本"
echo "========================================"

echo
echo "[1/5] 检查Python环境"
if ! command -v python3 &> /dev/null; then
    echo "错误：未找到Python，请先安装Python 3.8+"
    exit 1
fi
python3 --version

echo
echo "[2/5] 清理旧文件"
rm -rf build dist *.spec

echo
echo "[3/5] 安装依赖"
echo "安装项目依赖..."
pip3 install -e . --quiet 2>/dev/null || echo "警告：项目依赖安装失败，继续尝试..."

echo "安装PyInstaller..."
pip3 install pyinstaller --quiet 2>/dev/null || {
    echo "错误：PyInstaller安装失败"
    exit 1
}

echo
echo "[4/5] 构建可执行文件"
echo "这可能需要几分钟时间..."

# 检测操作系统
OS="$(uname -s)"
case "$OS" in
    Linux*)
        PLATFORM="linux"
        ;;
    Darwin*)
        PLATFORM="macos"
        ;;
    *)
        echo "未知平台: $OS"
        PLATFORM="unknown"
        ;;
esac

pyinstaller --onefile \
    --name yanlv \
    --console \
    --clean \
    --noconfirm \
    --hidden-import jieba \
    --hidden-import yanlv.compiler \
    --hidden-import yanlv.lexer.lexer_modular \
    --hidden-import yanlv.interpreter_complete \
    --hidden-import yanlv.advanced_interpreter \
    --hidden-import yanlv.semantic.context_tracker \
    --hidden-import yanlv.semantic.ambiguity_resolver \
    --hidden-import yanlv.interop \
    --hidden-import yanlv.interop.python_track \
    --hidden-import yanlv.interop.javascript_track \
    --hidden-import yanlv.interop.sql_track \
    --hidden-import yanlv.interop.c_track \
    --hidden-import yanlv.interop.cpp_track \
    --collect-all jieba \
    src/yanlv/cli.py

if [ $? -ne 0 ]; then
    echo "错误：构建失败"
    exit 1
fi

echo
echo "[5/5] 测试可执行文件"
if [ -f "dist/yanlv" ]; then
    echo "测试运行..."
    chmod +x dist/yanlv
    ./dist/yanlv --help

    echo
    echo "========================================"
    echo "打包成功！"
    echo "========================================"
    echo
    echo "可执行文件位置: dist/yanlv"
    echo "文件大小: $(du -h dist/yanlv | cut -f1)"
    echo "平台: $PLATFORM"
    echo
    echo "使用方法:"
    echo "  ./dist/yanlv --help        查看帮助"
    echo "  ./dist/yanlv 交互          进入交互模式"
    echo "  ./dist/yanlv 编译 文件.yan  编译文件"
    echo "  ./dist/yanlv 运行 文件.yan  运行文件"
    echo

    # 创建平台特定的副本
    cp dist/yanlv "dist/yanlv-$PLATFORM-x64"
    echo "已创建: dist/yanlv-$PLATFORM-x64"
else
    echo "错误：未找到生成的可执行文件"
    exit 1
fi
