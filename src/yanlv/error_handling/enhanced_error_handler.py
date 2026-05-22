"""
言律语言增强错误处理系统

提供完善的错误恢复、上下文信息和建议系统
"""

from typing import Dict, List, Optional, Any, Tuple, Callable
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
import traceback
import re


class ErrorCategory(Enum):
    """错误类别"""
    LEXICAL = "lexical"  # 词法错误
    SYNTACTIC = "syntactic"  # 语法错误
    SEMANTIC = "semantic"  # 语义错误
    RUNTIME = "runtime"  # 运行时错误
    SYSTEM = "system"  # 系统错误


class ErrorSeverity(Enum):
    """错误严重程度"""
    INFO = "info"  # 信息
    WARNING = "warning"  # 警告
    ERROR = "error"  # 错误
    FATAL = "fatal"  # 致命错误


class RecoveryStrategy(Enum):
    """恢复策略"""
    SKIP = "skip"  # 跳过
    INSERT = "insert"  # 插入
    DELETE = "delete"  # 删除
    REPLACE = "replace"  # 替换
    PANIC = "panic"  # 恐慌模式
    NONE = "none"  # 无恢复


@dataclass
class ErrorContext:
    """错误上下文"""
    source_code: str  # 源代码
    line_number: int  # 行号
    column_number: int  # 列号
    offset: int  # 偏移量
    surrounding_lines: List[str]  # 周围行
    current_token: Optional[str]  # 当前词元
    expected_tokens: List[str]  # 期望词元
    call_stack: List[str]  # 调用栈
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'source_code': self.source_code[:100] + '...' if len(self.source_code) > 100 else self.source_code,
            'line_number': self.line_number,
            'column_number': self.column_number,
            'offset': self.offset,
            'surrounding_lines': self.surrounding_lines,
            'current_token': self.current_token,
            'expected_tokens': self.expected_tokens,
            'call_stack': self.call_stack,
            'metadata': self.metadata
        }
    
    def get_context_snippet(self, context_size: int = 3) -> str:
        """获取上下文片段"""
        lines = self.source_code.split('\n')
        start = max(0, self.line_number - context_size - 1)
        end = min(len(lines), self.line_number + context_size)
        
        snippet_lines = []
        for i in range(start, end):
            line_num = i + 1
            prefix = ">>> " if line_num == self.line_number else "    "
            snippet_lines.append(f"{prefix}{line_num:4d} | {lines[i]}")
        
        return '\n'.join(snippet_lines)


@dataclass
class ErrorSuggestion:
    """错误建议"""
    suggestion_id: str  # 建议ID
    description: str  # 描述
    fix_code: Optional[str]  # 修复代码
    confidence: float  # 置信度
    category: str  # 类别
    priority: int  # 优先级
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'suggestion_id': self.suggestion_id,
            'description': self.description,
            'fix_code': self.fix_code,
            'confidence': self.confidence,
            'category': self.category,
            'priority': self.priority
        }


@dataclass
class EnhancedError:
    """增强错误"""
    error_id: str  # 错误ID
    error_code: str  # 错误代码
    category: ErrorCategory  # 类别
    severity: ErrorSeverity  # 严重程度
    message: str  # 消息
    context: ErrorContext  # 上下文
    suggestions: List[ErrorSuggestion]  # 建议
    recovery_strategy: RecoveryStrategy  # 恢复策略
    timestamp: datetime = field(default_factory=datetime.now)
    handled: bool = False
    recovered: bool = False
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'error_id': self.error_id,
            'error_code': self.error_code,
            'category': self.category.value,
            'severity': self.severity.value,
            'message': self.message,
            'context': self.context.to_dict(),
            'suggestions': [s.to_dict() for s in self.suggestions],
            'recovery_strategy': self.recovery_strategy.value,
            'timestamp': self.timestamp.isoformat(),
            'handled': self.handled,
            'recovered': self.recovered
        }
    
    def format_error(self) -> str:
        """格式化错误"""
        lines = [
            f"错误 [{self.error_code}] ({self.category.value}/{self.severity.value})",
            f"位置: 行 {self.context.line_number}, 列 {self.context.column_number}",
            f"消息: {self.message}",
            "",
            "上下文:",
            self.context.get_context_snippet(),
        ]
        
        if self.suggestions:
            lines.append("")
            lines.append("建议:")
            for i, suggestion in enumerate(self.suggestions[:3], 1):
                lines.append(f"  {i}. {suggestion.description}")
                if suggestion.fix_code:
                    lines.append(f"     修复: {suggestion.fix_code}")
        
        return '\n'.join(lines)


