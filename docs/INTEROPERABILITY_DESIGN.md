# 言律语言互操作能力设计方案

**设计时间：** 2026-06-01
**目标：** 提供与主流语言（Python、JavaScript、SQL等）的互操作能力

---

## 一、设计理念

### 1.1 核心原则

1. **无缝集成** - 在言律代码中直接调用其他语言代码
2. **类型安全** - 自动处理类型转换和类型检查
3. **性能优化** - 最小化跨语言调用开销
4. **错误处理** - 统一的错误处理机制
5. **易于使用** - 简洁的语法和清晰的API

### 1.2 互操作层次

```
┌─────────────────────────────────────┐
│   言律语言代码                        │
├─────────────────────────────────────┤
│   多轨制系统 (Track System)          │
├──────────┬──────────┬───────────────┤
│ Python轨 │ JS轨     │ SQL轨 │ ...   │
├──────────┼──────────┼───────────────┤
│ Python   │ Node.js  │ 数据库 │ ...   │
└──────────┴──────────┴───────────────┘
```

---

## 二、多轨制架构设计

### 2.1 核心接口

```python
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

class Track(ABC):
    """轨基类 - 定义互操作接口"""

    @abstractmethod
    def execute(self, code: str, context: Dict[str, Any]) -> Any:
        """
        执行代码

        Args:
            code: 外部语言代码
            context: 执行上下文（变量、函数等）

        Returns:
            执行结果
        """
        pass

    @abstractmethod
    def validate(self, code: str) -> Dict[str, Any]:
        """
        验证代码

        Args:
            code: 外部语言代码

        Returns:
            验证结果 {"valid": bool, "errors": List[str]}
        """
        pass

    @abstractmethod
    def get_capabilities(self) -> List[str]:
        """
        获取轨的能力

        Returns:
            能力列表，如 ["async", "modules", "classes"]
        """
        pass

    @abstractmethod
    def convert_type(self, value: Any, target_type: str) -> Any:
        """
        类型转换

        Args:
            value: 值
            target_type: 目标类型

        Returns:
            转换后的值
        """
        pass
```

### 2.2 轨管理器

```python
class TrackManager:
    """轨管理器 - 管理所有轨实例"""

    def __init__(self):
        self.tracks: Dict[str, Track] = {}
        self.active_track: Optional[str] = None

    def register_track(self, name: str, track: Track) -> None:
        """注册轨"""
        self.tracks[name] = track

    def get_track(self, name: str) -> Optional[Track]:
        """获取轨"""
        return self.tracks.get(name)

    def execute_in_track(self, track_name: str, code: str,
                        context: Dict[str, Any]) -> Any:
        """在指定轨中执行代码"""
        track = self.get_track(track_name)
        if not track:
            raise ValueError(f"未找到轨: {track_name}")

        return track.execute(code, context)
```

---

## 三、Python轨实现

### 3.1 实现代码

```python
import ast
import sys
from typing import Any, Dict, List
from .track_base import Track

class PythonTrack(Track):
    """Python轨 - 嵌入Python代码"""

    def __init__(self):
        self.globals: Dict[str, Any] = {}
        self.locals: Dict[str, Any] = {}

    def execute(self, code: str, context: Dict[str, Any]) -> Any:
        """
        执行Python代码

        支持三种模式：
        1. 表达式模式 - 返回表达式值
        2. 语句模式 - 执行语句，返回None
        3. 函数模式 - 执行函数定义，返回函数
        """
        # 合并上下文
        exec_globals = {**self.globals, **context}
        exec_locals = self.locals.copy()

        try:
            # 尝试作为表达式执行
            result = eval(code, exec_globals, exec_locals)
            return result
        except SyntaxError:
            # 作为语句执行
            exec(code, exec_globals, exec_locals)

            # 更新全局和局部变量
            self.globals.update(exec_globals)
            self.locals.update(exec_locals)

            # 检查是否定义了函数
            if 'return' in code or 'def ' in code:
                # 提取最后定义的函数
                tree = ast.parse(code)
                for node in reversed(tree.body):
                    if isinstance(node, ast.FunctionDef):
                        return exec_locals.get(node.name)

            return None

    def validate(self, code: str) -> Dict[str, Any]:
        """验证Python代码语法"""
        try:
            ast.parse(code)
            return {"valid": True, "errors": []}
        except SyntaxError as e:
            return {
                "valid": False,
                "errors": [f"语法错误 (行{e.lineno}): {e.msg}"]
            }

    def get_capabilities(self) -> List[str]:
        """Python轨能力"""
        return [
            "async",           # 支持异步
            "modules",         # 支持模块导入
            "classes",         # 支持类定义
            "exceptions",      # 支持异常处理
            "generators",      # 支持生成器
            "decorators",      # 支持装饰器
        ]

    def convert_type(self, value: Any, target_type: str) -> Any:
        """类型转换"""
        type_map = {
            "int": int,
            "float": float,
            "str": str,
            "bool": bool,
            "list": list,
            "dict": dict,
        }

        if target_type in type_map:
            return type_map[target_type](value)

        return value
```

