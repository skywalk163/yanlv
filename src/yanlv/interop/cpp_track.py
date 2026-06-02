"""
C++语言轨实现

支持C++特性的互操作，包括类、模板、异常、STL等
"""

import ctypes
from ctypes import *
import tempfile
import subprocess
import os
import platform
from typing import Any, Dict, List, Optional, Union

# 导入C轨基类
try:
    from .c_track import CTrack
except ImportError:
    try:
        from yanlv.interop.c_track import CTrack
    except ImportError:
        # 如果导入失败，定义简化版本
        from abc import ABC, abstractmethod
        class Track(ABC):
            @abstractmethod
            def execute(self, code: str, context: Dict[str, Any]) -> Any:
                pass
        CTrack = Track


class CPPTrack(CTrack):
    """C++语言轨 - 支持C++特性"""

    def __init__(self, compiler: str = None, 
                 cpp_standard: str = "c++17"):
        """
        初始化C++轨

        Args:
            compiler: C++编译器 (g++, clang++, MSVC等)
            cpp_standard: C++标准 (c++11, c++14, c++17, c++20)
        """
        super().__init__(compiler)
        
        self.cpp_standard = cpp_standard
        
        # C++类型映射（扩展C的类型映射）
        self.type_map.update({
            "std::string": c_char_p,
            "std::vector<int>*": c_void_p,
            "std::vector<double>*": c_void_p,
            "std::map*": c_void_p,
        })
        
        # 已注册的类
        self.classes: Dict[str, Dict] = {}
        
        # C++编译选项
        self.compile_flags = [
            "-shared", 
            "-fPIC", 
            f"-std={cpp_standard}",
            "-O2"
        ]

    def _detect_compiler(self) -> Optional[str]:
        """自动检测C++编译器"""
        compilers = ["g++", "clang++"]
        
        for compiler in compilers:
            try:
                result = subprocess.run(
                    [compiler, "--version"],
                    capture_output=True,
                    timeout=2,
                    shell=True
                )
                if result.returncode == 0:
                    return compiler
            except:
                continue
        
        return None

    def compile_code(self, cpp_code: str, 
                     output_name: str = None,
                     include_dirs: List[str] = None,
                     libraries: List[str] = None) -> str:
        """
        编译C++代码为共享库

        Args:
            cpp_code: C++源代码
            output_name: 输出文件名
            include_dirs: 包含目录
            libraries: 链接库

        Returns:
            共享库路径
        """
        if not self.compiler:
            raise RuntimeError("未找到C++编译器")
        
        # 创建临时文件
        if output_name is None:
            output_name = tempfile.mktemp()
        
        # 确定输出文件名
        if platform.system() == "Windows":
            lib_path = output_name + ".dll"
        else:
            lib_path = output_name + ".so"
        
        # 写入C++代码
        cpp_file = tempfile.mktemp(suffix='.cpp')
        try:
            with open(cpp_file, 'w', encoding='utf-8') as f:
                f.write(cpp_code)
            
            # 构建编译命令
            cmd = [self.compiler] + self.compile_flags + ["-o", lib_path, cpp_file]
            
            # 添加包含目录
            if include_dirs:
                for dir in include_dirs:
                    cmd.extend(["-I", dir])
            
            # 添加链接库
            if libraries:
                for lib in libraries:
                    cmd.extend(["-l", lib])
            
            # 执行编译
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode != 0:
                error_msg = result.stderr or result.stdout
                raise RuntimeError(f"C++编译失败:\n{error_msg}")
            
            return lib_path
            
        finally:
            if os.path.exists(cpp_file):
                os.remove(cpp_file)

    def register_class(self, 
                      class_name: str,
                      lib: ctypes.CDLL,
                      methods: Dict[str, Dict]):
        """
        注册C++类

        Args:
            class_name: 类名
            lib: 共享库
            methods: 方法字典 {
                "method_name": {
                    "args": ["int", "double"],
                    "return": "int",
                    "is_static": False
                }
            }
        """
        class_info = {
            'name': class_name,
            'library': lib,
            'methods': {}
        }
        
        # 注册每个方法
        for method_name, method_info in methods.items():
            # C++方法名修饰（简化版，实际需要根据编译器处理）
            mangled_name = f"_ZN{len(class_name)}{class_name}{len(method_name)}{method_name}E"
            
            # 尝试不同的名称修饰方式
            names_to_try = [
                mangled_name,
                f"{class_name}_{method_name}",  # 简化名称
                method_name,  # 原始名称
            ]
            
            for name in names_to_try:
                try:
                    func = getattr(lib, name)
                    
                    # 设置类型
                    if method_info.get('args'):
                        func.argtypes = [
                            self.type_map.get(t, c_int)
                            for t in method_info['args']
                        ]
                    
                    func.restype = self.type_map.get(
                        method_info.get('return', 'void'), 
                        c_int
                    )
                    
                    class_info['methods'][method_name] = {
                        'function': func,
                        'info': method_info
                    }
                    break
                    
                except AttributeError:
                    continue
        
        self.classes[class_name] = class_info

    def call_method(self, 
                   class_name: str,
                   method_name: str,
                   *args) -> Any:
        """
        调用C++类方法

        Args:
            class_name: 类名
            method_name: 方法名
            *args: 参数

        Returns:
            方法返回值
        """
        if class_name not in self.classes:
            raise ValueError(f"类 '{class_name}' 未注册")
        
        class_info = self.classes[class_name]
        
        if method_name not in class_info['methods']:
            raise ValueError(f"方法 '{method_name}' 未注册")
        
        method = class_info['methods'][method_name]
        func = method['function']
        
        # 转换参数
        converted_args = []
        arg_types = method['info'].get('args', [])
        
        for arg, arg_type in zip(args, arg_types):
            converted = self._convert_arg(arg, arg_type)
            converted_args.append(converted)
        
        # 调用方法
        result = func(*converted_args)
        
        # 转换返回值
        return self._convert_return(
            result, 
            method['info'].get('return', 'void')
        )

    def execute(self, code: str, context: Dict[str, Any]) -> Any:
        """
        执行C++代码

        支持三种模式：
        1. 函数调用: "call func_name args..."
        2. 方法调用: "call Class.method args..."
        3. 编译执行: 编译C++代码并执行
        """
        code = code.strip()
        
        # 检查是否是方法调用
        if code.startswith("call ") and "." in code:
            parts = code[5:].split()
            class_method = parts[0]
            class_name, method_name = class_method.split(".", 1)
            
            args = []
            for part in parts[1:]:
                try:
                    if '.' in part:
                        args.append(float(part))
                    else:
                        args.append(int(part))
                except:
                    args.append(part)
            
            return self.call_method(class_name, method_name, *args)
        
        # 其他情况使用父类实现
        return super().execute(code, context)

    def get_capabilities(self) -> List[str]:
        """C++轨能力"""
        capabilities = super().get_capabilities()
        
        cpp_capabilities = [
            "classes",          # 类支持
            "templates",        # 模板支持
            "exceptions",       # 异常处理
            "stl",              # STL支持
            "inheritance",      # 继承
            "polymorphism",     # 多态
            f"cpp_{self.cpp_standard}",  # C++标准
        ]
        
        return capabilities + cpp_capabilities

    def validate(self, code: str) -> Dict[str, Any]:
        """验证C++代码语法"""
        if not self.compiler:
            return {"valid": False, "errors": ["未找到C++编译器"]}
        
        try:
            cpp_file = tempfile.mktemp(suffix='.cpp')
            with open(cpp_file, 'w', encoding='utf-8') as f:
                f.write(code)
            
            try:
                result = subprocess.run(
                    [self.compiler, f"-std={self.cpp_standard}", "-fsyntax-only", cpp_file],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                
                if result.returncode == 0:
                    return {"valid": True, "errors": []}
                else:
                    errors = result.stderr or result.stdout
                    return {"valid": False, "errors": [errors.strip()]}
                    
            finally:
                if os.path.exists(cpp_file):
                    os.remove(cpp_file)
                    
        except Exception as e:
            return {"valid": False, "errors": [str(e)]}


# ============================================================================
# 使用示例
# ============================================================================

def example_cpp_usage():
    """C++轨使用示例"""
    print("\n" + "=" * 70)
    print("C++语言轨使用示例")
    print("=" * 70)

    try:
        track = CPPTrack()
        
        # 检查编译器
        if not track.compiler:
            print("\n警告: 未找到C++编译器，跳过测试")
            print("请安装g++或clang++以使用完整功能")
            return
        
        print(f"\n检测到编译器: {track.compiler}")
        print(f"C++标准: {track.cpp_standard}")
        
        # 示例1: 编译简单的C++代码
        print("\n--- 示例1: 编译C++代码 ---")
        cpp_code = """
#include <cmath>
#include <string>

extern "C" {
    int add(int a, int b) {
        return a + b;
    }
    
    double power(double base, int exp) {
        return std::pow(base, exp);
    }
    
    int factorial(int n) {
        if (n <= 1) return 1;
        return n * factorial(n - 1);
    }
}
"""
        
        print("编译C++代码...")
        lib_path = track.compile_code(cpp_code)
        print(f"编译成功: {lib_path}")
        
        # 加载库
        lib = track.load_library(lib_path)
        print("库加载成功")
        
        # 注册函数
        track.register_function("add", lib, ["int", "int"], "int")
        track.register_function("power", lib, ["double", "int"], "double")
        track.register_function("factorial", lib, ["int"], "int")
        print("函数注册成功: add, power, factorial")
        
        # 调用函数
        print("\n--- 示例2: 调用C++函数 ---")
        result1 = track.call_function("add", 3, 5)
        print(f"add(3, 5) = {result1}")
        
        result2 = track.call_function("power", 2.0, 10)
        print(f"power(2.0, 10) = {result2}")
        
        result3 = track.call_function("factorial", 5)
        print(f"factorial(5) = {result3}")
        
        # 示例3: 使用STL
        print("\n--- 示例3: 使用STL ---")
        stl_code = """
#include <vector>
#include <algorithm>

extern "C" {
    int sum_array(int* arr, int size) {
        std::vector<int> vec(arr, arr + size);
        int sum = 0;
        for (int x : vec) {
            sum += x;
        }
        return sum;
    }
    
    int find_max(int* arr, int size) {
        std::vector<int> vec(arr, arr + size);
        return *std::max_element(vec.begin(), vec.end());
    }
}
"""
        
        lib_path2 = track.compile_code(stl_code)
        lib2 = track.load_library(lib_path2)
        
        track.register_function("sum_array", lib2, ["int*", "int"], "int")
        track.register_function("find_max", lib2, ["int*", "int"], "int")
        
        # 创建数组
        arr = (c_int * 5)(1, 2, 3, 4, 5)
        result = track.call_function("sum_array", arr, 5)
        print(f"sum_array([1,2,3,4,5]) = {result}")
        
        result = track.call_function("find_max", arr, 5)
        print(f"find_max([1,2,3,4,5]) = {result}")
        
        # 示例4: 代码验证
        print("\n--- 示例4: 代码验证 ---")
        valid_code = """
#include <iostream>
int main() { return 0; }
"""
        invalid_code = """
#include <iostream>
int main() { return
"""
        
        valid_result = track.validate(valid_code)
        print(f"验证有效代码: {valid_result}")
        
        invalid_result = track.validate(invalid_code)
        print(f"验证无效代码: {invalid_result}")
        
        # 示例5: 查看能力
        print("\n--- 示例5: 轨的能力 ---")
        capabilities = track.get_capabilities()
        print(f"C++轨能力: {', '.join(capabilities)}")
        
        # 清理
        if os.path.exists(lib_path):
            os.remove(lib_path)
        if os.path.exists(lib_path2):
            os.remove(lib_path2)
        
    except Exception as e:
        print(f"\n错误: {e}")
        import traceback
        traceback.print_exc()

    print("\n" + "=" * 70)


if __name__ == "__main__":
    example_cpp_usage()
