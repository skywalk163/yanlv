"""
言律语言扩展标准库

网络请求、图形界面、数据库操作
"""

import urllib.request
import urllib.parse
import json
import sqlite3
from typing import Dict, Any, List, Optional, Union
from datetime import datetime


# ============================================================================
# 网络请求函数
# ============================================================================

def HTTP请求(url: str, method: str = "GET", 
             headers: Dict[str, str] = None,
             data: Dict[str, Any] = None,
             timeout: int = 30) -> Dict[str, Any]:
    """
    发送HTTP请求
    
    Args:
        url: 请求URL
        method: 请求方法（GET/POST/PUT/DELETE）
        headers: 请求头
        data: 请求数据
        timeout: 超时时间
        
    Returns:
        响应数据
    """
    try:
        # 准备请求
        req_data = None
        if data and method in ["POST", "PUT"]:
            req_data = urllib.parse.urlencode(data).encode('utf-8')
        
        # 创建请求
        req = urllib.request.Request(url, data=req_data, method=method)
        
        # 添加请求头
        if headers:
            for key, value in headers.items():
                req.add_header(key, value)
        
        # 发送请求
        with urllib.request.urlopen(req, timeout=timeout) as response:
            result = {
                'status': response.status,
                'headers': dict(response.headers),
                'body': response.read().decode('utf-8'),
                'success': True
            }
            
            # 尝试解析JSON
            try:
                result['json'] = json.loads(result['body'])
            except:
                pass
            
            return result
    
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }


