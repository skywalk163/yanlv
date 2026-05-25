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
                if tokens[i].type == TokenType.NUMBER:
                    self.variables[var_name] = float(tokens[i].value)
                    i += 1
                elif tokens[i].type == TokenType.STRING:
                    self.variables[var_name] = tokens[i].value.strip('"\'')
                    i += 1
                elif tokens[i].type == TokenType.LBRACKET:
                    # 处理数组 [1, 2, 3]
                    i += 1  # 跳过 [
                    arr = []
                    while i < len(tokens) and tokens[i].type != TokenType.RBRACKET:
                        if tokens[i].type == TokenType.NUMBER:
                            arr.append(float(tokens[i].value))
                            i += 1
                        elif tokens[i].type == TokenType.STRING:
                            arr.append(tokens[i].value.strip('"\''))
                            i += 1
                        elif tokens[i].type == TokenType.COMMA:
                            i += 1  # 跳过逗号
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


def create_interpreter() -> YanLuInterpreter:
    """创建解释器实例"""
    return YanLuInterpreter()
