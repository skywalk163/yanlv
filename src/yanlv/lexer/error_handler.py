"""
言律语言词法分析器 - 错误处理模块

包含错误处理、警告和异常处理功能
"""

from typing import List, Optional, Dict, Any, Union
from dataclasses import dataclass, field
from enum import Enum
from utils import ErrorInfo, Position, Range
from lexer_token import Token, TokenType


class ErrorSeverity(Enum):
    """错误严重程度"""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    FATAL = "fatal"


class ErrorCode(Enum):
    """错误代码"""
    # 词法错误
    LEXER_INVALID_CHAR = "LEX001"
    LEXER_UNEXPECTED_TOKEN = "LEX002"
    LEXER_UNTERMINATED_STRING = "LEX003"
    LEXER_INVALID_NUMBER = "LEX004"
    LEXER_INVALID_IDENTIFIER = "LEX005"
    
    # 语法错误
    SYNTAX_UNEXPECTED_TOKEN = "SYN001"
    SYNTAX_MISSING_TOKEN = "SYN002"
    SYNTAX_INVALID_EXPRESSION = "SYN003"
    SYNTAX_INVALID_STATEMENT = "SYN004"
    
    # 语义错误
    SEMANTIC_UNDEFINED_VARIABLE = "SEM001"
    SEMANTIC_TYPE_MISMATCH = "SEM002"
    SEMANTIC_INVALID_OPERATION = "SEM003"
    SEMANTIC_DUPLICATE_DEFINITION = "SEM004"
    
    # 运行时错误
    RUNTIME_DIVISION_BY_ZERO = "RUN001"
    RUNTIME_INDEX_OUT_OF_BOUNDS = "RUN002"
    RUNTIME_INVALID_ARGUMENT = "RUN003"
    RUNTIME_FILE_NOT_FOUND = "RUN004"
    
    # 系统错误
    SYSTEM_OUT_OF_MEMORY = "SYS001"
    SYSTEM_TIMEOUT = "SYS002"
    SYSTEM_IO_ERROR = "SYS003"


@dataclass
class LexerError:
    """词法分析错误"""
    code: ErrorCode
    message: str
    position: Position
    severity: ErrorSeverity = ErrorSeverity.ERROR
    suggestion: Optional[str] = None
    context: Optional[str] = None
    token: Optional[Token] = None
    
    def __str__(self) -> str:
        """返回错误字符串表示"""
        result = f"{self.severity.value.upper()}[{self.code.value}] at {self.position}: {self.message}"
        
        if self.context:
            result += f"\n上下文: {self.context}"
        
        if self.token:
            result += f"\n词元: {self.token}"
        
        if self.suggestion:
            result += f"\n建议: {self.suggestion}"
        
        return result
    
    def to_error_info(self) -> ErrorInfo:
        """转换为ErrorInfo对象"""
        return ErrorInfo(
            code=self.code.value,
            message=self.message,
            position=self.position,
            severity=self.severity.value,
            suggestion=self.suggestion
        )


