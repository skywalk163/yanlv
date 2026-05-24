#!/usr/bin/env python3
"""
Playground API 测试脚本
"""
import sys
import os
import json

# 添加src目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src'))

def test_api():
    """测试 API 端点"""
    print("=" * 60)
    print("Playground API 测试")
    print("=" * 60)

    # 导入 Flask 应用
    from flask import Flask
    import importlib.util

    spec = importlib.util.spec_from_file_location("server", "server.py")
    server = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(server)

    app = server.app
    client = app.test_client()

    # 测试1: 首页
    print("\n[1] 测试首页...")
    response = client.get('/')
    print(f"    状态码: {response.status_code}")
    if response.status_code == 200:
        print("    [OK] 首页可访问")
        if response.content_type.startswith('text/html'):
            print("    [OK] 返回 HTML 页面")
        else:
            data = json.loads(response.data)
            print(f"    [OK] 返回 API 信息: {data.get('name', 'N/A')}")
    else:
        print("    [FAIL] 首页访问失败")

    # 测试2: 运行代码
    print("\n[2] 测试运行代码...")
    response = client.post('/api/run',
                          data=json.dumps({'code': '输出 "测试"'}),
                          content_type='application/json')
    print(f"    状态码: {response.status_code}")
    if response.status_code == 200:
        data = json.loads(response.data)
        if data.get('success'):
            print(f"    [OK] 代码执行成功")
            print(f"    输出: {data.get('output', 'N/A')}")
        else:
            print(f"    [FAIL] 执行失败: {data.get('error', 'N/A')}")
    else:
        print("    [FAIL] API 调用失败")

    # 测试3: 分析代码
    print("\n[3] 测试分析代码...")
    response = client.post('/api/analyze',
                          data=json.dumps({'code': '输出 "测试"'}),
                          content_type='application/json')
    print(f"    状态码: {response.status_code}")
    if response.status_code == 200:
        data = json.loads(response.data)
        if data.get('success'):
            print(f"    [OK] 代码分析成功")
            print(f"    词元数: {data.get('total_tokens', 0)}")
            tokens = data.get('tokens', [])
            if tokens:
                print(f"    词元列表:")
                for token in tokens[:5]:
                    print(f"      - {token['type']}: {token['value']}")
        else:
            print(f"    [FAIL] 分析失败: {data.get('error', 'N/A')}")
    else:
        print("    [FAIL] API 调用失败")

    # 测试4: 获取示例
    print("\n[4] 测试获取示例...")
    response = client.get('/api/examples')
    print(f"    状态码: {response.status_code}")
    if response.status_code == 200:
        data = json.loads(response.data)
        if data.get('success'):
            examples = data.get('examples', [])
            print(f"    [OK] 获取示例成功")
            print(f"    示例数量: {len(examples)}")
            for example in examples[:3]:
                print(f"      - {example['name']}")
        else:
            print(f"    [FAIL] 获取失败")
    else:
        print("    [FAIL] API 调用失败")

    # 测试5: 获取统计
    print("\n[5] 测试获取统计...")
    response = client.get('/api/stats')
    print(f"    状态码: {response.status_code}")
    if response.status_code == 200:
        data = json.loads(response.data)
        if data.get('success'):
            print(f"    [OK] 获取统计成功")
        else:
            print(f"    [FAIL] 获取失败: {data.get('error', 'N/A')}")
    else:
        print("    [FAIL] API 调用失败")

    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)

if __name__ == '__main__':
    test_api()
