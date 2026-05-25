"""
言律语言简单解释器
支持条件、循环、函数等程序块的执行
"""
import math
import random
import os
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

            # 处理变量赋值（设置）
            elif token.type == TokenType.SET:
                i = self._execute_set(tokens, i)

            # 处理数组添加
            elif token.type == TokenType.ADD:
                i = self._execute_add(tokens, i)

            # 处理数组删除
            elif token.type == TokenType.REMOVE:
                i = self._execute_remove(tokens, i)

            # 处理长度查询
            elif token.type == TokenType.LENGTH:
                i = self._execute_length(tokens, i)

            # 处理字符串查找
            elif token.type == TokenType.FIND:
                i = self._execute_find(tokens, i)

            # 处理字符串替换
            elif token.type == TokenType.REPLACE:
                i = self._execute_replace(tokens, i)

            # 处理字符串分割
            elif token.type == TokenType.SPLIT:
                i = self._execute_split(tokens, i)

            # 处理子串
            elif token.type == TokenType.SUBSTRING:
                i = self._execute_substring(tokens, i)

            # 处理数学内置函数
            elif token.type == TokenType.ABS:
                i = self._execute_abs(tokens, i)

            elif token.type == TokenType.SQRT:
                i = self._execute_sqrt(tokens, i)

            elif token.type == TokenType.POW:
                i = self._execute_pow(tokens, i)

            elif token.type == TokenType.INT:
                i = self._execute_int(tokens, i)

            elif token.type == TokenType.RANDOM:
                i = self._execute_random(tokens, i)

            # 处理数学扩展函数
            elif token.type == TokenType.SIN:
                i = self._execute_sin(tokens, i)

            elif token.type == TokenType.COS:
                i = self._execute_cos(tokens, i)

            elif token.type == TokenType.TAN:
                i = self._execute_tan(tokens, i)

            elif token.type == TokenType.LOG:
                i = self._execute_log(tokens, i)

            elif token.type == TokenType.LOG10:
                i = self._execute_log10(tokens, i)

            elif token.type == TokenType.EXP:
                i = self._execute_exp(tokens, i)

            elif token.type == TokenType.CEIL:
                i = self._execute_ceil(tokens, i)

            elif token.type == TokenType.FLOOR:
                i = self._execute_floor(tokens, i)

            elif token.type == TokenType.ROUND:
                i = self._execute_round(tokens, i)

            elif token.type == TokenType.FACTORIAL:
                i = self._execute_factorial(tokens, i)

            # 处理数组内置函数
            elif token.type == TokenType.SORT:
                i = self._execute_sort(tokens, i)

            elif token.type == TokenType.REVERSE:
                i = self._execute_reverse(tokens, i)

            elif token.type == TokenType.MAX:
                i = self._execute_max(tokens, i)

            elif token.type == TokenType.MIN:
                i = self._execute_min(tokens, i)

            elif token.type == TokenType.SUM:
                i = self._execute_sum(tokens, i)

            # 处理字符串操作增强
            elif token.type == TokenType.CONCAT:
                i = self._execute_concat(tokens, i)

            elif token.type == TokenType.SLICE:
                i = self._execute_slice(tokens, i)

            elif token.type == TokenType.FIND_ALL:
                i = self._execute_find_all(tokens, i)

            elif token.type == TokenType.REPLACE_ONCE:
                i = self._execute_replace_once(tokens, i)

            elif token.type == TokenType.UPPER:
                i = self._execute_upper(tokens, i)

            elif token.type == TokenType.LOWER:
                i = self._execute_lower(tokens, i)

            elif token.type == TokenType.TRIM:
                i = self._execute_trim(tokens, i)

            elif token.type == TokenType.TRIM_ALL:
                i = self._execute_trim_all(tokens, i)

            elif token.type == TokenType.FOR_EACH_CHAR:
                i = self._execute_for_each_char(tokens, i)

            # 处理文件操作
            elif token.type == TokenType.READ_FILE:
                i = self._execute_read_file(tokens, i)

            elif token.type == TokenType.READ_LINES:
                i = self._execute_read_lines(tokens, i)

            elif token.type == TokenType.WRITE_FILE:
                i = self._execute_write_file(tokens, i)

            elif token.type == TokenType.APPEND_FILE:
                i = self._execute_append_file(tokens, i)

            elif token.type == TokenType.FILE_EXISTS:
                i = self._execute_file_exists(tokens, i)

            elif token.type == TokenType.FILE_SIZE:
                i = self._execute_file_size(tokens, i)

            elif token.type == TokenType.FILE_NAME:
                i = self._execute_file_name(tokens, i)

            elif token.type == TokenType.DIR_NAME:
                i = self._execute_dir_name(tokens, i)

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
            elif token.type == TokenType.CALL:
                i = self._execute_call(tokens, i)
            elif token.type == TokenType.IDENTIFIER:
                # 检查是否是函数调用
                if i + 1 < len(tokens) and tokens[i + 1].type == TokenType.PARAMETER:
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
            elif tokens[i].type == TokenType.LPAREN:
                # 输出括号表达式
                value, i = self._parse_expression(tokens, i)
                self.output.append(f"=> {value}")
            elif tokens[i].type == TokenType.IDENTIFIER:
                # 输出变量或表达式
                var_name = tokens[i].value
                i += 1
                
                # 检查是否是数组索引访问 arr[i]
                if i < len(tokens) and tokens[i].type == TokenType.LBRACKET:
                    i += 1  # 跳过 [
                    # 获取索引
                    if i < len(tokens):
                        if tokens[i].type == TokenType.NUMBER:
                            index = int(float(tokens[i].value))
                            i += 1
                        elif tokens[i].type == TokenType.IDENTIFIER:
                            index_var = tokens[i].value
                            if index_var in self.variables:
                                index = int(self.variables[index_var])
                            else:
                                index = 0
                            i += 1
                        else:
                            index = 0
                        
                        # 跳过 ]
                        if i < len(tokens) and tokens[i].type == TokenType.RBRACKET:
                            i += 1
                        
                        # 获取数组元素
                        if var_name in self.variables:
                            arr = self.variables[var_name]
                            if isinstance(arr, list) and 0 <= index < len(arr):
                                self.output.append(f"=> {arr[index]}")
                            else:
                                self.output.append(f"=> 索引 {index} 超出范围")
                        else:
                            self.output.append(f"=> 数组 '{var_name}' 未定义")
                else:
                    # 检查后面是否有运算符（表达式）
                    if i < len(tokens) and tokens[i].type in (TokenType.PLUS, TokenType.MINUS, TokenType.MULTIPLY, TokenType.DIVIDE, TokenType.MODULO):
                        # 计算表达式
                        i -= 1  # 回退到变量名
                        value, i = self._evaluate_expression(tokens, i)
                        self.output.append(f"=> {value}")
                    else:
                        # 输出变量值
                        if var_name in self.variables:
                            self.output.append(f"=> {self.variables[var_name]}")
                        else:
                            self.output.append(f"=> 变量 '{var_name}' 未定义")
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
                # 处理负数
                if tokens[i].type == TokenType.MINUS:
                    i += 1  # 跳过负号
                    if i < len(tokens) and tokens[i].type == TokenType.NUMBER:
                        self.variables[var_name] = -float(tokens[i].value)
                        i += 1
                elif tokens[i].type == TokenType.NUMBER:
                    # 检查后面是否有运算符（表达式）
                    if i + 1 < len(tokens) and tokens[i + 1].type in (TokenType.PLUS, TokenType.MINUS, TokenType.MULTIPLY, TokenType.DIVIDE, TokenType.MODULO):
                        value, i = self._evaluate_expression(tokens, i)
                        self.variables[var_name] = value
                    else:
                        self.variables[var_name] = float(tokens[i].value)
                        i += 1
                elif tokens[i].type == TokenType.STRING:
                    # 检查后面是否有加号（字符串连接）
                    if i + 1 < len(tokens) and tokens[i + 1].type == TokenType.PLUS:
                        value, i = self._evaluate_expression(tokens, i)
                        self.variables[var_name] = value
                    else:
                        self.variables[var_name] = tokens[i].value.strip('"\'')
                        i += 1
                elif tokens[i].type == TokenType.IDENTIFIER:
                    # 可能是变量引用或表达式
                    if i + 1 < len(tokens) and tokens[i + 1].type in (TokenType.PLUS, TokenType.MINUS, TokenType.MULTIPLY, TokenType.DIVIDE, TokenType.MODULO):
                        value, i = self._evaluate_expression(tokens, i)
                        self.variables[var_name] = value
                    else:
                        # 变量引用
                        ref_name = tokens[i].value
                        if ref_name in self.variables:
                            self.variables[var_name] = self.variables[ref_name]
                        else:
                            self.variables[var_name] = ref_name
                        i += 1
                elif tokens[i].type == TokenType.LBRACKET:
                    # 处理数组 [1, 2, 3]
                    i += 1  # 跳过 [
                    arr = []
                    while i < len(tokens) and tokens[i].type != TokenType.RBRACKET:
                        # 处理负数
                        if tokens[i].type == TokenType.MINUS:
                            i += 1  # 跳过负号
                            if i < len(tokens) and tokens[i].type == TokenType.NUMBER:
                                arr.append(-float(tokens[i].value))
                                i += 1
                        elif tokens[i].type == TokenType.NUMBER:
                            arr.append(float(tokens[i].value))
                            i += 1
                        elif tokens[i].type == TokenType.STRING:
                            arr.append(tokens[i].value.strip('"\''))
                            i += 1
                        elif tokens[i].type == TokenType.COMMA:
                            i += 1  # 跳过逗号
                        elif tokens[i].type == TokenType.IDENTIFIER and tokens[i].value == ',':
                            i += 1  # 跳过逗号（处理为IDENTIFIER的情况）
                        else:
                            i += 1
                    if i < len(tokens) and tokens[i].type == TokenType.RBRACKET:
                        i += 1  # 跳过 ]
                    self.variables[var_name] = arr
                else:
                    self.variables[var_name] = tokens[i].value
                    i += 1

        return i

    def _execute_set(self, tokens: List[Token], i: int) -> int:
        """执行变量赋值"""
        i += 1  # 跳过 SET

        # 获取变量名
        if i < len(tokens) and tokens[i].type == TokenType.IDENTIFIER:
            var_name = tokens[i].value
            i += 1
            
            # 检查是否是数组元素赋值 arr[i]
            if i < len(tokens) and tokens[i].type == TokenType.LBRACKET:
                i += 1  # 跳过 [
                # 获取索引
                if i < len(tokens):
                    if tokens[i].type == TokenType.NUMBER:
                        index = int(float(tokens[i].value))
                        i += 1
                    elif tokens[i].type == TokenType.IDENTIFIER:
                        index_var = tokens[i].value
                        if index_var in self.variables:
                            index = int(self.variables[index_var])
                        else:
                            index = 0
                        i += 1
                    else:
                        index = 0
                    
                    # 跳过 ]
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
                        elif tokens[i].type == TokenType.STRING:
                            value = tokens[i].value.strip('"\'')
                            i += 1
                        elif tokens[i].type == TokenType.IDENTIFIER:
                            # 可能是另一个变量
                            if tokens[i].value in self.variables:
                                value = self.variables[tokens[i].value]
                            else:
                                value = tokens[i].value
                            i += 1
                        else:
                            value = 0
                        
                        # 修改数组元素
                        if var_name in self.variables:
                            arr = self.variables[var_name]
                            if isinstance(arr, list) and 0 <= index < len(arr):
                                arr[index] = value
            else:
                # 普通变量赋值
                # 跳过 IS
                if i < len(tokens) and tokens[i].type == TokenType.IS:
                    i += 1

                # 获取值
                if i < len(tokens):
                    if tokens[i].type == TokenType.NUMBER:
                        self.variables[var_name] = float(tokens[i].value)
                    elif tokens[i].type == TokenType.STRING:
                        self.variables[var_name] = tokens[i].value.strip('"\'')
                    elif tokens[i].type == TokenType.IDENTIFIER:
                        # 可能是另一个变量或表达式
                        if tokens[i].value in self.variables:
                            self.variables[var_name] = self.variables[tokens[i].value]
                        else:
                            self.variables[var_name] = tokens[i].value
                    i += 1

        return i

    def _execute_add(self, tokens: List[Token], i: int) -> int:
        """执行数组添加操作"""
        i += 1  # 跳过 ADD

        # 获取数组名
        if i < len(tokens) and tokens[i].type == TokenType.IDENTIFIER:
            arr_name = tokens[i].value
            i += 1

            # 获取要添加的值
            if i < len(tokens):
                if tokens[i].type == TokenType.NUMBER:
                    value = float(tokens[i].value)
                    i += 1
                elif tokens[i].type == TokenType.STRING:
                    value = tokens[i].value.strip('"\'')
                    i += 1
                elif tokens[i].type == TokenType.IDENTIFIER:
                    if tokens[i].value in self.variables:
                        value = self.variables[tokens[i].value]
                    else:
                        value = tokens[i].value
                    i += 1
                else:
                    value = 0

                # 添加到数组
                if arr_name in self.variables:
                    arr = self.variables[arr_name]
                    if isinstance(arr, list):
                        arr.append(value)
                else:
                    # 如果数组不存在，创建新数组
                    self.variables[arr_name] = [value]

        return i

    def _execute_remove(self, tokens: List[Token], i: int) -> int:
        """执行数组删除操作"""
        i += 1  # 跳过 REMOVE

        # 获取数组名
        if i < len(tokens) and tokens[i].type == TokenType.IDENTIFIER:
            arr_name = tokens[i].value
            i += 1

            # 获取索引
            if i < len(tokens):
                if tokens[i].type == TokenType.NUMBER:
                    index = int(float(tokens[i].value))
                    i += 1
                elif tokens[i].type == TokenType.IDENTIFIER:
                    index_var = tokens[i].value
                    if index_var in self.variables:
                        index = int(self.variables[index_var])
                    else:
                        index = 0
                    i += 1
                else:
                    index = 0

                # 从数组删除
                if arr_name in self.variables:
                    arr = self.variables[arr_name]
                    if isinstance(arr, list) and 0 <= index < len(arr):
                        arr.pop(index)

        return i

    def _execute_length(self, tokens: List[Token], i: int) -> int:
        """执行长度查询"""
        i += 1  # 跳过 LENGTH

        # 获取变量名
        if i < len(tokens) and tokens[i].type == TokenType.IDENTIFIER:
            var_name = tokens[i].value
            i += 1

            # 计算长度
            if var_name in self.variables:
                value = self.variables[var_name]
                if isinstance(value, list):
                    self.output.append(f"=> {len(value)}")
                elif isinstance(value, str):
                    self.output.append(f"=> {len(value)}")
                else:
                    self.output.append(f"=> 1")
            else:
                self.output.append(f"=> 0")

        return i

    def _execute_find(self, tokens: List[Token], i: int) -> int:
        """执行字符串查找"""
        i += 1  # 跳过 FIND

        # 获取字符串变量名
        if i < len(tokens) and tokens[i].type == TokenType.IDENTIFIER:
            str_name = tokens[i].value
            i += 1

            # 获取要查找的子串
            if i < len(tokens):
                if tokens[i].type == TokenType.STRING:
                    substr = tokens[i].value.strip('"\'')
                    i += 1
                elif tokens[i].type == TokenType.IDENTIFIER:
                    if tokens[i].value in self.variables:
                        substr = str(self.variables[tokens[i].value])
                    else:
                        substr = tokens[i].value
                    i += 1
                else:
                    substr = ""

                # 执行查找
                if str_name in self.variables:
                    string = str(self.variables[str_name])
                    pos = string.find(substr)
                    self.output.append(f"=> {pos}")
                else:
                    self.output.append(f"=> -1")

        return i

    def _execute_replace(self, tokens: List[Token], i: int) -> int:
        """执行字符串替换"""
        i += 1  # 跳过 REPLACE

        # 获取字符串变量名
        if i < len(tokens) and tokens[i].type == TokenType.IDENTIFIER:
            str_name = tokens[i].value
            i += 1

            # 获取要替换的子串
            if i < len(tokens):
                if tokens[i].type == TokenType.STRING:
                    old_str = tokens[i].value.strip('"\'')
                    i += 1
                elif tokens[i].type == TokenType.IDENTIFIER:
                    if tokens[i].value in self.variables:
                        old_str = str(self.variables[tokens[i].value])
                    else:
                        old_str = tokens[i].value
                    i += 1
                else:
                    old_str = ""

                # 获取新字符串
                if i < len(tokens):
                    if tokens[i].type == TokenType.STRING:
                        new_str = tokens[i].value.strip('"\'')
                        i += 1
                    elif tokens[i].type == TokenType.IDENTIFIER:
                        if tokens[i].value in self.variables:
                            new_str = str(self.variables[tokens[i].value])
                        else:
                            new_str = tokens[i].value
                        i += 1
                    else:
                        new_str = ""

                    # 执行替换
                    if str_name in self.variables:
                        string = str(self.variables[str_name])
                        result = string.replace(old_str, new_str)
                        self.variables[str_name] = result
                        self.output.append(f"=> {result}")

        return i

    def _execute_split(self, tokens: List[Token], i: int) -> int:
        """执行字符串分割"""
        i += 1  # 跳过 SPLIT

        # 获取字符串变量名
        if i < len(tokens) and tokens[i].type == TokenType.IDENTIFIER:
            str_name = tokens[i].value
            i += 1

            # 获取分隔符
            if i < len(tokens):
                if tokens[i].type == TokenType.STRING:
                    sep = tokens[i].value.strip('"\'')
                    i += 1
                elif tokens[i].type == TokenType.IDENTIFIER:
                    if tokens[i].value in self.variables:
                        sep = str(self.variables[tokens[i].value])
                    else:
                        sep = tokens[i].value
                    i += 1
                else:
                    sep = " "

                # 执行分割
                if str_name in self.variables:
                    string = str(self.variables[str_name])
                    parts = string.split(sep)
                    self.variables[str_name] = parts
                    self.output.append(f"=> {parts}")

        return i

    def _execute_substring(self, tokens: List[Token], i: int) -> int:
        """执行子串提取"""
        i += 1  # 跳过 SUBSTRING

        # 获取字符串变量名
        if i < len(tokens) and tokens[i].type == TokenType.IDENTIFIER:
            str_name = tokens[i].value
            i += 1

            # 获取起始位置
            if i < len(tokens):
                if tokens[i].type == TokenType.NUMBER:
                    start = int(float(tokens[i].value))
                    i += 1
                elif tokens[i].type == TokenType.IDENTIFIER:
                    if tokens[i].value in self.variables:
                        start = int(self.variables[tokens[i].value])
                    else:
                        start = 0
                    i += 1
                else:
                    start = 0

                # 获取结束位置（可选）
                end = None
                if i < len(tokens) and tokens[i].type == TokenType.NUMBER:
                    end = int(float(tokens[i].value))
                    i += 1
                elif i < len(tokens) and tokens[i].type == TokenType.IDENTIFIER:
                    if tokens[i].value in self.variables:
                        end = int(self.variables[tokens[i].value])
                        i += 1

                # 执行子串提取
                if str_name in self.variables:
                    string = str(self.variables[str_name])
                    if end is not None:
                        result = string[start:end]
                    else:
                        result = string[start:]
                    self.output.append(f"=> {result}")

        return i

    def _execute_abs(self, tokens: List[Token], i: int) -> int:
        """执行绝对值函数"""
        i += 1  # 跳过 ABS

        # 获取值
        if i < len(tokens):
            # 处理负数
            if tokens[i].type == TokenType.MINUS:
                i += 1  # 跳过负号
                if i < len(tokens) and tokens[i].type == TokenType.NUMBER:
                    value = -float(tokens[i].value)
                    i += 1
                else:
                    value = 0
            elif tokens[i].type == TokenType.NUMBER:
                value = float(tokens[i].value)
                i += 1
            elif tokens[i].type == TokenType.IDENTIFIER:
                var_name = tokens[i].value
                if var_name in self.variables:
                    value = self.variables[var_name]
                    # 确保是数字
                    if isinstance(value, str):
                        try:
                            value = float(value)
                        except ValueError:
                            self.output.append(f"=> 错误：'{var_name}' 不是数字")
                            return i
                else:
                    value = 0
                i += 1
            else:
                value = 0

            result = abs(value)
            self.output.append(f"=> {result}")

        return i

    def _execute_sqrt(self, tokens: List[Token], i: int) -> int:
        """执行平方根函数"""
        i += 1  # 跳过 SQRT

        # 获取值
        if i < len(tokens):
            if tokens[i].type == TokenType.NUMBER:
                value = float(tokens[i].value)
                i += 1
            elif tokens[i].type == TokenType.IDENTIFIER:
                var_name = tokens[i].value
                if var_name in self.variables:
                    value = self.variables[var_name]
                else:
                    value = 0
                i += 1
            else:
                value = 0

            if value >= 0:
                result = math.sqrt(value)
                self.output.append(f"=> {result}")
            else:
                self.output.append(f"=> 错误：不能对负数求平方根")

        return i

    def _execute_pow(self, tokens: List[Token], i: int) -> int:
        """执行幂函数"""
        i += 1  # 跳过 POW

        # 获取底数
        base = 0
        if i < len(tokens):
            if tokens[i].type == TokenType.NUMBER:
                base = float(tokens[i].value)
                i += 1
            elif tokens[i].type == TokenType.IDENTIFIER:
                var_name = tokens[i].value
                if var_name in self.variables:
                    base = self.variables[var_name]
                i += 1

        # 获取指数
        exp = 1
        if i < len(tokens):
            if tokens[i].type == TokenType.NUMBER:
                exp = float(tokens[i].value)
                i += 1
            elif tokens[i].type == TokenType.IDENTIFIER:
                var_name = tokens[i].value
                if var_name in self.variables:
                    exp = self.variables[var_name]
                i += 1

        result = math.pow(base, exp)
        self.output.append(f"=> {result}")

        return i

    def _execute_int(self, tokens: List[Token], i: int) -> int:
        """执行取整函数"""
        i += 1  # 跳过 INT

        # 获取值
        if i < len(tokens):
            # 处理负数
            if tokens[i].type == TokenType.MINUS:
                i += 1  # 跳过负号
                if i < len(tokens) and tokens[i].type == TokenType.NUMBER:
                    value = -float(tokens[i].value)
                    i += 1
                else:
                    value = 0
            elif tokens[i].type == TokenType.NUMBER:
                value = float(tokens[i].value)
                i += 1
            elif tokens[i].type == TokenType.IDENTIFIER:
                var_name = tokens[i].value
                if var_name in self.variables:
                    value = self.variables[var_name]
                else:
                    value = 0
                i += 1
            else:
                value = 0

            result = int(value)
            self.output.append(f"=> {result}")

        return i

    def _execute_random(self, tokens: List[Token], i: int) -> int:
        """执行随机数函数"""
        i += 1  # 跳过 RANDOM

        # 检查是否有参数（范围）
        min_val = 0
        max_val = 1

        if i < len(tokens):
            if tokens[i].type == TokenType.NUMBER:
                min_val = float(tokens[i].value)
                i += 1
                # 检查是否有第二个参数
                if i < len(tokens) and tokens[i].type == TokenType.NUMBER:
                    max_val = float(tokens[i].value)
                    i += 1
            elif tokens[i].type == TokenType.IDENTIFIER:
                var_name = tokens[i].value
                if var_name in self.variables:
                    min_val = self.variables[var_name]
                i += 1
                # 检查是否有第二个参数
                if i < len(tokens):
                    if tokens[i].type == TokenType.NUMBER:
                        max_val = float(tokens[i].value)
                        i += 1
                    elif tokens[i].type == TokenType.IDENTIFIER:
                        var_name = tokens[i].value
                        if var_name in self.variables:
                            max_val = self.variables[var_name]
                        i += 1

        result = random.uniform(min_val, max_val)
        self.output.append(f"=> {result}")

        return i

    def _execute_sort(self, tokens: List[Token], i: int) -> int:
        """执行排序函数"""
        i += 1  # 跳过 SORT

        # 获取数组名
        if i < len(tokens) and tokens[i].type == TokenType.IDENTIFIER:
            arr_name = tokens[i].value
            i += 1

            if arr_name in self.variables:
                arr = self.variables[arr_name]
                if isinstance(arr, list):
                    # 尝试排序
                    try:
                        sorted_arr = sorted(arr)
                        self.variables[arr_name] = sorted_arr
                        self.output.append(f"=> {sorted_arr}")
                    except TypeError:
                        self.output.append(f"=> 错误：数组元素类型不一致，无法排序")
                else:
                    self.output.append(f"=> 错误：'{arr_name}' 不是数组")
            else:
                self.output.append(f"=> 错误：数组 '{arr_name}' 未定义")

        return i

    def _execute_reverse(self, tokens: List[Token], i: int) -> int:
        """执行反转函数"""
        i += 1  # 跳过 REVERSE

        # 获取数组名
        if i < len(tokens) and tokens[i].type == TokenType.IDENTIFIER:
            arr_name = tokens[i].value
            i += 1

            if arr_name in self.variables:
                arr = self.variables[arr_name]
                if isinstance(arr, list):
                    reversed_arr = list(reversed(arr))
                    self.variables[arr_name] = reversed_arr
                    self.output.append(f"=> {reversed_arr}")
                else:
                    self.output.append(f"=> 错误：'{arr_name}' 不是数组")
            else:
                self.output.append(f"=> 错误：数组 '{arr_name}' 未定义")

        return i

    def _execute_max(self, tokens: List[Token], i: int) -> int:
        """执行最大值函数"""
        i += 1  # 跳过 MAX

        # 获取数组名
        if i < len(tokens) and tokens[i].type == TokenType.IDENTIFIER:
            arr_name = tokens[i].value
            i += 1

            if arr_name in self.variables:
                arr = self.variables[arr_name]
                if isinstance(arr, list) and len(arr) > 0:
                    try:
                        result = max(arr)
                        self.output.append(f"=> {result}")
                    except TypeError:
                        self.output.append(f"=> 错误：数组元素类型不一致")
                else:
                    self.output.append(f"=> 错误：数组为空或不是数组")
            else:
                self.output.append(f"=> 错误：数组 '{arr_name}' 未定义")

        return i

    def _execute_min(self, tokens: List[Token], i: int) -> int:
        """执行最小值函数"""
        i += 1  # 跳过 MIN

        # 获取数组名
        if i < len(tokens) and tokens[i].type == TokenType.IDENTIFIER:
            arr_name = tokens[i].value
            i += 1

            if arr_name in self.variables:
                arr = self.variables[arr_name]
                if isinstance(arr, list) and len(arr) > 0:
                    try:
                        result = min(arr)
                        self.output.append(f"=> {result}")
                    except TypeError:
                        self.output.append(f"=> 错误：数组元素类型不一致")
                else:
                    self.output.append(f"=> 错误：数组为空或不是数组")
            else:
                self.output.append(f"=> 错误：数组 '{arr_name}' 未定义")

        return i

    def _execute_sum(self, tokens: List[Token], i: int) -> int:
        """执行求和函数"""
        i += 1  # 跳过 SUM

        # 获取数组名
        if i < len(tokens) and tokens[i].type == TokenType.IDENTIFIER:
            arr_name = tokens[i].value
            i += 1

            if arr_name in self.variables:
                arr = self.variables[arr_name]
                if isinstance(arr, list):
                    try:
                        result = sum(arr)
                        self.output.append(f"=> {result}")
                    except TypeError:
                        self.output.append(f"=> 错误：数组元素不是数字")
                else:
                    self.output.append(f"=> 错误：'{arr_name}' 不是数组")
            else:
                self.output.append(f"=> 错误：数组 '{arr_name}' 未定义")

        return i

    def _execute_if(self, tokens: List[Token], i: int) -> int:
        """执行条件语句"""
        i += 1  # 跳过 IF

        # 计算条件表达式
        condition_result = True  # 默认为真

        # 简单的条件判断：检查是否有 "大于"、"小于"、"等于" 等
        condition_tokens = []
        while i < len(tokens) and tokens[i].type not in (TokenType.NEWLINE, TokenType.THEN):
            condition_tokens.append(tokens[i])
            i += 1

        # 跳过 THEN 或 "则"
        if i < len(tokens) and tokens[i].type in (TokenType.THEN, TokenType.IDENTIFIER):
            i += 1
        # 跳过换行
        while i < len(tokens) and tokens[i].type == TokenType.NEWLINE:
            i += 1

        # 计算条件
        if condition_tokens:
            condition_result = self._evaluate_condition(condition_tokens)

        # 找到 ELSE 和 END 的位置
        if_start = i
        else_start = None
        depth = 1
        while i < len(tokens) and depth > 0:
            if tokens[i].type == TokenType.IF:
                depth += 1
            elif tokens[i].type == TokenType.ELSE and depth == 1:
                # 找到 ELSE 分支
                else_start = i + 1
                # 跳过 ELSE 后的换行
                while else_start < len(tokens) and tokens[else_start].type == TokenType.NEWLINE:
                    else_start += 1
            elif tokens[i].type == TokenType.END:
                depth -= 1
            i += 1

        # 执行相应的分支
        if condition_result:
            # 执行 IF 分支
            if else_start:
                # 有 ELSE 分支，执行到 ELSE 之前
                self._execute_tokens(tokens, if_start, else_start - 1)
            else:
                # 没有 ELSE 分支，执行到 END 之前
                self._execute_tokens(tokens, if_start, i - 1)
        elif else_start:
            # 条件为假，执行 ELSE 分支
            self._execute_tokens(tokens, else_start, i - 1)

        return i

    def _evaluate_condition(self, condition_tokens: List[Token]) -> bool:
        """计算条件表达式"""
        if not condition_tokens:
            return True

        # 简单的条件判断
        # 查找比较运算符
        for i, token in enumerate(condition_tokens):
            if token.type == TokenType.GREATER_THAN:
                # 获取左值和右值
                left_val = self._get_value(condition_tokens[:i])
                right_val = self._get_value(condition_tokens[i+1:])
                return left_val > right_val
            elif token.type == TokenType.LESS_THAN:
                left_val = self._get_value(condition_tokens[:i])
                right_val = self._get_value(condition_tokens[i+1:])
                return left_val < right_val
            elif token.type == TokenType.EQUAL_TO:
                left_val = self._get_value(condition_tokens[:i])
                right_val = self._get_value(condition_tokens[i+1:])
                return left_val == right_val
            elif token.type == TokenType.GREATER_EQUAL:
                left_val = self._get_value(condition_tokens[:i])
                right_val = self._get_value(condition_tokens[i+1:])
                return left_val >= right_val
            elif token.type == TokenType.LESS_EQUAL:
                left_val = self._get_value(condition_tokens[:i])
                right_val = self._get_value(condition_tokens[i+1:])
                return left_val <= right_val
            elif token.type == TokenType.NOT_EQUAL:
                left_val = self._get_value(condition_tokens[:i])
                right_val = self._get_value(condition_tokens[i+1:])
                return left_val != right_val
            elif token.type == TokenType.IDENTIFIER:
                # 检查是否是比较运算符
                if '大于等于' in token.value:
                    # 获取左值和右值
                    left_val = self._get_value(condition_tokens[:i])
                    right_val = self._get_value(condition_tokens[i+1:])
                    return left_val >= right_val
                elif '小于等于' in token.value:
                    left_val = self._get_value(condition_tokens[:i])
                    right_val = self._get_value(condition_tokens[i+1:])
                    return left_val <= right_val
                elif '不等于' in token.value:
                    left_val = self._get_value(condition_tokens[:i])
                    right_val = self._get_value(condition_tokens[i+1:])
                    return left_val != right_val
                elif '大于' in token.value:
                    # 获取左值和右值
                    left_val = self._get_value(condition_tokens[:i])
                    right_val = self._get_value(condition_tokens[i+1:])
                    return left_val > right_val
                elif '小于' in token.value:
                    left_val = self._get_value(condition_tokens[:i])
                    right_val = self._get_value(condition_tokens[i+1:])
                    return left_val < right_val
                elif '等于' in token.value:
                    left_val = self._get_value(condition_tokens[:i])
                    right_val = self._get_value(condition_tokens[i+1:])
                    return left_val == right_val

        # 默认返回真
        return True

    def _get_value(self, tokens: List[Token]) -> Any:
        """从词元列表获取值"""
        if not tokens:
            return 0

        # 过滤掉非值词元
        value_tokens = [t for t in tokens if t.type in (TokenType.NUMBER, TokenType.IDENTIFIER)]

        if not value_tokens:
            return 0

        # 获取第一个值
        token = value_tokens[0]
        if token.type == TokenType.NUMBER:
            return float(token.value)
        elif token.type == TokenType.IDENTIFIER:
            if token.value in self.variables:
                return self.variables[token.value]

        return 0

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

        # 执行循环，提供循环变量
        old_vars = self.variables.copy()
        for idx in range(count):
            # 设置循环变量
            self.variables['i'] = idx + 1
            self.variables['索引'] = idx + 1
            self._execute_tokens(tokens, start, end_pos - 1)
        # 恢复变量（移除循环变量）
        self.variables = old_vars

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
        # 跳过第一个 PARAMETER 关键字
        if i < len(tokens) and tokens[i].type == TokenType.PARAMETER:
            i += 1
        
        # 获取所有参数（支持多参数）
        while i < len(tokens):
            if tokens[i].type == TokenType.IDENTIFIER:
                params.append(tokens[i].value)
                i += 1
            elif tokens[i].type == TokenType.NEWLINE:
                # 参数列表结束
                break
            else:
                # 跳过其他词元（如逗号等）
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
        # 跳过 CALL
        if tokens[i].type == TokenType.CALL:
            i += 1

        # 获取函数名
        func_name = tokens[i].value
        i += 1

        # 跳过 PARAMETER
        if i < len(tokens) and tokens[i].type == TokenType.PARAMETER:
            i += 1

        # 获取参数值（支持多参数和表达式）
        args = []
        while i < len(tokens):
            if tokens[i].type == TokenType.NUMBER:
                args.append(float(tokens[i].value))
                i += 1
            elif tokens[i].type == TokenType.STRING:
                # 支持字符串参数
                args.append(tokens[i].value.strip('"\''))
                i += 1
            elif tokens[i].type == TokenType.IDENTIFIER:
                if tokens[i].value in self.variables:
                    # 可能是表达式的一部分
                    val = self.variables[tokens[i].value]
                    # 检查后面是否有运算符
                    if i + 1 < len(tokens) and tokens[i + 1].type in (TokenType.PLUS, TokenType.MINUS):
                        val, i = self._evaluate_expression(tokens, i)
                        args.append(val)
                    else:
                        args.append(val)
                        i += 1
                else:
                    # 可能是字符串参数（如柱子名称 A, B, C）
                    args.append(tokens[i].value)
                    i += 1
            elif tokens[i].type in (TokenType.PLUS, TokenType.MINUS):
                # 处理负数或表达式
                i += 1
                if i < len(tokens) and tokens[i].type == TokenType.NUMBER:
                    args.append(-float(tokens[i].value))
                    i += 1
            elif tokens[i].type == TokenType.NEWLINE:
                # 参数列表结束
                break
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

    def _evaluate_expression(self, tokens: List[Token], i: int) -> Tuple[Any, int]:
        """计算表达式 - 支持完整运算符和优先级"""
        # 使用递归下降解析器处理运算符优先级
        return self._parse_expression(tokens, i)

    def _parse_expression(self, tokens: List[Token], i: int) -> Tuple[Any, int]:
        """解析表达式（处理加减）"""
        result, i = self._parse_term(tokens, i)
        
        while i < len(tokens) and tokens[i].type in (TokenType.PLUS, TokenType.MINUS):
            op = tokens[i].type
            i += 1
            right, i = self._parse_term(tokens, i)
            if op == TokenType.PLUS:
                result += right
            else:
                result -= right
        
        return result, i

    def _parse_term(self, tokens: List[Token], i: int) -> Tuple[Any, int]:
        """解析项（处理乘除取模）"""
        result, i = self._parse_factor(tokens, i)
        
        while i < len(tokens) and tokens[i].type in (TokenType.MULTIPLY, TokenType.DIVIDE, TokenType.MODULO):
            op = tokens[i].type
            i += 1
            right, i = self._parse_factor(tokens, i)
            if op == TokenType.MULTIPLY:
                result *= right
            elif op == TokenType.DIVIDE:
                if right != 0:
                    result /= right
            else:
                result %= right
        
        return result, i

    def _parse_factor(self, tokens: List[Token], i: int) -> Tuple[Any, int]:
        """解析因子（处理数字、变量、括号）"""
        if i >= len(tokens):
            return 0, i
        
        # 处理括号
        if tokens[i].type == TokenType.LPAREN:
            i += 1  # 跳过 (
            result, i = self._parse_expression(tokens, i)
            if i < len(tokens) and tokens[i].type == TokenType.RPAREN:
                i += 1  # 跳过 )
            return result, i
        
        # 处理负号
        if tokens[i].type == TokenType.MINUS:
            i += 1
            result, i = self._parse_factor(tokens, i)
            return -result, i
        
        # 处理数字
        if tokens[i].type == TokenType.NUMBER:
            result = float(tokens[i].value)
            i += 1
            return result, i
        
        # 处理字符串
        if tokens[i].type == TokenType.STRING:
            result = tokens[i].value.strip('"\'')
            i += 1
            return result, i
        
        # 处理变量
        if tokens[i].type == TokenType.IDENTIFIER:
            var_name = tokens[i].value
            i += 1
            
            # 检查是否是数组索引访问
            if i < len(tokens) and tokens[i].type == TokenType.LBRACKET:
                i += 1  # 跳过 [
                # 获取索引
                if i < len(tokens):
                    if tokens[i].type == TokenType.NUMBER:
                        index = int(float(tokens[i].value))
                        i += 1
                    elif tokens[i].type == TokenType.IDENTIFIER:
                        index_var = tokens[i].value
                        if index_var in self.variables:
                            index = int(self.variables[index_var])
                        else:
                            index = 0
                        i += 1
                    else:
                        index = 0
                    
                    # 跳过 ]
                    if i < len(tokens) and tokens[i].type == TokenType.RBRACKET:
                        i += 1
                    
                    # 获取数组元素
                    if var_name in self.variables:
                        arr = self.variables[var_name]
                        if isinstance(arr, list) and 0 <= index < len(arr):
                            return arr[index], i
                    return 0, i
            else:
                # 普通变量
                if var_name in self.variables:
                    return self.variables[var_name], i
                return 0, i
        
        return 0, i

    def _execute_return(self, tokens: List[Token], i: int) -> Tuple[Any, int]:
        """执行返回语句"""
        i += 1  # 跳过 RETURN

        # 获取返回值
        return_value = None
        if i < len(tokens):
            if tokens[i].type == TokenType.IDENTIFIER:
                var_name = tokens[i].value
                if var_name in self.variables:
                    return_value = self.variables[var_name]
                i += 1
            elif tokens[i].type == TokenType.NUMBER:
                return_value = float(tokens[i].value)
                i += 1
            elif tokens[i].type == TokenType.STRING:
                return_value = tokens[i].value.strip('"\'')
                i += 1

        # 返回值和位置
        return return_value, i

    def _execute_concat(self, tokens: List[Token], i: int) -> int:
        """执行字符串连接操作"""
        i += 1  # 跳过 CONCAT

        elements = []
        target_var = None

        # 收集所有要连接的元素
        while i < len(tokens) and tokens[i].type not in (TokenType.NEWLINE, TokenType.END):
            if tokens[i].type == TokenType.STRING:
                elements.append(tokens[i].value.strip('"\''))
                i += 1
            elif tokens[i].type == TokenType.NUMBER:
                elements.append(str(float(tokens[i].value)))
                i += 1
            elif tokens[i].type == TokenType.IDENTIFIER:
                var_name = tokens[i].value
                i += 1
                if var_name in self.variables:
                    elements.append(str(self.variables[var_name]))
                else:
                    elements.append(var_name)
            elif tokens[i].type == TokenType.IS:
                # 后面是目标变量
                i += 1
                if i < len(tokens) and tokens[i].type == TokenType.IDENTIFIER:
                    target_var = tokens[i].value
                    i += 1
                break
            else:
                i += 1

        # 连接所有元素
        result = ''.join(elements)

        # 输出或赋值
        if target_var:
            self.variables[target_var] = result
        else:
            self.output.append(f"=> {result}")

        return i

    def _execute_slice(self, tokens: List[Token], i: int) -> int:
        """执行字符串切片操作"""
        i += 1  # 跳过 SLICE

        # 获取字符串变量
        if i < len(tokens) and tokens[i].type == TokenType.IDENTIFIER:
            var_name = tokens[i].value
            i += 1

            if var_name not in self.variables:
                self.output.append(f"错误：变量 '{var_name}' 未定义")
                return i

            string_value = str(self.variables[var_name])

            # 获取起始位置
            start = 0
            if i < len(tokens) and tokens[i].type == TokenType.NUMBER:
                start = int(float(tokens[i].value))
                i += 1
            elif i < len(tokens) and tokens[i].type == TokenType.MINUS:
                i += 1
                if i < len(tokens) and tokens[i].type == TokenType.NUMBER:
                    start = -int(float(tokens[i].value))
                    i += 1

            # 获取结束位置（可选）
            end = None
            if i < len(tokens) and tokens[i].type == TokenType.NUMBER:
                end = int(float(tokens[i].value))
                i += 1
            elif i < len(tokens) and tokens[i].type == TokenType.MINUS:
                i += 1
                if i < len(tokens) and tokens[i].type == TokenType.NUMBER:
                    end = -int(float(tokens[i].value))
                    i += 1

            # 获取步长（可选）
            step = None
            if i < len(tokens) and tokens[i].type == TokenType.NUMBER:
                step = int(float(tokens[i].value))
                i += 1

            # 执行切片
            if step:
                result = string_value[start:end:step]
            elif end is not None:
                result = string_value[start:end]
            else:
                result = string_value[start:]

            self.output.append(f"=> {result}")
            self.variables[var_name] = result

        return i

    def _execute_find_all(self, tokens: List[Token], i: int) -> int:
        """执行查找所有位置操作"""
        i += 1  # 跳过 FIND_ALL

        # 获取字符串变量
        if i < len(tokens) and tokens[i].type == TokenType.IDENTIFIER:
            var_name = tokens[i].value
            i += 1

            if var_name not in self.variables:
                self.output.append(f"错误：变量 '{var_name}' 未定义")
                return i

            string_value = str(self.variables[var_name])

            # 获取要查找的子串
            substring = ""
            if i < len(tokens) and tokens[i].type == TokenType.STRING:
                substring = tokens[i].value.strip('"\'')
                i += 1

            # 查找所有位置
            positions = []
            start = 0
            while True:
                pos = string_value.find(substring, start)
                if pos == -1:
                    break
                positions.append(pos)
                start = pos + 1

            self.output.append(f"=> {positions}")

        return i

    def _execute_replace_once(self, tokens: List[Token], i: int) -> int:
        """执行单次替换操作"""
        i += 1  # 跳过 REPLACE_ONCE

        # 获取字符串变量
        if i < len(tokens) and tokens[i].type == TokenType.IDENTIFIER:
            var_name = tokens[i].value
            i += 1

            if var_name not in self.variables:
                self.output.append(f"错误：变量 '{var_name}' 未定义")
                return i

            string_value = str(self.variables[var_name])

            # 获取旧子串
            old_substring = ""
            if i < len(tokens) and tokens[i].type == TokenType.STRING:
                old_substring = tokens[i].value.strip('"\'')
                i += 1

            # 获取新子串
            new_substring = ""
            if i < len(tokens) and tokens[i].type == TokenType.STRING:
                new_substring = tokens[i].value.strip('"\'')
                i += 1

            # 执行单次替换
            result = string_value.replace(old_substring, new_substring, 1)
            self.variables[var_name] = result
            self.output.append(f"=> {result}")

        return i

    def _execute_upper(self, tokens: List[Token], i: int) -> int:
        """执行大写转换操作"""
        i += 1  # 跳过 UPPER

        # 获取字符串变量
        if i < len(tokens) and tokens[i].type == TokenType.IDENTIFIER:
            var_name = tokens[i].value
            i += 1

            if var_name not in self.variables:
                self.output.append(f"错误：变量 '{var_name}' 未定义")
                return i

            string_value = str(self.variables[var_name])
            result = string_value.upper()
            self.variables[var_name] = result
            self.output.append(f"=> {result}")

        return i

    def _execute_lower(self, tokens: List[Token], i: int) -> int:
        """执行小写转换操作"""
        i += 1  # 跳过 LOWER

        # 获取字符串变量
        if i < len(tokens) and tokens[i].type == TokenType.IDENTIFIER:
            var_name = tokens[i].value
            i += 1

            if var_name not in self.variables:
                self.output.append(f"错误：变量 '{var_name}' 未定义")
                return i

            string_value = str(self.variables[var_name])
            result = string_value.lower()
            self.variables[var_name] = result
            self.output.append(f"=> {result}")

        return i

    def _execute_trim(self, tokens: List[Token], i: int) -> int:
        """执行去除首尾空格操作"""
        i += 1  # 跳过 TRIM

        # 获取字符串变量
        if i < len(tokens) and tokens[i].type == TokenType.IDENTIFIER:
            var_name = tokens[i].value
            i += 1

            if var_name not in self.variables:
                self.output.append(f"错误：变量 '{var_name}' 未定义")
                return i

            string_value = str(self.variables[var_name])
            result = string_value.strip()
            self.variables[var_name] = result
            self.output.append(f"=> {result}")

        return i

    def _execute_trim_all(self, tokens: List[Token], i: int) -> int:
        """执行去除所有空格操作"""
        i += 1  # 跳过 TRIM_ALL

        # 获取字符串变量
        if i < len(tokens) and tokens[i].type == TokenType.IDENTIFIER:
            var_name = tokens[i].value
            i += 1

            if var_name not in self.variables:
                self.output.append(f"错误：变量 '{var_name}' 未定义")
                return i

            string_value = str(self.variables[var_name])
            result = string_value.replace(' ', '').replace('\t', '').replace('\n', '')
            self.variables[var_name] = result
            self.output.append(f"=> {result}")

        return i

    def _execute_for_each_char(self, tokens: List[Token], i: int) -> int:
        """执行字符遍历操作"""
        i += 1  # 跳过 FOR_EACH_CHAR

        # 获取字符串变量
        if i < len(tokens) and tokens[i].type == TokenType.IDENTIFIER:
            string_var = tokens[i].value
            i += 1

            if string_var not in self.variables:
                self.output.append(f"错误：变量 '{string_var}' 未定义")
                return i

            string_value = str(self.variables[string_var])

            # 获取循环变量名
            loop_var = None
            if i < len(tokens) and tokens[i].type == TokenType.IDENTIFIER:
                loop_var = tokens[i].value
                i += 1

            # 查找循环体（直到"结束"）
            body_start = i
            body_end = i
            depth = 1

            while i < len(tokens) and depth > 0:
                if tokens[i].type == TokenType.FOR_EACH_CHAR:
                    depth += 1
                elif tokens[i].type == TokenType.END:
                    depth -= 1
                    if depth == 0:
                        body_end = i
                        break
                i += 1

            # 对每个字符执行循环体
            if loop_var:
                for char in string_value:
                    self.variables[loop_var] = char
                    self._execute_tokens(tokens, body_start, body_end)

            i += 1  # 跳过 END

        return i

    def _execute_sin(self, tokens: List[Token], i: int) -> int:
        """执行正弦函数"""
        i += 1  # 跳过 SIN
        if i < len(tokens):
            if tokens[i].type == TokenType.NUMBER:
                value = float(tokens[i].value)
                i += 1
            elif tokens[i].type == TokenType.IDENTIFIER:
                var_name = tokens[i].value
                if var_name in self.variables:
                    value = float(self.variables[var_name])
                else:
                    value = 0
                i += 1
            else:
                value = 0
            result = math.sin(value)
            self.output.append(f"=> {result}")
        return i

    def _execute_cos(self, tokens: List[Token], i: int) -> int:
        """执行余弦函数"""
        i += 1  # 跳过 COS
        if i < len(tokens):
            if tokens[i].type == TokenType.NUMBER:
                value = float(tokens[i].value)
                i += 1
            elif tokens[i].type == TokenType.IDENTIFIER:
                var_name = tokens[i].value
                if var_name in self.variables:
                    value = float(self.variables[var_name])
                else:
                    value = 0
                i += 1
            else:
                value = 0
            result = math.cos(value)
            self.output.append(f"=> {result}")
        return i

    def _execute_tan(self, tokens: List[Token], i: int) -> int:
        """执行正切函数"""
        i += 1  # 跳过 TAN
        if i < len(tokens):
            if tokens[i].type == TokenType.NUMBER:
                value = float(tokens[i].value)
                i += 1
            elif tokens[i].type == TokenType.IDENTIFIER:
                var_name = tokens[i].value
                if var_name in self.variables:
                    value = float(self.variables[var_name])
                else:
                    value = 0
                i += 1
            else:
                value = 0
            result = math.tan(value)
            self.output.append(f"=> {result}")
        return i

    def _execute_log(self, tokens: List[Token], i: int) -> int:
        """执行自然对数函数"""
        i += 1  # 跳过 LOG
        if i < len(tokens):
            if tokens[i].type == TokenType.NUMBER:
                value = float(tokens[i].value)
                i += 1
            elif tokens[i].type == TokenType.IDENTIFIER:
                var_name = tokens[i].value
                if var_name in self.variables:
                    value = float(self.variables[var_name])
                else:
                    value = 0
                i += 1
            else:
                value = 0
            if value > 0:
                result = math.log(value)
                self.output.append(f"=> {result}")
            else:
                self.output.append(f"=> 错误：对数函数的参数必须大于0")
        return i

    def _execute_log10(self, tokens: List[Token], i: int) -> int:
        """执行常用对数函数"""
        i += 1  # 跳过 LOG10
        if i < len(tokens):
            if tokens[i].type == TokenType.NUMBER:
                value = float(tokens[i].value)
                i += 1
            elif tokens[i].type == TokenType.IDENTIFIER:
                var_name = tokens[i].value
                if var_name in self.variables:
                    value = float(self.variables[var_name])
                else:
                    value = 0
                i += 1
            else:
                value = 0
            if value > 0:
                result = math.log10(value)
                self.output.append(f"=> {result}")
            else:
                self.output.append(f"=> 错误：对数函数的参数必须大于0")
        return i

    def _execute_exp(self, tokens: List[Token], i: int) -> int:
        """执行指数函数"""
        i += 1  # 跳过 EXP
        if i < len(tokens):
            if tokens[i].type == TokenType.NUMBER:
                value = float(tokens[i].value)
                i += 1
            elif tokens[i].type == TokenType.IDENTIFIER:
                var_name = tokens[i].value
                if var_name in self.variables:
                    value = float(self.variables[var_name])
                else:
                    value = 0
                i += 1
            else:
                value = 0
            result = math.exp(value)
            self.output.append(f"=> {result}")
        return i

    def _execute_ceil(self, tokens: List[Token], i: int) -> int:
        """执行向上取整函数"""
        i += 1  # 跳过 CEIL
        if i < len(tokens):
            if tokens[i].type == TokenType.NUMBER:
                value = float(tokens[i].value)
                i += 1
            elif tokens[i].type == TokenType.IDENTIFIER:
                var_name = tokens[i].value
                if var_name in self.variables:
                    value = float(self.variables[var_name])
                else:
                    value = 0
                i += 1
            else:
                value = 0
            result = math.ceil(value)
            self.output.append(f"=> {result}")
        return i

    def _execute_floor(self, tokens: List[Token], i: int) -> int:
        """执行向下取整函数"""
        i += 1  # 跳过 FLOOR
        if i < len(tokens):
            if tokens[i].type == TokenType.NUMBER:
                value = float(tokens[i].value)
                i += 1
            elif tokens[i].type == TokenType.IDENTIFIER:
                var_name = tokens[i].value
                if var_name in self.variables:
                    value = float(self.variables[var_name])
                else:
                    value = 0
                i += 1
            else:
                value = 0
            result = math.floor(value)
            self.output.append(f"=> {result}")
        return i

    def _execute_round(self, tokens: List[Token], i: int) -> int:
        """执行四舍五入函数"""
        i += 1  # 跳过 ROUND
        if i < len(tokens):
            if tokens[i].type == TokenType.NUMBER:
                value = float(tokens[i].value)
                i += 1
            elif tokens[i].type == TokenType.IDENTIFIER:
                var_name = tokens[i].value
                if var_name in self.variables:
                    value = float(self.variables[var_name])
                else:
                    value = 0
                i += 1
            else:
                value = 0
            result = round(value)
            self.output.append(f"=> {result}")
        return i

    def _execute_factorial(self, tokens: List[Token], i: int) -> int:
        """执行阶乘函数"""
        i += 1  # 跳过 FACTORIAL
        if i < len(tokens):
            if tokens[i].type == TokenType.NUMBER:
                value = int(float(tokens[i].value))
                i += 1
            elif tokens[i].type == TokenType.IDENTIFIER:
                var_name = tokens[i].value
                if var_name in self.variables:
                    value = int(float(self.variables[var_name]))
                else:
                    value = 0
                i += 1
            else:
                value = 0
            if value >= 0:
                result = math.factorial(value)
                self.output.append(f"=> {result}")
            else:
                self.output.append(f"=> 错误：阶乘函数的参数必须是非负整数")
        return i

    def _execute_read_file(self, tokens: List[Token], i: int) -> int:
        """执行读取文件操作"""
        i += 1  # 跳过 READ_FILE
        
        # 获取文件路径
        filepath = ""
        if i < len(tokens) and tokens[i].type == TokenType.STRING:
            filepath = tokens[i].value.strip('"\'')
            i += 1
        
        # 获取目标变量
        target_var = None
        if i < len(tokens) and tokens[i].type == TokenType.IS:
            i += 1
            if i < len(tokens) and tokens[i].type == TokenType.IDENTIFIER:
                target_var = tokens[i].value
                i += 1
        
        # 读取文件
        try:
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                if target_var:
                    self.variables[target_var] = content
                    self.output.append(f"=> 文件已读取到变量 '{target_var}'")
                else:
                    self.output.append(f"=> {content}")
            else:
                self.output.append(f"=> 错误：文件 '{filepath}' 不存在")
        except Exception as e:
            self.output.append(f"=> 错误：读取文件失败 - {str(e)}")
        
        return i

    def _execute_read_lines(self, tokens: List[Token], i: int) -> int:
        """执行读取文件行操作"""
        i += 1  # 跳过 READ_LINES
        
        # 获取文件路径
        filepath = ""
        if i < len(tokens) and tokens[i].type == TokenType.STRING:
            filepath = tokens[i].value.strip('"\'')
            i += 1
        
        # 获取目标变量
        target_var = None
        if i < len(tokens) and tokens[i].type == TokenType.IS:
            i += 1
            if i < len(tokens) and tokens[i].type == TokenType.IDENTIFIER:
                target_var = tokens[i].value
                i += 1
        
        # 读取文件行
        try:
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                lines = [line.strip() for line in lines]
                if target_var:
                    self.variables[target_var] = lines
                    self.output.append(f"=> 文件行已读取到变量 '{target_var}'")
                else:
                    self.output.append(f"=> {lines}")
            else:
                self.output.append(f"=> 错误：文件 '{filepath}' 不存在")
        except Exception as e:
            self.output.append(f"=> 错误：读取文件失败 - {str(e)}")
        
        return i

    def _execute_write_file(self, tokens: List[Token], i: int) -> int:
        """执行写入文件操作"""
        i += 1  # 跳过 WRITE_FILE
        
        # 获取文件路径
        filepath = ""
        if i < len(tokens) and tokens[i].type == TokenType.STRING:
            filepath = tokens[i].value.strip('"\'')
            i += 1
        
        # 获取内容
        content = ""
        if i < len(tokens):
            if tokens[i].type == TokenType.STRING:
                content = tokens[i].value.strip('"\'')
                i += 1
            elif tokens[i].type == TokenType.IDENTIFIER:
                var_name = tokens[i].value
                if var_name in self.variables:
                    content = str(self.variables[var_name])
                i += 1
        
        # 写入文件
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            self.output.append(f"=> 文件已写入 '{filepath}'")
        except Exception as e:
            self.output.append(f"=> 错误：写入文件失败 - {str(e)}")
        
        return i

    def _execute_append_file(self, tokens: List[Token], i: int) -> int:
        """执行追加文件操作"""
        i += 1  # 跳过 APPEND_FILE
        
        # 获取文件路径
        filepath = ""
        if i < len(tokens) and tokens[i].type == TokenType.STRING:
            filepath = tokens[i].value.strip('"\'')
            i += 1
        
        # 获取内容
        content = ""
        if i < len(tokens):
            if tokens[i].type == TokenType.STRING:
                content = tokens[i].value.strip('"\'')
                i += 1
            elif tokens[i].type == TokenType.IDENTIFIER:
                var_name = tokens[i].value
                if var_name in self.variables:
                    content = str(self.variables[var_name])
                i += 1
        
        # 追加文件
        try:
            with open(filepath, 'a', encoding='utf-8') as f:
                f.write(content)
            self.output.append(f"=> 内容已追加到 '{filepath}'")
        except Exception as e:
            self.output.append(f"=> 错误：追加文件失败 - {str(e)}")
        
        return i

    def _execute_file_exists(self, tokens: List[Token], i: int) -> int:
        """执行文件存在检查"""
        i += 1  # 跳过 FILE_EXISTS
        
        # 获取文件路径
        filepath = ""
        if i < len(tokens) and tokens[i].type == TokenType.STRING:
            filepath = tokens[i].value.strip('"\'')
            i += 1
        
        # 检查文件存在
        exists = os.path.exists(filepath)
        self.output.append(f"=> {'真' if exists else '假'}")
        
        return i

    def _execute_file_size(self, tokens: List[Token], i: int) -> int:
        """执行获取文件大小"""
        i += 1  # 跳过 FILE_SIZE
        
        # 获取文件路径
        filepath = ""
        if i < len(tokens) and tokens[i].type == TokenType.STRING:
            filepath = tokens[i].value.strip('"\'')
            i += 1
        
        # 获取文件大小
        try:
            if os.path.exists(filepath):
                size = os.path.getsize(filepath)
                self.output.append(f"=> {size}")
            else:
                self.output.append(f"=> 错误：文件 '{filepath}' 不存在")
        except Exception as e:
            self.output.append(f"=> 错误：获取文件大小失败 - {str(e)}")
        
        return i

    def _execute_file_name(self, tokens: List[Token], i: int) -> int:
        """执行获取文件名"""
        i += 1  # 跳过 FILE_NAME
        
        # 获取文件路径
        filepath = ""
        if i < len(tokens) and tokens[i].type == TokenType.STRING:
            filepath = tokens[i].value.strip('"\'')
            i += 1
        
        # 获取文件名
        filename = os.path.basename(filepath)
        self.output.append(f"=> {filename}")
        
        return i

    def _execute_dir_name(self, tokens: List[Token], i: int) -> int:
        """执行获取目录名"""
        i += 1  # 跳过 DIR_NAME
        
        # 获取文件路径
        filepath = ""
        if i < len(tokens) and tokens[i].type == TokenType.STRING:
            filepath = tokens[i].value.strip('"\'')
            i += 1
        
        # 获取目录名
        dirname = os.path.dirname(filepath)
        self.output.append(f"=> {dirname}")
        
        return i


def create_interpreter() -> YanLuInterpreter:
    """创建解释器实例"""
    return YanLuInterpreter()
