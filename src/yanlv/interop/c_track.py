"""
C语言轨实现

通过ctypes实现与C语言的互操作，支持编译C代码和调用C函数
"""

import ctypes
from ctypes import *
import tempfile
import subprocess
import os
import platform
from typing import Any, Dict, List, Optional, Union

# 导入Track基类
try:
    from .track_base import Track
except ImportError:
    try:
        from yanlv.interop.track_base import Track
    except ImportError:
        from abc import ABC, abstractmethod
        class Track(ABC):
            @abstractmethod
            def execute(self, code: str, context: Dict[str, Any]) -> Any:
                pass
            
            @abstractmethod
            def validate(self, code: str) -> Dict[str, Any]:
                pass
            
            @abstractmethod
            def get_capabilities(self) -> List[str]:
                pass
            
            @abstractmethod
            def convert_type(self, value: Any, target_type: str) -> Any:
                pass


class CTrack(Track):
    """C语言轨 - 使用ctypes实现"""

    def __init__(self, compiler: str = None):
        """
        初始化C轨

        Args:
            compiler: C编译器 (gcc, clang, cl等)，None则自动检测
        """
        # 自动检测编译器
        if compiler is None:
            self.compiler = self._detect_compiler()
        else:
            self.compiler = compiler
        
        # 已加载的库
        self.libraries: Dict[str, ctypes.CDLL] = {}
        
        # 已注册的函数
        self.functions: Dict[str, Any] = {}
        
        # 类型映射
        self.type_map = {
            "int": c_int,
            "unsigned int": c_uint,
            "long": c_long,
            "unsigned long": c_ulong,
            "float": c_float,
            "double": c_double,
            "char": c_char,
            "char*": c_char_p,
            "void": None,
            "int*": POINTER(c_int),
            "float*": POINTER(c_float),
            "double*": POINTER(c_double),
            "long*": POINTER(c_long),
        }
        
        # 分配的内存（用于自动清理）
        self.allocated_memory: List[Any] = []
        
        # 编译选项
        self.compile_flags = ["-shared", "-fPIC", "-O2"]

    def _detect_compiler(self) -> Optional[str]:
        """自动检测系统中的C编译器"""
        compilers = ["gcc", "clang", "cc"]
        
        for compiler in compilers:
            try:
                result = subprocess.run(
                    [compiler, "--version"],
                    capture_output=True,
                    timeout=2,
                    shell=True  # Windows下需要shell=True
                )
                if result.returncode == 0:
                    return compiler
            except:
                continue
        
        # Windows下检查gcc (MinGW)
        if platform.system() == "Windows":
            try:
                result = subprocess.run(
                    ["gcc", "--version"],
                    capture_output=True,
                    timeout=2,
                    shell=True
                )
                if result.returncode == 0:
                    return "gcc"
            except:
                pass
        
        return None

    def compile_code(self, c_code: str, 
                     output_name: str = None,
                     include_dirs: List[str] = None,
                     libraries: List[str] = None) -> str:
        """
        编译C代码为共享库

        Args:
            c_code: C源代码
            output_name: 输出文件名（不含扩展名）
            include_dirs: 包含目录列表
            libraries: 链接库列表

        Returns:
            共享库路径
        """
        if not self.compiler:
            raise RuntimeError("未找到C编译器，无法编译代码")
        
        # 创建临时文件
        if output_name is None:
            output_name = tempfile.mktemp()
        
        # 根据平台确定输出文件名
        if platform.system() == "Windows":
            lib_path = output_name + ".dll"
        else:
            lib_path = output_name + ".so"
        
        # 写入C代码到临时文件
        c_file = tempfile.mktemp(suffix='.c')
        try:
            with open(c_file, 'w', encoding='utf-8') as f:
                f.write(c_code)
            
            # 构建编译命令
            if self.compiler in ["gcc", "clang", "cc"]:
                cmd = [self.compiler] + self.compile_flags + ["-o", lib_path, c_file]
                
                # 添加包含目录
                if include_dirs:
                    for dir in include_dirs:
                        cmd.extend(["-I", dir])
                
                # 添加链接库
                if libraries:
                    for lib in libraries:
                        cmd.extend(["-l", lib])
            
            elif self.compiler == "cl":
                # MSVC编译器
                cmd = [
                    "cl", "/LD", "/O2",
                    c_file,
                    f"/Fe{lib_path}",
                    "/link"
                ]
            else:
                raise ValueError(f"不支持的编译器: {self.compiler}")
            
            # 执行编译
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode != 0:
                error_msg = result.stderr or result.stdout
                raise RuntimeError(f"编译失败:\n{error_msg}")
            
            if not os.path.exists(lib_path):
                raise RuntimeError(f"编译成功但未生成库文件: {lib_path}")
            
            return lib_path
            
        finally:
            # 清理临时C文件
            if os.path.exists(c_file):
                os.remove(c_file)

    def load_library(self, lib_path: str) -> ctypes.CDLL:
        """
        加载共享库

        Args:
            lib_path: 库文件路径

        Returns:
            加载的库对象
        """
        try:
            # 检查文件是否存在
            if not os.path.exists(lib_path):
                raise FileNotFoundError(f"库文件不存在: {lib_path}")
            
            # 加载库
            lib = ctypes.CDLL(lib_path)
            self.libraries[lib_path] = lib
            return lib
            
        except Exception as e:
            raise RuntimeError(f"加载库失败: {e}")

    def register_function(self, 
                         func_name: str,
                         lib: ctypes.CDLL,
                         arg_types: List[str] = None,
                         return_type: str = "int"):
        """
        注册C函数

        Args:
            func_name: 函数名
            lib: 共享库对象
            arg_types: 参数类型列表（字符串）
            return_type: 返回类型（字符串）
        """
        try:
            # 获取函数
            func = getattr(lib, func_name)
            
            # 设置参数类型
            if arg_types:
                func.argtypes = [
                    self.type_map.get(t, c_int)
                    for t in arg_types
                ]
            else:
                func.argtypes = []
            
            # 设置返回类型
            func.restype = self.type_map.get(return_type, c_int)
            
            # 保存函数
            self.functions[func_name] = {
                'function': func,
                'arg_types': arg_types or [],
                'return_type': return_type
            }
            
            return func
            
        except AttributeError:
            raise ValueError(f"函数 '{func_name}' 在库中不存在")

    def call_function(self, func_name: str, *args) -> Any:
        """
        调用C函数

        Args:
            func_name: 函数名
            *args: 参数

        Returns:
            函数返回值
        """
        if func_name not in self.functions:
            raise ValueError(f"函数 '{func_name}' 未注册")
        
        func_info = self.functions[func_name]
        func = func_info['function']
        arg_types = func_info['arg_types']
        
        # 转换参数
        converted_args = []
        for i, (arg, arg_type) in enumerate(zip(args, arg_types)):
            converted = self._convert_arg(arg, arg_type)
            converted_args.append(converted)
        
        # 调用函数
        result = func(*converted_args)
        
        # 转换返回值
        return self._convert_return(result, func_info['return_type'])

    def _convert_arg(self, arg: Any, arg_type: str) -> Any:
        """转换参数类型"""
        if arg_type == "char*":
            if isinstance(arg, str):
                return arg.encode('utf-8')
            return bytes(arg)
        elif arg_type in ["int", "long", "unsigned int", "unsigned long"]:
            return int(arg)
        elif arg_type in ["float", "double"]:
            return float(arg)
        elif arg_type.endswith('*'):
            # 指针类型
            return arg
        
        return arg

    def _convert_return(self, result: Any, return_type: str) -> Any:
        """转换返回值类型"""
        if return_type == "char*":
            if result:
                return result.decode('utf-8')
            return ""
        elif return_type in ["int", "long", "unsigned int", "unsigned long"]:
            return int(result)
        elif return_type in ["float", "double"]:
            return float(result)
        
        return result

    def execute(self, code: str, context: Dict[str, Any]) -> Any:
        """
        执行C代码

        支持两种模式：
        1. 函数调用: "call func_name arg1 arg2 ..."
        2. 编译执行: 编译C代码并执行
        """
        code = code.strip()
        
        # 检查是否是函数调用
        if code.startswith("call "):
            parts = code[5:].split()
            func_name = parts[0]
            args = []
            
            for part in parts[1:]:
                # 尝试转换为数值
                try:
                    if '.' in part:
                        args.append(float(part))
                    else:
                        args.append(int(part))
                except:
                    args.append(part)
            
            return self.call_function(func_name, *args)
        
        # 否则编译并执行
        # 包装为完整的C程序
        wrapped_code = f"""
#include <stdio.h>
#include <stdlib.h>

{code}
"""
        
        # 编译
        lib_path = self.compile_code(wrapped_code)
        
        try:
            # 加载
            lib = self.load_library(lib_path)
            
            # 如果有main函数，执行它
            if hasattr(lib, 'main'):
                result = lib.main()
                return result
            
            return None
            
        finally:
            # 清理临时库文件
            if os.path.exists(lib_path):
                try:
                    os.remove(lib_path)
                except:
                    pass

    def validate(self, code: str) -> Dict[str, Any]:
        """验证C代码语法"""
        if not self.compiler:
            return {"valid": False, "errors": ["未找到C编译器"]}
        
        try:
            # 创建临时文件
            c_file = tempfile.mktemp(suffix='.c')
            with open(c_file, 'w', encoding='utf-8') as f:
                f.write(code)
            
            try:
                # 使用编译器检查语法
                if self.compiler in ["gcc", "clang", "cc"]:
                    result = subprocess.run(
                        [self.compiler, "-fsyntax-only", c_file],
                        capture_output=True,
                        text=True,
                        timeout=5
                    )
                elif self.compiler == "cl":
                    result = subprocess.run(
                        ["cl", "/Zs", c_file],
                        capture_output=True,
                        text=True,
                        timeout=5
                    )
                else:
                    return {"valid": False, "errors": [f"不支持的编译器: {self.compiler}"]}
                
                if result.returncode == 0:
                    return {"valid": True, "errors": []}
                else:
                    errors = result.stderr or result.stdout
                    return {"valid": False, "errors": [errors.strip()]}
                    
            finally:
                if os.path.exists(c_file):
                    os.remove(c_file)
                    
        except Exception as e:
            return {"valid": False, "errors": [str(e)]}

    def get_capabilities(self) -> List[str]:
        """C轨能力"""
        capabilities = [
            "native_code",      # 原生代码执行
            "shared_libraries", # 共享库支持
            "compilation",      # 代码编译
            "pointers",         # 指针操作
            "manual_memory",    # 手动内存管理
            "low_level",        # 底层操作
            "high_performance", # 高性能
        ]
        
        if self.compiler:
            capabilities.append(f"compiler_{self.compiler}")
        
        return capabilities

    def convert_type(self, value: Any, target_type: str) -> Any:
        """类型转换"""
        return self._convert_arg(value, target_type)

    def malloc(self, size: int) -> ctypes.c_void_p:
        """
        分配内存

        Args:
            size: 字节数

        Returns:
            内存指针
        """
        ptr = ctypes.create_string_buffer(size)
        self.allocated_memory.append(ptr)
        return ptr

    def free_all(self):
        """释放所有分配的内存"""
        self.allocated_memory.clear()

    def __del__(self):
        """析构时清理"""
        self.free_all()


