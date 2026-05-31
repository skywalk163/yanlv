"""
言律语言高级解析器
支持因果链语法、语境省略语法、状态流语法等高级特性
"""

from typing import List, Dict, Any, Optional, Tuple
from .lexer.lexer_token import Token, TokenType


class CausalChainParser:
    """因果链解析器"""
    
    def __init__(self):
        """初始化因果链解析器"""
        self.causal_chains: List[Dict] = []
    
    def parse_causal_chain(self, tokens: List[Token], start: int) -> Tuple[Dict, int]:
        """
        解析因果链语法
        格式：条件，动作。
        
        Args:
            tokens: 词元列表
            start: 起始位置
            
        Returns:
            (因果链字典, 下一个位置)
        """
        i = start
        condition_tokens = []
        action_tokens = []
        
        # 解析条件部分（直到遇到逗号）
        while i < len(tokens) and tokens[i].type != TokenType.COMMA:
            if tokens[i].type == TokenType.NEWLINE:
                break
            condition_tokens.append(tokens[i])
            i += 1
        
        # 跳过逗号
        if i < len(tokens) and tokens[i].type == TokenType.COMMA:
            i += 1
        
        # 解析动作部分（直到遇到句号）
        while i < len(tokens) and tokens[i].type != TokenType.PERIOD:
            if tokens[i].type == TokenType.NEWLINE:
                break
            action_tokens.append(tokens[i])
            i += 1
        
        # 跳过句号
        if i < len(tokens) and tokens[i].type == TokenType.PERIOD:
            i += 1
        
        causal_chain = {
            'type': 'causal_chain',
            'condition': condition_tokens,
            'action': action_tokens
        }
        
        return causal_chain, i
    
    def is_causal_chain_start(self, tokens: List[Token], i: int) -> bool:
        """检查是否是因果链的开始"""
        # 因果链的特征：后面有逗号和句号
        j = i
        has_comma = False
        has_period = False
        
        while j < len(tokens) and tokens[j].type not in (TokenType.NEWLINE, TokenType.EOF):
            if tokens[j].type == TokenType.COMMA:
                has_comma = True
            elif tokens[j].type == TokenType.PERIOD:
                has_period = True
                break
            j += 1
        
        return has_comma and has_period


class ContextOmissionParser:
    """语境省略解析器"""
    
    def __init__(self):
        """初始化语境省略解析器"""
        self.context_stack: List[Dict] = []
    
    def parse_theme_block(self, tokens: List[Token], start: int) -> Tuple[Dict, int]:
        """
        解析主题块
        格式：以X为主题：... 或 X：...
        
        Args:
            tokens: 词元列表
            start: 起始位置
            
        Returns:
            (主题块字典, 下一个位置)
        """
        i = start
        theme_name = None
        
        # 检查是否是"以X为主题"格式
        if tokens[i].value == '以':
            i += 1
            if i < len(tokens) and tokens[i].type == TokenType.IDENTIFIER:
                theme_name = tokens[i].value
                i += 1
                # 跳过"为主题"
                while i < len(tokens) and tokens[i].value in ('为', '主题'):
                    i += 1
        # 否则是"X："格式
        elif tokens[i].type == TokenType.IDENTIFIER:
            theme_name = tokens[i].value
            i += 1
        
        # 跳过冒号
        if i < len(tokens) and tokens[i].type == TokenType.COLON:
            i += 1
        
        # 解析块内容
        block_tokens = []
        indent_level = tokens[i].indent if i < len(tokens) else 0
        
        while i < len(tokens):
            if tokens[i].type == TokenType.NEWLINE:
                i += 1
                continue
            
            # 检查缩进级别
            if tokens[i].indent <= indent_level:
                break
            
            block_tokens.append(tokens[i])
            i += 1
        
        theme_block = {
            'type': 'theme_block',
            'theme': theme_name,
            'body': block_tokens
        }
        
        return theme_block, i
    
    def is_theme_block_start(self, tokens: List[Token], i: int) -> bool:
        """检查是否是主题块的开始"""
        # "以X为主题：" 或 "X："
        if tokens[i].value == '以':
            return True
        if tokens[i].type == TokenType.IDENTIFIER:
            # 检查后面是否有冒号
            j = i + 1
            while j < len(tokens) and tokens[j].type == TokenType.NEWLINE:
                j += 1
            if j < len(tokens) and tokens[j].type == TokenType.COLON:
                return True
        return False


class StateFlowParser:
    """状态流解析器"""
    
    def __init__(self):
        """初始化状态流解析器"""
        self.state_transitions: List[Dict] = []
    
    def parse_state_transition(self, tokens: List[Token], start: int) -> Tuple[Dict, int]:
        """
        解析状态转换
        格式：状态变为X，动作。
        
        Args:
            tokens: 词元列表
            start: 起始位置
            
        Returns:
            (状态转换字典, 下一个位置)
        """
        i = start
        state_tokens = []
        action_tokens = []
        
        # 解析状态部分
        while i < len(tokens) and tokens[i].type != TokenType.COMMA:
            if tokens[i].type == TokenType.NEWLINE:
                break
            state_tokens.append(tokens[i])
            i += 1
        
        # 跳过逗号
        if i < len(tokens) and tokens[i].type == TokenType.COMMA:
            i += 1
        
        # 解析动作部分
        while i < len(tokens) and tokens[i].type != TokenType.PERIOD:
            if tokens[i].type == TokenType.NEWLINE:
                break
            action_tokens.append(tokens[i])
            i += 1
        
        # 跳过句号
        if i < len(tokens) and tokens[i].type == TokenType.PERIOD:
            i += 1
        
        state_transition = {
            'type': 'state_transition',
            'state': state_tokens,
            'action': action_tokens
        }
        
        return state_transition, i


class AdvancedParser:
    """高级解析器 - 整合所有高级语法解析器"""
    
    def __init__(self):
        """初始化高级解析器"""
        self.causal_parser = CausalChainParser()
        self.context_parser = ContextOmissionParser()
        self.state_parser = StateFlowParser()
    
    def parse(self, tokens: List[Token]) -> List[Dict]:
        """
        解析高级语法
        
        Args:
            tokens: 词元列表
            
        Returns:
            解析结果列表
        """
        results = []
        i = 0
        
        while i < len(tokens):
            token = tokens[i]
            
            # 跳过换行符
            if token.type == TokenType.NEWLINE:
                i += 1
                continue
            
            # 检查因果链
            if self.causal_parser.is_causal_chain_start(tokens, i):
                causal_chain, i = self.causal_parser.parse_causal_chain(tokens, i)
                results.append(causal_chain)
                continue
            
            # 检查主题块
            if self.context_parser.is_theme_block_start(tokens, i):
                theme_block, i = self.context_parser.parse_theme_block(tokens, i)
                results.append(theme_block)
                continue
            
            # 其他情况，跳过
            i += 1
        
        return results
