"""
言律语言多轨制支持

支持在言律代码中嵌入Python、JavaScript、SQL代码
"""

from typing import List, Dict, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum


class TrackType(Enum):
    """轨类型"""
    YANLV = "yanlv"       # 言律轨
    PYTHON = "python"     # Python轨
    JAVASCRIPT = "javascript"  # JavaScript轨
    SQL = "sql"           # SQL轨


@dataclass
class TrackBlock:
    """轨块"""
    track_type: TrackType
    code: str
    start_line: int
    end_line: int
    variables: Dict[str, Any] = field(default_factory=dict)


@dataclass
class MultiTrackProgram:
    """多轨程序"""
    blocks: List[TrackBlock] = field(default_factory=list)
    global_variables: Dict[str, Any] = field(default_factory=dict)


class MultiTrackParser:
    """多轨解析器"""
    
    def __init__(self):
        """初始化解析器"""
        self.track_keywords = {
            'Python轨': TrackType.PYTHON,
            'JavaScript轨': TrackType.JAVASCRIPT,
            'SQL轨': TrackType.SQL,
            '言律轨': TrackType.YANLV,
        }
        
        self.end_keywords = {
            '结束Python轨',
            '结束JavaScript轨',
            '结束SQL轨',
            '结束言律轨',
            '结束轨',
        }
    
    def parse(self, source: str) -> MultiTrackProgram:
        """
        解析多轨源代码
        
        Args:
            source: 源代码
            
        Returns:
            多轨程序
        """
        program = MultiTrackProgram()
        lines = source.split('\n')
        
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            
            # 检查是否是轨开始
            track_type = self._get_track_type(line)
            
            if track_type:
                # 解析轨块
                block, i = self._parse_track_block(lines, i, track_type)
                program.blocks.append(block)
            else:
                # 默认为言律轨
                if line and not line.startswith('//'):
                    block = TrackBlock(
                        track_type=TrackType.YANLV,
                        code=line,
                        start_line=i,
                        end_line=i
                    )
                    program.blocks.append(block)
            
            i += 1
        
        return program
    
    def _get_track_type(self, line: str) -> Optional[TrackType]:
        """获取轨类型"""
        for keyword, track_type in self.track_keywords.items():
            if line.startswith(keyword):
                return track_type
        return None
    
    def _parse_track_block(self, lines: List[str], start: int, 
                          track_type: TrackType) -> Tuple[TrackBlock, int]:
        """解析轨块"""
        code_lines = []
        i = start + 1  # 跳过开始行
        
        while i < len(lines):
            line = lines[i].strip()
            
            # 检查是否是轨结束
            if self._is_track_end(line, track_type):
                break
            
            code_lines.append(lines[i])
            i += 1
        
        code = '\n'.join(code_lines)
        
        return TrackBlock(
            track_type=track_type,
            code=code,
            start_line=start,
            end_line=i
        ), i
    
    def _is_track_end(self, line: str, track_type: TrackType) -> bool:
        """检查是否是轨结束"""
        if line in self.end_keywords:
            return True
        
        end_keyword = f'结束{track_type.value}轨'
        return line == end_keyword


