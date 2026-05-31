"""
言律语言模块系统功能测试
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from yanlv.module_manager import create_module_manager, Module, Namespace


def test_module_creation():
    """测试模块创建"""
    print("\n=== 测试模块创建 ===")
    
    manager = create_module_manager()
    
    # 创建模块
    module = manager.create_module("测试模块")
    print(f"测试1 - 创建模块: {module.name}")
    assert module.name == "测试模块"
    
    # 添加函数
    module.add_function("测试函数", lambda x: x * 2)
    print(f"测试2 - 添加函数: {list(module.functions.keys())}")
    assert "测试函数" in module.functions
    
    # 导出函数
    module.export_item("测试函数")
    print(f"测试3 - 导出函数: {module.exports}")
    assert "测试函数" in module.exports
    
    print("[PASS] 模块创建测试通过")


def test_namespace():
    """测试命名空间"""
    print("\n=== 测试命名空间 ===")
    
    # 创建命名空间
    global_ns = Namespace("global")
    local_ns = Namespace("local", global_ns)
    
    # 添加符号
    global_ns.add_symbol("全局变量", 100)
    local_ns.add_symbol("局部变量", 200)
    
    # 查找符号
    value1 = local_ns.get_symbol("局部变量")
    print(f"测试1 - 查找局部变量: {value1}")
    assert value1 == 200
    
    value2 = local_ns.get_symbol("全局变量")
    print(f"测试2 - 查找全局变量: {value2}")
    assert value2 == 100
    
    # 检查符号存在
    exists = local_ns.has_symbol("全局变量")
    print(f"测试3 - 检查符号存在: {exists}")
    assert exists == True
    
    print("[PASS] 命名空间测试通过")


def test_module_manager():
    """测试模块管理器"""
    print("\n=== 测试模块管理器 ===")
    
    manager = create_module_manager()
    
    # 创建模块
    module1 = manager.create_module("模块1")
    module1.add_function("函数1", lambda x: x + 1)
    module1.export_item("函数1")
    
    module2 = manager.create_module("模块2")
    module2.add_function("函数2", lambda x: x * 2)
    module2.export_item("函数2")
    
    # 检查模块存在
    has_module1 = manager.has_module("模块1")
    print(f"测试1 - 检查模块存在: {has_module1}")
    assert has_module1 == True
    
    # 获取模块
    module = manager.get_module("模块1")
    print(f"测试2 - 获取模块: {module.name}")
    assert module.name == "模块1"
    
    # 导入模块
    success = manager.import_module("模块1")
    print(f"测试3 - 导入模块: {success}")
    assert success == True
    
    print("[PASS] 模块管理器测试通过")


def test_import_from_module():
    """测试从模块导入"""
    print("\n=== 测试从模块导入 ===")
    
    manager = create_module_manager()
    
    # 创建模块
    module = manager.create_module("数学工具")
    module.add_function("平方", lambda x: x * x)
    module.add_function("立方", lambda x: x * x * x)
    module.export_item("平方")
    module.export_item("立方")
    
    # 从模块导入
    success = manager.import_from_module("数学工具", ["平方", "立方"])
    print(f"测试1 - 从模块导入: {success}")
    assert success == True
    
    # 获取导入的符号
    func = manager.get_symbol("平方")
    print(f"测试2 - 获取导入的函数: {func is not None}")
    assert func is not None
    
    # 测试函数调用
    result = func(5)
    print(f"测试3 - 调用导入的函数: 平方(5) = {result}")
    assert result == 25
    
    print("[PASS] 从模块导入测试通过")


def test_stdlib_modules():
    """测试标准库模块"""
    print("\n=== 测试标准库模块 ===")
    
    # 检查标准库文件是否存在
    stdlib_path = os.path.join(os.path.dirname(__file__), 'stdlib')
    
    math_file = os.path.join(stdlib_path, '数学.yan')
    string_file = os.path.join(stdlib_path, '字符串.yan')
    array_file = os.path.join(stdlib_path, '数组.yan')
    file_file = os.path.join(stdlib_path, '文件.yan')
    
    print(f"测试1 - 数学模块文件存在: {os.path.exists(math_file)}")
    assert os.path.exists(math_file)
    
    print(f"测试2 - 字符串模块文件存在: {os.path.exists(string_file)}")
    assert os.path.exists(string_file)
    
    print(f"测试3 - 数组模块文件存在: {os.path.exists(array_file)}")
    assert os.path.exists(array_file)
    
    print(f"测试4 - 文件模块文件存在: {os.path.exists(file_file)}")
    assert os.path.exists(file_file)
    
    print("[PASS] 标准库模块测试通过")


def run_all_tests():
    """运行所有测试"""
    print("\n" + "="*50)
    print("言律语言模块系统功能测试")
    print("="*50)
    
    try:
        test_module_creation()
        test_namespace()
        test_module_manager()
        test_import_from_module()
        test_stdlib_modules()
        
        print("\n" + "="*50)
        print("[PASS] 所有测试通过！")
        print("="*50)
        return True
    except Exception as e:
        print(f"\n[FAIL] 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
