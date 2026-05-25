"""测试playground服务"""
import requests
import time
import subprocess
import sys

print("=" * 80)
print("测试言律语言 Playground 服务")
print("=" * 80)

# 测试1: 检查服务是否运行
print("\n测试1: 检查服务是否运行")
print("-" * 80)

try:
    response = requests.get('http://127.0.0.1:5000', timeout=5)
    print(f"状态码: {response.status_code}")
    print(f"响应: {response.text[:200]}")
    print("[OK] 服务正在运行")
except requests.exceptions.ConnectionError as e:
    print(f"[FAIL] 无法连接到服务: {e}")
    print("\n可能的原因:")
    print("1. 服务未启动 - 请运行: python playground/server.py")
    print("2. 端口被占用 - 请检查: netstat -ano | findstr :5000")
    print("3. 防火墙阻止 - 请检查Windows防火墙设置")
    sys.exit(1)
except Exception as e:
    print(f"[FAIL] 其他错误: {e}")
    sys.exit(1)

# 测试2: 测试运行代码API
print("\n\n测试2: 测试运行代码API")
print("-" * 80)

code = '输出"你好，言律语言！"'
try:
    response = requests.post('http://127.0.0.1:5000/api/run',
                            json={'code': code},
                            timeout=5)
    result = response.json()
    print(f"代码: {code}")
    print(f"结果: {result}")
    if result.get('success'):
        print(f"输出: {result.get('output')}")
        print("[OK] 运行代码API正常")
    else:
        print(f"[FAIL] 运行失败: {result.get('error')}")
except Exception as e:
    print(f"[FAIL] 请求失败: {e}")

# 测试3: 测试分析代码API
print("\n\n测试3: 测试分析代码API")
print("-" * 80)

code = '定义变量x为10'
try:
    response = requests.post('http://127.0.0.1:5000/api/analyze',
                            json={'code': code},
                            timeout=5)
    result = response.json()
    print(f"代码: {code}")
    if result.get('success'):
        print(f"词元数量: {result.get('total_tokens')}")
        print(f"词元列表: {result.get('tokens')[:5]}")
        print("[OK] 分析代码API正常")
    else:
        print(f"[FAIL] 分析失败: {result.get('error')}")
except Exception as e:
    print(f"[FAIL] 请求失败: {e}")

# 测试4: 测试获取示例API
print("\n\n测试4: 测试获取示例API")
print("-" * 80)

try:
    response = requests.get('http://127.0.0.1:5000/api/examples', timeout=5)
    result = response.json()
    if result.get('success'):
        examples = result.get('examples', [])
        print(f"示例数量: {len(examples)}")
        print(f"示例列表: {[e['name'] for e in examples[:5]]}")
        print("[OK] 获取示例API正常")
    else:
        print(f"[FAIL] 获取失败: {result.get('error')}")
except Exception as e:
    print(f"[FAIL] 请求失败: {e}")

# 测试5: 测试汉诺塔算法
print("\n\n测试5: 测试汉诺塔算法")
print("-" * 80)

code = '''函数汉诺塔参数n from to aux
如果n大于0则
调用汉诺塔参数n-1 from aux to
输出"移动盘子"
输出n
输出"从"
输出from
输出"到"
输出to
调用汉诺塔参数n-1 aux to from
结束
结束
调用汉诺塔参数3 A C B'''

try:
    response = requests.post('http://127.0.0.1:5000/api/run',
                            json={'code': code},
                            timeout=10)
    result = response.json()
    if result.get('success'):
        output = result.get('output', '')
        move_count = output.count('移动盘子')
        print(f"汉诺塔输出:")
        print(output)
        print(f"\n移动次数: {move_count}")
        if move_count == 7:
            print("[OK] 汉诺塔算法正确（7次移动）")
        else:
            print(f"[FAIL] 汉诺塔算法错误（应该是7次移动，实际{move_count}次）")
    else:
        print(f"[FAIL] 运行失败: {result.get('error')}")
except Exception as e:
    print(f"[FAIL] 请求失败: {e}")

print("\n" + "=" * 80)
print("测试完成")
print("=" * 80)