class MultiTrackExecutor:
    """多轨执行器"""
    
    def __init__(self):
        """初始化执行器"""
        self.parsers = {
            TrackType.YANLV: self._execute_yanlv,
            TrackType.PYTHON: self._execute_python,
            TrackType.JAVASCRIPT: self._execute_javascript,
            TrackType.SQL: self._execute_sql,
        }
    
    def execute(self, program: MultiTrackProgram) -> Dict[str, Any]:
        """
        执行多轨程序
        
        Args:
            program: 多轨程序
            
        Returns:
            执行结果
        """
        results = {}
        context = {'variables': program.global_variables.copy()}
        
        for block in program.blocks:
            executor = self.parsers.get(block.track_type)
            if executor:
                result = executor(block.code, context)
                results[f'{block.track_type.value}_{block.start_line}'] = result
                
                # 更新上下文
                if isinstance(result, dict):
                    context['variables'].update(result)
        
        return results
    
    def _execute_yanlv(self, code: str, context: Dict) -> Any:
        """执行言律代码"""
        # 这里应该调用言律解释器
        # 简化实现：返回代码
        return {'type': 'yanlv', 'code': code}
    
    def _execute_python(self, code: str, context: Dict) -> Any:
        """执行Python代码"""
        try:
            # 创建执行环境
            local_vars = context['variables'].copy()
            exec(code, {}, local_vars)
            return local_vars
        except Exception as e:
            return {'error': str(e)}
    
    def _execute_javascript(self, code: str, context: Dict) -> Any:
        """执行JavaScript代码"""
        # 这里需要JavaScript运行时
        # 简化实现：返回代码
        return {'type': 'javascript', 'code': code}
    
    def _execute_sql(self, code: str, context: Dict) -> Any:
        """执行SQL代码"""
        # 这里需要数据库连接
        # 简化实现：返回代码
        return {'type': 'sql', 'code': code}


class MultiTrackCodeGenerator:
    """多轨代码生成器"""
    
    def __init__(self):
        """初始化生成器"""
        self.generators = {
            TrackType.YANLV: self._generate_yanlv,
            TrackType.PYTHON: self._generate_python,
            TrackType.JAVASCRIPT: self._generate_javascript,
            TrackType.SQL: self._generate_sql,
        }
    
    def generate(self, program: MultiTrackProgram, 
                target: TrackType = TrackType.PYTHON) -> str:
        """
        生成目标代码
        
        Args:
            program: 多轨程序
            target: 目标轨类型
            
        Returns:
            生成的代码
        """
        lines = []
        
        for block in program.blocks:
            if block.track_type == target:
                # 同轨代码，直接输出
                lines.append(block.code)
            else:
                # 异轨代码，需要转换
                generator = self.generators.get(block.track_type)
                if generator:
                    converted = generator(block.code, target)
                    lines.append(converted)
        
        return '\n\n'.join(lines)
    
    def _generate_yanlv(self, code: str, target: TrackType) -> str:
        """转换言律代码"""
        if target == TrackType.PYTHON:
            return f"# 言律代码（需要转换）\n# {code}"
        elif target == TrackType.JAVASCRIPT:
            return f"// 言律代码（需要转换）\n// {code}"
        else:
            return code
    
    def _generate_python(self, code: str, target: TrackType) -> str:
        """转换Python代码"""
        if target == TrackType.JAVASCRIPT:
            return f"// Python代码（需要转换）\n/* {code} */"
        else:
            return code
    
    def _generate_javascript(self, code: str, target: TrackType) -> str:
        """转换JavaScript代码"""
        if target == TrackType.PYTHON:
            return f"# JavaScript代码（需要转换）\n# {code}"
        else:
            return code
    
    def _generate_sql(self, code: str, target: TrackType) -> str:
        """转换SQL代码"""
        if target == TrackType.PYTHON:
            return f'# SQL代码\n"""{code}"""'
        elif target == TrackType.JAVASCRIPT:
            return f'// SQL代码\n`{code}`'
        else:
            return code


# ============================================================================
# 辅助函数
# ============================================================================

def create_multi_track_parser() -> MultiTrackParser:
    """创建多轨解析器"""
    return MultiTrackParser()


def create_multi_track_executor() -> MultiTrackExecutor:
    """创建多轨执行器"""
    return MultiTrackExecutor()


def create_multi_track_generator() -> MultiTrackCodeGenerator:
    """创建多轨代码生成器"""
    return MultiTrackCodeGenerator()


# ============================================================================
# 导出
# ============================================================================

__all__ = [
    'TrackType',
    'TrackBlock',
    'MultiTrackProgram',
    'MultiTrackParser',
    'MultiTrackExecutor',
    'MultiTrackCodeGenerator',
    'create_multi_track_parser',
    'create_multi_track_executor',
    'create_multi_track_generator',
]
