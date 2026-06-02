#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
言律语言快速测试脚本
验证是否可以正常编译和运行
"""

import sys
import os
import io

# 设置标准输出编码为UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 添加src目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_basic():
    """测试基本功能"""
    print("=" * 50)
    print("言律语言功能测试")
    print("=" * 50)
    print()

    try:
        from yanlv.compiler import YanLuCompiler
        print("✓ 成功导入编译器")
    except ImportError as e:
        print(f"✗ 导入编译器失败: {e}")
        return False

    # 创建编译器实例
    try:
        compiler = YanLuCompiler()
        print("✓ 成功创建编译器实例")
    except Exception as e:
        print(f"✗ 创建编译器失败: {e}")
        return False

    # 测试代码
    test_cases = [
        ("Hello World", '输出 "你好世界"'),
        ("变量定义", "定义变量 x 为 10\n输出 x"),
        ("数学运算", "定义变量 a 为 5\n定义变量 b 为 3\n定义变量 c 为 a 加 b\n输出 c"),
    ]

    print()
    print("运行测试用例:")
    print("-" * 50)

    success_count = 0
    for name, code in test_cases:
        try:
            result = compiler.compile(code)
            print(f"✓ {name}: {result.strip() if result else '(无输出)'}")
            success_count += 1
        except Exception as e:
            print(f"✗ {name}: {e}")

    print("-" * 50)
    print(f"测试结果: {success_count}/{len(test_cases)} 通过")
    print()

    return success_count == len(test_cases)


def test_cli():
    """测试CLI"""
    print("=" * 50)
    print("CLI测试")
    print("=" * 50)
    print()

    try:
        from yanlv.cli import main
        print("✓ CLI模块导入成功")
        print()
        print("可用命令:")
        print("  yanlv 编译 <文件> [输出文件]  - 编译言律文件")
        print("  yanlv 运行 <文件>            - 运行言律文件")
        print("  yanlv 交互                   - 进入交互模式")
        print("  yanlv --help                 - 显示帮助")
        return True
    except ImportError as e:
        print(f"✗ CLI导入失败: {e}")
        return False


def main_test():
    """主测试函数"""
    print()
    print("╔" + "═" * 48 + "╗")
    print("║" + " " * 10 + "言律语言系统测试" + " " * 18 + "║")
    print("╚" + "═" * 48 + "╝")
    print()

    # 测试基本功能
    basic_ok = test_basic()

    # 测试CLI
    cli_ok = test_cli()

    # 总结
    print()
    print("=" * 50)
    print("测试总结")
    print("=" * 50)
    print(f"基本功能: {'✓ 通过' if basic_ok else '✗ 失败'}")
    print(f"CLI功能:  {'✓ 通过' if cli_ok else '✗ 失败'}")
    print()

    if basic_ok and cli_ok:
        print("🎉 所有测试通过！言律语言可以正常使用。")
        print()
        print("快速开始:")
        print("  1. 交互模式: python src/yanlv/cli.py 交互")
        print("  2. 编译文件: python src/yanlv/cli.py 编译 文件.yan")
        print("  3. 安装使用: pip install -e .")
        print("  4. 打包exe:  build_windows.bat (Windows)")
        print("               bash build_unix.sh (Linux/macOS)")
        return 0
    else:
        print("⚠ 部分测试失败，请检查错误信息。")
        return 1


if __name__ == "__main__":
    sys.exit(main_test())