### 3.2 使用示例

```言律
# 示例1: 简单表达式
定结果是 {{python
2 ** 10
}}
输出 结果  # 输出: 1024

# 示例2: 使用Python库
定数据列表是列1 2 3 4 5
定平均值是 {{python
import statistics
statistics.mean(data_list)
}}
输出 平均值

# 示例3: 定义Python函数
定快速排序是函列表：
  {{python
  def quicksort(arr):
      if len(arr) <= 1:
          return arr
      pivot = arr[len(arr) // 2]
      left = [x for x in arr if x < pivot]
      middle = [x for x in arr if x == pivot]
      right = [x for x in arr if x > pivot]
      return quicksort(left) + middle + quicksort(right)
  return quicksort
  }}

定排序结果是快速排序参数列3 1 4 1 5 9 2 6
输出 排序结果
```

---

## 四、JavaScript轨实现

### 4.1 实现代码

```python
import subprocess
import json
from typing import Any, Dict, List
from .track_base import Track

class JavaScriptTrack(Track):
    """JavaScript轨 - 嵌入JavaScript代码"""

    def __init__(self, node_path: str = "node"):
        self.node_path = node_path
        self.context: Dict[str, Any] = {}

    def execute(self, code: str, context: Dict[str, Any]) -> Any:
        """
        执行JavaScript代码

        通过Node.js执行JavaScript代码
        """
        # 构建完整的JS代码
        js_code = self._build_js_code(code, context)

        # 执行Node.js
        try:
            result = subprocess.run(
                [self.node_path, "-e", js_code],
                capture_output=True,
                text=True,
                timeout=10
            )

            if result.returncode != 0:
                raise RuntimeError(f"JavaScript执行错误: {result.stderr}")

            # 解析JSON输出
            output = result.stdout.strip()
            if output:
                return json.loads(output)
            return None

        except subprocess.TimeoutExpired:
            raise RuntimeError("JavaScript执行超时")

    def _build_js_code(self, code: str, context: Dict[str, Any]) -> str:
        """构建完整的JavaScript代码"""
        # 将上下文变量注入到JS环境
        context_json = json.dumps(context)

        js_code = f"""
        // 注入上下文
        const __context = {context_json};
        Object.assign(global, __context);

        // 用户代码
        {code}

        // 输出结果（如果有return语句）
        if (typeof __result !== 'undefined') {{
            console.log(JSON.stringify(__result));
        }}
        """

        return js_code

    def validate(self, code: str) -> Dict[str, Any]:
        """验证JavaScript代码"""
        # 使用Node.js的--check参数验证语法
        try:
            result = subprocess.run(
                [self.node_path, "--check", "-e", code],
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                return {"valid": True, "errors": []}
            else:
                return {"valid": False, "errors": [result.stderr]}

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
        ]

    def convert_type(self, value: Any, target_type: str) -> Any:
        """类型转换（JS <-> Python）"""
        if target_type == "array":
            return list(value) if isinstance(value, (list, tuple)) else [value]
        elif target_type == "object":
            return dict(value) if isinstance(value, dict) else {"value": value}
        elif target_type == "number":
            return float(value) if not isinstance(value, (int, float)) else value
        elif target_type == "string":
            return str(value)

        return value
```

### 4.2 使用示例

```言律
# 示例1: 异步HTTP请求
定用户数据是 {{javascript
const response = await fetch('https://api.example.com/users');
const data = await response.json();
return data;
}}

# 示例2: 使用npm包
定加密结果是函文本：
  {{javascript
  const crypto = require('crypto');
  const hash = crypto.createHash('sha256');
  hash.update(text);
  return hash.digest('hex');
  }}

# 示例3: 数组操作
定数据是列1 2 3 4 5
定平方和是 {{javascript
data.map(x => x * x).reduce((a, b) => a + b, 0);
}}
输出 平方和  # 输出: 55
```

