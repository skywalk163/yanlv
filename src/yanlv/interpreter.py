"""
言律语言简单解释器
支持条件、循环、函数等程序块的执行
"""
from typing import List, Dict, Any, Optional, Tuple
from .lexer.lexer_token import Token, TokenType


class YanLuInterpreter:
    """言律语言解释器"""

    def __init__(self):
        """初始化解释器"""
        self.variables: Dict[str, Any] = {}
        self.functions: Dict[str, Dict] = {}
        self.output: List[str] = []

    def execute(self, tokens: List[Token]) -> List[str]:
        """
        执行词元列表

        Args:
            tokens: 词元列表

        Returns:
            输出列表
        """
        self.output = []
        self._execute_tokens(tokens, 0, len(tokens))
        return self.output

    def _execute_tokens(self, tokens: List[Token], start: int, end: int) -> int:
        """
        执行指定范围的词元

        Args:
            tokens: 词元列表
            start: 起始位置
            end: 结束位置

        Returns:
            执行到的位置
        """
        i = start
        while i < end:
            token = tokens[i]

            # 跳过换行符
            if token.type == TokenType.NEWLINE:
                i += 1
                continue

            # 处理输出语句
            if token.type == TokenType.OUTPUT:
                i = self._execute_output(tokens, i)

            # 处理变量定义
            elif token.type == TokenType.DEFINE:
                i = self._execute_define(tokens, i)

            # 处理条件语句
            elif token.type == TokenType.IF:
                i = self._execute_if(tokens, i)

            # 处理循环语句
            elif token.type == TokenType.LOOP:
                i = self._execute_loop(tokens, i)

            # 处理函数定义
            elif token.type == TokenType.FUNCTION:
                i = self._execute_function(tokens, i)

            # 处理函数调用
            elif token.type == TokenType.IDENTIFIER and i + 1 < len(tokens):
                if tokens[i + 1].type == TokenType.PARAMETER:
                    i = self._execute_call(tokens, i)
                else:
                    i += 1

            # 处理返回语句
            elif token.type == TokenType.RETURN:
                i = self._execute_return(tokens, i)

            else:
                i += 1

        return i

    def _execute_output(self, tokens: List[Token], i: int) -> int:
        """执行输出语句"""
        i += 1  # 跳过 OUTPUT

        if i < len(tokens):
            if tokens[i].type == TokenType.STRING:
                # 输出字符串
                value = tokens[i].value.strip('"\'')
                self.output.append(f"=> {value}")
                i += 1
            elif tokens[i].type == TokenType.IDENTIFIER:
                # 输出变量
                var_name = tokens[i].value
                if var_name in self.variables:
                    self.output.append(f"=> {self.variables[var_name]}")
                else:
                    self.output.append(f"=> 变量 '{var_name}' 未定义")
                i += 1
            elif tokens[i].type == TokenType.NUMBER:
                # 输出数字
                self.output.append(f"=> {tokens[i].value}")
                i += 1

        return i

    def _execute_define(self, tokens: List[Token], i: int) -> int:
        """执行变量定义"""
        i += 1  # 跳过 DEFINE

        # 跳过 VARIABLE 关键字
        if i < len(tokens) and tokens[i].type == TokenType.VARIABLE:
            i += 1

        # 获取变量名
        if i < len(tokens) and tokens[i].type == TokenType.IDENTIFIER:
            var_name = tokens[i].value
            i += 1

            # 跳过 IS
            if i < len(tokens) and tokens[i].type == TokenType.IS:
                i += 1

            # 获取值
            if i < len(tokens):
                if tokens[i].type == TokenType.NUMBER:
                    self.variables[var_name] = float(tokens[i].value)
                elif tokens[i].type == TokenType.STRING:
                    self.variables[var_name] = tokens[i].value.strip('"\'')
                else:
                    self.variables[var_name] = tokens[i].value
                i += 1

        return i

    def _execute_if(self, tokens: List[Token], i: int) -> int:
        """执行条件语句"""
        i += 1  # 跳过 IF

        # 简化处理：假设条件为真
        # 找到 END 的位置
        start = i
        depth = 1
        while i < len(tokens) and depth > 0:
            if tokens[i].type == TokenType.IF:
                depth += 1
            elif tokens[i].type == TokenType.END:
                depth -= 1
            i += 1

        # 执行条件块内的代码
        self._execute_tokens(tokens, start, i - 1)

        return i

    def _execute_loop(self, tokens: List[Token], i: int) -> int:
        """执行循环语句"""
        i += 1  # 跳过 LOOP

        # 获取循环次数
        count = 1
        if i < len(tokens) and tokens[i].type == TokenType.NUMBER:
            count = int(tokens[i].value)
            i += 1

        # 跳过 "次执行"
        while i < len(tokens) and tokens[i].type == TokenType.IDENTIFIER:
            i += 1

        # 找到 END 的位置
        start = i
        depth = 1
        end_pos = i
        while end_pos < len(tokens) and depth > 0:
            if tokens[end_pos].type == TokenType.LOOP:
                depth += 1
            elif tokens[end_pos].type == TokenType.END:
                depth -= 1
            end_pos += 1

        # 执行循环
        for _ in range(count):
            self._execute_tokens(tokens, start, end_pos - 1)

        return end_pos

    def _execute_function(self, tokens: List[Token], i: int) -> int:
        """执行函数定义"""
        i += 1  # 跳过 FUNCTION

        # 获取函数名
        func_name = ""
        if i < len(tokens) and tokens[i].type == TokenType.IDENTIFIER:
            func_name = tokens[i].value
            i += 1

        # 获取参数列表
        params = []
        while i < len(tokens) and tokens[i].type == TokenType.PARAMETER:
            i += 1
            if i < len(tokens) and tokens[i].type == TokenType.IDENTIFIER:
                params.append(tokens[i].value)
                i += 1

        # 找到函数体的 END
        start = i
        depth = 1
        end_pos = i
        while end_pos < len(tokens) and depth > 0:
            if tokens[end_pos].type == TokenType.FUNCTION:
                depth += 1
            elif tokens[end_pos].type == TokenType.END:
                depth -= 1
            end_pos += 1

        # 保存函数定义
        self.functions[func_name] = {
            'params': params,
            'body_start': start,
            'body_end': end_pos - 1,
            'tokens': tokens
        }

        self.output.append(f"=> 函数 {func_name} 已定义")

        return end_pos

    def _execute_call(self, tokens: List[Token], i: int) -> int:
        """执行函数调用"""
        # 获取函数名
        func_name = tokens[i].value
        i += 1

        # 跳过 PARAMETER
        if i < len(tokens) and tokens[i].type == TokenType.PARAMETER:
            i += 1

        # 获取参数值
        args = []
        while i < len(tokens):
            if tokens[i].type == TokenType.NUMBER:
                args.append(float(tokens[i].value))
                i += 1
            elif tokens[i].type == TokenType.IDENTIFIER:
                if tokens[i].value in self.variables:
                    args.append(self.variables[tokens[i].value])
                else:
                    args.append(tokens[i].value)
                i += 1
            else:
                break

        # 执行函数
        if func_name in self.functions:
            func = self.functions[func_name]
            # 保存当前变量
            old_vars = self.variables.copy()

            # 绑定参数
            for param, arg in zip(func['params'], args):
                self.variables[param] = arg

            # 执行函数体
            self._execute_tokens(func['tokens'], func['body_start'], func['body_end'])

            # 恢复变量
            self.variables = old_vars

        return i

    def _execute_return(self, tokens: List[Token], i: int) -> int:
        """执行返回语句"""
        i += 1  # 跳过 RETURN

        # 获取返回值
        if i < len(tokens):
            if tokens[i].type == TokenType.IDENTIFIER:
                var_name = tokens[i].value
                if var_name in self.variables:
                    return self.variables[var_name]
                i += 1
            elif tokens[i].type == TokenType.NUMBER:
                return float(tokens[i].value)

        return i


def create_interpreter() -> YanLuInterpreter:
    """创建解释器实例"""
    return YanLuInterpreter()
