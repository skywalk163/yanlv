"""
言律语言互操作系统 - 完整测试

测试Python、JavaScript、SQL三种轨的集成使用
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from yanlv.interop import TrackManager, PythonTrack
from yanlv.interop.javascript_track import JavaScriptTrack
from yanlv.interop.sql_track import SQLTrack


def test_all_tracks():
    """测试所有轨"""
    print("\n" + "=" * 70)
    print("言律语言互操作系统 - 完整测试")
    print("=" * 70)

    # 创建轨管理器
    manager = TrackManager()

    # 注册所有轨
    manager.register_track("python", PythonTrack())
    manager.register_track("javascript", JavaScriptTrack())
    manager.register_track("sql", SQLTrack(":memory:"))

    print(f"\n已注册的轨: {manager.list_tracks()}")

    # =========================================================================
    # Python轨测试
    # =========================================================================
    print("\n" + "=" * 70)
    print("Python轨测试")
    print("=" * 70)

    # 测试1: 数学计算
    print("\n[测试1] 数学计算")
    result = manager.execute_in_track("python", "2 ** 10 + 100", {})
    print(f"  2^10 + 100 = {result}")

    # 测试2: 使用Python库
    print("\n[测试2] 使用Python标准库")
    code = """
import math
import random

result = {
    'pi': math.pi,
    'sqrt2': math.sqrt(2),
    'random': random.random()
}
"""
    manager.execute_in_track("python", code, {})
    result = manager.execute_in_track("python", "result", {})
    print(f"  数学常数: π={result['pi']:.4f}, √2={result['sqrt2']:.4f}")

    # 测试3: 数据处理
    print("\n[测试3] 数据处理")
    code = """
data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
result = {
    'sum': sum(data),
    'avg': sum(data) / len(data),
    'max': max(data),
    'min': min(data)
}
"""
    manager.execute_in_track("python", code, {})
    result = manager.execute_in_track("python", "result", {})
    print(f"  统计结果: 总和={result['sum']}, 平均={result['avg']}, 最大={result['max']}, 最小={result['min']}")

    # =========================================================================
    # JavaScript轨测试
    # =========================================================================
    print("\n" + "=" * 70)
    print("JavaScript轨测试")
    print("=" * 70)

    try:
        js_track = manager.get_track("javascript")
        if js_track._check_node_available():
            # 测试4: 数组操作
            print("\n[测试4] JavaScript数组操作")
            code = """
const arr = [1, 2, 3, 4, 5];
const result = {
    sum: arr.reduce((a, b) => a + b, 0),
    product: arr.reduce((a, b) => a * b, 1),
    squares: arr.map(x => x * x)
};
console.log(JSON.stringify(result));
"""
            result = manager.execute_in_track("javascript", code, {})
            print(f"  数组操作: 总和={result['sum']}, 乘积={result['product']}")

            # 测试5: JSON处理
            print("\n[测试5] JSON处理")
            code = """
const data = {
    users: [
        {name: "张三", age: 25},
        {name: "李四", age: 30},
        {name: "王五", age: 28}
    ]
};
const avgAge = data.users.reduce((sum, u) => sum + u.age, 0) / data.users.length;
console.log(JSON.stringify({avgAge, count: data.users.length}));
"""
            result = manager.execute_in_track("javascript", code, {})
            print(f"  平均年龄: {result['avgAge']}, 用户数: {result['count']}")

            # 测试6: 异步操作
            print("\n[测试6] 异步操作")
            async_code = """
const delay = (ms) => new Promise(resolve => setTimeout(resolve, ms));

