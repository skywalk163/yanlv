#!/usr/bin/env python3
"""
言律语言命令行接口
"""

import argparse
import sys
from pathlib import Path
from typing import Optional

from .compiler import YanLuCompiler


def compile_file(input_file: str, output_file: Optional[str] = None) -> None:
    """编译言律文件"""
    try:
        with open(input_file, "r", encoding="utf-8") as f:
            source_code = f.read()
        
        compiler = YanLuCompiler()
        result = compiler.compile(source_code)
        
        if output_file:
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(result)
            print(f"编译成功: {input_file} -> {output_file}")
        else:
            print(result)
            
    except FileNotFoundError:
        print(f"错误: 文件不存在 {input_file}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"编译错误: {e}", file=sys.stderr)
        sys.exit(1)


def run_interactive() -> None:
    """运行交互式解释器"""
    print("言律语言交互式解释器 v0.1.0")
    print("输入 '退出' 或 'exit' 退出")
    print("输入 '帮助' 或 'help' 查看帮助")
    print()
    
    compiler = YanLuCompiler()
    
    while True:
        try:
            line = input("言律> ").strip()
            
            if line.lower() in ["退出", "exit", "quit"]:
                print("再见!")
                break
            elif line.lower() in ["帮助", "help"]:
                print_help()
                continue
            elif not line:
                continue
            
            # 尝试编译单行代码
            try:
                result = compiler.compile(line)
                print(result)
            except Exception as e:
                print(f"错误: {e}")
                
        except KeyboardInterrupt:
            print("\n再见!")
            break
        except EOFError:
            print("\n再见!")
            break


def print_help() -> None:
    """打印帮助信息"""
    help_text = """
可用命令:
  编译 <文件> [输出文件]  - 编译言律文件
  运行 <文件>            - 运行言律文件
  交互                   - 进入交互模式
  帮助                   - 显示此帮助信息
  退出                   - 退出程序

示例:
  编译 hello.yan hello.py
  运行 hello.yan
  交互
"""
    print(help_text)


def main() -> None:
    """主函数"""
    parser = argparse.ArgumentParser(
        description="言律(Yán Lǜ) - 中文原生编程语言编译器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s 编译 hello.yan          # 编译文件并输出到控制台
  %(prog)s 编译 hello.yan hello.py # 编译文件到指定输出
  %(prog)s 运行 hello.yan          # 运行言律文件
  %(prog)s 交互                    # 进入交互模式
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="命令")
    
    # 编译命令
    compile_parser = subparsers.add_parser("编译", help="编译言律文件")
    compile_parser.add_argument("input_file", help="输入文件")
    compile_parser.add_argument("output_file", nargs="?", help="输出文件（可选）")
    
    # 运行命令
    run_parser = subparsers.add_parser("运行", help="运行言律文件")
    run_parser.add_argument("input_file", help="输入文件")
    
    # 交互命令
    subparsers.add_parser("交互", help="进入交互模式")
    
    # 帮助命令
    subparsers.add_parser("帮助", help="显示帮助信息")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    if args.command == "编译":
        compile_file(args.input_file, args.output_file)
    elif args.command == "运行":
        # 暂时只编译，后续添加执行功能
        compile_file(args.input_file)
    elif args.command == "交互":
        run_interactive()
    elif args.command == "帮助":
        parser.print_help()
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()