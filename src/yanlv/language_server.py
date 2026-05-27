"""
言律语言Language Server Protocol实现

提供智能补全、语法诊断、跳转定义等IDE功能
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import re


@dataclass
class Position:
    """位置"""
    line: int      # 行号(从0开始)
    character: int # 列号(从0开始)


@dataclass
class Range:
    """范围"""
    start: Position
    end: Position


@dataclass
class Diagnostic:
    """诊断信息"""
    range: Range
    message: str
    severity: int  # 1=Error, 2=Warning, 3=Information, 4=Hint
    source: str = "yanlv"
    code: Optional[str] = None


@dataclass
class CompletionItem:
    """补全项"""
    label: str           # 显示文本
    kind: int            # 补全类型
    detail: str = ""     # 详细信息
    documentation: str = ""  # 文档
    insert_text: str = ""    # 插入文本


@dataclass
class Location:
    """位置信息"""
    uri: str      # 文件URI
    range: Range


class YanLvLanguageServer:
    """
    言律语言服务器
    
    实现LSP核心功能
    """
    
    def __init__(self):
        """初始化语言服务器"""
        # 关键字列表
        self.keywords = [
            "定义", "设", "若", "则", "否则", "当", "执行", "函数",
            "返回", "输出", "输入", "导入", "导出", "类", "继承",
            "真", "假", "空", "且", "或", "非", "在", "不在",
            "添加", "删除", "长度", "查找", "替换", "分割", "子串"
        ]
        
        # 内置函数列表
        self.builtins = [
            "打印", "取整", "取余", "绝对值", "平方根", "幂",
            "正弦", "余弦", "正切", "对数", "指数",
            "取最大", "取最小", "求和", "排序", "反转",
            "连接", "包含", "索引", "计数", "清空",
            "读取文件", "写入文件", "执行命令"
        ]
        
        # 标准库函数
        self.stdlib = [
            "数学.圆周率", "数学.自然常数", "数学.随机数",
            "字符串.转大写", "字符串.转小写", "字符串.去空格",
            "数组.创建", "数组.填充", "数组.映射", "数组.过滤"
        ]
        
        # 文档缓存
        self.documents: Dict[str, str] = {}
        
        # 符号表(用于跳转定义)
        self.symbols: Dict[str, List[Location]] = {}
    
    def did_open(self, uri: str, content: str) -> None:
        """
        文档打开事件
        
        Args:
            uri: 文档URI
            content: 文档内容
        """
        self.documents[uri] = content
        self._analyze_document(uri, content)
    
    def did_change(self, uri: str, content: str) -> None:
        """
        文档变更事件
        
        Args:
            uri: 文档URI
            content: 新内容
        """
        self.documents[uri] = content
        self._analyze_document(uri, content)
    
    def did_close(self, uri: str) -> None:
        """
        文档关闭事件
        
        Args:
            uri: 文档URI
        """
        if uri in self.documents:
            del self.documents[uri]
    
    def _analyze_document(self, uri: str, content: str) -> None:
        """
        分析文档,提取符号
        
        Args:
            uri: 文档URI
            content: 文档内容
        """
        # 清除旧符号
        symbols_to_remove = [
            name for name, locs in self.symbols.items()
            if any(loc.uri == uri for loc in locs)
        ]
        for name in symbols_to_remove:
            self.symbols[name] = [
                loc for loc in self.symbols[name] if loc.uri != uri
            ]
        
        # 提取新符号
        lines = content.split('\n')
        
        for line_num, line in enumerate(lines):
            # 匹配变量定义: 定义 变量名 为 值
            match = re.search(r'定义\s+(\w+)\s+为', line)
            if match:
                var_name = match.group(1)
                start_char = match.start(1)
                end_char = match.end(1)
                
                location = Location(
                    uri=uri,
                    range=Range(
                        start=Position(line_num, start_char),
                        end=Position(line_num, end_char)
                    )
                )
                
                if var_name not in self.symbols:
                    self.symbols[var_name] = []
                self.symbols[var_name].append(location)
            
            # 匹配函数定义: 函数 函数名(参数)
            match = re.search(r'函数\s+(\w+)\s*\(', line)
            if match:
                func_name = match.group(1)
                start_char = match.start(1)
                end_char = match.end(1)
                
                location = Location(
                    uri=uri,
                    range=Range(
                        start=Position(line_num, start_char),
                        end=Position(line_num, end_char)
                    )
                )
                
                if func_name not in self.symbols:
                    self.symbols[func_name] = []
                self.symbols[func_name].append(location)
    
    def get_diagnostics(self, uri: str) -> List[Diagnostic]:
        """
        获取诊断信息
        
        Args:
            uri: 文档URI
            
        Returns:
            诊断列表
        """
        if uri not in self.documents:
            return []
        
        content = self.documents[uri]
        diagnostics = []
        
        lines = content.split('\n')
        
        for line_num, line in enumerate(lines):
            # 检查未闭合的括号
            open_parens = line.count('(') - line.count(')')
            if open_parens > 0:
                diagnostics.append(Diagnostic(
                    range=Range(
                        start=Position(line_num, 0),
                        end=Position(line_num, len(line))
                    ),
                    message="括号未闭合",
                    severity=1,
                    code="YANLV-0001"
                ))
            
            # 检查未闭合的引号
            quote_count = line.count('"') + line.count("'")
            if quote_count % 2 != 0:
                diagnostics.append(Diagnostic(
                    range=Range(
                        start=Position(line_num, 0),
                        end=Position(line_num, len(line))
                    ),
                    message="引号未闭合",
                    severity=1,
                    code="YANLV-0002"
                ))
        
        return diagnostics
    
    def get_completions(
        self, 
        uri: str, 
        position: Position
    ) -> List[CompletionItem]:
        """
        获取补全列表
        
        Args:
            uri: 文档URI
            position: 位置
            
        Returns:
            补全项列表
        """
        completions = []
        
        # 添加关键字补全
        for keyword in self.keywords:
            completions.append(CompletionItem(
                label=keyword,
                kind=14,  # Keyword
                detail="关键字",
                insert_text=keyword
            ))
        
        # 添加内置函数补全
        for builtin in self.builtins:
            completions.append(CompletionItem(
                label=builtin,
                kind=3,  # Function
                detail="内置函数",
                insert_text=builtin
            ))
        
        # 添加标准库函数补全
        for std_func in self.stdlib:
            completions.append(CompletionItem(
                label=std_func,
                kind=3,  # Function
                detail="标准库函数",
                insert_text=std_func
            ))
        
        # 添加用户定义的符号补全
        for symbol_name in self.symbols:
            completions.append(CompletionItem(
                label=symbol_name,
                kind=13,  # Variable
                detail="用户定义",
                insert_text=symbol_name
            ))
        
        return completions
    
    def get_definition(
        self, 
        uri: str, 
        position: Position
    ) -> Optional[Location]:
        """
        获取定义位置
        
        Args:
            uri: 文档URI
            position: 位置
            
        Returns:
            定义位置
        """
        if uri not in self.documents:
            return None
        
        content = self.documents[uri]
        lines = content.split('\n')
        
        if position.line >= len(lines):
            return None
        
        line = lines[position.line]
        
        # 提取光标位置的标识符
        # 简化实现: 查找光标附近的单词
        start = position.character
        while start > 0 and (line[start-1].isalnum() or line[start-1] == '_'):
            start -= 1
        
        end = position.character
        while end < len(line) and (line[end].isalnum() or line[end] == '_'):
            end += 1
        
        if start == end:
            return None
        
        identifier = line[start:end]
        
        # 查找定义
        if identifier in self.symbols and self.symbols[identifier]:
            return self.symbols[identifier][0]
        
        return None
    
    def get_references(
        self, 
        uri: str, 
        position: Position
    ) -> List[Location]:
        """
        查找所有引用
        
        Args:
            uri: 文档URI
            position: 位置
            
        Returns:
            引用位置列表
        """
        # 先获取定义
        definition = self.get_definition(uri, position)
        if not definition:
            return []
        
        # 提取标识符
        def_uri = definition.uri
        if def_uri not in self.documents:
            return []
        
        def_content = self.documents[def_uri]
        def_lines = def_content.split('\n')
        
        if definition.range.start.line >= len(def_lines):
            return []
        
        def_line = def_lines[definition.range.start.line]
        identifier = def_line[
            definition.range.start.character:definition.range.end.character
        ]
        
        # 在所有文档中查找引用
        references = []
        
        for doc_uri, doc_content in self.documents.items():
            lines = doc_content.split('\n')
            
            for line_num, line in enumerate(lines):
                # 查找所有匹配
                for match in re.finditer(r'\b' + re.escape(identifier) + r'\b', line):
                    references.append(Location(
                        uri=doc_uri,
                        range=Range(
                            start=Position(line_num, match.start()),
                            end=Position(line_num, match.end())
                        )
                    ))
        
        return references
    
    def get_hover(
        self, 
        uri: str, 
        position: Position
    ) -> Optional[str]:
        """
        获取悬停提示
        
        Args:
            uri: 文档URI
            position: 位置
            
        Returns:
            提示文本
        """
        if uri not in self.documents:
            return None
        
        content = self.documents[uri]
        lines = content.split('\n')
        
        if position.line >= len(lines):
            return None
        
        line = lines[position.line]
        
        # 提取光标位置的标识符
        start = position.character
        while start > 0 and (line[start-1].isalnum() or line[start-1] == '_'):
            start -= 1
        
        end = position.character
        while end < len(line) and (line[end].isalnum() or line[end] == '_'):
            end += 1
        
        if start == end:
            return None
        
        identifier = line[start:end]
        
        # 检查是否是关键字
        if identifier in self.keywords:
            return f"**关键字**: {identifier}"
        
        # 检查是否是内置函数
        if identifier in self.builtins:
            return f"**内置函数**: {identifier}"
        
        # 检查是否是标准库函数
        if identifier in self.stdlib:
            return f"**标准库函数**: {identifier}"
        
        # 检查是否是用户定义的符号
        if identifier in self.symbols:
            locations = self.symbols[identifier]
            if locations:
                loc = locations[0]
                return f"**定义位置**: {loc.uri}:{loc.range.start.line + 1}"
        
        return None