---

## 五、SQL轨实现

### 5.1 实现代码

```python
import sqlite3
from typing import Any, Dict, List, Optional
from .track_base import Track

class SQLTrack(Track):
    """SQL轨 - 数据库查询"""

    def __init__(self, connection_string: Optional[str] = None):
        self.connection_string = connection_string or ":memory:"
        self.connection: Optional[sqlite3.Connection] = None

    def _get_connection(self) -> sqlite3.Connection:
        """获取数据库连接"""
        if not self.connection:
            self.connection = sqlite3.connect(self.connection_string)
        return self.connection

    def execute(self, code: str, context: Dict[str, Any]) -> Any:
        """
        执行SQL查询

        支持参数化查询，参数从context中获取
        """
        conn = self._get_connection()
        cursor = conn.cursor()

        try:
            # 提取参数
            params = context.get("params", [])

            # 执行查询
            if params:
                cursor.execute(code, params)
            else:
                cursor.execute(code)

            # 判断是查询还是更新
            if code.strip().upper().startswith("SELECT"):
                # 查询操作
                columns = [desc[0] for desc in cursor.description]
                rows = cursor.fetchall()

                # 转换为字典列表
                result = [
                    dict(zip(columns, row))
                    for row in rows
                ]
                return result
            else:
                # 更新操作
                conn.commit()
                return {
                    "affected_rows": cursor.rowcount,
                    "last_insert_id": cursor.lastrowid
                }

        except Exception as e:
            conn.rollback()
            raise RuntimeError(f"SQL执行错误: {e}")

    def validate(self, code: str) -> Dict[str, Any]:
        """验证SQL语法"""
        # 简单的语法检查
        code_upper = code.strip().upper()

        valid_starts = [
            "SELECT", "INSERT", "UPDATE", "DELETE",
            "CREATE", "DROP", "ALTER", "BEGIN", "COMMIT"
        ]

        is_valid = any(code_upper.startswith(cmd) for cmd in valid_starts)

        return {
            "valid": is_valid,
            "errors": [] if is_valid else ["无效的SQL语句"]
        }

    def get_capabilities(self) -> List[str]:
        """SQL轨能力"""
        return [
            "transactions",    # 支持事务
            "parameters",      # 支持参数化查询
            "batch",           # 支持批量操作
            "joins",           # 支持连接查询
            "aggregation",     # 支持聚合函数
        ]

    def convert_type(self, value: Any, target_type: str) -> Any:
        """类型转换（SQL <-> Python）"""
        if target_type == "INTEGER":
            return int(value)
        elif target_type == "REAL":
            return float(value)
        elif target_type == "TEXT":
            return str(value)
        elif target_type == "BLOB":
            return bytes(value)

        return value
```

### 5.2 使用示例

```言律
# 示例1: 查询数据
定用户列表是 {{sql
SELECT id, name, email FROM users WHERE age > 18
}}
对于用户在用户列表：
  输出 用户算"name"

# 示例2: 参数化查询
定用户ID是123
定用户信息是 {{sql
SELECT * FROM users WHERE id = ?
}} 参数用户ID

# 示例3: 插入数据
定插入结果是 {{sql
INSERT INTO users (name, email, age) VALUES (?, ?, ?)
}} 参数"张三" "zhangsan@example.com" 25

输出 "插入成功，ID：" 加 插入结果算"last_insert_id"
```

---

## 六、语法设计

### 6.1 内联代码块语法

```言律
# 基本语法
定变量名是 {{语言名
代码内容
}}

# 带参数的函数
定函数名是函参数1 参数2：
  {{语言名
  代码内容
  }}

# 执行带参数
定结果是函数名参数值1 参数值2
```

### 6.2 多行代码块

```言律
定复杂数据是 {{python
import pandas as pd
import numpy as np

# 创建DataFrame
df = pd.DataFrame({
    'name': ['Alice', 'Bob', 'Charlie'],
    'age': [25, 30, 35],
    'score': [85.5, 92.0, 78.5]
})

# 数据分析
result = df.groupby('age').agg({
    'score': ['mean', 'std']
})

return result.to_dict()
}}
```

### 6.3 上下文共享

```言律
# 言律变量传递到Python
定数据是列1 2 3 4 5
定平方和是 {{python
# data变量自动从言律传入
sum(x**2 for x in data)
}}

# Python结果返回到言律
输出 平方和  # 输出: 55
```

