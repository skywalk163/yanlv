"""
言律语言解释器 - 完整版

修复所有核心问题，提供稳定可靠的执行引擎
"""

import math
import random
from typing import List, Dict, Any, Optional, Tuple
from .lexer.lexer_token import Token, TokenType


class CompleteInterpreter:
    """完整版言律语言解释器"""

    def __init__(self):
        """初始化解释器"""
        self.variables: Dict[str, Any] = {}
        self.functions: Dict[str, Dict] = {}
        self.output: List[str] = []
        self.return_value: Any = None
        self.in_function: bool = False

    def execute(self, tokens: List[Token]) -> List[str]:
        """执行词元列表"""
        self.output = []
        self._execute_tokens(tokens, 0, len(tokens))
        return self.output

    def _execute_tokens(self, tokens: List[Token], start: int, end: int) -> int:
        """执行指定范围的词元"""
        i = start
        while i < end:
            token = tokens[i]

            # 跳过换行符
            if token.type == TokenType.NEWLINE:
                i += 1
                continue

            # 根据token类型处理
            if token.type == TokenType.OUTPUT:
                i = self._execute_output(tokens, i)
            elif token.type == TokenType.DEFINE or token.type == TokenType.DEF:
                i = self._execute_define(tokens, i)
            elif token.type == TokenType.SET:
                i = self._execute_set(tokens, i)
            elif token.type == TokenType.IF:
                i = self._execute_if(tokens, i)
            elif token.type == TokenType.LOOP:
                i = self._execute_loop(tokens, i)
            elif token.type == TokenType.FUNCTION:
                i = self._execute_function(tokens, i)
            elif token.type == TokenType.CALL:
                i = self._execute_call(tokens, i)
            elif token.type == TokenType.RETURN:
                i = self._execute_return(tokens, i)
            elif token.type == TokenType.ADD:
                i = self._execute_add(tokens, i)
            elif token.type == TokenType.REMOVE:
                i = self._execute_remove(tokens, i)
            elif token.type == TokenType.LENGTH:
                i = self._execute_length(tokens, i)
            else:
                i += 1

        return i

    def _execute_output(self, tokens: List[Token], i: int) -> int:
        """执行输出语句 - 完整版"""
        i += 1  # 跳过 OUTPUT

        if i >= len(tokens):
            return i

        # 处理字符串字面量
        if tokens[i].type == TokenType.STRING:
            self.output.append(tokens[i].value)
            return i + 1

        # 处理数字字面量
        if tokens[i].type == TokenType.NUMBER:
            self.output.append(str(tokens[i].value))
            return i + 1

        # 处理标识符（变量或表达式）
        if tokens[i].type == TokenType.IDENTIFIER:
            # 检查是否是表达式
            if self._is_expression_start(tokens, i):
                value, i = self._parse_full_expression(tokens, i)
                self.output.append(str(value))
            else:
                # 简单变量输出
                var_name = tokens[i].value
                i += 1
                
                # 检查数组访问
                if i < len(tokens) and tokens[i].type == TokenType.LBRACKET:
                    i += 1  # 跳过 [
                    index, i = self._parse_full_expression(tokens, i)
                    if i < len(tokens) and tokens[i].type == TokenType.RBRACKET:
                        i += 1
                    # 获取数组元素
                    if var_name in self.variables:
                        arr = self.variables[var_name]
                        if isinstance(arr, list) and 0 <= int(index) < len(arr):
                            self.output.append(str(arr[int(index)]))
                        else:
                            self.output.append(f"错误：索引超出范围")
                else:
                    # 输出变量值
                    if var_name in self.variables:
                        self.output.append(str(self.variables[var_name]))
                    else:
                        self.output.append(f"错误：变量未定义")

        return i

    def _is_expression_start(self, tokens: List[Token], i: int) -> bool:
        """检查是否是表达式开始"""
        if i >= len(tokens):
            return False
        
        # 如果当前是标识符，检查后面是否有运算符
        if tokens[i].type == TokenType.IDENTIFIER:
            # 检查下一个token
            if i + 1 < len(tokens):
                next_type = tokens[i + 1].type
                # 如果是运算符，则是表达式
                if next_type in (TokenType.PLUS, TokenType.MINUS, 
                                TokenType.MULTIPLY, TokenType.DIVIDE,
                                TokenType.MODULO, TokenType.LBRACKET):
                    return True
                # 如果是比较运算符，也是表达式
                if next_type in (TokenType.GREATER, TokenType.LESS,
                                TokenType.GREATER_EQUAL, TokenType.LESS_EQUAL,
                                TokenType.IS, TokenType.NOT_EQUAL):
                    return True
        
        # 如果是数字后面跟运算符
        if tokens[i].type == TokenType.NUMBER:
            if i + 1 < len(tokens):
                next_type = tokens[i + 1].type
                if next_type in (TokenType.PLUS, TokenType.MINUS,
                                TokenType.MULTIPLY, TokenType.DIVIDE,
                                TokenType.MODULO):
                    return True
        
        # 如果是左括号，是表达式
        if tokens[i].type == TokenType.LPAREN:
            return True
        
        return False

    def _parse_full_expression(self, tokens: List[Token], i: int) -> Tuple[Any, int]:
        """解析完整表达式"""
        return self._parse_additive(tokens, i)

    def _parse_additive(self, tokens: List[Token], i: int) -> Tuple[Any, int]:
        """解析加减表达式"""
        left, i = self._parse_multiplicative(tokens, i)

        while i < len(tokens) and tokens[i].type in (TokenType.PLUS, TokenType.MINUS):
            op = tokens[i].type
            i += 1
            right, i = self._parse_multiplicative(tokens, i)

            if op == TokenType.PLUS:
                # 处理字符串连接
                if isinstance(left, str) or isinstance(right, str):
                    left = str(left) + str(right)
                else:
                    left = left + right
            else:
                left = left - right

        return left, i

    def _parse_multiplicative(self, tokens: List[Token], i: int) -> Tuple[Any, int]:
        """解析乘除表达式"""
        left, i = self._parse_unary(tokens, i)

        while i < len(tokens) and tokens[i].type in (TokenType.MULTIPLY, TokenType.DIVIDE, TokenType.MODULO):
            op = tokens[i].type
            i += 1
            right, i = self._parse_unary(tokens, i)

            if op == TokenType.MULTIPLY:
                left = left * right
            elif op == TokenType.DIVIDE:
                left = left / right if right != 0 else 0
            else:
                left = left % right

        return left, i

    def _parse_unary(self, tokens: List[Token], i: int) -> Tuple[Any, int]:
        """解析一元表达式"""
        if i < len(tokens) and tokens[i].type == TokenType.MINUS:
            i += 1
            value, i = self._parse_primary(tokens, i)
            return -value, i
        
        return self._parse_primary(tokens, i)

    def _parse_primary(self, tokens: List[Token], i: int) -> Tuple[Any, int]:
        """解析基本表达式"""
        if i >= len(tokens):
            return 0, i

        token = tokens[i]

        # 数字
        if token.type == TokenType.NUMBER:
            return float(token.value), i + 1

        # 字符串
        if token.type == TokenType.STRING:
            return token.value, i + 1

        # 标识符
        if token.type == TokenType.IDENTIFIER:
            var_name = token.value
            i += 1

            # 数组访问
            if i < len(tokens) and tokens[i].type == TokenType.LBRACKET:
                i += 1  # 跳过 [
                index, i = self._parse_full_expression(tokens, i)
                if i < len(tokens) and tokens[i].type == TokenType.RBRACKET:
                    i += 1
                
                if var_name in self.variables:
                    arr = self.variables[var_name]
                    if isinstance(arr, list) and 0 <= int(index) < len(arr):
                        return arr[int(index)], i
                return 0, i
            else:
                # 变量值
                if var_name in self.variables:
                    return self.variables[var_name], i
                return 0, i

        # 括号表达式
        if token.type == TokenType.LPAREN:
            i += 1
            value, i = self._parse_full_expression(tokens, i)
            if i < len(tokens) and tokens[i].type == TokenType.RPAREN:
                i += 1
            return value, i

        return 0, i + 1

    def _execute_define(self, tokens: List[Token], i: int) -> int:
        """执行变量定义 - 完整版"""
        i += 1  # 跳过 DEFINE 或 DEF

        # 跳过 VARIABLE 关键字（如果有）
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
                # 数组
                if tokens[i].type == TokenType.LBRACKET:
                    arr, i = self._parse_array(tokens, i)
                    self.variables[var_name] = arr
                # 表达式
                elif self._is_expression_start(tokens, i) or tokens[i].type in (TokenType.NUMBER, TokenType.STRING, TokenType.IDENTIFIER):
                    value, i = self._parse_full_expression(tokens, i)
                    self.variables[var_name] = value
                else:
                    i += 1

        return i

    def _parse_array(self, tokens: List[Token], i: int) -> Tuple[List, int]:
        """解析数组"""
        arr = []
        i += 1  # 跳过 [

        while i < len(tokens) and tokens[i].type != TokenType.RBRACKET:
            if tokens[i].type == TokenType.NUMBER:
                arr.append(float(tokens[i].value))
                i += 1
            elif tokens[i].type == TokenType.STRING:
                arr.append(tokens[i].value)
                i += 1
            elif tokens[i].type == TokenType.COMMA:
                i += 1
            else:
                i += 1

        if i < len(tokens) and tokens[i].type == TokenType.RBRACKET:
            i += 1

        return arr, i

    def _execute_set(self, tokens: List[Token], i: int) -> int:
        """执行变量赋值"""
        i += 1  # 跳过 SET

        if i < len(tokens) and tokens[i].type == TokenType.IDENTIFIER:
            var_name = tokens[i].value
            i += 1

            # 数组元素赋值
            if i < len(tokens) and tokens[i].type == TokenType.LBRACKET:
                i += 1
                index, i = self._parse_full_expression(tokens, i)
                if i < len(tokens) and tokens[i].type == TokenType.RBRACKET:
                    i += 1
                if i < len(tokens) and tokens[i].type == TokenType.IS:
                    i += 1
                value, i = self._parse_full_expression(tokens, i)
                
                if var_name in self.variables:
                    arr = self.variables[var_name]
                    if isinstance(arr, list) and 0 <= int(index) < len(arr):
                        arr[int(index)] = value
            else:
                # 普通变量赋值
                if i < len(tokens) and tokens[i].type == TokenType.IS:
                    i += 1
                value, i = self._parse_full_expression(tokens, i)
                self.variables[var_name] = value

        return i

    def _execute_if(self, tokens: List[Token], i: int) -> int:
        """执行条件语句"""
        i += 1  # 跳过 IF

        # 计算条件
        condition_result, i = self._evaluate_condition(tokens, i)

        # 跳过 THEN
        if i < len(tokens) and tokens[i].type == TokenType.THEN:
            i += 1

        if condition_result:
            # 执行 IF 块
            while i < len(tokens):
                if tokens[i].type in (TokenType.ELSE, TokenType.END):
                    break
                i = self._execute_statement(tokens, i)
            
            # 跳过 ELSE 块
            if i < len(tokens) and tokens[i].type == TokenType.ELSE:
                i += 1
                while i < len(tokens):
                    if tokens[i].type == TokenType.END:
                        break
                    i += 1
        else:
            # 跳过 IF 块
            while i < len(tokens):
                if tokens[i].type == TokenType.ELSE:
                    i += 1
                    # 执行 ELSE 块
                    while i < len(tokens):
                        if tokens[i].type == TokenType.END:
                            break
                        i = self._execute_statement(tokens, i)
                    break
                elif tokens[i].type == TokenType.END:
                    break
                i += 1

        if i < len(tokens) and tokens[i].type == TokenType.END:
            i += 1

        return i

    def _execute_statement(self, tokens: List[Token], i: int) -> int:
        """执行单个语句"""
        if i >= len(tokens):
            return i

        token = tokens[i]
        
        if token.type == TokenType.OUTPUT:
            return self._execute_output(tokens, i)
        elif token.type == TokenType.DEFINE:
            return self._execute_define(tokens, i)
        elif token.type == TokenType.SET:
            return self._execute_set(tokens, i)
        elif token.type == TokenType.IF:
            return self._execute_if(tokens, i)
        elif token.type == TokenType.LOOP:
            return self._execute_loop(tokens, i)
        elif token.type == TokenType.CALL:
            return self._execute_call(tokens, i)
        elif token.type == TokenType.RETURN:
            return self._execute_return(tokens, i)
        else:
            return i + 1

    def _evaluate_condition(self, tokens: List[Token], i: int) -> Tuple[bool, int]:
        """计算条件表达式"""
        left, i = self._parse_full_expression(tokens, i)

        if i < len(tokens):
            op_type = tokens[i].type
            i += 1
            right, i = self._parse_full_expression(tokens, i)

            if op_type == TokenType.GREATER:
                return left > right, i
            elif op_type == TokenType.LESS:
                return left < right, i
            elif op_type == TokenType.IS:
                return left == right, i
            elif op_type == TokenType.GREATER_EQUAL:
                return left >= right, i
            elif op_type == TokenType.LESS_EQUAL:
                return left <= right, i
            elif op_type == TokenType.NOT_EQUAL:
                return left != right, i

        return bool(left), i

    def _execute_loop(self, tokens: List[Token], i: int) -> int:
        """执行循环"""
        i += 1  # 跳过 LOOP

        if i < len(tokens) and tokens[i].type == TokenType.NUMBER:
            count = int(tokens[i].value)
            i += 1

            # 跳过 "次执行"
            while i < len(tokens) and tokens[i].type not in (TokenType.END, TokenType.LBRACE):
                i += 1

            loop_start = i

            for iteration in range(count):
                self.variables['i'] = iteration
                self.variables['索引'] = iteration
                i = loop_start
                
                while i < len(tokens):
                    if tokens[i].type == TokenType.END:
                        break
                    i = self._execute_statement(tokens, i)

            if i < len(tokens) and tokens[i].type == TokenType.END:
                i += 1

        return i

    def _execute_function(self, tokens: List[Token], i: int) -> int:
        """执行函数定义"""
        i += 1  # 跳过 FUNCTION

        if i < len(tokens) and tokens[i].type == TokenType.IDENTIFIER:
            func_name = tokens[i].value
            i += 1

            if i < len(tokens) and tokens[i].type == TokenType.PARAMETER:
                i += 1

            params = []
            while i < len(tokens) and tokens[i].type == TokenType.IDENTIFIER:
                params.append(tokens[i].value)
                i += 1

            body_start = i
            while i < len(tokens):
                if tokens[i].type == TokenType.END:
                    break
                i += 1

            self.functions[func_name] = {
                'params': params,
                'body_start': body_start,
                'body_end': i
            }

            if i < len(tokens) and tokens[i].type == TokenType.END:
                i += 1

        return i

    def _execute_call(self, tokens: List[Token], i: int) -> int:
        """执行函数调用"""
        i += 1  # 跳过 CALL

        if i < len(tokens) and tokens[i].type == TokenType.IDENTIFIER:
            func_name = tokens[i].value
            i += 1

            if i < len(tokens) and tokens[i].type == TokenType.PARAMETER:
                i += 1

            args = []
            while i < len(tokens) and tokens[i].type not in (TokenType.END, TokenType.NEWLINE):
                if tokens[i].type == TokenType.NUMBER:
                    args.append(float(tokens[i].value))
                    i += 1
                elif tokens[i].type == TokenType.STRING:
                    args.append(tokens[i].value)
                    i += 1
                elif tokens[i].type == TokenType.IDENTIFIER:
                    var_name = tokens[i].value
                    if var_name in self.variables:
                        args.append(self.variables[var_name])
                    i += 1
                else:
                    i += 1

            if func_name in self.functions:
                func_def = self.functions[func_name]
                params = func_def['params']
                saved_vars = self.variables.copy()

                for param, arg in zip(params, args):
                    self.variables[param] = arg

                self.in_function = True
                self._execute_tokens(tokens, func_def['body_start'], func_def['body_end'])
                self.in_function = False

                self.variables = saved_vars

        return i

    def _execute_return(self, tokens: List[Token], i: int) -> int:
        """执行返回语句"""
        i += 1

        if i < len(tokens):
            value, i = self._parse_full_expression(tokens, i)
            self.return_value = value

        return i

    def _execute_add(self, tokens: List[Token], i: int) -> int:
        """执行数组添加"""
        i += 1

        if i < len(tokens) and tokens[i].type == TokenType.IDENTIFIER:
            arr_name = tokens[i].value
            i += 1

            if i < len(tokens):
                value, i = self._parse_full_expression(tokens, i)
                if arr_name in self.variables and isinstance(self.variables[arr_name], list):
                    self.variables[arr_name].append(value)

        return i

    def _execute_remove(self, tokens: List[Token], i: int) -> int:
        """执行数组删除"""
        i += 1

        if i < len(tokens) and tokens[i].type == TokenType.IDENTIFIER:
            arr_name = tokens[i].value
            i += 1

            if i < len(tokens) and tokens[i].type == TokenType.NUMBER:
                index = int(tokens[i].value)
                i += 1
                if arr_name in self.variables and isinstance(self.variables[arr_name], list):
                    arr = self.variables[arr_name]
                    if 0 <= index < len(arr):
                        arr.pop(index)

        return i

    def _execute_length(self, tokens: List[Token], i: int) -> int:
        """执行长度查询"""
        i += 1

        if i < len(tokens) and tokens[i].type == TokenType.IDENTIFIER:
            arr_name = tokens[i].value
            i += 1

            if arr_name in self.variables:
                value = self.variables[arr_name]
                if isinstance(value, (list, str)):
                    self.output.append(str(len(value)))
                else:
                    self.output.append("1")
            else:
                self.output.append("0")

        return i


def create_complete_interpreter() -> CompleteInterpreter:
    """创建完整解释器"""
    return CompleteInterpreter()


__all__ = ['CompleteInterpreter', 'create_complete_interpreter']
