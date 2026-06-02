"""
SQL轨实现

支持多种数据库的SQL查询和操作
"""

import sqlite3
from typing import Any, Dict, List, Optional, Union

# 导入Track基类
try:
    from .track_base import Track
except ImportError:
    # 如果相对导入失败，尝试绝对导入
    try:
        from yanlv.interop.track_base import Track
    except ImportError:
        # 如果还是失败，定义一个简化版本
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


class SQLTrack(Track):
    """SQL轨 - 数据库查询和操作"""

    def __init__(self, connection_string: Optional[str] = None,
                 db_type: str = "sqlite"):
        """
        初始化SQL轨

        Args:
            connection_string: 数据库连接字符串
            db_type: 数据库类型 (sqlite, mysql, postgres等)
        """
        self.connection_string = connection_string or ":memory:"
        self.db_type = db_type
        self.connection: Optional[sqlite3.Connection] = None
        self._initialize_database()

    def _initialize_database(self) -> None:
        """初始化数据库连接"""
        if self.db_type == "sqlite":
            self.connection = sqlite3.connect(self.connection_string)
            self.connection.row_factory = sqlite3.Row
        # 其他数据库类型可以在这里扩展
        # elif self.db_type == "mysql":
        #     import mysql.connector
        #     self.connection = mysql.connector.connect(...)

    def _get_connection(self) -> sqlite3.Connection:
        """获取数据库连接"""
        if not self.connection:
            self._initialize_database()
        return self.connection

    def execute(self, code: str, context: Dict[str, Any]) -> Any:
        """
        执行SQL查询

        支持参数化查询，参数从context中获取

        Args:
            code: SQL代码
            context: 执行上下文，可包含params参数

        Returns:
            查询结果或操作结果
        """
        conn = self._get_connection()
        cursor = conn.cursor()

        try:
            # 提取参数
            params = context.get("params", [])

            # 处理参数类型
            if isinstance(params, (list, tuple)):
                params = tuple(params)
            elif isinstance(params, dict):
                # 命名参数，需要特殊处理
                params = tuple(params.values())

            # 执行查询
            if params:
                cursor.execute(code, params)
            else:
                cursor.execute(code)

            # 判断是查询还是更新
            code_upper = code.strip().upper()

            if any(code_upper.startswith(cmd) for cmd in ["SELECT", "PRAGMA"]):
                # 查询操作
                columns = [desc[0] for desc in cursor.description] if cursor.description else []
                rows = cursor.fetchall()

                # 转换为字典列表
                result = []
                for row in rows:
                    if isinstance(row, sqlite3.Row):
                        result.append(dict(row))
                    else:
                        result.append(dict(zip(columns, row)))

                return result
            else:
                # 更新操作
                conn.commit()
                return {
                    "affected_rows": cursor.rowcount,
                    "last_insert_id": cursor.lastrowid,
                    "success": True
                }

        except Exception as e:
            conn.rollback()
            raise RuntimeError(f"SQL执行错误: {e}")

    def validate(self, code: str) -> Dict[str, Any]:
        """验证SQL语法"""
        # 简单的语法检查
        code_stripped = code.strip().upper()

        valid_commands = [
            "SELECT", "INSERT", "UPDATE", "DELETE",
            "CREATE", "DROP", "ALTER", "TRUNCATE",
            "BEGIN", "COMMIT", "ROLLBACK", "SAVEPOINT",
            "PRAGMA", "EXPLAIN"
        ]

        is_valid = any(code_stripped.startswith(cmd) for cmd in valid_commands)

        if is_valid:
            # 尝试EXPLAIN验证（仅SQLite）
            if self.db_type == "sqlite":
                try:
                    conn = self._get_connection()
                    cursor = conn.cursor()
                    cursor.execute(f"EXPLAIN {code}")
                    return {"valid": True, "errors": []}
                except Exception as e:
                    return {"valid": False, "errors": [str(e)]}
            else:
                return {"valid": True, "errors": []}
        else:
            return {"valid": False, "errors": ["无效的SQL语句"]}

    def get_capabilities(self) -> List[str]:
        """SQL轨能力"""
        capabilities = [
            "transactions",    # 支持事务
            "parameters",      # 支持参数化查询
            "batch",           # 支持批量操作
            "joins",           # 支持连接查询
            "aggregation",     # 支持聚合函数
            "subqueries",      # 支持子查询
        ]

        if self.db_type == "sqlite":
            capabilities.extend([
                "in_memory",    # 支持内存数据库
                "file_based",   # 支持文件数据库
                "pragma",       # 支持PRAGMA指令
            ])

        return capabilities

    def convert_type(self, value: Any, target_type: str) -> Any:
        """类型转换（SQL <-> Python）"""
        type_converters = {
            "INTEGER": int,
            "INT": int,
            "REAL": float,
            "FLOAT": float,
            "DOUBLE": float,
            "TEXT": str,
            "VARCHAR": str,
            "CHAR": str,
            "BLOB": bytes,
            "BOOLEAN": bool,
            "BOOL": bool,
        }

        if target_type.upper() in type_converters:
            try:
                return type_converters[target_type.upper()](value)
            except:
                return value

        return value

    def execute_script(self, script: str) -> List[Any]:
        """
        执行多条SQL语句

        Args:
            script: SQL脚本（多条语句）

        Returns:
            结果列表
        """
        conn = self._get_connection()
        results = []

        try:
            # 分割语句
            statements = script.split(';')

            for statement in statements:
                statement = statement.strip()
                if statement:
                    result = self.execute(statement, {})
                    results.append(result)

            return results

        except Exception as e:
            raise RuntimeError(f"SQL脚本执行错误: {e}")

    def create_table(self, table_name: str, columns: Dict[str, str]) -> bool:
        """
        创建表

        Args:
            table_name: 表名
            columns: 列定义 {"列名": "类型"}

        Returns:
            是否成功
        """
        column_defs = ", ".join([f"{name} {type_}" for name, type_ in columns.items()])
        sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({column_defs})"

        try:
            self.execute(sql, {})
            return True
        except:
            return False

    def insert(self, table_name: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        插入数据

        Args:
            table_name: 表名
            data: 数据字典

        Returns:
            插入结果
        """
        columns = ", ".join(data.keys())
        placeholders = ", ".join(["?" for _ in data])
        sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

        return self.execute(sql, {"params": tuple(data.values())})

    def select(self, table_name: str, columns: str = "*",
               where: Optional[str] = None,
               params: Optional[tuple] = None) -> List[Dict]:
        """
        查询数据

        Args:
            table_name: 表名
            columns: 列名（逗号分隔）
            where: WHERE条件
            params: 参数

        Returns:
            查询结果
        """
        sql = f"SELECT {columns} FROM {table_name}"

        if where:
            sql += f" WHERE {where}"

        context = {"params": params} if params else {}
        return self.execute(sql, context)

    def close(self) -> None:
        """关闭数据库连接"""
        if self.connection:
            self.connection.close()
            self.connection = None


# ============================================================================
# 使用示例
# ============================================================================

def example_sql_usage():
    """SQL轨使用示例"""
    print("\n" + "=" * 60)
    print("SQL轨使用示例")
    print("=" * 60)

    # 创建内存数据库
    track = SQLTrack(":memory:")

    # 示例1: 创建表
    print("\n--- 示例1: 创建表 ---")
    result = track.create_table("users", {
        "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
        "name": "TEXT NOT NULL",
        "age": "INTEGER",
        "email": "TEXT"
    })
    print(f"创建表: {'成功' if result else '失败'}")

    # 示例2: 插入数据
    print("\n--- 示例2: 插入数据 ---")
    users = [
        {"name": "张三", "age": 25, "email": "zhangsan@example.com"},
        {"name": "李四", "age": 30, "email": "lisi@example.com"},
        {"name": "王五", "age": 28, "email": "wangwu@example.com"},
    ]

    for user in users:
        result = track.insert("users", user)
        print(f"插入 {user['name']}: ID={result['last_insert_id']}")

    # 示例3: 查询所有数据
    print("\n--- 示例3: 查询所有数据 ---")
    all_users = track.select("users")
    for user in all_users:
        print(f"  {user['name']}, {user['age']}岁, {user['email']}")

    # 示例4: 条件查询
    print("\n--- 示例4: 条件查询 ---")
    young_users = track.select("users", where="age < 30")
    print(f"年龄小于30的用户: {len(young_users)}个")
    for user in young_users:
        print(f"  {user['name']}, {user['age']}岁")

    # 示例5: 参数化查询
    print("\n--- 示例5: 参数化查询 ---")
    result = track.execute(
        "SELECT * FROM users WHERE name = ?",
        {"params": ("张三",)}
    )
    print(f"查询'张三': {result}")

    # 示例6: 聚合查询
    print("\n--- 示例6: 聚合查询 ---")
    result = track.execute(
        "SELECT COUNT(*) as count, AVG(age) as avg_age FROM users",
        {}
    )
    print(f"统计结果: {result}")

    # 示例7: 更新数据
    print("\n--- 示例7: 更新数据 ---")
    result = track.execute(
        "UPDATE users SET age = ? WHERE name = ?",
        {"params": (26, "张三")}
    )
    print(f"更新结果: 影响{result['affected_rows']}行")

    # 验证更新
    updated_user = track.select("users", where="name = '张三'")
    print(f"更新后的数据: {updated_user}")

    # 示例8: 删除数据
    print("\n--- 示例8: 删除数据 ---")
    result = track.execute(
        "DELETE FROM users WHERE name = ?",
        {"params": ("王五",)}
    )
    print(f"删除结果: 影响{result['affected_rows']}行")

    # 示例9: 代码验证
    print("\n--- 示例9: 代码验证 ---")
    valid_sql = "SELECT * FROM users WHERE age > 20"
    invalid_sql = "INVALID SQL STATEMENT"

    valid_result = track.validate(valid_sql)
    print(f"验证有效SQL: {valid_result}")

    invalid_result = track.validate(invalid_sql)
    print(f"验证无效SQL: {invalid_result}")

    # 示例10: 查看能力
    print("\n--- 示例10: 轨的能力 ---")
    capabilities = track.get_capabilities()
    print(f"SQL轨能力: {capabilities}")

    # 关闭连接
    track.close()

    print("\n" + "=" * 60)


if __name__ == "__main__":
    example_sql_usage()
