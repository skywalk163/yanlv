@echo off
echo ============================================================
echo   启动言律语言 Playground 服务
echo ============================================================
echo.

cd /d "%~dp0"

echo 正在启动服务...
echo 访问地址: http://localhost:5000
echo.

start "言律语言 Playground" python server.py

echo 服务已在后台启动
echo 请等待几秒钟，然后访问: http://localhost:5000
echo.

timeout /t 3 /nobreak >nul

echo 测试服务连接...
curl -s http://localhost:5000 >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] 服务启动成功！
    echo.
    echo API端点:
    echo   POST /api/run      - 运行代码
    echo   POST /api/analyze  - 分析代码
    echo   POST /api/feedback - 提交反馈
    echo   GET  /api/stats    - 获取统计
    echo   GET  /api/examples - 获取示例
) else (
    echo [FAIL] 服务启动失败，请检查日志
)

echo.
pause
