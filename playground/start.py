#!/usr/bin/env python3
"""
言律语言 Playground 启动脚本
"""

import sys
import os
import subprocess
import webbrowser
import time
from threading import Thread

def start_backend():
    """启动后端服务"""
    print("正在启动后端服务...")
    server_path = os.path.join(os.path.dirname(__file__), 'server.py')
    subprocess.run([sys.executable, server_path])

def open_browser():
    """打开浏览器"""
    time.sleep(2)  # 等待服务器启动
    print("正在打开浏览器...")
    webbrowser.open('http://localhost:5000')

def main():
    """主函数"""
    print("="*60)
    print("  言律语言 Playground")
    print("="*60)
    print()

    # 检查依赖
    try:
        import flask
        import flask_cors
    except ImportError:
        print("缺少依赖，正在安装...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'flask', 'flask-cors'])
        print()

    # 启动后端
    print("启动方式:")
    print("1. 仅启动后端服务 (API)")
    print("2. 启动后端并打开浏览器")
    print()

    choice = input("请选择 (1/2): ").strip()

    if choice == '2':
        # 在后台线程中打开浏览器
        browser_thread = Thread(target=open_browser)
        browser_thread.daemon = True
        browser_thread.start()

    # 启动后端服务
    start_backend()

if __name__ == '__main__':
    main()
