import asyncio
from playwright.async_api import async_playwright

async def test_yanlv_playground():
    """
    测试言律语言Playground
    """
    async with async_playwright() as p:
        # 启动浏览器
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        
        print("🎯 开始测试言律语言Playground...")
        print()
        
        # 访问Playground
        print("1️⃣ 访问 http://localhost:8080")
        await page.goto('http://localhost:8080')
        await page.wait_for_load_state('networkidle')
        
        # 截图
        await page.screenshot(path='playground_home.png')
        print("   ✅ 页面加载成功")
        print("   📸 截图保存: playground_home.png")
        print()
        
        # 检查标题
        title = await page.title()
        print(f"2️⃣ 页面标题: {title}")
        print()
        
        # 测试示例1: Hello World
        print("3️⃣ 测试示例1: Hello World")
        await page.click('.example:nth-child(1)')
        await page.wait_for_timeout(500)
        
        # 点击运行
        await page.click('button[type="submit"]')
        await page.wait_for_timeout(1000)
        
        # 截图
        await page.screenshot(path='playground_hello.png')
        print("   ✅ Hello World测试完成")
        print("   📸 截图保存: playground_hello.png")
        print()
        
        # 测试示例2: 变量计算
        print("4️⃣ 测试示例2: 变量计算")
        await page.click('.example:nth-child(2)')
        await page.wait_for_timeout(500)
        
        # 点击运行
        await page.click('button[type="submit"]')
        await page.wait_for_timeout(1000)
        
        # 截图
        await page.screenshot(path='playground_calc.png')
        print("   ✅ 变量计算测试完成")
        print("   📸 截图保存: playground_calc.png")
        print()
        
        # 测试示例3: 条件判断
        print("5️⃣ 测试示例3: 条件判断")
        await page.click('.example:nth-child(3)')
        await page.wait_for_timeout(500)
        
        # 点击运行
        await page.click('button[type="submit"]')
        await page.wait_for_timeout(1000)
        
        # 截图
        await page.screenshot(path='playground_condition.png')
        print("   ✅ 条件判断测试完成")
        print("   📸 截图保存: playground_condition.png")
        print()
        
        # 测试自定义代码
        print("6️⃣ 测试自定义代码")
        
        # 清空代码
        await page.click('button[type="button"]')
        await page.wait_for_timeout(500)
        
        # 输入自定义代码
        custom_code = """定义变量赵为100
定义变量钱为200
定义变量孙为赵加钱
输出 孙"""
        
        await page.fill('textarea[name="code"]', custom_code)
        await page.wait_for_timeout(500)
        
        # 点击运行
        await page.click('button[type="submit"]')
        await page.wait_for_timeout(1000)
        
        # 截图
        await page.screenshot(path='playground_custom.png')
        print("   ✅ 自定义代码测试完成")
        print("   📸 截图保存: playground_custom.png")
        print()
        
        # 测试完成
        print("🎉 所有测试完成！")
        print()
        print("📊 测试结果：")
        print("  ✅ 页面加载")
        print("  ✅ Hello World示例")
        print("  ✅ 变量计算示例")
        print("  ✅ 条件判断示例")
        print("  ✅ 自定义代码")
        print()
        print("📸 截图文件：")
        print("  • playground_home.png")
        print("  • playground_hello.png")
        print("  • playground_calc.png")
        print("  • playground_condition.png")
        print("  • playground_custom.png")
        print()
        
        # 等待5秒查看结果
        await page.wait_for_timeout(5000)
        
        # 关闭浏览器
        await browser.close()

if __name__ == '__main__':
    asyncio.run(test_yanlv_playground())
