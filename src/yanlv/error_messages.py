"""
言律语言错误信息系统

提供友好的中文错误信息和修复建议
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass
import json


@dataclass
class ErrorInfo:
    """错误信息"""
    code: str           # 错误代码(如YANLV-0001)
    message: str        # 错误消息
    severity: int       # 严重程度(1=错误, 2=警告, 3=信息)
    category: str       # 错误类别
    suggestion: str     # 修复建议
    example: str = ""   # 示例代码


class ErrorMessageManager:
    """
    错误消息管理器
    
    管理所有错误消息,提供友好的中文提示
    """
    
    def __init__(self):
        """初始化错误消息管理器"""
        self.errors: Dict[str, ErrorInfo] = {}
        self._init_error_messages()
    
    def _init_error_messages(self) -> None:
        """初始化错误消息"""
        
        # 词法错误 (YANLV-0001 ~ YANLV-0099)
        self.errors["YANLV-0001"] = ErrorInfo(
            code="YANLV-0001",
            message="括号未闭合",
            severity=1,
            category="词法错误",
            suggestion="请检查括号是否成对出现,确保每个左括号都有对应的右括号",
            example="正确: 函数 test(a, b) { ... }\n错误: 函数 test(a, b { ... }"
        )
        
        self.errors["YANLV-0002"] = ErrorInfo(
            code="YANLV-0002",
            message="引号未闭合",
            severity=1,
            category="词法错误",
            suggestion="请检查引号是否成对出现,确保每个引号都有对应的闭合引号",
            example='正确: 定义 s 为 "hello"\n错误: 定义 s 为 "hello'
        )
        
        self.errors["YANLV-0003"] = ErrorInfo(
            code="YANLV-0003",
            message="非法字符",
            severity=1,
            category="词法错误",
            suggestion="该字符在言律语言中不被支持,请使用合法的字符",
            example="支持: 中文、英文字母、数字、下划线\n不支持: 特殊符号(除运算符外)"
        )
        
        self.errors["YANLV-0004"] = ErrorInfo(
            code="YANLV-0004",
            message="数字格式错误",
            severity=1,
            category="词法错误",
            suggestion="数字格式不正确,请检查数字的书写格式",
            example="正确: 123, 3.14, 0xFF\n错误: 123., .5, 12.34.56"
        )
        
        # 语法错误 (YANLV-0100 ~ YANLV-0199)
        self.errors["YANLV-0100"] = ErrorInfo(
            code="YANLV-0100",
            message="语法错误: 缺少关键字",
            severity=1,
            category="语法错误",
            suggestion="语句缺少必要的关键字,请检查语法结构",
            example="正确: 定义 x 为 10\n错误: x 为 10"
        )
        
        self.errors["YANLV-0101"] = ErrorInfo(
            code="YANLV-0101",
            message="语法错误: 缺少标识符",
            severity=1,
            category="语法错误",
            suggestion="缺少变量名或函数名,请提供有效的标识符",
            example="正确: 定义 x 为 10\n错误: 定义 为 10"
        )
        
        self.errors["YANLV-0102"] = ErrorInfo(
            code="YANLV-0102",
            message="语法错误: 缺少表达式",
            severity=1,
            category="语法错误",
            suggestion="缺少必要的表达式,请提供完整的表达式",
            example="正确: 设 x 为 10 + 20\n错误: 设 x 为 +"
        )
        
        self.errors["YANLV-0103"] = ErrorInfo(
            code="YANLV-0103",
            message="语法错误: 无效的语句",
            severity=1,
            category="语法错误",
            suggestion="该语句不符合言律语言的语法规则",
            example="请参考言律语言语法文档"
        )
        
        self.errors["YANLV-0104"] = ErrorInfo(
            code="YANLV-0104",
            message="语法错误: 缺少右大括号",
            severity=1,
            category="语法错误",
            suggestion="代码块缺少闭合的大括号,请检查代码块结构",
            example="正确: 函数 test() { ... }\n错误: 函数 test() { ..."
        )
        
        # 语义错误 (YANLV-0200 ~ YANLV-0299)
        self.errors["YANLV-0200"] = ErrorInfo(
            code="YANLV-0200",
            message="未定义的变量",
            severity=1,
            category="语义错误",
            suggestion="该变量在使用前未被定义,请先定义变量再使用",
            example="正确: 定义 x 为 10\n       输出 x\n错误: 输出 x  (x未定义)"
        )
        
        self.errors["YANLV-0201"] = ErrorInfo(
            code="YANLV-0201",
            message="未定义的函数",
            severity=1,
            category="语义错误",
            suggestion="该函数在调用前未被定义,请先定义函数再调用",
            example="正确: 函数 test() { ... }\n       test()\n错误: test()  (test未定义)"
        )
        
        self.errors["YANLV-0202"] = ErrorInfo(
            code="YANLV-0202",
            message="参数数量不匹配",
            severity=1,
            category="语义错误",
            suggestion="函数调用时提供的参数数量与定义时不符",
            example="定义: 函数 add(a, b) { ... }\n正确: add(1, 2)\n错误: add(1)  (缺少参数)"
        )
        
        self.errors["YANLV-0203"] = ErrorInfo(
            code="YANLV-0203",
            message="类型不匹配",
            severity=1,
            category="语义错误",
            suggestion="操作数的类型与期望的类型不符",
            example="期望数字: 定义 x 为 10 + \"hello\"  (错误)\n正确: 定义 x 为 10 + 20"
        )
        
        self.errors["YANLV-0204"] = ErrorInfo(
            code="YANLV-0204",
            message="重复定义",
            severity=2,
            category="语义错误",
            suggestion="该名称已被定义,请使用不同的名称或删除重复定义",
            example="错误: 定义 x 为 10\n       定义 x 为 20  (x重复定义)"
        )
        
        # 运行时错误 (YANLV-0300 ~ YANLV-0399)
        self.errors["YANLV-0300"] = ErrorInfo(
            code="YANLV-0300",
            message="除零错误",
            severity=1,
            category="运行时错误",
            suggestion="不能除以零,请检查除数是否为零",
            example="错误: 定义 x 为 10 / 0\n正确: 定义 x 为 10 / 2"
        )
        
        self.errors["YANLV-0301"] = ErrorInfo(
            code="YANLV-0301",
            message="数组索引越界",
            severity=1,
            category="运行时错误",
            suggestion="访问的数组索引超出范围,请检查索引值",
            example="数组: 定义 arr 为 [1, 2, 3]\n正确: arr[0], arr[1], arr[2]\n错误: arr[3]  (越界)"
        )
        
        self.errors["YANLV-0302"] = ErrorInfo(
            code="YANLV-0302",
            message="空值引用",
            severity=1,
            category="运行时错误",
            suggestion="尝试访问空值的成员或方法",
            example="错误: 定义 x 为 空\n       输出 x.属性  (x为空)"
        )
        
        self.errors["YANLV-0303"] = ErrorInfo(
            code="YANLV-0303",
            message="文件不存在",
            severity=1,
            category="运行时错误",
            suggestion="尝试访问不存在的文件,请检查文件路径",
            example="错误: 读取文件(\"不存在的文件.txt\")"
        )
        
        # 警告 (YANLV-0400 ~ YANLV-0499)
        self.errors["YANLV-0400"] = ErrorInfo(
            code="YANLV-0400",
            message="未使用的变量",
            severity=2,
            category="警告",
            suggestion="该变量被定义但从未使用,可以考虑删除",
            example="定义 x 为 10  (x从未使用)"
        )
        
        self.errors["YANLV-0401"] = ErrorInfo(
            code="YANLV-0401",
            message="代码不可达",
            severity=2,
            category="警告",
            suggestion="该代码永远不会被执行,可以删除",
            example="返回 10\n输出 20  (不可达)"
        )
        
        self.errors["YANLV-0402"] = ErrorInfo(
            code="YANLV-0402",
            message="无限循环",
            severity=2,
            category="警告",
            suggestion="检测到可能的无限循环,请检查循环条件",
            example="当 真 执行 { ... }  (无限循环)"
        )
    
    def get_error(self, code: str) -> Optional[ErrorInfo]:
        """
        获取错误信息
        
        Args:
            code: 错误代码
            
        Returns:
            错误信息
        """
        return self.errors.get(code)
    
    def format_error(
        self, 
        code: str, 
        line: int = None, 
        column: int = None,
        **kwargs
    ) -> str:
        """
        格式化错误消息
        
        Args:
            code: 错误代码
            line: 行号
            column: 列号
            **kwargs: 额外参数
            
        Returns:
            格式化的错误消息
        """
        error_info = self.get_error(code)
        
        if not error_info:
            return f"未知错误: {code}"
        
        # 构建错误消息
        parts = []
        
        # 错误代码和类别
        parts.append(f"[{error_info.code}] {error_info.category}")
        
        # 位置信息
        if line is not None:
            if column is not None:
                parts.append(f"位置: 第{line}行, 第{column}列")
            else:
                parts.append(f"位置: 第{line}行")
        
        # 错误消息
        parts.append(f"错误: {error_info.message}")
        
        # 修复建议
        parts.append(f"建议: {error_info.suggestion}")
        
        # 示例
        if error_info.example:
            parts.append(f"示例:\n{error_info.example}")
        
        # 额外信息
        for key, value in kwargs.items():
            parts.append(f"{key}: {value}")
        
        return "\n".join(parts)
    
    def get_all_errors(self) -> List[ErrorInfo]:
        """获取所有错误信息"""
        return list(self.errors.values())
    
    def get_errors_by_category(self, category: str) -> List[ErrorInfo]:
        """
        按类别获取错误
        
        Args:
            category: 错误类别
            
        Returns:
            错误列表
        """
        return [
            error for error in self.errors.values()
            if error.category == category
        ]
    
    def export_to_json(self, file_path: str) -> None:
        """
        导出为JSON文件
        
        Args:
            file_path: 文件路径
        """
        data = {
            code: {
                'code': error.code,
                'message': error.message,
                'severity': error.severity,
                'category': error.category,
                'suggestion': error.suggestion,
                'example': error.example
            }
            for code, error in self.errors.items()
        }
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)


# 全局错误消息管理器
_global_manager: Optional[ErrorMessageManager] = None


def get_error_manager() -> ErrorMessageManager:
    """获取全局错误消息管理器"""
    global _global_manager
    if _global_manager is None:
        _global_manager = ErrorMessageManager()
    return _global_manager


def format_error(code: str, line: int = None, column: int = None, **kwargs) -> str:
    """
    格式化错误消息(便捷函数)
    
    Args:
        code: 错误代码
        line: 行号
        column: 列号
        **kwargs: 额外参数
        
    Returns:
        格式化的错误消息
    """
    return get_error_manager().format_error(code, line, column, **kwargs)
