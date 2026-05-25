@echo off
echo ============================================================
echo   测试言律语言 Playground 服务
echo ============================================================
echo.

echo 测试1: 检查服务是否运行
echo ------------------------------------------------------------
curl -s http://localhost:5000/api/examples | python -c "import sys, json; d=json.load(sys.stdin); print('状态: OK' if d.get('success') else '状态: FAIL')"
echo.

echo 测试2: 运行Hello World
echo ------------------------------------------------------------
curl -s -X POST http://localhost:5000/api/run -H "Content-Type: application/json" -d "{\"code\": \"输出\\\"你好\\\"\"}" | python -c "import sys, json; d=json.load(sys.stdin); print('输出:', d.get('output', 'N/A')) if d.get('success') else print('错误:', d.get('error', 'N/A'))"
echo.

echo 测试3: 运行变量定义
echo ------------------------------------------------------------
curl -s -X POST http://localhost:5000/api/run -H "Content-Type: application/json" -d "{\"code\": \"定义变量x为10\n输出x\"}" | python -c "import sys, json; d=json.load(sys.stdin); print('输出:', d.get('output', 'N/A')) if d.get('success') else print('错误:', d.get('error', 'N/A'))"
echo.

echo 测试4: 运行循环
echo ------------------------------------------------------------
curl -s -X POST http://localhost:5000/api/run -H "Content-Type: application/json" -d "{\"code\": \"循环3次执行\n输出i\n结束\"}" | python -c "import sys, json; d=json.load(sys.stdin); print('输出:', d.get('output', 'N/A').replace(chr(10), ' | ')) if d.get('success') else print('错误:', d.get('error', 'N/A'))"
echo.

echo 测试5: 分析代码
echo ------------------------------------------------------------
curl -s -X POST http://localhost:5000/api/analyze -H "Content-Type: application/json" -d "{\"code\": \"定义变量x为10\"}" | python -c "import sys, json; d=json.load(sys.stdin); print('词元数量:', d.get('total_tokens', 0)) if d.get('success') else print('错误:', d.get('error', 'N/A'))"
echo.

echo ============================================================
echo   测试完成
echo ============================================================
pause
