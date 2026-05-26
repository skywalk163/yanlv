"""
言律语言代码生成器

将AST转换为目标语言代码（Python）
"""

from typing import List, Optional
from .ast_nodes import (
    ASTNode, Program, VariableDeclaration, FunctionDeclaration,
    IfStatement, WhileStatement, ForStatement, ReturnStatement,
    OutputStatement, BinaryExpression, UnaryExpression, CallExpression,
    MemberExpression, Identifier, Literal, ArrayLiteral, NodeType
)


class CodeGenerator:
    """代码生成器基类"""
    
    def __init__(self):
        """初始化代码生成器"""
        self.indent_level = 0
        self.indent_str = "    "  # 4空格缩进
    
    def generate(self, node: ASTNode) -> str:
        """
        生成代码
        
        Args:
            node: AST节点
            
        Returns:
            生成的代码字符串
        """
        if node.node_type == NodeType.PROGRAM:
            return self._generate_program(node)
        elif node.node_type == NodeType.VARIABLE_DECL:
            return self._generate_variable_declaration(node)
        elif node.node_type == NodeType.FUNCTION_DECL:
            return self._generate_function_declaration(node)
        elif node.node_type == NodeType.IF_STMT:
            return self._generate_if_statement(node)
        elif node.node_type == NodeType.WHILE_STMT:
            return self._generate_while_statement(node)
        elif node.node_type == NodeType.FOR_STMT:
            return self._generate_for_statement(node)
        elif node.node_type == NodeType.RETURN_STMT:
            return self._generate_return_statement(node)
        elif node.node_type == NodeType.OUTPUT_STMT:
            return self._generate_output_statement(node)
        elif node.node_type == NodeType.BINARY_EXPR:
            return self._generate_binary_expression(node)
        elif node.node_type == NodeType.UNARY_EXPR:
            return self._generate_unary_expression(node)
        elif node.node_type == NodeType.CALL_EXPR:
            return self._generate_call_expression(node)
        elif node.node_type == NodeType.MEMBER_EXPR:
            return self._generate_member_expression(node)
        elif node.node_type == NodeType.IDENTIFIER:
            return self._generate_identifier(node)
        elif node.node_type == NodeType.LITERAL:
            return self._generate_literal(node)
        elif node.node_type == NodeType.ARRAY_LITERAL:
            return self._generate_array_literal(node)
        else:
            return ""
    
    def _indent(self) -> str:
        """获取当前缩进"""
        return self.indent_str * self.indent_level
    
    def _generate_program(self, node: Program) -> str:
        """生成程序代码"""
        lines = []
        for stmt in node.statements:
            code = self.generate(stmt)
            if code:
                lines.append(code)
        return '\n'.join(lines)
    
    def _generate_variable_declaration(self, node: VariableDeclaration) -> str:
        """生成变量声明"""
        name = node.name
        if node.initializer:
            init_code = self.generate(node.initializer)
            return f"{self._indent()}{name} = {init_code}"
        else:
            return f"{self._indent()}{name} = None"
    
    def _generate_function_declaration(self, node: FunctionDeclaration) -> str:
        """生成函数声明"""
        name = node.name
        params = ', '.join(node.parameters)
        
        lines = [f"{self._indent()}def {name}({params}):"]
        
        self.indent_level += 1
        
        if node.body:
            for stmt in node.body:
                code = self.generate(stmt)
                if code:
                    lines.append(code)
        else:
            lines.append(f"{self._indent()}pass")
        
        self.indent_level -= 1
        
        return '\n'.join(lines)
    
    def _generate_if_statement(self, node: IfStatement) -> str:
        """生成条件语句"""
        condition_code = self.generate(node.condition)
        lines = [f"{self._indent()}if {condition_code}:"]
        
        self.indent_level += 1
        
        if node.consequent:
            for stmt in node.consequent:
                code = self.generate(stmt)
                if code:
                    lines.append(code)
        else:
            lines.append(f"{self._indent()}pass")
        
        self.indent_level -= 1
        
        if node.alternate:
            lines.append(f"{self._indent()}else:")
            self.indent_level += 1
            
            for stmt in node.alternate:
                code = self.generate(stmt)
                if code:
                    lines.append(code)
            
            self.indent_level -= 1
        
        return '\n'.join(lines)
    
    def _generate_while_statement(self, node: WhileStatement) -> str:
        """生成While循环"""
        condition_code = self.generate(node.condition)
        lines = [f"{self._indent()}while {condition_code}:"]
        
        self.indent_level += 1
        
        if node.body:
            for stmt in node.body:
                code = self.generate(stmt)
                if code:
                    lines.append(code)
        else:
            lines.append(f"{self._indent()}pass")
        
        self.indent_level -= 1
        
        return '\n'.join(lines)
    
    def _generate_for_statement(self, node: ForStatement) -> str:
        """生成For循环"""
        # 简化实现：假设是 range 循环
        lines = []
        
        if node.init and node.condition:
            # 假设 init 是变量声明，condition 是比较表达式
            var_name = node.init.name
            start = self.generate(node.init.initializer) if node.init.initializer else "0"
            
            # 简化：假设 condition 是 < 表达式
            end = "10"  # 默认值
            
            lines.append(f"{self._indent()}for {var_name} in range({start}, {end}):")
            
            self.indent_level += 1
            
            if node.body:
                for stmt in node.body:
                    code = self.generate(stmt)
                    if code:
                        lines.append(code)
            else:
                lines.append(f"{self._indent()}pass")
            
            self.indent_level -= 1
        
        return '\n'.join(lines)
    
    def _generate_return_statement(self, node: ReturnStatement) -> str:
        """生成返回语句"""
        if node.value:
            value_code = self.generate(node.value)
            return f"{self._indent()}return {value_code}"
        else:
            return f"{self._indent()}return"
    
    def _generate_output_statement(self, node: OutputStatement) -> str:
        """生成输出语句"""
        if node.value:
            value_code = self.generate(node.value)
            return f"{self._indent()}print({value_code})"
        else:
            return f"{self._indent()}print()"
    
    def _generate_binary_expression(self, node: BinaryExpression) -> str:
        """生成二元表达式"""
        left_code = self.generate(node.left)
        right_code = self.generate(node.right)
        op = self._map_operator(node.operator)
        return f"({left_code} {op} {right_code})"
    
    def _generate_unary_expression(self, node: UnaryExpression) -> str:
        """生成一元表达式"""
        operand_code = self.generate(node.operand)
        op = self._map_operator(node.operator)
        return f"({op}{operand_code})"
    
    def _generate_call_expression(self, node: CallExpression) -> str:
        """生成函数调用"""
        args = [self.generate(arg) for arg in node.arguments]
        args_str = ', '.join(args)
        return f"{node.callee}({args_str})"
    
    def _generate_member_expression(self, node: MemberExpression) -> str:
        """生成成员访问"""
        obj_code = self.generate(node.obj)
        prop_code = self.generate(node.prop)
        return f"{obj_code}[{prop_code}]"
    
    def _generate_identifier(self, node: Identifier) -> str:
        """生成标识符"""
        return node.name
    
    def _generate_literal(self, node: Literal) -> str:
        """生成字面量"""
        if node.literal_type == 'string':
            return f'"{node.value}"'
        elif node.literal_type == 'boolean':
            return 'True' if node.value else 'False'
        else:
            return str(node.value)
    
    def _generate_array_literal(self, node: ArrayLiteral) -> str:
        """生成数组字面量"""
        elements = [self.generate(elem) for elem in node.elements]
        return f"[{', '.join(elements)}]"
    
    def _map_operator(self, op: str) -> str:
        """映射运算符"""
        op_map = {
            '+': '+',
            '-': '-',
            '*': '*',
            '/': '/',
            '%': '%',
            '^': '**',
            '=': '==',
            '≠': '!=',
            '<': '<',
            '>': '>',
            '≤': '<=',
            '≥': '>=',
            '且': 'and',
            '或': 'or',
            '非': 'not',
            '大于': '>',
            '小于': '<',
            '等于': '==',
            '不等于': '!=',
            '大于等于': '>=',
            '小于等于': '<=',
        }
        return op_map.get(op, op)


class PythonCodeGenerator(CodeGenerator):
    """Python代码生成器"""
    pass


# ============================================================================
# 辅助函数
# ============================================================================

def create_python_generator() -> PythonCodeGenerator:
    """创建Python代码生成器"""
    return PythonCodeGenerator()


def generate_python_code(node: ASTNode) -> str:
    """生成Python代码"""
    generator = create_python_generator()
    return generator.generate(node)


# ============================================================================
# 导出
# ============================================================================

__all__ = [
    'CodeGenerator',
    'PythonCodeGenerator',
    'create_python_generator',
    'generate_python_code',
]
