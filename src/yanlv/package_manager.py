"""
言律语言包管理器

支持包的发布、安装、依赖管理
"""

import os
import json
import shutil
import zipfile
import requests
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class PackageInfo:
    """包信息"""
    name: str
    version: str
    description: str = ""
    author: str = ""
    dependencies: Dict[str, str] = field(default_factory=dict)
    entry_point: str = "main.yan"
    keywords: List[str] = field(default_factory=list)
    license: str = "MIT"


@dataclass
class PackageRegistry:
    """包注册表"""
    packages: Dict[str, PackageInfo] = field(default_factory=dict)
    
    def add_package(self, package: PackageInfo):
        """添加包"""
        self.packages[package.name] = package
    
    def get_package(self, name: str) -> Optional[PackageInfo]:
        """获取包"""
        return self.packages.get(name)
    
    def list_packages(self) -> List[PackageInfo]:
        """列出所有包"""
        return list(self.packages.values())


class PackageManager:
    """包管理器"""
    
    def __init__(self, registry_url: str = "https://registry.yanlv.org"):
        """
        初始化包管理器
        
        Args:
            registry_url: 包注册表URL
        """
        self.registry_url = registry_url
        self.local_registry = PackageRegistry()
        self.install_dir = Path.home() / ".yanlv" / "packages"
        self.cache_dir = Path.home() / ".yanlv" / "cache"
        
        # 创建目录
        self.install_dir.mkdir(parents=True, exist_ok=True)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
    
    def create_package(self, name: str, version: str = "0.1.0",
                      description: str = "", author: str = "") -> PackageInfo:
        """
        创建新包
        
        Args:
            name: 包名
            version: 版本
            description: 描述
            author: 作者
            
        Returns:
            包信息
        """
        package = PackageInfo(
            name=name,
            version=version,
            description=description,
            author=author
        )
        
        # 创建包目录
        package_dir = Path(name)
        package_dir.mkdir(exist_ok=True)
        
        # 创建package.json
        self._write_package_json(package_dir, package)
        
        # 创建main.yan
        main_file = package_dir / "main.yan"
        if not main_file.exists():
            main_file.write_text(f'// {name} 包\n输出"Hello from {name}!"\n', encoding='utf-8')
        
        # 创建README.md
        readme_file = package_dir / "README.md"
        if not readme_file.exists():
            readme_file.write_text(f'# {name}\n\n{description}\n', encoding='utf-8')
        
        return package
    
    def _write_package_json(self, package_dir: Path, package: PackageInfo):
        """写入package.json"""
        package_json = {
            'name': package.name,
            'version': package.version,
            'description': package.description,
            'author': package.author,
            'dependencies': package.dependencies,
            'entry_point': package.entry_point,
            'keywords': package.keywords,
            'license': package.license
        }
        
        with open(package_dir / "package.json", 'w', encoding='utf-8') as f:
            json.dump(package_json, f, indent=2, ensure_ascii=False)
    
    def _read_package_json(self, package_dir: Path) -> Optional[PackageInfo]:
        """读取package.json"""
        package_file = package_dir / "package.json"
        
        if not package_file.exists():
            return None
        
        with open(package_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return PackageInfo(
            name=data['name'],
            version=data['version'],
            description=data.get('description', ''),
            author=data.get('author', ''),
            dependencies=data.get('dependencies', {}),
            entry_point=data.get('entry_point', 'main.yan'),
            keywords=data.get('keywords', []),
            license=data.get('license', 'MIT')
        )
    
    def install(self, package_name: str, version: str = None) -> bool:
        """
        安装包
        
        Args:
            package_name: 包名
            version: 版本（可选）
            
        Returns:
            是否成功
        """
        print(f"正在安装 {package_name}...")
        
        # 检查本地是否已安装
        installed_dir = self.install_dir / package_name
        if installed_dir.exists():
            print(f"{package_name} 已安装")
            return True
        
        # 模拟从远程下载（实际应该从注册表下载）
        # 这里简化处理：从本地查找
        local_package = Path(package_name)
        if local_package.exists():
            # 复制到安装目录
            shutil.copytree(local_package, installed_dir)
            print(f"成功安装 {package_name}")
            return True
        
        print(f"未找到包 {package_name}")
        return False
    
    def uninstall(self, package_name: str) -> bool:
        """
        卸载包
        
        Args:
            package_name: 包名
            
        Returns:
            是否成功
        """
        installed_dir = self.install_dir / package_name
        
        if not installed_dir.exists():
            print(f"{package_name} 未安装")
            return False
        
        shutil.rmtree(installed_dir)
        print(f"成功卸载 {package_name}")
        return True
    
    def publish(self, package_dir: str = ".") -> bool:
        """
        发布包
        
        Args:
            package_dir: 包目录
            
        Returns:
            是否成功
        """
        package_path = Path(package_dir)
        package = self._read_package_json(package_path)
        
        if not package:
            print("未找到 package.json")
            return False
        
        print(f"正在发布 {package.name} v{package.version}...")
        
        # 创建包文件
        package_file = self.cache_dir / f"{package.name}-{package.version}.zip"
        
        with zipfile.ZipFile(package_file, 'w', zipfile.ZIP_DEFLATED) as zf:
            for file in package_path.rglob('*'):
                if file.is_file() and not file.name.startswith('.'):
                    zf.write(file, file.relative_to(package_path))
        
        print(f"成功创建包文件: {package_file}")
        print(f"包名: {package.name}")
        print(f"版本: {package.version}")
        print(f"描述: {package.description}")
        
        # 添加到本地注册表
        self.local_registry.add_package(package)
        
        return True
    
    def list_installed(self) -> List[PackageInfo]:
        """
        列出已安装的包
        
        Returns:
            包列表
        """
        packages = []
        
        for package_dir in self.install_dir.iterdir():
            if package_dir.is_dir():
                package = self._read_package_json(package_dir)
                if package:
                    packages.append(package)
        
        return packages
    
    def search(self, keyword: str) -> List[PackageInfo]:
        """
        搜索包
        
        Args:
            keyword: 关键词
            
        Returns:
            匹配的包列表
        """
        results = []
        
        # 搜索本地注册表
        for package in self.local_registry.list_packages():
            if (keyword.lower() in package.name.lower() or
                keyword.lower() in package.description.lower() or
                keyword in package.keywords):
                results.append(package)
        
        return results
    
    def update(self, package_name: str = None) -> bool:
        """
        更新包
        
        Args:
            package_name: 包名（可选，不指定则更新所有）
            
        Returns:
            是否成功
        """
        if package_name:
            print(f"正在更新 {package_name}...")
            # 简化处理：重新安装
            return self.install(package_name)
        else:
            print("正在更新所有包...")
            success = True
            for package in self.list_installed():
                if not self.install(package.name):
                    success = False
            return success
    
    def info(self, package_name: str) -> Optional[PackageInfo]:
        """
        查看包信息
        
        Args:
            package_name: 包名
            
        Returns:
            包信息
        """
        # 先检查已安装的包
        installed_dir = self.install_dir / package_name
        if installed_dir.exists():
            return self._read_package_json(installed_dir)
        
        # 再检查本地注册表
        return self.local_registry.get_package(package_name)


# ============================================================================
# 命令行接口
# ============================================================================

def main():
    """命令行主函数"""
    import sys
    
    if len(sys.argv) < 2:
        print("用法: yanlv-pm <command> [args]")
        print("命令:")
        print("  create <name>     创建新包")
        print("  install <name>    安装包")
        print("  uninstall <name>  卸载包")
        print("  publish           发布包")
        print("  list              列出已安装的包")
        print("  search <keyword>  搜索包")
        print("  update [name]     更新包")
        print("  info <name>       查看包信息")
        return
    
    manager = PackageManager()
    command = sys.argv[1]
    
    if command == "create":
        if len(sys.argv) < 3:
            print("用法: yanlv-pm create <name>")
            return
        name = sys.argv[2]
        package = manager.create_package(name)
        print(f"成功创建包 {name}")
    
    elif command == "install":
        if len(sys.argv) < 3:
            print("用法: yanlv-pm install <name>")
            return
        name = sys.argv[2]
        manager.install(name)
    
    elif command == "uninstall":
        if len(sys.argv) < 3:
            print("用法: yanlv-pm uninstall <name>")
            return
        name = sys.argv[2]
        manager.uninstall(name)
    
    elif command == "publish":
        manager.publish()
    
    elif command == "list":
        packages = manager.list_installed()
        if packages:
            print("已安装的包:")
            for package in packages:
                print(f"  {package.name} v{package.version}")
        else:
            print("没有已安装的包")
    
    elif command == "search":
        if len(sys.argv) < 3:
            print("用法: yanlv-pm search <keyword>")
            return
        keyword = sys.argv[2]
        results = manager.search(keyword)
        if results:
            print("搜索结果:")
            for package in results:
                print(f"  {package.name} v{package.version} - {package.description}")
        else:
            print("未找到匹配的包")
    
    elif command == "update":
        name = sys.argv[2] if len(sys.argv) > 2 else None
        manager.update(name)
    
    elif command == "info":
        if len(sys.argv) < 3:
            print("用法: yanlv-pm info <name>")
            return
        name = sys.argv[2]
        package = manager.info(name)
        if package:
            print(f"包名: {package.name}")
            print(f"版本: {package.version}")
            print(f"描述: {package.description}")
            print(f"作者: {package.author}")
            print(f"入口: {package.entry_point}")
            print(f"许可证: {package.license}")
        else:
            print(f"未找到包 {name}")
    
    else:
        print(f"未知命令: {command}")


# ============================================================================
# 导出
# ============================================================================

__all__ = [
    'PackageInfo',
    'PackageRegistry',
    'PackageManager',
    'main',
]


if __name__ == '__main__':
    main()