# ============================================================================
# 使用示例
# ============================================================================

def example_c_usage():
    """C轨使用示例"""
    print("\n" + "=" * 70)
    print("C语言轨使用示例")
    print("=" * 70)

    try:
        track = CTrack()
        
        # 检查编译器
        if not track.compiler:
            print("\n警告: 未找到C编译器，跳过编译测试")
            print("请安装gcc或clang以使用完整功能")
            return
        
        print(f"\n检测到编译器: {track.compiler}")
        
        # 示例1: 编译简单的C代码
        print("\n--- 示例1: 编译C代码 ---")
        c_code = """
int add(int a, int b) {
    return a + b;
}

int multiply(int a, int b) {
    return a * b;
}

double square(double x) {
    return x * x;
}
"""
        
        print("编译C代码...")
        lib_path = track.compile_code(c_code)
        print(f"编译成功: {lib_path}")
        
        # 加载库
        lib = track.load_library(lib_path)
        print("库加载成功")
        
        # 注册函数
        track.register_function("add", lib, ["int", "int"], "int")
        track.register_function("multiply", lib, ["int", "int"], "int")
        track.register_function("square", lib, ["double"], "double")
        print("函数注册成功: add, multiply, square")
        
        # 调用函数
        print("\n--- 示例2: 调用C函数 ---")
        result1 = track.call_function("add", 3, 5)
        print(f"add(3, 5) = {result1}")
        
        result2 = track.call_function("multiply", 4, 7)
        print(f"multiply(4, 7) = {result2}")
        
        result3 = track.call_function("square", 4.0)
        print(f"square(4.0) = {result3}")
        
        # 示例3: 使用函数调用语法
        print("\n--- 示例3: 使用函数调用语法 ---")
        result = track.execute("call add 10 20")
        print(f"call add 10 20 = {result}")
        
        # 示例4: 代码验证
        print("\n--- 示例4: 代码验证 ---")
        valid_code = "int main() { return 0; }"
        invalid_code = "int main() { return "
        
        valid_result = track.validate(valid_code)
        print(f"验证有效代码: {valid_result}")
        
        invalid_result = track.validate(invalid_code)
        print(f"验证无效代码: {invalid_result}")
        
        # 示例5: 查看能力
        print("\n--- 示例5: 轨的能力 ---")
        capabilities = track.get_capabilities()
        print(f"C轨能力: {', '.join(capabilities)}")
        
        # 清理
        if os.path.exists(lib_path):
            os.remove(lib_path)
        
    except Exception as e:
        print(f"\n错误: {e}")
        import traceback
        traceback.print_exc()

    print("\n" + "=" * 70)


if __name__ == "__main__":
    example_c_usage()
