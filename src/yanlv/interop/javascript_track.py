"""
JavaScript轨实现

通过Node.js执行JavaScript代码，支持异步操作和npm包
"""

import subprocess
import json
import os
from typing import Any, Dict, List, Optional

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


class JavaScriptTrack(Track):
    """JavaScript轨 - 嵌入JavaScript代码"""

    def __init__(self, node_path: str = "node"):
        """
        初始化JavaScript轨

        Args:
            node_path: Node.js可执行文件路径
        """
        self.node_path = node_path
        self.context: Dict[str, Any] = {}
        self._check_node_available()

    def _check_node_available(self) -> bool:
        """检查Node.js是否可用"""
        try:
            result = subprocess.run(
                [self.node_path, "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.returncode == 0
        except:
            return False

    def execute(self, code: str, context: Dict[str, Any]) -> Any:
        """
        执行JavaScript代码

        支持三种模式：
        1. 表达式模式 - 返回表达式值
        2. 语句模式 - 执行语句，返回undefined
        3. 异步模式 - 支持async/await
        """
        # 合并上下文
        merged_context = {**self.context, **context}

        # 构建完整的JS代码
        js_code = self._build_js_code(code, merged_context)

        # 执行Node.js
        try:
            result = subprocess.run(
                [self.node_path, "-e", js_code],
                capture_output=True,
                text=True,
                timeout=30,
                encoding='utf-8'
            )

            if result.returncode != 0:
                error_msg = result.stderr.strip() or "未知错误"
                raise RuntimeError(f"JavaScript执行错误: {error_msg}")

            # 解析JSON输出
            output = result.stdout.strip()
            if output:
                try:
                    return json.loads(output)
                except json.JSONDecodeError:
                    # 如果不是JSON，返回原始字符串
                    return output
            return None

        except subprocess.TimeoutExpired:
            raise RuntimeError("JavaScript执行超时（30秒）")
        except FileNotFoundError:
            raise RuntimeError(f"未找到Node.js: {self.node_path}")

    def _build_js_code(self, code: str, context: Dict[str, Any]) -> str:
        """构建完整的JavaScript代码"""
        # 将上下文变量注入到JS环境
        context_json = json.dumps(context, ensure_ascii=False)

        # 检测是否包含return语句
        has_return = 'return ' in code or 'return;' in code

        # 检测是否是异步代码
        is_async = 'await ' in code or 'async ' in code

        if is_async:
            # 异步代码包装
            js_code = f"""
// 注入上下文
const __context = {context_json};
Object.assign(global, __context);

// 异步执行
(async () => {{
    try {{
        {code}
    }} catch (error) {{
        console.error('Error:', error.message);
        process.exit(1);
    }}
}})();
"""
        elif has_return:
            # 函数代码包装
            js_code = f"""
// 注入上下文
const __context = {context_json};
Object.assign(global, __context);

// 执行并输出
const __result = (function() {{
    {code}
}})();

if (typeof __result !== 'undefined') {{
    console.log(JSON.stringify(__result));
}}
"""
        else:
            # 表达式或语句包装
            js_code = f"""
// 注入上下文
const __context = {context_json};
Object.assign(global, __context);

// 执行代码
{code}

// 输出结果（如果有__result变量）
if (typeof __result !== 'undefined') {{
    console.log(JSON.stringify(__result));
}}
"""

        return js_code

    def validate(self, code: str) -> Dict[str, Any]:
        """验证JavaScript代码语法"""
        try:
            # 使用Node.js的--check参数验证语法
            result = subprocess.run(
                [self.node_path, "--check", "-e", code],
                capture_output=True,
                text=True,
                timeout=5
            )

            if result.returncode == 0:
                return {"valid": True, "errors": []}
            else:
                error_msg = result.stderr.strip()
                return {"valid": False, "errors": [error_msg]}

        except subprocess.TimeoutExpired:
            return {"valid": False, "errors": ["验证超时"]}
        except Exception as e:
            return {"valid": False, "errors": [str(e)]}

    def get_capabilities(self) -> List[str]:
        """JavaScript轨能力"""
        return [
            "async",           # 支持异步（Promise, async/await）
            "modules",         # 支持ES6模块
            "classes",         # 支持类
            "exceptions",      # 支持异常处理
            "json",            # 原生JSON支持
            "npm",             # 支持npm包
            "promises",        # 支持Promise
            "arrow_functions", # 支持箭头函数
        ]

    def convert_type(self, value: Any, target_type: str) -> Any:
        """类型转换（JS <-> Python）"""
        if target_type == "array":
            if isinstance(value, (list, tuple)):
                return list(value)
            else:
                return [value]
        elif target_type == "object":
            if isinstance(value, dict):
                return dict(value)
            else:
                return {"value": value}
        elif target_type == "number":
            if isinstance(value, (int, float)):
                return value
            else:
                try:
                    return float(value)
                except:
                    return 0
        elif target_type == "string":
            return str(value)
        elif target_type == "boolean":
            if isinstance(value, bool):
                return value
            else:
                return bool(value)

        return value

    def install_package(self, package_name: str) -> bool:
        """
        安装npm包

        Args:
            package_name: 包名

        Returns:
            是否安装成功
        """
        try:
            result = subprocess.run(
                ["npm", "install", package_name],
                capture_output=True,
                text=True,
                timeout=60
            )
            return result.returncode == 0
        except:
            return False


# ============================================================================
# 使用示例
# ============================================================================

def example_javascript_usage():
    """JavaScript轨使用示例"""
    print("\n" + "=" * 60)
    print("JavaScript轨使用示例")
    print("=" * 60)

    try:
        track = JavaScriptTrack()

        # 检查Node.js是否可用
        if not track._check_node_available():
            print("警告: Node.js不可用，跳过测试")
            return

        # 示例1: 简单表达式
        print("\n--- 示例1: 简单表达式 ---")
        result = track.execute("2 ** 10", {})
        print(f"2 ** 10 = {result}")

        # 示例2: 数组操作
        print("\n--- 示例2: 数组操作 ---")
        code = """
const arr = [1, 2, 3, 4, 5];
const result = arr.map(x => x * x).reduce((a, b) => a + b, 0);
console.log(JSON.stringify(result));
"""
        result = track.execute(code, {})
        print(f"平方和 = {result}")

        # 示例3: JSON处理
        print("\n--- 示例3: JSON处理 ---")
        code = """
const data = {
    name: "张三",
    age: 25,
    skills: ["JavaScript", "Python", "SQL"]
};
const jsonStr = JSON.stringify(data);
const parsed = JSON.parse(jsonStr);
console.log(JSON.stringify(parsed));
"""
        result = track.execute(code, {})
        print(f"JSON结果: {result}")

        # 示例4: 使用上下文
        print("\n--- 示例4: 使用上下文 ---")
        context = {"x": 10, "y": 20}
        result = track.execute("console.log(JSON.stringify(x + y));", context)
        print(f"x + y = {result}")

        # 示例5: 异步操作（模拟）
        print("\n--- 示例5: 异步操作 ---")
        async_code = """
const delay = (ms) => new Promise(resolve => setTimeout(resolve, ms));

await delay(100);
const result = "异步执行完成";
console.log(JSON.stringify(result));
"""
        result = track.execute(async_code, {})
        print(f"异步结果: {result}")

        # 示例6: 代码验证
        print("\n--- 示例6: 代码验证 ---")
        valid_result = track.validate("const x = 10;")
        print(f"验证有效代码: {valid_result}")

        invalid_result = track.validate("const x = ")
        print(f"验证无效代码: {invalid_result}")

        # 示例7: 查看能力
        print("\n--- 示例7: 轨的能力 ---")
        capabilities = track.get_capabilities()
        print(f"JavaScript轨能力: {capabilities}")

    except Exception as e:
        print(f"错误: {e}")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    example_javascript_usage()