---

## 七、类型转换系统

### 7.1 自动类型映射

```python
class TypeConverter:
    """类型转换器"""

    # 言律类型 <-> Python类型 <-> JavaScript类型
    type_mappings = {
        "言律": {
            "整数": "int",
            "小数": "float",
            "文本": "str",
            "布尔": "bool",
            "列表": "list",
            "字典": "dict",
        },
        "Python": {
            "int": "整数",
            "float": "小数",
            "str": "文本",
            "bool": "布尔",
            "list": "列表",
            "dict": "字典",
        },
        "JavaScript": {
            "number": "小数",
            "string": "文本",
            "boolean": "布尔",
            "array": "列表",
            "object": "字典",
        }
    }

    @staticmethod
    def convert(value: Any, from_lang: str, to_lang: str) -> Any:
        """跨语言类型转换"""
        # 获取值的类型
        from_type = type(value).__name__

        # 查找映射
        from_mapping = TypeConverter.type_mappings.get(from_lang, {})
        to_mapping = TypeConverter.type_mappings.get(to_lang, {})

        # 转换类型
        common_type = from_mapping.get(from_type, from_type)
        target_type = to_mapping.get(common_type, common_type)

        # 执行转换
        return TypeConverter._convert_value(value, target_type)

    @staticmethod
    def _convert_value(value: Any, target_type: str) -> Any:
        """执行实际的类型转换"""
        converters = {
            "int": int,
            "float": float,
            "str": str,
            "bool": bool,
            "list": list,
            "dict": dict,
        }

        if target_type in converters:
            return converters[target_type](value)

        return value
```

### 7.2 类型检查

```python
def check_type_compatibility(value: Any, expected_type: str,
                            lang: str) -> bool:
    """检查类型兼容性"""
    actual_type = type(value).__name__

    compatibility_matrix = {
        "Python": {
            ("int", "float"): True,    # int可以转float
            ("list", "dict"): False,   # list不能转dict
        },
        "JavaScript": {
            ("number", "string"): True,  # 自动转换
            ("array", "object"): True,   # 数组是对象
        }
    }

    lang_rules = compatibility_matrix.get(lang, {})
    return lang_rules.get((actual_type, expected_type), False)
```

---

## 八、错误处理机制

### 8.1 统一错误处理

```python
class InteropError(Exception):
    """互操作错误基类"""
    pass

class ExecutionError(InteropError):
    """执行错误"""
    def __init__(self, lang: str, message: str, details: Dict = None):
        self.lang = lang
        self.message = message
        self.details = details or {}
        super().__init__(f"[{lang}] {message}")

class TypeConversionError(InteropError):
    """类型转换错误"""
    def __init__(self, value: Any, from_type: str, to_type: str):
        self.value = value
        self.from_type = from_type
        self.to_type = to_type
        super().__init__(
            f"无法将 {from_type} 类型的值 {value} 转换为 {to_type}"
        )

class ValidationError(InteropError):
    """验证错误"""
    def __init__(self, lang: str, errors: List[str]):
        self.lang = lang
        self.errors = errors
        super().__init__(f"[{lang}] 验证失败: {', '.join(errors)}")
```

### 8.2 错误恢复策略

```python
class ErrorRecovery:
    """错误恢复策略"""

    @staticmethod
    def handle_execution_error(error: ExecutionError,
                              fallback_value: Any = None) -> Any:
        """处理执行错误"""
        # 记录错误日志
        log_error(error)

        # 返回回退值
        if fallback_value is not None:
            return fallback_value

        # 抛出错误
        raise error

    @staticmethod
    def handle_type_error(error: TypeConversionError) -> Any:
        """处理类型转换错误"""
        # 尝试宽松转换
        try:
            return str(error.value)  # 转为字符串
        except:
            raise error
```

---

## 九、性能优化

### 9.1 缓存机制

```python
from functools import lru_cache

class CachedTrack:
    """带缓存的轨"""

    def __init__(self, track: Track):
        self.track = track
        self.code_cache: Dict[str, Any] = {}

    @lru_cache(maxsize=100)
    def execute(self, code: str, context_hash: str) -> Any:
        """执行代码（带缓存）"""
        return self.track.execute(code, context)

    def validate(self, code: str) -> Dict[str, Any]:
        """验证代码（带缓存）"""
        if code in self.code_cache:
            return self.code_cache[code]

        result = self.track.validate(code)
        self.code_cache[code] = result
        return result
```

