"""
言律语言JavaScript代码生成器

将AST转换为JavaScript代码
"""

from typing import List, Optional
from .ast_nodes import (
    ASTNode, Program, VariableDeclaration, FunctionDeclaration,
    IfStatement, WhileStatement, ForStatement, ReturnStatement,
    OutputStatement, BinaryExpression, UnaryExpression, CallExpression,
    MemberExpression, Identifier, Literal, ArrayLiteral
)


class JavaScriptCodeGenerator:
    """JavaScript代码生成器"""
    
    def __init__(self):
        """初始化生成器"""
        self.indent_level = 0
        self.indent_char = "  "  # 2空格缩进
    
    def generate(self, node: ASTNode) -> str:
        """
        生成JavaScript代码
        
        Args:
            node: AST节点
            
        Returns:
            JavaScript代码字符串
        """
        if isinstance(node, Program):
            return self._generate_program(node)
        elif isinstance(node, VariableDeclaration):
            return self._generate_variable_declaration(node)
        elif isinstance(node, FunctionDeclaration):
            return self._generate_function_declaration(node)
        elif isinstance(node, IfStatement):
            return self._generate_if_statement(node)
        elif isinstance(node, WhileStatement):
            return self._generate_while_statement(node)
        elif isinstance(node, ForStatement):
            return self._generate_for_statement(node)
        elif isinstance(node, ReturnStatement):
            return self._generate_return_statement(node)
        elif isinstance(node, OutputStatement):
            return self._generate_output_statement(node)
        elif isinstance(node, BinaryExpression):
            return self._generate_binary_expression(node)
        elif isinstance(node, UnaryExpression):
            return self._generate_unary_expression(node)
        elif isinstance(node, CallExpression):
            return self._generate_call_expression(node)
        elif isinstance(node, MemberExpression):
            return self._generate_member_expression(node)
        elif isinstance(node, Identifier):
            return self._generate_identifier(node)
        elif isinstance(node, Literal):
            return self._generate_literal(node)
        elif isinstance(node, ArrayLiteral):
            return self._generate_array_literal(node)
        else:
            return ""
    
    def _indent(self) -> str:
        """获取当前缩进"""
        return self.indent_char * self.indent_level
    
    def _generate_program(self, node: Program) -> str:
        """生成程序"""
        lines = []
        for stmt in node.statements:
            code = self.generate(stmt)
            if code:
                lines.append(code)
        return '\n'.join(lines)
    
    def _generate_variable_declaration(self, node: VariableDeclaration) -> str:
        """生成变量声明"""
        name = node.name
        initializer = self.generate(node.initializer) if node.initializer else "undefined"
        return f"{self._indent()}let {name} = {initializer};"
    
    def _generate_function_declaration(self, node: FunctionDeclaration) -> str:
        """生成函数声明"""
        name = node.name
        params = ', '.join(node.parameters)
        
        lines = [f"{self._indent()}function {name}({params}) {{"]
        
        self.indent_level += 1
        
        for stmt in node.body:
            code = self.generate(stmt)
            if code:
                lines.append(code)
        
        self.indent_level -= 1
        
        lines.append(f"{self._indent()}}}")
        
        return '\n'.join(lines)
    
    def _generate_if_statement(self, node: IfStatement) -> str:
        """生成条件语句"""
        condition = self.generate(node.condition)
        
        lines = [f"{self._indent()}if ({condition}) {{"]
        
        self.indent_level += 1
        
        for stmt in node.consequent:
            code = self.generate(stmt)
            if code:
                lines.append(code)
        
        self.indent_level -= 1
        
        if node.alternate:
            lines.append(f"{self._indent()}}} else {{")
            
            self.indent_level += 1
            
            for stmt in node.alternate:
                code = self.generate(stmt)
                if code:
                    lines.append(code)
            
            self.indent_level -= 1
        
        lines.append(f"{self._indent()}}}")
        
        return '\n'.join(lines)
    
    def _generate_while_statement(self, node: WhileStatement) -> str:
        """生成While循环"""
        condition = self.generate(node.condition)
        
        lines = [f"{self._indent()}while ({condition}) {{"]
        
        self.indent_level += 1
        
        for stmt in node.body:
            code = self.generate(stmt)
            if code:
                lines.append(code)
        
        self.indent_level -= 1
        
        lines.append(f"{self._indent()}}}")
        
        return '\n'.join(lines)
    
    def _generate_for_statement(self, node: ForStatement) -> str:
        """生成For循环"""
        init = self.generate(node.init) if node.init else ""
        condition = self.generate(node.condition) if node.condition else ""
        update = self.generate(node.update) if node.update else ""
        
        lines = [f"{self._indent()}for ({init}; {condition}; {update}) {{"]
        
        self.indent_level += 1
        
        for stmt in node.body:
            code = self.generate(stmt)
            if code:
                lines.append(code)
        
        self.indent_level -= 1
        
        lines.append(f"{self._indent()}}}")
        
        return '\n'.join(lines)
    
    def _generate_return_statement(self, node: ReturnStatement) -> str:
        """生成返回语句"""
        if node.value:
            value = self.generate(node.value)
            return f"{self._indent()}return {value};"
        return f"{self._indent()}return;"
    
    def _generate_output_statement(self, node: OutputStatement) -> str:
        """生成输出语句"""
        value = self.generate(node.value)
        return f"{self._indent()}console.log({value});"
    
    def _generate_binary_expression(self, node: BinaryExpression) -> str:
        """生成二元表达式"""
        left = self.generate(node.left)
        right = self.generate(node.right)
        operator = self._convert_operator(node.operator)
        return f"({left} {operator} {right})"
    
    def _generate_unary_expression(self, node: UnaryExpression) -> str:
        """生成一元表达式"""
        right = self.generate(node.right)
        operator = self._convert_operator(node.operator)
        return f"({operator}{right})"
    
    def _generate_call_expression(self, node: CallExpression) -> str:
        """生成函数调用"""
        args = ', '.join([self.generate(arg) for arg in node.arguments])
        return f"{node.callee}({args})"
    
    def _generate_member_expression(self, node: MemberExpression) -> str:
        """生成成员表达式"""
        obj = self.generate(node.object)
        prop = self.generate(node.property)
        return f"{obj}[{prop}]"
    
    def _generate_identifier(self, node: Identifier) -> str:
        """生成标识符"""
        return node.name
    
    def _generate_literal(self, node: Literal) -> str:
        """生成字面量"""
        if node.literal_type == 'string':
            return f'"{node.value}"'
        elif node.literal_type == 'boolean':
            return 'true' if node.value else 'false'
        else:
            return str(node.value)
    
    def _generate_array_literal(self, node: ArrayLiteral) -> str:
        """生成数组字面量"""
        elements = ', '.join([self.generate(elem) for elem in node.elements])
        return f"[{elements}]"
    
    def _convert_operator(self, operator: str) -> str:
        """转换运算符"""
        operator_map = {
            '+': '+',
            '-': '-',
            '*': '*',
            '/': '/',
            '%': '%',
            '^': '**',
            '==': '===',
            '!=': '!==',
            '<': '<',
            '>': '>',
            '<=': '<=',
            '>=': '>=',
            '且': '&&',
            '或': '||',
            '非': '!',
        }
        return operator_map.get(operator, operator)


# ============================================================================
# 辅助函数
# ============================================================================

def generate_javascript(node: ASTNode) -> str:
    """生成JavaScript代码"""
    generator = JavaScriptCodeGenerator()
    return generator.generate(node)


# ============================================================================
# 导出
# ============================================================================

__all__ = [
    'JavaScriptCodeGenerator',
    'generate_javascript',
]
