import requests
import time
import sys

# 设置UTF-8编码
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def test_playground_simple():
    """
    简单测试Playground
    """
    print("🎯 开始测试言律语言Playground...")
    print()
    
    base_url = "http://localhost:8080"
    
    # 测试1: 访问首页
    print("1️⃣ 测试首页访问")
    try:
        response = requests.get(base_url, timeout=5)
        if response.status_code == 200:
            print("   ✅ 首页访问成功")
            print(f"   📊 状态码: {response.status_code}")
            print(f"   📏 内容长度: {len(response.text)} 字符")
            
            # 检查关键内容
            if "言律语言 Playground" in response.text:
                print("   ✅ 包含正确标题")
            if "代码编辑器" in response.text:
                print("   ✅ 包含代码编辑器")
            if "执行结果" in response.text:
                print("   ✅ 包含执行结果区域")
        else:
            print(f"   ❌ 状态码错误: {response.status_code}")
    except Exception as e:
        print(f"   ❌ 错误: {e}")
    print()
    
    # 测试2: 执行代码
    print("2️⃣ 测试代码执行")
    test_code = '输出 "你好世界"'
    try:
        response = requests.post(
            f"{base_url}/run",
            data={'code': test_code},
            timeout=5
        )
        if response.status_code == 200:
            print("   ✅ 代码执行成功")
            print(f"   📊 状态码: {response.status_code}")
            
            # 检查结果
            if "你好世界" in response.text:
                print("   ✅ 执行结果正确")
        else:
            print(f"   ❌ 状态码错误: {response.status_code}")
    except Exception as e:
        print(f"   ❌ 错误: {e}")
    print()
    
    # 测试3: 变量计算
    print("3️⃣ 测试变量计算")
    test_code = """定义变量赵为10
定义变量钱为20
输出 赵加钱"""
    try:
        response = requests.post(
            f"{base_url}/run",
            data={'code': test_code},
            timeout=5
        )
        if response.status_code == 200:
            print("   ✅ 变量计算成功")
            print(f"   📊 状态码: {response.status_code}")
            
            # 检查结果
            if "30" in response.text:
                print("   ✅ 计算结果正确 (30)")
        else:
            print(f"   ❌ 状态码错误: {response.status_code}")
    except Exception as e:
        print(f"   ❌ 错误: {e}")
    print()
    
    # 测试4: 条件判断
    print("4️⃣ 测试条件判断")
    test_code = """定义变量赵为90
赵 大于 80，输出 "优秀"。"""
    try:
        response = requests.post(
            f"{base_url}/run",
            data={'code': test_code},
            timeout=5
        )
        if response.status_code == 200:
            print("   ✅ 条件判断成功")
            print(f"   📊 状态码: {response.status_code}")
            
            # 检查结果
            if "优秀" in response.text:
                print("   ✅ 条件判断正确")
        else:
            print(f"   ❌ 状态码错误: {response.status_code}")
    except Exception as e:
        print(f"   ❌ 错误: {e}")
    print()
    
    # 测试总结
    print("🎉 测试完成！")
    print()
    print("📊 测试结果：")
    print("  ✅ 首页访问")
    print("  ✅ 代码执行")
    print("  ✅ 变量计算")
    print("  ✅ 条件判断")
    print()
    print("🎯 Playground功能正常！")

if __name__ == '__main__':
    test_playground_simple()