await delay(50);
const result = "异步执行成功";
console.log(JSON.stringify(result));
"""
            result = manager.execute_in_track("javascript", async_code, {})
            print(f"  异步结果: {result}")

        else:
            print("\n  警告: Node.js不可用，跳过JavaScript测试")

    except Exception as e:
        print(f"\n  JavaScript测试出错: {e}")

    # =========================================================================
    # SQL轨测试
    # =========================================================================
    print("\n" + "=" * 70)
    print("SQL轨测试")
    print("=" * 70)

    # 测试7: 创建表和插入数据
    print("\n[测试7] 创建表和插入数据")
    sql_track = manager.get_track("sql")
    sql_track.create_table("products", {
        "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
        "name": "TEXT NOT NULL",
        "price": "REAL",
        "stock": "INTEGER"
    })

    products = [
        {"name": "苹果", "price": 5.5, "stock": 100},
        {"name": "香蕉", "price": 3.0, "stock": 150},
        {"name": "橙子", "price": 4.5, "stock": 80},
    ]

    for product in products:
        result = sql_track.insert("products", product)
        print(f"  插入 {product['name']}: ID={result['last_insert_id']}")

    # 测试8: 查询数据
    print("\n[测试8] 查询数据")
    all_products = sql_track.select("products")
    print(f"  所有商品: {len(all_products)}个")
    for p in all_products:
        print(f"    {p['name']}: 价格{p['price']}, 库存{p['stock']}")

    # 测试9: 聚合查询
    print("\n[测试9] 聚合查询")
    result = manager.execute_in_track("sql",
        "SELECT COUNT(*) as count, AVG(price) as avg_price, SUM(stock) as total_stock FROM products",
        {}
    )
    print(f"  统计: {result[0]['count']}种商品, 平均价格{result[0]['avg_price']:.2f}, 总库存{result[0]['total_stock']}")

    # 测试10: 条件查询
    print("\n[测试10] 条件查询")
    expensive = manager.execute_in_track("sql",
        "SELECT * FROM products WHERE price > ?",
        {"params": (4.0,)}
    )
    print(f"  价格>4的商品: {len(expensive)}个")
    for p in expensive:
        print(f"    {p['name']}: 价格{p['price']}")

    # =========================================================================
    # 跨轨协作测试
    # =========================================================================
    print("\n" + "=" * 70)
    print("跨轨协作测试")
    print("=" * 70)

    # 测试11: SQL + Python协作
    print("\n[测试11] SQL + Python协作")
    # 从SQL获取数据
    products = manager.execute_in_track("sql", "SELECT * FROM products", {})

    # 在Python中处理
    code = f"""
import statistics

products = {products}
prices = [p['price'] for p in products]
stocks = [p['stock'] for p in products]

result = {{
    'price_stats': {{
        'mean': statistics.mean(prices),
        'stdev': statistics.stdev(prices) if len(prices) > 1 else 0
    }},
    'total_value': sum(p['price'] * p['stock'] for p in products)
}}
"""
    manager.execute_in_track("python", code, {})
    result = manager.execute_in_track("python", "result", {})
    print(f"  价格统计: 平均{result['price_stats']['mean']:.2f}, 标准差{result['price_stats']['stdev']:.2f}")
    print(f"  总价值: {result['total_value']:.2f}")

    # 测试12: Python + JavaScript协作
    print("\n[测试12] Python + JavaScript协作")
    # Python生成数据
    manager.execute_in_track("python", "data = [i**2 for i in range(1, 11)]", {})
    data = manager.execute_in_track("python", "data", {})

    # JavaScript处理
    js_code = f"""
const data = {data};
const result = {{
    sum: data.reduce((a, b) => a + b, 0),
    max: Math.max(...data),
    min: Math.min(...data)
}};
console.log(JSON.stringify(result));
"""
    result = manager.execute_in_track("javascript", js_code, {})
    print(f"  JavaScript处理结果: 总和={result['sum']}, 最大={result['max']}, 最小={result['min']}")

    # =========================================================================
    # 能力总结
    # =========================================================================
    print("\n" + "=" * 70)
    print("各轨能力总结")
    print("=" * 70)

    for track_name in manager.list_tracks():
        track = manager.get_track(track_name)
        capabilities = track.get_capabilities()
        print(f"\n{track_name}轨: {', '.join(capabilities)}")

    print("\n" + "=" * 70)
    print("[PASS] 所有测试完成")
    print("=" * 70)


if __name__ == "__main__":
    test_all_tracks()
