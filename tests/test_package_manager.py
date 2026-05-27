"""
言律语言包管理器测试
"""

import unittest
import sys
import os
import tempfile
import shutil

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from yanlv.package_manager import (
    PackageInfo, PackageRegistry, PackageManager
)


class TestPackageInfo(unittest.TestCase):
    """测试包信息"""
    
    def test_create_package_info(self):
        """测试创建包信息"""
        package = PackageInfo(
            name="test-package",
            version="1.0.0",
            description="测试包",
            author="测试作者"
        )
        
        self.assertEqual(package.name, "test-package")
        self.assertEqual(package.version, "1.0.0")
        self.assertEqual(package.description, "测试包")
        self.assertEqual(package.author, "测试作者")
    
    def test_package_dependencies(self):
        """测试包依赖"""
        package = PackageInfo(
            name="test-package",
            version="1.0.0",
            dependencies={"dep1": "1.0.0", "dep2": "2.0.0"}
        )
        
        self.assertEqual(len(package.dependencies), 2)
        self.assertIn("dep1", package.dependencies)
        self.assertIn("dep2", package.dependencies)


class TestPackageRegistry(unittest.TestCase):
    """测试包注册表"""
    
    def setUp(self):
        self.registry = PackageRegistry()
    
    def test_add_package(self):
        """测试添加包"""
        package = PackageInfo(name="test", version="1.0.0")
        self.registry.add_package(package)
        
        self.assertIn("test", self.registry.packages)
    
    def test_get_package(self):
        """测试获取包"""
        package = PackageInfo(name="test", version="1.0.0")
        self.registry.add_package(package)
        
        result = self.registry.get_package("test")
        self.assertEqual(result.name, "test")
        
        # 获取不存在的包
        result = self.registry.get_package("not-exist")
        self.assertIsNone(result)
    
    def test_list_packages(self):
        """测试列出包"""
        package1 = PackageInfo(name="test1", version="1.0.0")
        package2 = PackageInfo(name="test2", version="2.0.0")
        
        self.registry.add_package(package1)
        self.registry.add_package(package2)
        
        packages = self.registry.list_packages()
        self.assertEqual(len(packages), 2)


class TestPackageManager(unittest.TestCase):
    """测试包管理器"""
    
    def setUp(self):
        # 使用临时目录
        self.temp_dir = tempfile.mkdtemp()
        self.manager = PackageManager()
        self.manager.install_dir = Path(self.temp_dir) / "packages"
        self.manager.cache_dir = Path(self.temp_dir) / "cache"
        self.manager.install_dir.mkdir(parents=True, exist_ok=True)
        self.manager.cache_dir.mkdir(parents=True, exist_ok=True)
    
    def tearDown(self):
        # 清理临时目录
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_create_package(self):
        """测试创建包"""
        package = self.manager.create_package(
            name="test-package",
            version="1.0.0",
            description="测试包"
        )
        
        self.assertEqual(package.name, "test-package")
        self.assertEqual(package.version, "1.0.0")
        
        # 检查目录是否创建
        self.assertTrue(Path("test-package").exists())
        
        # 清理
        shutil.rmtree("test-package", ignore_errors=True)
    
    def test_list_installed_empty(self):
        """测试列出已安装的包（空）"""
        packages = self.manager.list_installed()
        self.assertEqual(len(packages), 0)
    
    def test_search_empty(self):
        """测试搜索（空结果）"""
        results = self.manager.search("nonexistent")
        self.assertEqual(len(results), 0)
    
    def test_info_nonexistent(self):
        """测试查看不存在的包信息"""
        info = self.manager.info("nonexistent")
        self.assertIsNone(info)


# 导入Path
from pathlib import Path


if __name__ == '__main__':
    unittest.main()
