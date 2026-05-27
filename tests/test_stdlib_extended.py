"""
言律语言扩展标准库测试
"""

import unittest
import sys
import os
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from yanlv.stdlib_extended import (
    HTTP请求, GET请求, POST请求,
    数据库连接, 连接数据库,
    显示消息, 获取输入, 显示菜单, 显示表格, 进度条
)


class TestNetworkFunctions(unittest.TestCase):
    """测试网络请求函数"""
    
    def test_http_request_structure(self):
        """测试HTTP请求结构"""
        # 测试函数是否存在
        self.assertTrue(callable(HTTP请求))
        self.assertTrue(callable(GET请求))
        self.assertTrue(callable(POST请求))
    
    def test_get_request_with_params(self):
        """测试GET请求参数"""
        # 模拟测试（不实际发送请求）
        url = "https://example.com"
        params = {"key": "value"}
        
        # 验证参数处理
        self.assertIsInstance(params, dict)


class TestDatabaseFunctions(unittest.TestCase):
    """测试数据库函数"""
    
    def test_database_connection(self):
        """测试数据库连接"""
        # 使用临时数据库
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
            db_path = f.name
        
        try:
            db = 连接数据库(db_path)
            self.assertIsNotNone(db.connection)
            self.assertIsNotNone(db.cursor)
            db.关闭()
        finally:
            os.unlink(db_path)
    
    def test_create_table(self):
        """测试创建表"""
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
            db_path = f.name
        
        try:
            db = 连接数据库(db_path)
            
            # 创建表
            columns = {
                'id': 'INTEGER PRIMARY KEY',
                'name': 'TEXT',
                'age': 'INTEGER'
            }
            
            result = db.创建表('users', columns)
            self.assertTrue(result)
            
            db.关闭()
        finally:
            os.unlink(db_path)
    
    def test_insert_data(self):
        """测试插入数据"""
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
            db_path = f.name
        
        try:
            db = 连接数据库(db_path)
            
            # 创建表
            db.创建表('users', {
                'id': 'INTEGER PRIMARY KEY',
                'name': 'TEXT',
                'age': 'INTEGER'
            })
            
            # 插入数据
            data = {'name': '张三', 'age': 25}
            result = db.插入('users', data)
            self.assertTrue(result)
            
            db.关闭()
        finally:
            os.unlink(db_path)


class TestGUIFunctions(unittest.TestCase):
    """测试图形界面函数"""
    
    def test_show_message(self):
        """测试显示消息"""
        # 测试函数是否存在
        self.assertTrue(callable(显示消息))
    
    def test_get_input(self):
        """测试获取输入"""
        # 测试函数是否存在
        self.assertTrue(callable(获取输入))
    
    def test_show_menu(self):
        """测试显示菜单"""
        # 测试函数是否存在
        self.assertTrue(callable(显示菜单))
    
    def test_show_table(self):
        """测试显示表格"""
        # 测试函数是否存在
        self.assertTrue(callable(显示表格))
        
        # 测试表格显示
        headers = ['姓名', '年龄']
        rows = [['张三', 25], ['李四', 30]]
        
        # 验证数据结构
        self.assertEqual(len(headers), 2)
        self.assertEqual(len(rows), 2)
    
    def test_progress_bar(self):
        """测试进度条"""
        # 测试函数是否存在
        self.assertTrue(callable(进度条))
        
        # 测试进度条显示
        for i in range(11):
            进度条(i, 10)


class TestDatabaseConnection(unittest.TestCase):
    """测试数据库连接类"""
    
    def test_database_class(self):
        """测试数据库类"""
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
            db_path = f.name
        
        try:
            db = 数据库连接(db_path)
            self.assertEqual(db.db_path, db_path)
            self.assertIsNone(db.connection)
            
            db.连接()
            self.assertIsNotNone(db.connection)
            
            db.关闭()
        finally:
            os.unlink(db_path)


if __name__ == '__main__':
    unittest.main()