class ErrorHandler:
    """错误处理器"""
    
    def __init__(self, max_errors: int = 100, max_warnings: int = 1000):
        """
        初始化错误处理器
        
        Args:
            max_errors: 最大错误数
            max_warnings: 最大警告数
        """
        self.max_errors = max_errors
        self.max_warnings = max_warnings
        self.errors: List[LexerError] = []
        self.warnings: List[LexerError] = []
        self.infos: List[LexerError] = []
        
        # 错误统计
        self.stats = {
            'total_errors': 0,
            'total_warnings': 0,
            'total_infos': 0,
            'errors_by_code': {},
            'warnings_by_code': {},
            'infos_by_code': {},
        }
    
    def add_error(self, code: ErrorCode, message: str, position: Position, 
                  suggestion: Optional[str] = None, context: Optional[str] = None,
                  token: Optional[Token] = None) -> bool:
        """
        添加错误
        
        Args:
            code: 错误代码
            message: 错误消息
            position: 错误位置
            suggestion: 修复建议
            context: 上下文信息
            token: 相关词元
            
        Returns:
            是否成功添加（如果达到最大错误数则返回False）
        """
        if len(self.errors) >= self.max_errors:
            return False
        
        error = LexerError(
            code=code,
            message=message,
            position=position,
            severity=ErrorSeverity.ERROR,
            suggestion=suggestion,
            context=context,
            token=token
        )
        
        self.errors.append(error)
        self._update_stats(error)
        return True
    
    def add_warning(self, code: ErrorCode, message: str, position: Position,
                    suggestion: Optional[str] = None, context: Optional[str] = None,
                    token: Optional[Token] = None) -> bool:
        """
        添加警告
        
        Args:
            code: 警告代码
            message: 警告消息
            position: 警告位置
            suggestion: 修复建议
            context: 上下文信息
            token: 相关词元
            
        Returns:
            是否成功添加（如果达到最大警告数则返回False）
        """
        if len(self.warnings) >= self.max_warnings:
            return False
        
        warning = LexerError(
            code=code,
            message=message,
            position=position,
            severity=ErrorSeverity.WARNING,
            suggestion=suggestion,
            context=context,
            token=token
        )
        
        self.warnings.append(warning)
        self._update_stats(warning)
        return True
    
    def add_info(self, code: ErrorCode, message: str, position: Position,
                 suggestion: Optional[str] = None, context: Optional[str] = None,
                 token: Optional[Token] = None) -> bool:
        """
        添加信息
        
        Args:
            code: 信息代码
            message: 信息消息
            position: 信息位置
            suggestion: 修复建议
            context: 上下文信息
            token: 相关词元
            
        Returns:
            是否成功添加
        """
        info = LexerError(
            code=code,
            message=message,
            position=position,
            severity=ErrorSeverity.INFO,
            suggestion=suggestion,
            context=context,
            token=token
        )
        
        self.infos.append(info)
        self._update_stats(info)
        return True
    
    def _update_stats(self, error: LexerError):
        """更新统计信息"""
        code = error.code.value
        
        if error.severity == ErrorSeverity.ERROR:
            self.stats['total_errors'] += 1
            self.stats['errors_by_code'][code] = self.stats['errors_by_code'].get(code, 0) + 1
        elif error.severity == ErrorSeverity.WARNING:
            self.stats['total_warnings'] += 1
            self.stats['warnings_by_code'][code] = self.stats['warnings_by_code'].get(code, 0) + 1
        elif error.severity == ErrorSeverity.INFO:
            self.stats['total_infos'] += 1
            self.stats['infos_by_code'][code] = self.stats['infos_by_code'].get(code, 0) + 1
    
    def has_errors(self) -> bool:
        """检查是否有错误"""
        return len(self.errors) > 0
    
    def has_warnings(self) -> bool:
        """检查是否有警告"""
        return len(self.warnings) > 0
    
    def has_infos(self) -> bool:
        """检查是否有信息"""
        return len(self.infos) > 0
    
    def get_all_errors(self) -> List[LexerError]:
        """获取所有错误"""
        return self.errors.copy()
    
    def get_all_warnings(self) -> List[LexerError]:
        """获取所有警告"""
        return self.warnings.copy()
    
    def get_all_infos(self) -> List[LexerError]:
        """获取所有信息"""
        return self.infos.copy()
    
    def get_all_messages(self) -> List[LexerError]:
        """获取所有消息（错误、警告、信息）"""
        return self.errors + self.warnings + self.infos
    
    def get_error_count(self) -> int:
        """获取错误数量"""
        return len(self.errors)
    
    def get_warning_count(self) -> int:
        """获取警告数量"""
        return len(self.warnings)
    
    def get_info_count(self) -> int:
        """获取信息数量"""
        return len(self.infos)
    
    def get_total_count(self) -> int:
        """获取总消息数量"""
        return len(self.errors) + len(self.warnings) + len(self.infos)
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取统计信息"""
        stats = self.stats.copy()
        stats['current_errors'] = len(self.errors)
        stats['current_warnings'] = len(self.warnings)
        stats['current_infos'] = len(self.infos)
        return stats
    
    def clear(self):
        """清空所有消息"""
        self.errors.clear()
        self.warnings.clear()
        self.infos.clear()
        self.stats = {
            'total_errors': 0,
            'total_warnings': 0,
            'total_infos': 0,
            'errors_by_code': {},
            'warnings_by_code': {},
            'infos_by_code': {},
        }
    
    def format_messages(self, include_warnings: bool = True, include_infos: bool = False) -> str:
        """
        格式化所有消息
        
        Args:
            include_warnings: 是否包含警告
            include_infos: 是否包含信息
            
        Returns:
            格式化后的消息字符串
        """
        lines = []
        
        # 错误
        if self.errors:
            lines.append("错误:")
            for i, error in enumerate(self.errors, 1):
                lines.append(f"  {i}. {error}")
        
        # 警告
        if include_warnings and self.warnings:
            if lines:
                lines.append("")
            lines.append("警告:")
            for i, warning in enumerate(self.warnings, 1):
                lines.append(f"  {i}. {warning}")
        
        # 信息
        if include_infos and self.infos:
            if lines:
                lines.append("")
            lines.append("信息:")
            for i, info in enumerate(self.infos, 1):
                lines.append(f"  {i}. {info}")
        
        return "\n".join(lines)
    
    def to_error_infos(self) -> List[ErrorInfo]:
        """转换为ErrorInfo列表"""
        error_infos = []
        
        for error in self.errors:
            error_infos.append(error.to_error_info())
        
        for warning in self.warnings:
            error_infos.append(warning.to_error_info())
        
        for info in self.infos:
            error_infos.append(info.to_error_info())
        
        return error_infos


class LexerException(Exception):
    """词法分析异常基类"""
    
    def __init__(self, message: str, position: Optional[Position] = None,
                 code: Optional[ErrorCode] = None):
        """
        初始化异常
        
        Args:
            message: 异常消息
            position: 异常位置
            code: 错误代码
        """
        super().__init__(message)
        self.message = message
        self.position = position
        self.code = code
    
    def __str__(self) -> str:
        """返回异常字符串表示"""
        if self.position:
            return f"{self.__class__.__name__} at {self.position}: {self.message}"
        else:
            return f"{self.__class__.__name__}: {self.message}"


class InvalidCharacterError(LexerException):
    """无效字符异常"""
    
    def __init__(self, char: str, position: Position):
        """
        初始化无效字符异常
        
        Args:
            char: 无效字符
            position: 位置
        """
        super().__init__(
            f"无效字符: '{char}' (U+{ord(char):04X})",
            position,
            ErrorCode.LEXER_INVALID_CHAR
        )
        self.char = char


class UnexpectedTokenError(LexerException):
    """意外词元异常"""
    
    def __init__(self, token: Token, expected: Optional[str] = None):
        """
        初始化意外词元异常
        
        Args:
            token: 意外词元
            expected: 期望的词元类型
        """
        message = f"意外的词元: {token}"
        if expected:
            message += f"，期望: {expected}"
        
        super().__init__(
            message,
            Position(line=token.line, column=token.column, offset=-1),
            ErrorCode.LEXER_UNEXPECTED_TOKEN
        )
        self.token = token
        self.expected = expected


class UnterminatedStringError(LexerException):
    """未终止字符串异常"""
    
    def __init__(self, position: Position):
        """
        初始化未终止字符串异常
        
        Args:
            position: 位置
        """
        super().__init__(
            "未终止的字符串字面量",
            position,
            ErrorCode.LEXER_UNTERMINATED_STRING
        )


class InvalidNumberError(LexerException):
    """无效数字异常"""
    
    def __init__(self, value: str, position: Position):
        """
        初始化无效数字异常
        
        Args:
            value: 无效数字值
            position: 位置
        """
        super().__init__(
            f"无效的数字字面量: '{value}'",
            position,
            ErrorCode.LEXER_INVALID_NUMBER
        )
        self.value = value


class InvalidIdentifierError(LexerException):
    """无效标识符异常"""
    
    def __init__(self, identifier: str, position: Position):
        """
        初始化无效标识符异常
        
        Args:
            identifier: 无效标识符
            position: 位置
        """
        super().__init__(
            f"无效的标识符: '{identifier}'",
            position,
            ErrorCode.LEXER_INVALID_IDENTIFIER
        )
        self.identifier = identifier


class MaxErrorsExceededError(LexerException):
    """最大错误数超出异常"""
    
    def __init__(self, max_errors: int):
        """
        初始化最大错误数超出异常
        
        Args:
            max_errors: 最大错误数
        """
        super().__init__(
            f"达到最大错误数限制: {max_errors}",
            None,
            ErrorCode.SYSTEM_TIMEOUT
        )
        self.max_errors = max_errors


# 错误处理工具函数
def create_error_handler(max_errors: int = 100, max_warnings: int = 1000) -> ErrorHandler:
    """
    创建错误处理器
    
    Args:
        max_errors: 最大错误数
        max_warnings: 最大警告数
        
    Returns:
        错误处理器实例
    """
    return ErrorHandler(max_errors, max_warnings)


def handle_lexer_error(error_handler: ErrorHandler, error: LexerException) -> bool:
    """
    处理词法分析异常
    
    Args:
        error_handler: 错误处理器
        error: 词法分析异常
        
    Returns:
        是否成功处理
    """
    if isinstance(error, InvalidCharacterError):
        return error_handler.add_error(
            error.code,
            error.message,
            error.position,
            f"请检查字符 '{error.char}' 是否有效",
            f"无效字符: {error.char}"
        )
    
    elif isinstance(error, UnexpectedTokenError):
        suggestion = f"期望得到 {error.expected}" if error.expected else "请检查语法"
        return error_handler.add_error(
            error.code,
            error.message,
            error.position,
            suggestion,
            f"意外词元: {error.token.value}"
        )
    
    elif isinstance(error, UnterminatedStringError):
        return error_handler.add_error(
            error.code,
            error.message,
            error.position,
            "请添加缺失的引号",
            "未终止的字符串"
        )
    
    elif isinstance(error, InvalidNumberError):
        return error_handler.add_error(
            error.code,
            error.message,
            error.position,
            f"请检查数字格式: {error.value}",
            f"无效数字: {error.value}"
        )
    
    elif isinstance(error, InvalidIdentifierError):
        return error_handler.add_error(
            error.code,
            error.message,
            error.position,
            f"标识符 '{error.identifier}' 不符合命名规则",
            f"无效标识符: {error.identifier}"
        )
    
    elif isinstance(error, MaxErrorsExceededError):
        # 这是一个致命错误，直接抛出
        raise error
    
    else:
        # 未知异常
        return error_handler.add_error(
            ErrorCode.SYSTEM_IO_ERROR,
            str(error),
            Position(line=1, column=1, offset=0),
            "请检查代码语法",
            f"未知异常: {type(error).__name__}"
        )


def validate_identifier(name: str, position: Position, error_handler: ErrorHandler) -> bool:
    """
    验证标识符
    
    Args:
        name: 标识符名称
        position: 位置
        error_handler: 错误处理器
        
    Returns:
        是否有效
    """
    from utils import is_valid_identifier
    
    if not is_valid_identifier(name):
        error = InvalidIdentifierError(name, position)
        handle_lexer_error(error_handler, error)
        return False
    
    return True


def validate_number(value: str, position: Position, error_handler: ErrorHandler) -> bool:
    """
    验证数字
    
    Args:
        value: 数字值
        position: 位置
        error_handler: 错误处理器
        
    Returns:
        是否有效
    """
    from utils import is_numeric_string
    
    if not is_numeric_string(value):
        error = InvalidNumberError(value, position)
        handle_lexer_error(error_handler, error)
        return False
    
    return True


def check_max_errors(error_handler: ErrorHandler, max_errors: int) -> None:
    """
    检查是否达到最大错误数
    
    Args:
        error_handler: 错误处理器
        max_errors: 最大错误数
        
    Raises:
        MaxErrorsExceededError: 如果达到最大错误数
    """
    if error_handler.get_error_count() >= max_errors:
        raise MaxErrorsExceededError(max_errors)