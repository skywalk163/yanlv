"""
言律语言解释器增强版

修复核心问题，提升性能和稳定性
"""

import math
import random
import os
from typing import List, Dict, Any, Optional, Tuple
from .lexer.lexer_token import Token, TokenType


class EnhancedInterpreter:
    """增强版言律语言解释器"""

    def __init__(self):
        """初始化解释器"""
        self.variables: Dict[str, Any] = {}
        self.functions: Dict[str, Dict] = {}
        self.output: List[str] = []
        # 异常处理
        self.exception_stack: List[Dict[str, Any]] = []
        self.current_exception: Optional[Dict[str, Any]] = None
        self.in_try_block: bool = False
        # 性能优化
        self.cache: Dict[str, Any] = {}

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
        """执行指定范围的词元"""
        i = start
        while i < end:
            token = tokens[i]

            # 跳过换行符
            if token.type == TokenType.NEWLINE:
                i += 1
                continue

            # 根据token类型分发处理
            handler = self._get_handler(token.type)
            if handler:
                i = handler(tokens, i)
            else:
                i += 1

        return i

    def _get_handler(self, token_type: TokenType):
        """获取处理器"""
        handlers = {
            TokenType.OUTPUT: self._execute_output,
            TokenType.DEFINE: self._execute_define,
            TokenType.SET: self._execute_set,
            TokenType.ADD: self._execute_add,
            TokenType.REMOVE: self._execute_remove,
            TokenType.LENGTH: self._execute_length,
            TokenType.IF: self._execute_if,
            TokenType.LOOP: self._execute_loop,
            TokenType.FUNCTION: self._execute_function,
            TokenType.CALL: self._execute_call,
            TokenType.RETURN: self._execute_return,
        }
        return handlers.get(token_type)

    def _execute_output(self, tokens: List[Token], i: int) -> int:
        """执行输出语句 - 修复版"""
        i += 1  # 跳过 OUTPUT

        if i >= len(tokens):
            return i

        # 处理字符串
        if tokens[i].type == TokenType.STRING:
            value = tokens[i].value
            self.output.append(str(value))  # 直接输出，不添加前缀
            i += 1

        # 处理数字
        elif tokens[i].type == TokenType.NUMBER:
            value = tokens[i].value
            self.output.append(str(value))  # 直接输出数字
            i += 1

        # 处理标识符（变量）
        elif tokens[i].type == TokenType.IDENTIFIER:
            var_name = tokens[i].value
            i += 1

            # 检查是否是数组访问
            if i < len(tokens) and tokens[i].type == TokenType.LBRACKET:
                i += 1  # 跳过 [
                if i < len(tokens) and tokens[i].type == TokenType.NUMBER:
                    index = int(tokens[i].value)
                    i += 1
                    if i < len(tokens) and tokens[i].type == TokenType.RBRACKET:
                        i += 1
                        # 输出数组元素
                        if var_name in self.variables:
                            arr = self.variables[var_name]
                            if isinstance(arr, list) and 0 <= index < len(arr):
                                self.output.append(str(arr[index]))
                            else:
                                self.output.append(f"错误：索引 {index} 超出范围")
                        else:
                            self.output.append(f"错误：数组 '{var_name}' 未定义")
            else:
                # 检查后面是否有运算符（表达式）
                if i < len(tokens) and tokens[i].type in (TokenType.PLUS, TokenType.MINUS, 
                                                          TokenType.MULTIPLY, TokenType.DIVIDE, 
                                                          TokenType.MODULO):
                    # 计算表达式
                    i -= 1  # 回退到变量名
                    value, i = self._evaluate_expression(tokens, i)
                    self.output.append(str(value))
                else:
                    # 输出变量值
                    if var_name in self.variables:
                        self.output.append(str(self.variables[var_name]))
                    else:
                        self.output.append(f"错误：变量 '{var_name}' 未定义")

        # 处理表达式
        else:
            value, i = self._evaluate_expression(tokens, i)
            self.output.append(str(value))

        return i

    def _execute_define(self, tokens: List[Token], i: int) -> int:
        """执行变量定义 - 增强版"""
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
                # 处理负数
                if tokens[i].type == TokenType.MINUS:
                    i += 1
                    if i < len(tokens) and tokens[i].type == TokenType.NUMBER:
                        self.variables[var_name] = -float(tokens[i].value)
                        i += 1

                # 处理数字
                elif tokens[i].type == TokenType.NUMBER:
                    self.variables[var_name] = float(tokens[i].value)
                    i += 1

                # 处理字符串
                elif tokens[i].type == TokenType.STRING:
                    self.variables[var_name] = tokens[i].value
                    i += 1

                # 处理布尔值
                elif tokens[i].type == TokenType.BOOLEAN:
                    self.variables[var_name] = tokens[i].value == "真"
                    i += 1

                # 处理数组
                elif tokens[i].type == TokenType.LBRACKET:
                    arr, i = self._parse_array(tokens, i)
                    self.variables[var_name] = arr

                # 处理表达式
                elif tokens[i].type == TokenType.IDENTIFIER:
                    value, i = self._evaluate_expression(tokens, i)
                    self.variables[var_name] = value

        return i

    def _execute_set(self, tokens: List[Token], i: int) -> int:
        """执行变量赋值 - 增强版"""
        i += 1  # 跳过 SET

        # 获取变量名
        if i < len(tokens) and tokens[i].type == TokenType.IDENTIFIER:
            var_name = tokens[i].value
            i += 1

            # 检查是否是数组元素赋值
            if i < len(tokens) and tokens[i].type == TokenType.LBRACKET:
                i += 1  # 跳过 [
                if i < len(tokens) and tokens[i].type == TokenType.NUMBER:
                    index = int(tokens[i].value)
                    i += 1
                    if i < len(tokens) and tokens[i].type == TokenType.RBRACKET:
                        i += 1
                        # 跳过 IS
                        if i < len(tokens) and tokens[i].type == TokenType.IS:
                            i += 1
                        # 获取值
                        if i < len(tokens):
                            if tokens[i].type == TokenType.NUMBER:
                                value = float(tokens[i].value)
                                i += 1
                            elif tokens[i].type == TokenType.IDENTIFIER:
                                value, i = self._evaluate_expression(tokens, i)
                            else:
                                value = tokens[i].value
                                i += 1
                            # 设置数组元素
                            if var_name in self.variables:
                                arr = self.variables[var_name]
                                if isinstance(arr, list) and 0 <= index < len(arr):
                                    arr[index] = value
            else:
                # 跳过 IS
                if i < len(tokens) and tokens[i].type == TokenType.IS:
                    i += 1

                # 获取值
                if i < len(tokens):
                    if tokens[i].type == TokenType.NUMBER:
                        self.variables[var_name] = float(tokens[i].value)
                        i += 1
                    elif tokens[i].type == TokenType.STRING:
                        self.variables[var_name] = tokens[i].value
                        i += 1
                    elif tokens[i].type == TokenType.IDENTIFIER:
                        value, i = self._evaluate_expression(tokens, i)
                        self.variables[var_name] = value
                    else:
                        i += 1

        return i

    def _execute_if(self, tokens: List[Token], i: int) -> int:
        """执行条件语句 - 增强版"""
        i += 1  # 跳过 IF

        # 计算条件
        condition_result, i = self._evaluate_condition(tokens, i)

        # 跳过 THEN
        if i < len(tokens) and tokens[i].type == TokenType.THEN:
            i += 1

        # 执行条件为真的代码块
        if condition_result:
            # 执行到 ELSE 或 END
            while i < len(tokens):
                if tokens[i].type in (TokenType.ELSE, TokenType.END):
                    break
                # 执行语句
                handler = self._get_handler(tokens[i].type)
                if handler:
                    i = handler(tokens, i)
                else:
                    i += 1

            # 跳过 ELSE 块
            if i < len(tokens) and tokens[i].type == TokenType.ELSE:
                i += 1
                # 跳过 ELSE 块的内容
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
                        handler = self._get_handler(tokens[i].type)
                        if handler:
                            i = handler(tokens, i)
                        else:
                            i += 1
                    break
                elif tokens[i].type == TokenType.END:
                    break
                i += 1

        # 跳过 END
        if i < len(tokens) and tokens[i].type == TokenType.END:
            i += 1

        return i

    def _execute_loop(self, tokens: List[Token], i: int) -> int:
        """执行循环语句 - 增强版"""
        i += 1  # 跳过 LOOP

        # 获取循环次数
        if i < len(tokens) and tokens[i].type == TokenType.NUMBER:
            count = int(tokens[i].value)
            i += 1

            # 跳过 "次执行"
            while i < len(tokens) and tokens[i].type not in (TokenType.END, TokenType.LBRACE):
                i += 1

            # 记录循环体开始位置
            loop_body_start = i

            # 执行循环
            for iteration in range(count):
                # 设置循环变量
                self.variables['i'] = iteration
                self.variables['索引'] = iteration

                # 执行循环体
                i = loop_body_start
                while i < len(tokens):
                    if tokens[i].type == TokenType.END:
                        break
                    handler = self._get_handler(tokens[i].type)
                    if handler:
                        i = handler(tokens, i)
                    else:
                        i += 1

            # 跳过 END
            if i < len(tokens) and tokens[i].type == TokenType.END:
                i += 1

        return i

    def _execute_function(self, tokens: List[Token], i: int) -> int:
        """执行函数定义"""
        i += 1  # 跳过 FUNCTION

        # 获取函数名
        if i < len(tokens) and tokens[i].type == TokenType.IDENTIFIER:
            func_name = tokens[i].value
            i += 1

            # 跳过 PARAMETER
            if i < len(tokens) and tokens[i].type == TokenType.PARAMETER:
                i += 1

            # 获取参数列表
            params = []
            while i < len(tokens) and tokens[i].type == TokenType.IDENTIFIER:
                params.append(tokens[i].value)
                i += 1

            # 记录函数体开始位置
            body_start = i

            # 找到函数结束
            while i < len(tokens):
                if tokens[i].type == TokenType.END:
                    break
                i += 1

            # 保存函数定义
            self.functions[func_name] = {
                'params': params,
                'body_start': body_start,
                'body_end': i
            }

            # 跳过 END
            if i < len(tokens) and tokens[i].type == TokenType.END:
                i += 1

        return i

    def _execute_call(self, tokens: List[Token], i: int) -> int:
        """执行函数调用"""
        i += 1  # 跳过 CALL

        # 获取函数名
        if i < len(tokens) and tokens[i].type == TokenType.IDENTIFIER:
            func_name = tokens[i].value
            i += 1

            # 跳过 PARAMETER
            if i < len(tokens) and tokens[i].type == TokenType.PARAMETER:
                i += 1

            # 获取参数值
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

            # 执行函数
            if func_name in self.functions:
                func_def = self.functions[func_name]
                params = func_def['params']

                # 保存当前变量
                saved_vars = self.variables.copy()

                # 设置参数
                for param, arg in zip(params, args):
                    self.variables[param] = arg

                # 执行函数体
                body_start = func_def['body_start']
                body_end = func_def['body_end']
                self._execute_tokens(tokens, body_start, body_end)

                # 恢复变量
                self.variables = saved_vars

        return i

    def _execute_return(self, tokens: List[Token], i: int) -> int:
        """执行返回语句"""
        i += 1  # 跳过 RETURN

        # 获取返回值
        if i < len(tokens):
            if tokens[i].type == TokenType.NUMBER:
                return float(tokens[i].value)
            elif tokens[i].type == TokenType.IDENTIFIER:
                var_name = tokens[i].value
                if var_name in self.variables:
                    return self.variables[var_name]

        return i

    def _execute_add(self, tokens: List[Token], i: int) -> int:
        """执行数组添加"""
        i += 1  # 跳过 ADD

        # 获取数组名
        if i < len(tokens) and tokens[i].type == TokenType.IDENTIFIER:
            arr_name = tokens[i].value
            i += 1

            # 获取值
            if i < len(tokens):
                if tokens[i].type == TokenType.NUMBER:
                    value = float(tokens[i].value)
                    i += 1
                elif tokens[i].type == TokenType.IDENTIFIER:
                    var_name = tokens[i].value
                    value = self.variables.get(var_name)
                    i += 1
                else:
                    value = tokens[i].value
                    i += 1

                # 添加到数组
                if arr_name in self.variables and isinstance(self.variables[arr_name], list):
                    self.variables[arr_name].append(value)

        return i

    def _execute_remove(self, tokens: List[Token], i: int) -> int:
        """执行数组删除"""
        i += 1  # 跳过 REMOVE

        # 获取数组名
        if i < len(tokens) and tokens[i].type == TokenType.IDENTIFIER:
            arr_name = tokens[i].value
            i += 1

            # 获取索引
            if i < len(tokens) and tokens[i].type == TokenType.NUMBER:
                index = int(tokens[i].value)
                i += 1

                # 删除数组元素
                if arr_name in self.variables and isinstance(self.variables[arr_name], list):
                    arr = self.variables[arr_name]
                    if 0 <= index < len(arr):
                        arr.pop(index)

        return i

    def _execute_length(self, tokens: List[Token], i: int) -> int:
        """执行长度查询"""
        i += 1  # 跳过 LENGTH

        # 获取数组名
        if i < len(tokens) and tokens[i].type == TokenType.IDENTIFIER:
            arr_name = tokens[i].value
            i += 1

            # 输出长度
            if arr_name in self.variables:
                value = self.variables[arr_name]
                if isinstance(value, list):
                    self.output.append(str(len(value)))
                elif isinstance(value, str):
                    self.output.append(str(len(value)))
                else:
                    self.output.append("1")
            else:
                self.output.append("0")

        return i

    def _evaluate_expression(self, tokens: List[Token], i: int) -> Tuple[Any, int]:
        """计算表达式 - 增强版"""
        return self._parse_expression(tokens, i)

    def _parse_expression(self, tokens: List[Token], i: int) -> Tuple[Any, int]:
        """解析表达式（处理加减）"""
        left, i = self._parse_term(tokens, i)

        while i < len(tokens) and tokens[i].type in (TokenType.PLUS, TokenType.MINUS):
            op = tokens[i].type
            i += 1
            right, i = self._parse_term(tokens, i)

            if op == TokenType.PLUS:
                left = left + right
            else:
                left = left - right

        return left, i

    def _parse_term(self, tokens: List[Token], i: int) -> Tuple[Any, int]:
        """解析项（处理乘除取模）"""
        left, i = self._parse_factor(tokens, i)

        while i < len(tokens) and tokens[i].type in (TokenType.MULTIPLY, TokenType.DIVIDE, TokenType.MODULO):
            op = tokens[i].type
            i += 1
            right, i = self._parse_factor(tokens, i)

            if op == TokenType.MULTIPLY:
                left = left * right
            elif op == TokenType.DIVIDE:
                left = left / right if right != 0 else 0
            else:
                left = left % right

        return left, i

    def _parse_factor(self, tokens: List[Token], i: int) -> Tuple[Any, int]:
        """解析因子（处理数字、变量、括号）"""
        if i >= len(tokens):
            return 0, i

        token = tokens[i]

        # 处理负号
        if token.type == TokenType.MINUS:
            i += 1
            value, i = self._parse_factor(tokens, i)
            return -value, i

        # 处理数字
        if token.type == TokenType.NUMBER:
            return float(token.value), i + 1

        # 处理变量
        if token.type == TokenType.IDENTIFIER:
            var_name = token.value
            i += 1

            # 检查是否是数组访问
            if i < len(tokens) and tokens[i].type == TokenType.LBRACKET:
                i += 1  # 跳过 [
                if i < len(tokens) and tokens[i].type == TokenType.NUMBER:
                    index = int(tokens[i].value)
                    i += 1
                    if i < len(tokens) and tokens[i].type == TokenType.RBRACKET:
                        i += 1
                        if var_name in self.variables:
                            arr = self.variables[var_name]
                            if isinstance(arr, list) and 0 <= index < len(arr):
                                return arr[index], i
                return 0, i
            else:
                if var_name in self.variables:
                    return self.variables[var_name], i
                return 0, i

        # 处理括号
        if token.type == TokenType.LPAREN:
            i += 1
            value, i = self._parse_expression(tokens, i)
            if i < len(tokens) and tokens[i].type == TokenType.RPAREN:
                i += 1
            return value, i

        return 0, i + 1

    def _evaluate_condition(self, tokens: List[Token], i: int) -> Tuple[bool, int]:
        """计算条件表达式"""
        left, i = self._parse_expression(tokens, i)

        if i < len(tokens):
            op_token = tokens[i]
            i += 1

            right, i = self._parse_expression(tokens, i)

            # 比较运算
            if op_token.type == TokenType.GREATER:
                return left > right, i
            elif op_token.type == TokenType.LESS:
                return left < right, i
            elif op_token.type == TokenType.IS:
                return left == right, i
            elif op_token.type == TokenType.GREATER_EQUAL:
                return left >= right, i
            elif op_token.type == TokenType.LESS_EQUAL:
                return left <= right, i
            elif op_token.type == TokenType.NOT_EQUAL:
                return left != right, i

        return False, i

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


# ============================================================================
# 辅助函数
# ============================================================================

def create_enhanced_interpreter() -> EnhancedInterpreter:
    """创建增强版解释器"""
    return EnhancedInterpreter()


# ============================================================================
# 导出
# ============================================================================

__all__ = [
    'EnhancedInterpreter',
    'create_enhanced_interpreter',
]
