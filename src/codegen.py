"""
Генератор кода C++
Преобразует AST в код на C++
"""

from src.ast_nodes import (
    Program,
    VarDeclaration,
    Type,
    ArrayType,
    Subprogram,
    Procedure,
    Function,
    Parameter,
    Statement,
    CompoundStatement,
    AssignmentStatement,
    IfStatement,
    WhileStatement,
    RepeatStatement,
    ForStatement,
    CaseStatement,
    ProcedureCall,
    EmptyStatement,
    Expression,
    BinaryOp,
    UnaryOp,
    Variable,
    IntegerLiteral,
    RealLiteral,
    StringLiteral,
    CharLiteral,
    BooleanLiteral,
    FunctionCall,
)
from typing import List


class CodeGenerator:
    def __init__(self):
        self.indent_level = 0
        self.output = []
        self.array_info = {}  # Информация о массивах для корректировки индексов

    def indent(self) -> str:
        return "    " * self.indent_level

    def emit(self, code: str):
        self.output.append(self.indent() + code)

    def emit_line(self, code: str = ""):
        if code:
            self.output.append(self.indent() + code)
        else:
            self.output.append("")

    def generate(self, program: Program) -> str:
        self.output = []

        # Заголовочные файлы
        self.emit_line("#include <iostream>")
        self.emit_line("#include <string>")
        self.emit_line("#include <cmath>")
        self.emit_line()
        self.emit_line("using namespace std;")
        self.emit_line()

        # Объявление подпрограмм
        for subprogram in program.subprograms:
            self.generate_subprogram_declaration(subprogram)
            self.emit_line()

        # Главная функция
        self.emit_line("int main() {")
        self.indent_level += 1

        # Глобальные переменные
        for var_decl in program.variables:
            self.generate_var_declaration(var_decl)

        if program.variables:
            self.emit_line()

        # Тело программы
        self.generate_compound_statement(program.body, skip_braces=True)

        self.emit_line("return 0;")
        self.indent_level -= 1
        self.emit_line("}")
        self.emit_line()

        # Реализация подпрограмм
        for subprogram in program.subprograms:
            self.generate_subprogram_implementation(subprogram)
            self.emit_line()

        return "\n".join(self.output)

    def generate_subprogram_declaration(self, subprogram: Subprogram):
        if isinstance(subprogram, Procedure):
            params = self.generate_parameters(subprogram.parameters)
            self.emit_line(f"void {subprogram.name}({params});")
        elif isinstance(subprogram, Function):
            return_type = self.convert_type(subprogram.return_type)
            params = self.generate_parameters(subprogram.parameters)
            self.emit_line(f"{return_type} {subprogram.name}({params});")

    def generate_subprogram_implementation(self, subprogram: Subprogram):
        if isinstance(subprogram, Procedure):
            params = self.generate_parameters(subprogram.parameters)
            self.emit_line(f"void {subprogram.name}({params}) {{")
            self.indent_level += 1

            # Регистрируем информацию об массивах-параметрах
            for param in subprogram.parameters:
                if isinstance(param.param_type, ArrayType):
                    for name in param.names:
                        self.array_info[name] = param.param_type.dimensions

            for var_decl in subprogram.variables:
                self.generate_var_declaration(var_decl)

            if subprogram.variables:
                self.emit_line()

            self.generate_compound_statement(subprogram.body, skip_braces=True)

            self.indent_level -= 1
            self.emit_line("}")

        elif isinstance(subprogram, Function):
            return_type = self.convert_type(subprogram.return_type)
            params = self.generate_parameters(subprogram.parameters)
            self.emit_line(f"{return_type} {subprogram.name}({params}) {{")
            self.indent_level += 1

            # Регистрируем информацию об массивах-параметрах
            for param in subprogram.parameters:
                if isinstance(param.param_type, ArrayType):
                    for name in param.names:
                        self.array_info[name] = param.param_type.dimensions

            # Переменная для возврата значения
            self.emit_line(f"{return_type} {subprogram.name}_result;")

            for var_decl in subprogram.variables:
                self.generate_var_declaration(var_decl)

            self.emit_line()

            self.generate_compound_statement(
                subprogram.body, skip_braces=True, function_name=subprogram.name
            )

            self.emit_line(f"return {subprogram.name}_result;")

            self.indent_level -= 1
            self.emit_line("}")

    def generate_parameters(self, parameters: List[Parameter]) -> str:
        params = []
        for param in parameters:
            # Обработка массивов отдельно
            if isinstance(param.param_type, ArrayType):
                element_type = self.convert_type(param.param_type.element_type)
                for name in param.names:
                    params.append(f"{element_type} {name}[]")
            else:
                param_type = self.convert_type(param.param_type)
                for name in param.names:
                    if param.by_reference:
                        params.append(f"{param_type}& {name}")
                    else:
                        params.append(f"{param_type} {name}")
        return ", ".join(params)

    def generate_var_declaration(self, var_decl: VarDeclaration):
        cpp_type = self.convert_type(var_decl.var_type)

        if isinstance(var_decl.var_type, ArrayType):
            for name in var_decl.names:
                self.array_info[name] = var_decl.var_type.dimensions
                self.emit_line(self.generate_array_declaration(name, var_decl.var_type))
        else:
            for name in var_decl.names:
                self.emit_line(f"{cpp_type} {name};")

    def generate_array_declaration(self, name: str, array_type: ArrayType) -> str:
        sizes = []
        for start_expr, end_expr in array_type.dimensions:
            # Вычисляем размер
            if isinstance(start_expr, IntegerLiteral) and isinstance(
                end_expr, IntegerLiteral):
                size = end_expr.value - start_expr.value + 1
                sizes.append(str(size))
            else:
                sizes.append("100")  # Заглушка для динамических размеров

        element_type = self.convert_type(array_type.element_type)
        dimensions = "".join(f"[{size}]" for size in sizes)
        return f"{element_type} {name}{dimensions};"

    def convert_type(self, pascal_type: Type) -> str:
        type_map = {
            "integer": "int",
            "real": "double",
            "boolean": "bool",
            "char": "char",
            "string": "string",
        }

        if isinstance(pascal_type, ArrayType):
            return self.convert_type(pascal_type.element_type)

        return type_map.get(pascal_type.name, pascal_type.name)

    def generate_compound_statement(
        self, stmt: CompoundStatement, skip_braces=False, function_name=None
    ):
        if not skip_braces:
            self.emit_line("{")
            self.indent_level += 1

        for statement in stmt.statements:
            self.generate_statement(statement, function_name)

        if not skip_braces:
            self.indent_level -= 1
            self.emit_line("}")

    def generate_statement(self, stmt: Statement, function_name=None):
        if isinstance(stmt, CompoundStatement):
            self.generate_compound_statement(stmt, function_name=function_name)

        elif isinstance(stmt, AssignmentStatement):
            var_code = self.generate_variable(stmt.variable)
            expr_code = self.generate_expression(stmt.expression)

            # Проверка на присваивание результата функции
            if function_name and stmt.variable.name == function_name:
                self.emit_line(f"{function_name}_result = {expr_code};")
            else:
                self.emit_line(f"{var_code} = {expr_code};")

        elif isinstance(stmt, IfStatement):
            condition = self.generate_expression(stmt.condition)
            self.emit_line(f"if ({condition}) {{")
            self.indent_level += 1
            self.generate_statement(stmt.then_statement, function_name)
            self.indent_level -= 1

            if stmt.else_statement:
                self.emit_line("} else {")
                self.indent_level += 1
                self.generate_statement(stmt.else_statement, function_name)
                self.indent_level -= 1

            self.emit_line("}")

        elif isinstance(stmt, WhileStatement):
            condition = self.generate_expression(stmt.condition)
            self.emit_line(f"while ({condition}) {{")
            self.indent_level += 1
            self.generate_statement(stmt.body, function_name)
            self.indent_level -= 1
            self.emit_line("}")

        elif isinstance(stmt, RepeatStatement):
            condition = self.generate_expression(stmt.condition)
            self.emit_line("do {")
            self.indent_level += 1
            self.generate_compound_statement(
                stmt.body, skip_braces=True, function_name=function_name
            )
            self.indent_level -= 1
            self.emit_line(f"}} while (!({condition}));")

        elif isinstance(stmt, ForStatement):
            start = self.generate_expression(stmt.start_value)
            end = self.generate_expression(stmt.end_value)

            if stmt.downto:
                self.emit_line(
                    f"for (int {stmt.variable} = {start}; {stmt.variable} >= {end}; {stmt.variable}--) {{"
                )
            else:
                self.emit_line(
                    f"for (int {stmt.variable} = {start}; {stmt.variable} <= {end}; {stmt.variable}++) {{"
                )

            self.indent_level += 1
            self.generate_statement(stmt.body, function_name)
            self.indent_level -= 1
            self.emit_line("}")

        elif isinstance(stmt, CaseStatement):
            expr = self.generate_expression(stmt.expression)
            self.emit_line(f"switch ({expr}) {{")
            self.indent_level += 1

            for values, branch_stmt in stmt.branches:
                for value in values:
                    value_code = self.generate_expression(value)
                    self.emit_line(f"case {value_code}:")

                self.indent_level += 1
                self.generate_statement(branch_stmt, function_name)
                self.emit_line("break;")
                self.indent_level -= 1

            if stmt.else_statement:
                self.emit_line("default:")
                self.indent_level += 1
                self.generate_statement(stmt.else_statement, function_name)
                self.indent_level -= 1

            self.indent_level -= 1
            self.emit_line("}")

        elif isinstance(stmt, ProcedureCall):
            self.generate_procedure_call(stmt)

        elif isinstance(stmt, EmptyStatement):
            pass

    def generate_procedure_call(self, call: ProcedureCall):
        # Стандартные процедуры
        if call.name in ("write", "writeln"):
            args = " << ".join(self.generate_expression(arg) for arg in call.arguments)
            if call.name == "writeln":
                if args:
                    self.emit_line(f"cout << {args} << endl;")
                else:
                    self.emit_line(f"cout << endl;")
            else:
                if args:
                    self.emit_line(f"cout << {args};")

        elif call.name in ("read", "readln"):
            args = " >> ".join(self.generate_expression(arg) for arg in call.arguments)
            self.emit_line(f"cin >> {args};")

        elif call.name == "break":
            self.emit_line("break;")

        elif call.name == "continue":
            self.emit_line("continue;")

        else:
            args = ", ".join(self.generate_expression(arg) for arg in call.arguments)
            self.emit_line(f"{call.name}({args});")

    def generate_expression(self, expr: Expression) -> str:
        if isinstance(expr, BinaryOp):
            left = self.generate_expression(expr.left)
            right = self.generate_expression(expr.right)

            op_map = {
                "div": "/",
                "mod": "%",
                "and": "&&",
                "or": "||",
                "xor": "^",
                "<>": "!=",
            }

            operator = op_map.get(expr.operator, expr.operator)
            return f"({left} {operator} {right})"

        elif isinstance(expr, UnaryOp):
            operand = self.generate_expression(expr.operand)

            op_map = {
                "not": "!",
            }

            operator = op_map.get(expr.operator, expr.operator)
            return f"{operator}({operand})"

        elif isinstance(expr, Variable):
            return self.generate_variable(expr)

        elif isinstance(expr, IntegerLiteral):
            return str(expr.value)

        elif isinstance(expr, RealLiteral):
            return str(expr.value)

        elif isinstance(expr, StringLiteral):
            return f'"{expr.value}"'

        elif isinstance(expr, CharLiteral):
            return f"'{expr.value}'"

        elif isinstance(expr, BooleanLiteral):
            return "true" if expr.value else "false"

        elif isinstance(expr, FunctionCall):
            return self.generate_function_call(expr)

        return ""

    def generate_variable(self, var: Variable) -> str:
        if not var.indices:
            return var.name

        # Корректировка индексов для массивов
        indices_code = []
        if var.name in self.array_info:
            dimensions = self.array_info[var.name]
            for i, index_expr in enumerate(var.indices):
                index_code = self.generate_expression(index_expr)
                if i < len(dimensions):
                    start_expr, _ = dimensions[i]
                    if isinstance(start_expr, IntegerLiteral) and start_expr.value != 0:
                        index_code = f"({index_code} - {start_expr.value})"
                indices_code.append(index_code)
        else:
            indices_code = [self.generate_expression(idx) for idx in var.indices]

        indices_str = "][".join(indices_code)
        return f"{var.name}[{indices_str}]"

    def generate_function_call(self, call: FunctionCall) -> str:
        # Стандартные функции
        func_map = {
            "abs": "abs",
            "sqr": lambda x: f"({x} * {x})",
            "sqrt": "sqrt",
            "sin": "sin",
            "cos": "cos",
            "ln": "log",
            "exp": "exp",
            "length": lambda x: f"{x}.length()",
        }

        if call.name in func_map:
            args = [self.generate_expression(arg) for arg in call.arguments]

            if callable(func_map[call.name]):
                return func_map[call.name](args[0] if args else "")
            else:
                return f"{func_map[call.name]}({', '.join(args)})"

        # Пользовательские функции
        args = ", ".join(self.generate_expression(arg) for arg in call.arguments)
        return f"{call.name}({args})"