### 9.2 批量执行

```python
class BatchExecutor:
    """批量执行器"""

    def execute_batch(self, operations: List[Dict]) -> List[Any]:
        """
        批量执行多个操作

        Args:
            operations: 操作列表，每个操作包含:
                - track: 轨名称
                - code: 代码
                - context: 上下文

        Returns:
            结果列表
        """
        results = []

        # 按轨分组
        by_track = {}
        for op in operations:
            track_name = op["track"]
            if track_name not in by_track:
                by_track[track_name] = []
            by_track[track_name].append(op)

        # 批量执行
        for track_name, ops in by_track.items():
            track = self.track_manager.get_track(track_name)

            # 合并上下文
            merged_context = {}
            for op in ops:
                merged_context.update(op.get("context", {}))

            # 执行
            for op in ops:
                result = track.execute(op["code"], merged_context)
                results.append(result)

        return results
```

---

## 十、实现路线图

### 阶段一：基础框架（1-2周）

- [x] 设计Track接口
- [x] 实现TrackManager
- [x] 实现PythonTrack基础功能
- [x] 实现类型转换系统
- [x] 实现错误处理机制

### 阶段二：Python轨完善（1周）

- [ ] 完善Python代码执行
- [ ] 实现变量共享
- [ ] 实现模块导入
- [ ] 实现异常处理
- [ ] 编写测试用例

### 阶段三：JavaScript轨（2周）

- [ ] 实现JavaScriptTrack基础功能
- [ ] 集成Node.js环境
- [ ] 实现异步执行
- [ ] 支持npm包
- [ ] 编写测试用例

### 阶段四：SQL轨（1周）

- [ ] 实现SQLTrack基础功能
- [ ] 支持多种数据库
- [ ] 实现参数化查询
- [ ] 实现事务支持
- [ ] 编写测试用例

### 阶段五：优化和完善（1周）

- [ ] 实现缓存机制
- [ ] 实现批量执行
- [ ] 性能优化
- [ ] 文档完善
- [ ] 示例代码

---

## 十一、测试策略

### 11.1 单元测试

```python
def test_python_track():
    """测试Python轨"""
    track = PythonTrack()

    # 测试表达式
    result = track.execute("2 + 3", {})
    assert result == 5

    # 测试语句
    track.execute("x = 10", {})
    result = track.execute("x * 2", {})
    assert result == 20

    # 测试函数
    code = """
def add(a, b):
    return a + b
"""
    func = track.execute(code, {})
    assert func(2, 3) == 5

def test_type_conversion():
    """测试类型转换"""
    converter = TypeConverter()

    # Python -> 言律
    result = converter.convert(42, "Python", "言律")
    assert result == 42

    # JavaScript -> Python
    result = converter.convert([1, 2, 3], "JavaScript", "Python")
    assert result == [1, 2, 3]
```

### 11.2 集成测试

```python
def test_interop_integration():
    """测试互操作集成"""
    manager = TrackManager()
    manager.register_track("python", PythonTrack())

    # 在言律代码中使用Python
    yanlv_code = """
    定结果是 {{python
    import math
    math.sqrt(16)
    }}
    输出 结果
    """

    compiler = YanLuCompiler(track_manager=manager)
    output = compiler.run(yanlv_code)
    assert "4.0" in output
```

---

## 十二、总结

### 优势

1. **无缝集成** - 在言律中直接使用其他语言
2. **类型安全** - 自动类型转换和检查
3. **易于扩展** - 简单的Track接口
4. **性能优化** - 缓存和批量执行
5. **错误处理** - 统一的错误处理机制

### 应用场景

1. **数据处理** - 使用Python的pandas、numpy
2. **Web开发** - 使用JavaScript的fetch、DOM操作
3. **数据库操作** - 使用SQL查询
4. **科学计算** - 使用Python的scipy、matplotlib
5. **机器学习** - 使用Python的tensorflow、pytorch

### 未来扩展

1. **更多语言支持** - Rust、Go、Java等
2. **FFI支持** - 直接调用C/C++库
3. **WASM支持** - 运行WebAssembly模块
4. **分布式执行** - 远程代码执行
5. **可视化工具** - 互操作调试和监控

---

**设计者：** CodeArts Agent
**设计时间：** 2026-06-01
**状态：** 设计完成，待实现