class ErrorRecoverySystem:
    """错误恢复系统"""
    
    def __init__(self):
        """初始化错误恢复系统"""
        self.recovery_handlers: Dict[str, Callable] = {}
        self.recovery_stats = {
            'total_errors': 0,
            'recovered_errors': 0,
            'unrecoverable_errors': 0
        }
        
        # 注册默认恢复处理器
        self._register_default_handlers()
    
    def _register_default_handlers(self):
        """注册默认恢复处理器"""
        self.recovery_handlers[RecoveryStrategy.SKIP] = self._handle_skip
        self.recovery_handlers[RecoveryStrategy.INSERT] = self._handle_insert
        self.recovery_handlers[RecoveryStrategy.DELETE] = self._handle_delete
        self.recovery_handlers[RecoveryStrategy.REPLACE] = self._handle_replace
        self.recovery_handlers[RecoveryStrategy.PANIC] = self._handle_panic
    
    def _handle_skip(self, error: EnhancedError) -> bool:
        """跳过错误"""
        # 跳过当前词元，继续处理
        return True
    
    def _handle_insert(self, error: EnhancedError) -> bool:
        """插入修复"""
        # 插入期望的词元
        if error.context.expected_tokens:
            # 插入第一个期望词元
            return True
        return False
    
    def _handle_delete(self, error: EnhancedError) -> bool:
        """删除修复"""
        # 删除当前词元
        return True
    
    def _handle_replace(self, error: EnhancedError) -> bool:
        """替换修复"""
        # 用期望词元替换当前词元
        if error.context.expected_tokens and error.context.current_token:
            return True
        return False
    
    def _handle_panic(self, error: EnhancedError) -> bool:
        """恐慌模式恢复"""
        # 跳过直到找到同步词元
        return True
    
    def recover(self, error: EnhancedError) -> bool:
        """
        尝试恢复错误
        
        Args:
            error: 增强错误
            
        Returns:
            是否成功恢复
        """
        self.recovery_stats['total_errors'] += 1
        
        handler = self.recovery_handlers.get(error.recovery_strategy)
        if handler:
            try:
                success = handler(error)
                if success:
                    error.recovered = True
                    self.recovery_stats['recovered_errors'] += 1
                else:
                    self.recovery_stats['unrecoverable_errors'] += 1
                return success
            except Exception as e:
                print(f"恢复失败: {e}")
                self.recovery_stats['unrecoverable_errors'] += 1
                return False
        
        self.recovery_stats['unrecoverable_errors'] += 1
        return False
    
    def get_recovery_stats(self) -> Dict[str, Any]:
        """获取恢复统计"""
        stats = self.recovery_stats.copy()
        if stats['total_errors'] > 0:
            stats['recovery_rate'] = stats['recovered_errors'] / stats['total_errors']
        else:
            stats['recovery_rate'] = 0.0
        return stats


class ErrorSuggestionEngine:
    """错误建议引擎"""
    
    def __init__(self):
        """初始化建议引擎"""
        self.suggestion_rules: List[Dict[str, Any]] = []
        self._load_default_rules()
    
    def _load_default_rules(self):
        """加载默认规则"""
        # 词法错误建议
        self.suggestion_rules.append({
            'error_code': 'LEX001',
            'pattern': r'无效字符',
            'suggestions': [
                {
                    'description': '检查字符是否有效',
                    'fix': '删除无效字符',
                    'confidence': 0.8
                }
            ]
        })
        
        # 语法错误建议
        self.suggestion_rules.append({
            'error_code': 'SYN001',
            'pattern': r'缺少.*结束符',
            'suggestions': [
                {
                    'description': '添加结束符',
                    'fix': '添加结束符',
                    'confidence': 0.9
                }
            ]
        })
        
        # 语义错误建议
        self.suggestion_rules.append({
            'error_code': 'SEM001',
            'pattern': r'未定义的变量',
            'suggestions': [
                {
                    'description': '定义变量',
                    'fix': '定义 变量',
                    'confidence': 0.7
                },
                {
                    'description': '检查拼写错误',
                    'fix': None,
                    'confidence': 0.6
                }
            ]
        })
    
    def generate_suggestions(self, error: EnhancedError) -> List[ErrorSuggestion]:
        """
        生成错误建议
        
        Args:
            error: 增强错误
            
        Returns:
            建议列表
        """
        suggestions = []
        
        # 查找匹配的规则
        for rule in self.suggestion_rules:
            if rule['error_code'] == error.error_code:
                for i, sug in enumerate(rule['suggestions']):
                    suggestion = ErrorSuggestion(
                        suggestion_id=f"{error.error_id}-sug-{i}",
                        description=sug['description'],
                        fix_code=sug.get('fix'),
                        confidence=sug['confidence'],
                        category=error.category.value,
                        priority=int(sug['confidence'] * 10)
                    )
                    suggestions.append(suggestion)
        
        # 如果没有匹配的规则，生成通用建议
        if not suggestions:
            suggestions.append(ErrorSuggestion(
                suggestion_id=f"{error.error_id}-sug-0",
                description="请检查代码语法",
                fix_code=None,
                confidence=0.5,
                category="general",
                priority=5
            ))
        
        return suggestions


