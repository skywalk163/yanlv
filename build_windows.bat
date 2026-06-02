@echo off
chcp 65001 >nul
echo ========================================
echo 言律语言 Windows 打包脚本
echo ========================================

echo.
echo [1/5] 检查Python环境
python --version
if errorlevel 1 (
    echo 错误：未找到Python，请先安装Python 3.8+
    pause
    exit /b 1
)

echo.
echo [2/5] 清理旧文件
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist *.spec del *.spec

echo.
echo [3/5] 安装依赖
echo 安装项目依赖...
pip install -e . --quiet
if errorlevel 1 (
    echo 警告：项目依赖安装失败，继续尝试...
)

echo 安装PyInstaller...
pip install pyinstaller --quiet
if errorlevel 1 (
    echo 错误：PyInstaller安装失败
    pause
    exit /b 1
)

echo.
echo [4/5] 构建可执行文件
echo 这可能需要几分钟时间...
pyinstaller --onefile ^
    --name yanlv ^
    --console ^
    --clean ^
    --noconfirm ^
    --hidden-import jieba ^
    --hidden-import yanlv.compiler ^
    --hidden-import yanlv.lexer.lexer_modular ^
    --hidden-import yanlv.interpreter_complete ^
    --hidden-import yanlv.advanced_interpreter ^
    --hidden-import yanlv.semantic.context_tracker ^
    --hidden-import yanlv.semantic.ambiguity_resolver ^
    --hidden-import yanlv.interop ^
    --hidden-import yanlv.interop.python_track ^
    --hidden-import yanlv.interop.javascript_track ^
    --hidden-import yanlv.interop.sql_track ^
    --hidden-import yanlv.interop.c_track ^
    --hidden-import yanlv.interop.cpp_track ^
    --collect-all jieba ^
    src\yanlv\cli.py

if errorlevel 1 (
    echo 错误：构建失败
    pause
    exit /b 1
)

echo.
echo [5/5] 测试可执行文件
if exist dist\yanlv.exe (
    echo 测试运行...
    dist\yanlv.exe --help
    echo.
    echo ========================================
    echo 打包成功！
    echo ========================================
    echo.
    echo 可执行文件位置: dist\yanlv.exe
    echo 文件大小:
    for %%A in (dist\yanlv.exe) do echo   %%~zA 字节 (约 %%~zAKB)
    echo.
    echo 使用方法:
    echo   dist\yanlv.exe --help        查看帮助
    echo   dist\yanlv.exe 交互          进入交互模式
    echo   dist\yanlv.exe 编译 文件.yan  编译文件
    echo   dist\yanlv.exe 运行 文件.yan  运行文件
    echo.
) else (
    echo 错误：未找到生成的可执行文件
    pause
    exit /b 1
)

pause
