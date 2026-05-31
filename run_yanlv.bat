@echo off
echo ========================================
echo 言律语言 Racket 实现版
echo ========================================
echo.

if "%1"=="" (
    echo 用法: run_yanlv.bat 文件名.yan
    echo.
    echo 示例:
    echo   run_yanlv.bat quick_start.yan
    echo   run_yanlv.bat test_advanced.yan
    echo.
    echo 可用文件:
    echo   - quick_start.yan      快速开始示例
    echo   - test_advanced.yan    高级语法测试
    echo   - test_complete.yan    完整测试套件
    echo.
    pause
    exit /b 1
)

if not exist "%1" (
    echo 错误: 文件 %1 不存在
    pause
    exit /b 1
)

echo 运行文件: %1
echo.

"E:\Program Files\Racket\Racket.exe" run_advanced.rkt

echo.
pause
