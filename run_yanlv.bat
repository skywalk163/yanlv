@echo off
setlocal enabledelayedexpansion

echo ========================================
echo Yanlv Language
echo ========================================
echo.

if "%~1"=="" (
    echo Usage: run_yanlv.bat filename.yan
    echo.
    echo Examples:
    echo   run_yanlv.bat examples\hello.yan
    echo   run_yanlv.bat examples\quick_start.yan
    echo.
    pause
    exit /b 1
)

if not exist "%~1" (
    echo Error: File %~1 not found
    pause
    exit /b 1
)

echo Running file: %~1
echo.

python -m yanlv 运行 "%~1"

echo.
pause