class EnhancedErrorHandler:
    """增强错误处理器"""
    
    def __init__(self, max_errors: int = 100):
        """
        初始化错误处理器
        
        Args:
            max_errors: 最大错误数
        """
        self.max_errors = max_errors
        self.errors: List[EnhancedError] = []
        self.recovery_system = ErrorRecoverySystem()
        self.suggestion_engine = ErrorSuggestionEngine()
        
        # 统计
        self.stats = {
            'total_errors': 0,
            'errors_by_category': {},
            'errors_by_severity': {},
            'recovery_rate': 0.0
        }
    
    def create_error(
        self,
        error_code: str,
        category: ErrorCategory,
        severity: ErrorSeverity,
        message: str,
        context: ErrorContext,
        recovery_strategy: RecoveryStrategy = RecoveryStrategy.SKIP
    ) -> EnhancedError:
        """
        创建增强错误
        
        Args:
            error_code: 错误代码
            category: 类别
            severity: 严重程度
            message: 消息
            context: 上下文
            recovery_strategy: 恢复策略
            
        Returns:
            增强错误
        """
        import uuid
        
        error = EnhancedError(
            error_id=str(uuid.uuid4()),
            error_code=error_code,
            category=category,
            severity=severity,
            message=message,
            context=context,
            suggestions=[],
            recovery_strategy=recovery_strategy
        )
        
        # 生成建议
        error.suggestions = self.suggestion_engine.generate_suggestions(error)
        
        return error
    
    def handle_error(self, error: EnhancedError) -> bool:
        """
        处理错误
        
        Args:
            error: 增强错误
            
        Returns:
            是否成功处理
        """
        if len(self.errors) >= self.max_errors:
            print(f"错误数量达到上限: {self.max_errors}")
            return False
        
        # 添加错误
        self.errors.append(error)
        error.handled = True
        
        # 更新统计
        self._update_stats(error)
        
        # 尝试恢复
        if error.severity != ErrorSeverity.FATAL:
            recovered = self.recovery_system.recover(error)
            return recovered
        
        return False
    
    def _update_stats(self, error: EnhancedError):
        """更新统计"""
        self.stats['total_errors'] += 1
        
        # 按类别统计
        category = error.category.value
        if category not in self.stats['errors_by_category']:
            self.stats['errors_by_category'][category] = 0
        self.stats['errors_by_category'][category] += 1
        
        # 按严重程度统计
        severity = error.severity.value
        if severity not in self.stats['errors_by_severity']:
            self.stats['errors_by_severity'][severity] = 0
        self.stats['errors_by_severity'][severity] += 1
    
    def get_errors(self) -> List[EnhancedError]:
        """获取所有错误"""
        return self.errors.copy()
    
    def get_errors_by_category(self, category: ErrorCategory) -> List[EnhancedError]:
        """按类别获取错误"""
        return [e for e in self.errors if e.category == category]
    
    def get_errors_by_severity(self, severity: ErrorSeverity) -> List[EnhancedError]:
        """按严重程度获取错误"""
        return [e for e in self.errors if e.severity == severity]
    
    def has_errors(self) -> bool:
        """是否有错误"""
        return len(self.errors) > 0
    
    def has_fatal_errors(self) -> bool:
        """是否有致命错误"""
        return any(e.severity == ErrorSeverity.FATAL for e in self.errors)
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取统计信息"""
        stats = self.stats.copy()
        stats.update(self.recovery_system.get_recovery_stats())
        return stats
    
    def clear(self):
        """清空错误"""
        self.errors.clear()
        self.stats = {
            'total_errors': 0,
            'errors_by_category': {},
            'errors_by_severity': {},
            'recovery_rate': 0.0
        }
    
    def format_all_errors(self) -> str:
        """格式化所有错误"""
        if not self.errors:
            return "没有错误"
        
        lines = [f"共 {len(self.errors)} 个错误:\n"]
        for i, error in enumerate(self.errors, 1):
            lines.append(f"\n{'='*60}")
            lines.append(f"错误 {i}:")
            lines.append(error.format_error())
        
        return '\n'.join(lines)


# 工厂函数
def create_error_context(
    source_code: str,
    line_number: int,
    column_number: int,
    offset: int = 0,
    current_token: Optional[str] = None,
    expected_tokens: Optional[List[str]] = None
) -> ErrorContext:
    """创建错误上下文"""
    lines = source_code.split('\n')
    start = max(0, line_number - 2)
    end = min(len(lines), line_number + 2)
    surrounding_lines = lines[start:end]
    
    return ErrorContext(
        source_code=source_code,
        line_number=line_number,
        column_number=column_number,
        offset=offset,
        surrounding_lines=surrounding_lines,
        current_token=current_token,
        expected_tokens=expected_tokens or [],
        call_stack=[]
    )


def create_enhanced_error_handler(max_errors: int = 100) -> EnhancedErrorHandler:
    """创建增强错误处理器"""
    return EnhancedErrorHandler(max_errors)