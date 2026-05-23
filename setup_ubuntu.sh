#!/bin/bash
# 言律语言 - Ubuntu 完整安装脚本

set -e  # 遇到错误立即退出

echo "======================================"
echo "言律语言 - Ubuntu 安装脚本"
echo "======================================"
echo ""

# 获取脚本所在目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# 1. 检查 Python 版本
echo "[1/5] 检查 Python 版本..."
PYTHON_VERSION=$(python3 --version 2>&1)
echo "    $PYTHON_VERSION"

if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到 python3"
    echo "请安装 Python 3: sudo apt install python3"
    exit 1
fi
echo ""

# 2. 检查并安装 pip3
echo "[2/5] 检查 pip3..."
if ! command -v pip3 &> /dev/null; then
    echo "    未找到 pip3，正在安装..."
    sudo apt update
    sudo apt install -y python3-pip
fi
PIP_VERSION=$(pip3 --version 2>&1)
echo "    $PIP_VERSION"
echo ""

# 3. 安装核心依赖
echo "[3/5] 安装核心依赖..."
echo "    安装 jieba 和 typing-extensions..."
pip3 install --user jieba typing-extensions 2>&1 | grep -E "(Successfully|Requirement already|Installing)" || true
echo ""

# 4. 安装 playground 依赖
echo "[4/5] 安装 Playground 依赖..."
if [ -f "playground/requirements.txt" ]; then
    echo "    安装 Flask 和相关依赖..."
    pip3 install --user -r playground/requirements.txt 2>&1 | grep -E "(Successfully|Requirement already|Installing)" || true
else
    echo "    安装 Flask..."
    pip3 install --user flask flask-cors 2>&1 | grep -E "(Successfully|Requirement already|Installing)" || true
fi
echo ""

# 5. 验证安装
echo "[5/5] 验证安装..."
echo ""

# 验证核心模块
echo "    验证核心模块..."
python3 -c "import jieba; print('    ✓ jieba', jieba.__version__)" 2>&1
python3 -c "import typing_extensions; print('    ✓ typing-extensions')" 2>&1

# 验证 Flask
echo ""
echo "    验证 Web 框架..."
python3 -c "import flask; print('    ✓ Flask', flask.__version__)" 2>&1
python3 -c "import flask_cors; print('    ✓ Flask-CORS')" 2>&1

# 验证言律语言模块
echo ""
echo "    验证言律语言模块..."
python3 << 'EOF'
import sys
import os
sys.path.insert(0, os.path.join(os.getcwd(), 'src'))
try:
    from yanlv.lexer import create_lexer, TokenType
    lexer = create_lexer()
    tokens = lexer.tokenize("定义 x 为 整数")
    print(f"    ✓ 言律语言词法分析器 (测试通过，生成 {len(tokens)} 个词元)")
except Exception as e:
    print(f"    ✗ 言律语言模块导入失败: {e}")
    sys.exit(1)
EOF

if [ $? -ne 0 ]; then
    echo ""
    echo "======================================"
    echo "安装完成，但模块验证失败"
    echo "======================================"
    exit 1
fi

echo ""
echo "======================================"
echo "✓ 安装成功！"
echo "======================================"
echo ""
echo "下一步操作："
echo "  cd playground"
echo "  python3 server.py"
echo ""
echo "访问: http://localhost:5000"