def GET请求(url: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    发送GET请求
    
    Args:
        url: 请求URL
        params: 查询参数
        
    Returns:
        响应数据
    """
    if params:
        url = f"{url}?{urllib.parse.urlencode(params)}"
    
    return HTTP请求(url, "GET")


def POST请求(url: str, data: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    发送POST请求
    
    Args:
        url: 请求URL
        data: 请求数据
        
    Returns:
        响应数据
    """
    return HTTP请求(url, "POST", data=data)


def 下载文件(url: str, filepath: str, 
             chunk_size: int = 8192) -> bool:
    """
    下载文件
    
    Args:
        url: 文件URL
        filepath: 保存路径
        chunk_size: 块大小
        
    Returns:
        是否成功
    """
    try:
        with urllib.request.urlopen(url) as response:
            with open(filepath, 'wb') as f:
                while True:
                    chunk = response.read(chunk_size)
                    if not chunk:
                        break
                    f.write(chunk)
        return True
    except Exception as e:
        print(f"下载失败: {e}")
        return False


# ============================================================================
# 数据库操作函数
# ============================================================================

class 数据库连接:
    """数据库连接类"""
    
    def __init__(self, db_path: str):
        """
        初始化数据库连接
        
        Args:
            db_path: 数据库路径
        """
        self.db_path = db_path
        self.connection = None
        self.cursor = None
    
    def 连接(self):
        """连接数据库"""
        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()
    
    def 关闭(self):
        """关闭连接"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
    
    def 执行(self, sql: str, params: tuple = None) -> Any:
        """
        执行SQL语句
        
        Args:
            sql: SQL语句
            params: 参数
            
        Returns:
            执行结果
        """
        if params:
            return self.cursor.execute(sql, params)
        else:
            return self.cursor.execute(sql)
    
    def 查询(self, sql: str, params: tuple = None) -> List[tuple]:
        """
        查询数据
        
        Args:
            sql: SQL语句
            params: 参数
            
        Returns:
            查询结果
        """
        self.执行(sql, params)
        return self.cursor.fetchall()
    
    def 插入(self, table: str, data: Dict[str, Any]) -> bool:
        """
        插入数据
        
        Args:
            table: 表名
            data: 数据
            
        Returns:
            是否成功
        """
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?' for _ in data])
        values = tuple(data.values())
        
        sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        
        try:
            self.执行(sql, values)
            self.connection.commit()
            return True
        except Exception as e:
            print(f"插入失败: {e}")
            return False
    
    def 更新(self, table: str, data: Dict[str, Any], 
             condition: str) -> bool:
        """
        更新数据
        
        Args:
            table: 表名
            data: 数据
            condition: 条件
            
        Returns:
            是否成功
        """
        set_clause = ', '.join([f"{k} = ?" for k in data.keys()])
        values = tuple(data.values())
        
        sql = f"UPDATE {table} SET {set_clause} WHERE {condition}"
        
        try:
            self.执行(sql, values)
            self.connection.commit()
            return True
        except Exception as e:
            print(f"更新失败: {e}")
            return False
    
    def 删除(self, table: str, condition: str) -> bool:
        """
        删除数据
        
        Args:
            table: 表名
            condition: 条件
            
        Returns:
            是否成功
        """
        sql = f"DELETE FROM {table} WHERE {condition}"
        
        try:
            self.执行(sql)
            self.connection.commit()
            return True
        except Exception as e:
            print(f"删除失败: {e}")
            return False
    
    def 创建表(self, table: str, columns: Dict[str, str]) -> bool:
        """
        创建表
        
        Args:
            table: 表名
            columns: 列定义
            
        Returns:
            是否成功
        """
        column_defs = ', '.join([f"{name} {dtype}" for name, dtype in columns.items()])
        sql = f"CREATE TABLE IF NOT EXISTS {table} ({column_defs})"
        
        try:
            self.执行(sql)
            self.connection.commit()
            return True
        except Exception as e:
            print(f"创建表失败: {e}")
            return False


def 连接数据库(db_path: str) -> 数据库连接:
    """
    连接数据库
    
    Args:
        db_path: 数据库路径
        
    Returns:
        数据库连接对象
    """
    db = 数据库连接(db_path)
    db.连接()
    return db


# ============================================================================
# 图形界面函数（简化版）
# ============================================================================

def 显示消息(title: str, message: str) -> None:
    """
    显示消息框（控制台版本）
    
    Args:
        title: 标题
        message: 消息内容
    """
    print(f"\n{'='*50}")
    print(f"{title}")
    print(f"{'='*50}")
    print(message)
    print(f"{'='*50}\n")


def 获取输入(prompt: str = "") -> str:
    """
    获取用户输入
    
    Args:
        prompt: 提示信息
        
    Returns:
        用户输入
    """
    return input(prompt)


def 显示菜单(title: str, options: List[str]) -> int:
    """
    显示菜单并获取选择
    
    Args:
        title: 菜单标题
        options: 选项列表
        
    Returns:
        选择的索引
    """
    print(f"\n{title}")
    print("-" * 40)
    
    for i, option in enumerate(options, 1):
        print(f"{i}. {option}")
    
    print("-" * 40)
    
    while True:
        try:
            choice = int(input("请选择: "))
            if 1 <= choice <= len(options):
                return choice - 1
            else:
                print("无效选择，请重试")
        except ValueError:
            print("请输入数字")


def 显示表格(headers: List[str], rows: List[List[Any]]) -> None:
    """
    显示表格
    
    Args:
        headers: 表头
        rows: 数据行
    """
    # 计算列宽
    widths = [len(str(h)) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            widths[i] = max(widths[i], len(str(cell)))
    
    # 显示表头
    header_line = " | ".join(str(h).ljust(w) for h, w in zip(headers, widths))
    print(header_line)
    print("-" * len(header_line))
    
    # 显示数据行
    for row in rows:
        print(" | ".join(str(c).ljust(w) for c, w in zip(row, widths)))


def 进度条(current: int, total: int, width: int = 50) -> None:
    """
    显示进度条
    
    Args:
        current: 当前进度
        total: 总数
        width: 进度条宽度
    """
    percent = current / total
    filled = int(width * percent)
    bar = '█' * filled + '░' * (width - filled)
    
    print(f"\r[{bar}] {percent:.1%} ({current}/{total})", end='', flush=True)
    
    if current == total:
        print()  # 完成时换行


# ============================================================================
# 导出
# ============================================================================

__all__ = [
    # 网络请求
    'HTTP请求', 'GET请求', 'POST请求', '下载文件',
    
    # 数据库操作
    '数据库连接', '连接数据库',
    
    # 图形界面
    '显示消息', '获取输入', '显示菜单', '显示表格', '进度条',
]
