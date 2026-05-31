"""
言律语言高级解释器
支持因果链语法、语境省略语法、状态流语法等高级特性
"""

from typing import List, Dict, Any, Optional
from .lexer.lexer_token import Token, TokenType
from .advanced_parser import AdvancedParser
from .interpreter_complete import CompleteInterpreter


class AdvancedInterpreter:
    """高级解释器"""
    
    def __init__(self):
        """初始化高级解释器"""
        self.base_interpreter = CompleteInterpreter()
        self.advanced_parser = AdvancedParser()
        self.variables: Dict[str, Any] = {}
        self.functions: Dict[str, Dict] = {}
        self.output: List[str] = []
        self.context_stack: List[str] = []  # 语境栈
        self.return_value: Any = None  # 返回值
        self.in_function: bool = False  # 是否在函数中
    
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
            # 检查是否在函数中且有返回值
            if self.in_function and self.return_value is not None:
                return i
            
            token = tokens[i]
            
            # 跳过换行符
            if token.type == TokenType.NEWLINE:
                i += 1
                continue
            
            # 检查因果链语法
            if self._is_causal_chain(tokens, i):
                i = self._execute_causal_chain(tokens, i)
                continue
            
            # 检查主题块语法
            if self._is_theme_block(tokens, i):
                i = self._execute_theme_block(tokens, i)
                continue
            
            # 检查高级定义语法
            if token.type == TokenType.DEF:
                i = self._execute_advanced_define(tokens, i)
                continue
            
            # 检查简化数组定义 "列5 3 8..."
            if token.value == '列':
                i = self._execute_array_definition(tokens, i)
                continue
            
            # 检查"对于...从...到...："循环语法
            if token.value == '对于':
                i = self._execute_for_loop(tokens, i)
                continue
            
            # 检查"若...就："条件语法
            if token.value == '若':
                i = self._execute_if_simple(tokens, i)
                continue
            
            # 检查函数式数组访问 "列表算j"
            if self._is_functional_array_access(tokens, i):
                i = self._execute_functional_array_access(tokens, i)
                continue
            
            # 检查高级函数调用
            if self._is_advanced_call(tokens, i):
                i = self._execute_advanced_call(tokens, i)
                continue
            
            # 检查返回语句
            if token.value in ('回', '返回', 'return'):
                i = self._execute_return(tokens, i)
                continue
            
            # 使用基础解释器处理其他情况
            i = self._execute_with_base(tokens, i)
        
        return i
    
    def _is_causal_chain(self, tokens: List[Token], i: int) -> bool:
        """检查是否是因果链语法"""
        # 因果链特征：条件，动作。
        j = i
        has_comma = False
        has_period = False
        
        # 跳过可能的条件部分
        while j < len(tokens) and tokens[j].type not in (TokenType.NEWLINE, TokenType.EOF):
            if tokens[j].type == TokenType.COMMA:
                has_comma = True
            elif tokens[j].type == TokenType.PERIOD:
                has_period = True
                break
            j += 1
        
        return has_comma and has_period
    
    def _execute_causal_chain(self, tokens: List[Token], i: int) -> int:
        """执行因果链"""
        # 解析条件部分
        condition_tokens = []
        while i < len(tokens) and tokens[i].type != TokenType.COMMA:
            if tokens[i].type == TokenType.NEWLINE:
                break
            condition_tokens.append(tokens[i])
            i += 1
        
        # 跳过逗号
        if i < len(tokens) and tokens[i].type == TokenType.COMMA:
            i += 1
        
        # 解析动作部分
        action_tokens = []
        while i < len(tokens) and tokens[i].type != TokenType.PERIOD:
            if tokens[i].type == TokenType.NEWLINE:
                break
            action_tokens.append(tokens[i])
            i += 1
        
        # 跳过句号
        if i < len(tokens) and tokens[i].type == TokenType.PERIOD:
            i += 1
        
        # 评估条件
        condition_result = self._evaluate_condition(condition_tokens)
        
        # 如果条件为真，执行动作
        if condition_result:
            self._execute_action(action_tokens)
        
        return i
    
    def _evaluate_condition(self, condition_tokens: List[Token]) -> bool:
        """评估条件（支持组合条件和嵌套条件）"""
        if not condition_tokens:
            return False
        
        # 处理组合条件（且、或）
        # 例如：下雨了且温度小于10
        and_parts = []
        or_parts = []
        current_part = []
        has_and = False
        has_or = False
        
        for token in condition_tokens:
            if token.value in ('且', '并且', 'and', 'AND'):
                if current_part:
                    and_parts.append(current_part)
                    current_part = []
                has_and = True
            elif token.value in ('或', '或者', 'or', 'OR'):
                if current_part:
                    or_parts.append(current_part)
                    current_part = []
                has_or = True
            else:
                current_part.append(token)
        
        if current_part:
            if has_and:
                and_parts.append(current_part)
            elif has_or:
                or_parts.append(current_part)
        
        # 处理AND条件
        if has_and and and_parts:
            results = [self._evaluate_simple_condition(part) for part in and_parts]
            return all(results)
        
        # 处理OR条件
        if has_or and or_parts:
            results = [self._evaluate_simple_condition(part) for part in or_parts]
            return any(results)
        
        # 简单条件
        return self._evaluate_simple_condition(condition_tokens)
    
    def _evaluate_simple_condition(self, condition_tokens: List[Token]) -> bool:
        """评估简单条件"""
        if not condition_tokens:
            return False
        
        # 处理字符串包含条件
        # 例如：消息包含"价格"
        for i, token in enumerate(condition_tokens):
            if token.value in ('包含', '包括', '含有'):
                if i > 0 and i + 1 < len(condition_tokens):
                    var_name = condition_tokens[i - 1].value
                    if var_name in self.variables:
                        var_value = str(self.variables[var_name])
                        check_value = condition_tokens[i + 1].value.strip('"\'')
                        return check_value in var_value
        
        # 处理状态条件
        # 例如：用户状态为在线
        for i, token in enumerate(condition_tokens):
            if token.value in ('为', '是') and i > 0:
                var_name = condition_tokens[i - 1].value
                if i + 1 < len(condition_tokens):
                    expected_value = condition_tokens[i + 1].value
                    if var_name in self.variables:
                        var_value = self.variables[var_name]
                        # 处理对象属性访问
                        if isinstance(var_value, dict):
                            return expected_value in var_value.values()
                        return str(var_value) == expected_value
        
        # 处理比较条件
        # 例如：温度大于28
        if len(condition_tokens) >= 3:
            var_name = condition_tokens[0].value
            operator = condition_tokens[1].value
            value = condition_tokens[2].value
            
            # 获取变量值
            if var_name in self.variables:
                var_value = self.variables[var_name]
                
                # 尝试将value转换为数字
                try:
                    num_value = float(value)
                except:
                    num_value = value
                
                # 比较操作
                if operator in ('大于', '>', '大于等于', '>='):
                    return var_value > num_value if operator in ('大于', '>') else var_value >= num_value
                elif operator in ('小于', '<', '小于等于', '<='):
                    return var_value < num_value if operator in ('小于', '<') else var_value <= num_value
                elif operator in ('等于', '==', '为'):
                    return var_value == num_value
                elif operator in ('不等于', '!=', '不为'):
                    return var_value != num_value
        
        # 处理范围条件
        # 例如：温度在20到28之间
        for i, token in enumerate(condition_tokens):
            if token.value == '在':
                var_name = condition_tokens[i - 1].value if i > 0 else None
                if var_name and var_name in self.variables:
                    var_value = self.variables[var_name]
                    # 查找"到"和"之间"
                    try:
                        to_idx = None
                        for j in range(i + 1, len(condition_tokens)):
                            if condition_tokens[j].value == '到':
                                to_idx = j
                                break
                        
                        if to_idx:
                            min_val = float(condition_tokens[i + 1].value)
                            max_val = float(condition_tokens[to_idx + 1].value)
                            return min_val <= var_value <= max_val
                    except:
                        pass
        
        return False
    
    def _execute_action(self, action_tokens: List[Token]):
        """执行动作"""
        if not action_tokens:
            return
        
        # 检查是否是输出动作
        for i, token in enumerate(action_tokens):
            if token.value == '印':
                # 输出动作
                if i + 1 < len(action_tokens) and action_tokens[i + 1].type == TokenType.STRING:
                    self.output.append(action_tokens[i + 1].value.strip('"\''))
                elif i > 0 and action_tokens[i - 1].type == TokenType.IDENTIFIER:
                    var_name = action_tokens[i - 1].value
                    if var_name in self.variables:
                        self.output.append(str(self.variables[var_name]))
                return
        
        # 其他动作，使用基础解释器
        self.base_interpreter.variables = self.variables
        self.base_interpreter.functions = self.functions
        result = self.base_interpreter.execute(action_tokens)
        self.output.extend(result)
    
    def _is_theme_block(self, tokens: List[Token], i: int) -> bool:
        """检查是否是主题块"""
        # "以X为主题：" 或 "X："
        if tokens[i].value == '以':
            return True
        if tokens[i].type == TokenType.IDENTIFIER:
            j = i + 1
            while j < len(tokens) and tokens[j].type == TokenType.NEWLINE:
                j += 1
            if j < len(tokens) and tokens[j].type == TokenType.COLON:
                return True
        return False
    
    def _execute_theme_block(self, tokens: List[Token], i: int) -> int:
        """执行主题块"""
        theme_name = None
        
        # 解析主题名
        if tokens[i].value == '以':
            i += 1
            if i < len(tokens) and tokens[i].type == TokenType.IDENTIFIER:
                theme_name = tokens[i].value
                i += 1
                # 跳过"为主题"
                while i < len(tokens) and tokens[i].value in ('为', '主题'):
                    i += 1
        elif tokens[i].type == TokenType.IDENTIFIER:
            theme_name = tokens[i].value
            i += 1
        
        # 跳过冒号
        if i < len(tokens) and tokens[i].type == TokenType.COLON:
            i += 1
        
        # 将主题压入语境栈
        if theme_name:
            self.context_stack.append(theme_name)
        
        # 解析并执行块内容
        indent_level = tokens[i].indent if i < len(tokens) else 0
        
        while i < len(tokens):
            if tokens[i].type == TokenType.NEWLINE:
                i += 1
                continue
            
            # 检查缩进级别
            if hasattr(tokens[i], 'indent') and tokens[i].indent <= indent_level:
                break
            
            # 执行块内的语句
            i = self._execute_tokens(tokens, i, len(tokens))
        
        # 弹出语境栈
        if theme_name and self.context_stack:
            self.context_stack.pop()
        
        return i
    
    def _execute_advanced_define(self, tokens: List[Token], i: int) -> int:
        """执行高级定义语法"""
        i += 1  # 跳过 '定'
        
        if i >= len(tokens):
            return i
        
        # 获取名称
        name = tokens[i].value
        i += 1
        
        # 跳过 '是'
        if i < len(tokens) and tokens[i].type == TokenType.IS:
            i += 1
        
        # 检查定义类型
        if i < len(tokens):
            # 函数定义：定f是函参数：
            if tokens[i].value == '函':
                i += 1
                # 解析参数
                params = []
                while i < len(tokens) and tokens[i].type not in (TokenType.COLON, TokenType.NEWLINE):
                    if tokens[i].type == TokenType.IDENTIFIER:
                        params.append(tokens[i].value)
                    i += 1
                
                # 跳过冒号
                if i < len(tokens) and tokens[i].type == TokenType.COLON:
                    i += 1
                
                # 解析函数体
                body_tokens = []
                indent_level = tokens[i].indent if i < len(tokens) else 0
                
                while i < len(tokens):
                    if tokens[i].type == TokenType.NEWLINE:
                        i += 1
                        continue
                    
                    if hasattr(tokens[i], 'indent') and tokens[i].indent <= indent_level:
                        break
                    
                    body_tokens.append(tokens[i])
                    i += 1
                
                # 保存函数定义
                self.functions[name] = {
                    'params': params,
                    'body': body_tokens
                }
                
                return i
            
            # 典（对象）定义：定obj是典...
            elif tokens[i].value == '典':
                i += 1
                # 解析对象属性
                obj = {}
                while i < len(tokens) and tokens[i].type != TokenType.PERIOD:
                    if tokens[i].type == TokenType.IDENTIFIER:
                        prop_name = tokens[i].value
                        i += 1
                        # 跳过 '是'
                        if i < len(tokens) and tokens[i].type == TokenType.IS:
                            i += 1
                        # 获取值
                        if i < len(tokens):
                            if tokens[i].type == TokenType.NUMBER:
                                obj[prop_name] = float(tokens[i].value)
                            elif tokens[i].type == TokenType.STRING:
                                obj[prop_name] = tokens[i].value.strip('"\'')
                            elif tokens[i].type == TokenType.IDENTIFIER:
                                if tokens[i].value in ('真', '是'):
                                    obj[prop_name] = True
                                elif tokens[i].value in ('假', '否'):
                                    obj[prop_name] = False
                                else:
                                    obj[prop_name] = tokens[i].value
                            i += 1
                    else:
                        i += 1
                
                # 跳过句号
                if i < len(tokens) and tokens[i].type == TokenType.PERIOD:
                    i += 1
                
                self.variables[name] = obj
                return i
            
            # 变量定义：定x是值。
            else:
                # 获取值
                if tokens[i].type == TokenType.NUMBER:
                    value = float(tokens[i].value)
                    i += 1
                elif tokens[i].type == TokenType.STRING:
                    value = tokens[i].value.strip('"\'')
                    i += 1
                elif tokens[i].type == TokenType.IDENTIFIER:
                    value = tokens[i].value
                    i += 1
                else:
                    value = None
                    i += 1
                
                # 跳过句号
                if i < len(tokens) and tokens[i].type == TokenType.PERIOD:
                    i += 1
                
                self.variables[name] = value
                return i
        
        return i
    
    def _is_advanced_call(self, tokens: List[Token], i: int) -> bool:
        """检查是否是高级函数调用"""
        # 格式：参数，函数名。
        if tokens[i].type == TokenType.IDENTIFIER:
            j = i + 1
            # 查找逗号
            while j < len(tokens) and tokens[j].type not in (TokenType.COMMA, TokenType.NEWLINE, TokenType.EOF):
                j += 1
            
            if j < len(tokens) and tokens[j].type == TokenType.COMMA:
                j += 1
                # 检查逗号后是否是函数名
                if j < len(tokens) and tokens[j].type == TokenType.IDENTIFIER:
                    func_name = tokens[j].value
                    return func_name in self.functions
        
        return False
    
    def _execute_advanced_call(self, tokens: List[Token], i: int) -> int:
        """执行高级函数调用（支持多参数）"""
        # 解析参数（可能多个）
        args = []
        current_arg = []
        
        while i < len(tokens):
            token = tokens[i]
            
            # 遇到逗号，保存当前参数
            if token.type == TokenType.COMMA:
                if current_arg:
                    arg_value = self._evaluate_argument(current_arg)
                    args.append(arg_value)
                    current_arg = []
                i += 1
                
                # 检查逗号后是否是函数名
                if i < len(tokens) and tokens[i].type == TokenType.IDENTIFIER:
                    func_name = tokens[i].value
                    if func_name in self.functions:
                        i += 1
                        # 调用函数
                        return self._call_function(func_name, args, tokens, i)
                
                continue
            
            # 遇到句号，结束
            if token.type == TokenType.PERIOD:
                if current_arg:
                    arg_value = self._evaluate_argument(current_arg)
                    args.append(arg_value)
                i += 1
                break
            
            # 遇到换行，结束
            if token.type == TokenType.NEWLINE:
                if current_arg:
                    arg_value = self._evaluate_argument(current_arg)
                    args.append(arg_value)
                break
            
            # 收集参数token
            current_arg.append(token)
            i += 1
        
        return i
    
    def _evaluate_argument(self, arg_tokens: List[Token]) -> Any:
        """评估参数值"""
        if not arg_tokens:
            return None
        
        # 单个token
        if len(arg_tokens) == 1:
            token = arg_tokens[0]
            if token.type == TokenType.IDENTIFIER:
                var_name = token.value
                if var_name in self.variables:
                    return self.variables[var_name]
                return var_name
            elif token.type == TokenType.NUMBER:
                return float(token.value)
            elif token.type == TokenType.STRING:
                return token.value.strip('"\'')
        
        # 多个token，可能是表达式
        # 简单处理：返回第一个token的值
        return self._evaluate_argument([arg_tokens[0]])
    
    def _call_function(self, func_name: str, args: List[Any], tokens: List[Token], i: int) -> int:
        """调用函数"""
        if func_name not in self.functions:
            return i
        
        func_def = self.functions[func_name]
        params = func_def['params']
        body = func_def['body']
        
        # 保存当前状态
        old_vars = self.variables.copy()
        old_in_function = self.in_function
        old_return_value = self.return_value
        
        # 设置函数状态
        self.in_function = True
        self.return_value = None
        
        # 绑定参数
        for param, arg in zip(params, args):
            self.variables[param] = arg
        
        # 执行函数体
        self._execute_tokens(body, 0, len(body))
        
        # 获取返回值
        result = self.return_value
        
        # 恢复状态
        self.variables = old_vars
        self.in_function = old_in_function
        self.return_value = old_return_value
        
        # 如果有返回值，可以继续使用
        if result is not None:
            # 检查是否需要输出
            if i < len(tokens) and tokens[i].value == '印':
                self.output.append(str(result))
                i += 1
                # 跳过句号
                if i < len(tokens) and tokens[i].type == TokenType.PERIOD:
                    i += 1
        
        return i
    
    def _execute_with_base(self, tokens: List[Token], i: int) -> int:
        """使用基础解释器执行"""
        # 收集当前行的tokens
        line_tokens = []
        start_i = i
        
        while i < len(tokens) and tokens[i].type != TokenType.NEWLINE:
            line_tokens.append(tokens[i])
            i += 1
        
        if line_tokens:
            # 直接处理简单的输出语句
            if len(line_tokens) >= 2 and line_tokens[0].value in ('印', '输出'):
                # 输出语句
                if line_tokens[1].type == TokenType.STRING:
                    self.output.append(line_tokens[1].value.strip('"\''))
                elif line_tokens[1].type == TokenType.IDENTIFIER:
                    var_name = line_tokens[1].value
                    if var_name in self.variables:
                        self.output.append(str(self.variables[var_name]))
                    else:
                        self.output.append(var_name)
                elif line_tokens[1].type == TokenType.NUMBER:
                    self.output.append(line_tokens[1].value)
            else:
                # 使用基础解释器执行
                self.base_interpreter.variables = self.variables
                self.base_interpreter.functions = self.functions
                result = self.base_interpreter.execute(line_tokens)
                self.output.extend(result)
                
                # 同步变量和函数
                self.variables = self.base_interpreter.variables
                self.functions = self.base_interpreter.functions
        
        return i
    
    def _execute_return(self, tokens: List[Token], i: int) -> int:
        """执行返回语句"""
        i += 1  # 跳过 '回' 或 '返回'
        
        # 解析返回值
        return_tokens = []
        while i < len(tokens) and tokens[i].type not in (TokenType.PERIOD, TokenType.NEWLINE, TokenType.EOF):
            return_tokens.append(tokens[i])
            i += 1
        
        # 跳过句号
        if i < len(tokens) and tokens[i].type == TokenType.PERIOD:
            i += 1
        
        # 评估返回值
        if return_tokens:
            self.return_value = self._evaluate_argument(return_tokens)
        else:
            self.return_value = None
        
        return i
    
    def _execute_for_loop(self, tokens: List[Token], i: int) -> int:
        """执行'对于...从...到...：'循环语法"""
        i += 1  # 跳过 '对于'
        
        # 解析循环变量
        if i < len(tokens) and tokens[i].type == TokenType.IDENTIFIER:
            loop_var = tokens[i].value
            i += 1
        else:
            return i
        
        # 跳过 '从'
        if i < len(tokens) and tokens[i].value == '从':
            i += 1
        
        # 解析起始值
        start_value = 0
        if i < len(tokens):
            if tokens[i].type == TokenType.NUMBER:
                start_value = int(float(tokens[i].value))
                i += 1
            elif tokens[i].type == TokenType.IDENTIFIER:
                var_name = tokens[i].value
                if var_name in self.variables:
                    start_value = int(self.variables[var_name])
                i += 1
        
        # 跳过 '到'
        if i < len(tokens) and tokens[i].value == '到':
            i += 1
        
        # 解析结束值（可能包含表达式，如"长度减1"）
        end_value = 0
        end_tokens = []
        while i < len(tokens) and tokens[i].type not in (TokenType.COLON, TokenType.NEWLINE):
            end_tokens.append(tokens[i])
            i += 1
        
        # 评估结束值
        if end_tokens:
            end_value = self._evaluate_end_expression(end_tokens)
        
        # 跳过冒号
        if i < len(tokens) and tokens[i].type == TokenType.COLON:
            i += 1
        
        # 解析循环体
        body_tokens = []
        indent_level = tokens[i].indent if i < len(tokens) else 0
        
        while i < len(tokens):
            if tokens[i].type == TokenType.NEWLINE:
                i += 1
                continue
            
            # 检查缩进级别
            if hasattr(tokens[i], 'indent') and tokens[i].indent <= indent_level:
                break
            
            body_tokens.append(tokens[i])
            i += 1
        
        # 执行循环
        for value in range(start_value, end_value + 1):
            # 设置循环变量
            old_value = self.variables.get(loop_var)
            self.variables[loop_var] = value
            
            # 执行循环体
            self._execute_tokens(body_tokens, 0, len(body_tokens))
            
            # 恢复循环变量（如果需要）
            if old_value is not None:
                self.variables[loop_var] = old_value
        
        return i
    
    def _evaluate_end_expression(self, tokens: List[Token]) -> int:
        """评估结束值表达式（如"长度减1"）"""
        if not tokens:
            return 0
        
        # 简单数字
        if len(tokens) == 1 and tokens[0].type == TokenType.NUMBER:
            return int(float(tokens[0].value))
        
        # 变量
        if len(tokens) == 1 and tokens[0].type == TokenType.IDENTIFIER:
            var_name = tokens[0].value
            if var_name in self.variables:
                val = self.variables[var_name]
                return int(float(val)) if isinstance(val, (int, float, str)) else 0
            return 0
        
        # 表达式（如"长度减1"）
        if len(tokens) >= 3:
            # 获取基础值
            base_value = 0
            if tokens[0].type == TokenType.IDENTIFIER:
                var_name = tokens[0].value
                if var_name in self.variables:
                    val = self.variables[var_name]
                    base_value = float(val) if isinstance(val, (int, float, str)) else 0
            elif tokens[0].type == TokenType.NUMBER:
                base_value = float(tokens[0].value)
            
            # 获取操作符
            operator = tokens[1].value
            
            # 获取操作数
            operand = 0
            if tokens[2].type == TokenType.NUMBER:
                operand = float(tokens[2].value)
            elif tokens[2].type == TokenType.IDENTIFIER:
                var_name = tokens[2].value
                if var_name in self.variables:
                    val = self.variables[var_name]
                    operand = float(val) if isinstance(val, (int, float, str)) else 0
            
            # 执行操作
            if operator in ('减', '-', '减去'):
                return int(base_value - operand)
            elif operator in ('加', '+', '加上'):
                return int(base_value + operand)
            elif operator in ('乘', '*', '乘以'):
                return int(base_value * operand)
            elif operator in ('除', '/', '除以'):
                return int(base_value / operand) if operand != 0 else 0
        
        return 0
    
    def _execute_if_simple(self, tokens: List[Token], i: int) -> int:
        """执行'若...就：'条件语法"""
        i += 1  # 跳过 '若'
        
        # 解析条件
        condition_tokens = []
        while i < len(tokens) and tokens[i].value not in ('就', '则'):
            if tokens[i].type == TokenType.NEWLINE:
                break
            condition_tokens.append(tokens[i])
            i += 1
        
        # 跳过 '就'
        if i < len(tokens) and tokens[i].value in ('就', '则'):
            i += 1
        
        # 跳过冒号
        if i < len(tokens) and tokens[i].type == TokenType.COLON:
            i += 1
        
        # 解析条件体
        body_tokens = []
        indent_level = tokens[i].indent if i < len(tokens) else 0
        
        while i < len(tokens):
            if tokens[i].type == TokenType.NEWLINE:
                i += 1
                continue
            
            # 检查缩进级别
            if hasattr(tokens[i], 'indent') and tokens[i].indent <= indent_level:
                break
            
            body_tokens.append(tokens[i])
            i += 1
        
        # 评估条件
        condition_result = self._evaluate_condition(condition_tokens)
        
        # 如果条件为真，执行条件体
        if condition_result:
            self._execute_tokens(body_tokens, 0, len(body_tokens))
        
        return i
    
    def _execute_array_definition(self, tokens: List[Token], i: int) -> int:
        """执行简化数组定义 '列5 3 8...'"""
        i += 1  # 跳过 '列'
        
        # 收集数组元素
        elements = []
        while i < len(tokens) and tokens[i].type not in (TokenType.PERIOD, TokenType.NEWLINE, TokenType.EOF):
            if tokens[i].type == TokenType.NUMBER:
                elements.append(float(tokens[i].value))
            elif tokens[i].type == TokenType.STRING:
                elements.append(tokens[i].value.strip('"\''))
            elif tokens[i].type == TokenType.IDENTIFIER:
                # 可能是变量引用
                var_name = tokens[i].value
                if var_name in self.variables:
                    elements.append(self.variables[var_name])
            i += 1
        
        # 跳过句号
        if i < len(tokens) and tokens[i].type == TokenType.PERIOD:
            i += 1
        
        # 返回数组（作为表达式的结果）
        # 这里需要特殊处理，因为通常数组定义会赋值给变量
        # 例如：定数据是列5 3 8 4 2 1 9 6。
        # 这个方法会被 _execute_advanced_define 调用
        return i
    
    def _is_functional_array_access(self, tokens: List[Token], i: int) -> bool:
        """检查是否是函数式数组访问 '列表算j'"""
        # 格式：数组名 算 索引
        if i + 2 < len(tokens):
            if tokens[i].type == TokenType.IDENTIFIER:
                if tokens[i + 1].value == '算':
                    return True
        return False
    
    def _execute_functional_array_access(self, tokens: List[Token], i: int) -> int:
        """执行函数式数组访问 '列表算j'"""
        # 获取数组名
        array_name = tokens[i].value
        i += 1
        
        # 跳过 '算'
        if i < len(tokens) and tokens[i].value == '算':
            i += 1
        
        # 获取索引
        index = 0
        if i < len(tokens):
            if tokens[i].type == TokenType.NUMBER:
                index = int(float(tokens[i].value))
                i += 1
            elif tokens[i].type == TokenType.IDENTIFIER:
                var_name = tokens[i].value
                if var_name in self.variables:
                    index = int(float(self.variables[var_name]))
                i += 1
        
        # 访问数组元素
        if array_name in self.variables:
            arr = self.variables[array_name]
            if isinstance(arr, list) and 0 <= index < len(arr):
                # 将结果存储为特殊变量，供后续使用
                self.variables['__last_array_access__'] = arr[index]
        
        return i
    
    def _execute_advanced_define(self, tokens: List[Token], i: int) -> int:
        """执行高级定义语法"""
        i += 1  # 跳过 '定'
        
        if i >= len(tokens):
            return i
        
        # 获取名称
        name = tokens[i].value
        i += 1
        
        # 跳过 '是'
        if i < len(tokens) and tokens[i].type == TokenType.IS:
            i += 1
        
        # 检查定义类型
        if i < len(tokens):
            # 函数定义：定f是函参数：
            if tokens[i].value == '函':
                i += 1
                # 解析参数
                params = []
                while i < len(tokens) and tokens[i].type not in (TokenType.COLON, TokenType.NEWLINE):
                    if tokens[i].type == TokenType.IDENTIFIER:
                        params.append(tokens[i].value)
                    i += 1
                
                # 跳过冒号
                if i < len(tokens) and tokens[i].type == TokenType.COLON:
                    i += 1
                
                # 解析函数体
                body_tokens = []
                indent_level = tokens[i].indent if i < len(tokens) else 0
                
                while i < len(tokens):
                    if tokens[i].type == TokenType.NEWLINE:
                        i += 1
                        continue
                    
                    if hasattr(tokens[i], 'indent') and tokens[i].indent <= indent_level:
                        break
                    
                    body_tokens.append(tokens[i])
                    i += 1
                
                # 保存函数定义
                self.functions[name] = {
                    'params': params,
                    'body': body_tokens
                }
                
                return i
            
            # 典（对象）定义：定obj是典...
            elif tokens[i].value == '典':
                i += 1
                # 解析对象属性
                obj = {}
                while i < len(tokens) and tokens[i].type != TokenType.PERIOD:
                    if tokens[i].type == TokenType.IDENTIFIER:
                        prop_name = tokens[i].value
                        i += 1
                        # 跳过 '是'
                        if i < len(tokens) and tokens[i].type == TokenType.IS:
                            i += 1
                        # 获取值
                        if i < len(tokens):
                            if tokens[i].type == TokenType.NUMBER:
                                obj[prop_name] = float(tokens[i].value)
                            elif tokens[i].type == TokenType.STRING:
                                obj[prop_name] = tokens[i].value.strip('"\'')
                            elif tokens[i].type == TokenType.IDENTIFIER:
                                if tokens[i].value in ('真', '是'):
                                    obj[prop_name] = True
                                elif tokens[i].value in ('假', '否'):
                                    obj[prop_name] = False
                                else:
                                    obj[prop_name] = tokens[i].value
                            i += 1
                    else:
                        i += 1
                
                # 跳过句号
                if i < len(tokens) and tokens[i].type == TokenType.PERIOD:
                    i += 1
                
                self.variables[name] = obj
                return i
            
            # 数组定义：定arr是列5 3 8...
            elif tokens[i].value == '列':
                i += 1
                # 收集数组元素
                elements = []
                while i < len(tokens) and tokens[i].type not in (TokenType.PERIOD, TokenType.NEWLINE, TokenType.EOF):
                    if tokens[i].type == TokenType.NUMBER:
                        elements.append(float(tokens[i].value))
                    elif tokens[i].type == TokenType.STRING:
                        elements.append(tokens[i].value.strip('"\''))
                    elif tokens[i].type == TokenType.IDENTIFIER:
                        var_name = tokens[i].value
                        if var_name in self.variables:
                            elements.append(self.variables[var_name])
                    i += 1
                
                # 跳过句号
                if i < len(tokens) and tokens[i].type == TokenType.PERIOD:
                    i += 1
                
                self.variables[name] = elements
                return i
            
            # 变量定义：定x是值。
            else:
                # 获取值
                if tokens[i].type == TokenType.NUMBER:
                    value = float(tokens[i].value)
                    i += 1
                elif tokens[i].type == TokenType.STRING:
                    value = tokens[i].value.strip('"\'')
                    i += 1
                elif tokens[i].type == TokenType.IDENTIFIER:
                    value = tokens[i].value
                    i += 1
                else:
                    value = None
                    i += 1
                
                # 跳过句号
                if i < len(tokens) and tokens[i].type == TokenType.PERIOD:
                    i += 1
                
                self.variables[name] = value
                return i
        
        return i
