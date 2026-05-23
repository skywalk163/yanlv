#!/bin/bash
# 言律语言词法分析器 - Ubuntu 安装脚本

echo "======================================"
echo "言律语言词法分析器 - 安装脚本"
echo "======================================"
echo ""

# 检查 Python 版本
echo "[1/4] 检查 Python 版本..."
python3 --version
if [ $? -ne 0 ]; then
    echo "错误: 未找到 python3"
    echo "请安装 Python 3: sudo apt install python3"
    exit 1
fi
echo ""

# 检查 pip3
echo "[2/4] 检查 pip3..."
if ! command -v pip3 &> /dev/null; then
    echo "未找到 pip3，正在安装..."
    sudo apt update
    sudo apt install -y python3-pip
fi
pip3 --version
echo ""

# 安装核心依赖
echo "[3/4] 安装核心依赖..."
pip3 install jieba typing-extensions
if [ $? -ne 0 ]; then
    echo "错误: 依赖安装失败"
    echo "尝试使用 --user 参数..."
    pip3 install --user jieba typing-extensions
fi
echo ""

# 验证安装
echo "[4/4] 验证安装..."
python3 -c "import jieba; print('✓ jieba 安装成功')"
python3 -c "import typing_extensions; print('✓ typing-extensions 安装成功')"
echo ""

echo "======================================"
echo "安装完成！"
echo "======================================"
echo ""
echo "下一步："
echo "  cd playground"
echo "  python3 server.py"
