"""
言律语言编译器
整合词法分析和解释执行
"""

from typing import List, Optional, Dict, Any
from .lexer.lexer_modular import tokenize
from .interpreter_complete import CompleteInterpreter
from .advanced_interpreter import AdvancedInterpreter


class YanLuCompiler:
    """
    言律语言编译器
    支持词法分析、解释执行和代码编译
    """
    
    def __init__(self, use_advanced: bool = True):
        """
        初始化编译器
        
        Args:
            use_advanced: 是否使用高级解释器（支持因果链等高级语法）
        """
        if use_advanced:
            self.interpreter = AdvancedInterpreter()
        else:
            self.interpreter = CompleteInterpreter()
        self.variables: Dict[str, Any] = {}
        self.functions: Dict[str, Dict] = {}
    
    def compile(self, source_code: str) -> str:
        """
        编译言律代码（实际上是解释执行）
        
        Args:
            source_code: 言律源代码
            
        Returns:
            执行结果
        """
        # 词法分析
        tokens = tokenize(source_code)
        
        # 解释执行
        output = self.interpreter.execute(tokens)
        
        # 返回结果
        return "\n".join(output)
    
    def run(self, source_code: str) -> List[str]:
        """
        运行言律代码
        
        Args:
            source_code: 言律源代码
            
        Returns:
            输出列表
        """
        # 词法分析
        tokens = tokenize(source_code)
        
        # 解释执行
        return self.interpreter.execute(tokens)
    
    def execute(self, source_code: str) -> List[str]:
        """
        执行言律代码（与run方法相同，为了兼容性）
        
        Args:
            source_code: 言律源代码
            
        Returns:
            输出列表
        """
        return self.run(source_code)
    
    def compile_to_python(self, source_code: str) -> str:
        """
        编译言律代码到Python代码
        
        Args:
            source_code: 言律源代码
            
        Returns:
            Python代码
        """
        lines = source_code.split('\n')
        compiled = []
        
        for line in lines:
            trimmed = line.strip()
            
            if not trimmed or trimmed.startswith('//') or trimmed.startswith('#'):
                continue
            
            # 处理变量定义
            if trimmed.startswith('定义变量'):
                # 匹配: 定义变量x为10 或 定义变量x为"hello"
                import re
                match = re.match(r'定义变量(\w+)为(.+)', trimmed)
                if match:
                    name = match.group(1)
                    value = match.group(2).strip()
                    compiled.append(f'{name} = {value}')
            
            # 处理输出
            elif trimmed.startswith('输出'):
                content = trimmed[2:].strip()
                compiled.append(f'print({content})')
            
            # 处理数组定义
            elif trimmed.startswith('定义数组'):
                import re
                match = re.match(r'定义数组(\w+)为\[(.+)\]', trimmed)
                if match:
                    name = match.group(1)
                    values = match.group(2)
                    compiled.append(f'{name} = [{values}]')
        
        return '\n'.join(compiled)
    
    def compile_to_javascript(self, source_code: str) -> str:
        """
        编译言律代码到JavaScript代码
        
        Args:
            source_code: 言律源代码
            
        Returns:
            JavaScript代码
        """
        lines = source_code.split('\n')
        compiled = []
        
        for line in lines:
            trimmed = line.strip()
            
            if not trimmed or trimmed.startswith('//') or trimmed.startswith('#'):
                continue
            
            # 处理变量定义
            if trimmed.startswith('定义变量'):
                import re
                match = re.match(r'定义变量(\w+)为(.+)', trimmed)
                if match:
                    name = match.group(1)
                    value = match.group(2).strip()
                    compiled.append(f'let {name} = {value};')
            
            # 处理输出
            elif trimmed.startswith('输出'):
                content = trimmed[2:].strip()
                compiled.append(f'console.log({content});')
            
            # 处理数组定义
            elif trimmed.startswith('定义数组'):
                import re
                match = re.match(r'定义数组(\w+)为\[(.+)\]', trimmed)
                if match:
                    name = match.group(1)
                    values = match.group(2)
                    compiled.append(f'const {name} = [{values}];')
        
        return '\n'.join(compiled)
