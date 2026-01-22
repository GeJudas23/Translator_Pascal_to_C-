"""
Синтаксический анализатор
Строит AST дерево из последовательности токенов
"""

from typing import List, Optional
from src.lexer import Token, TokenType, Lexer
from src.ast_nodes import *


class ParserError(Exception):
    def __init__(self, message: str, token: Token):
        self.message = message
        self.token = token
        super().__init__(f"Parser error at {token.line}:{token.column}: {message}")


class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0

    def current_token(self) -> Token:
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return self.tokens[-1]

    def peek_token(self, offset: int = 1) -> Token:
        pos = self.pos + offset
        if pos < len(self.tokens):
            return self.tokens[pos]
        return self.tokens[-1]

    def advance(self):
        if self.pos < len(self.tokens) - 1:
            self.pos += 1

    def expect(self, token_type: TokenType) -> Token:
        token = self.current_token()
        if token.type != token_type:
            raise ParserError(
                f"Ожидается {token_type.name}, получено {token.type.name}", token
            )
        self.advance()
        return token

    def match(self, *token_types: TokenType) -> bool:
        return self.current_token().type in token_types

    def parse(self) -> Program:
        return self.parse_program()

    def parse_program(self) -> Program:
        self.expect(TokenType.PROGRAM)
        name_token = self.expect(TokenType.IDENTIFIER)
        name = name_token.value
        self.expect(TokenType.SEMICOLON)

        variables = []
        subprograms = []

        # Раздел переменных
        if self.match(TokenType.VAR):
            variables = self.parse_var_section()

        # Раздел подпрограмм
        while self.match(TokenType.PROCEDURE, TokenType.FUNCTION):
            subprograms.append(self.parse_subprogram())

        # Основной блок
        body = self.parse_compound_statement()
        self.expect(TokenType.DOT)

        return Program(name, variables, subprograms, body)

    def parse_var_section(self) -> List[VarDeclaration]:
        self.expect(TokenType.VAR)
        variables = []

        while self.match(TokenType.IDENTIFIER):
            variables.append(self.parse_var_declaration())
            self.expect(TokenType.SEMICOLON)

        return variables

    def parse_var_declaration(self) -> VarDeclaration:
        names = [self.expect(TokenType.IDENTIFIER).value]

        while self.match(TokenType.COMMA):
            self.advance()
            names.append(self.expect(TokenType.IDENTIFIER).value)

        self.expect(TokenType.COLON)
        var_type = self.parse_type()

        return VarDeclaration(names, var_type)

    def parse_type(self) -> Type:
        if self.match(TokenType.ARRAY):
            return self.parse_array_type()

        if self.match(
            TokenType.INTEGER,
            TokenType.REAL,
            TokenType.BOOLEAN,
            TokenType.CHAR,
            TokenType.STRING,
        ):
            type_name = self.current_token().value
            self.advance()
            return Type(type_name)

        raise ParserError("Ожидается тип данных", self.current_token())

    def parse_array_type(self) -> ArrayType:
        self.expect(TokenType.ARRAY)
        self.expect(TokenType.LBRACKET)

        dimensions = []
        dimensions.append(self.parse_range())

        while self.match(TokenType.COMMA):
            self.advance()
            dimensions.append(self.parse_range())

        self.expect(TokenType.RBRACKET)
        self.expect(TokenType.OF)

        element_type = self.parse_type()

        array_type = ArrayType("array", element_type, dimensions)
        return array_type

    def parse_range(self) -> tuple:
        start = self.parse_expression()
        self.expect(TokenType.RANGE)
        end = self.parse_expression()
        return (start, end)

    def parse_subprogram(self) -> Subprogram:
        if self.match(TokenType.PROCEDURE):
            return self.parse_procedure()
        elif self.match(TokenType.FUNCTION):
            return self.parse_function()
        raise ParserError(
            "Ожидается объявление процедуры или функции", self.current_token()
        )

    def parse_procedure(self) -> Procedure:
        self.expect(TokenType.PROCEDURE)
        name = self.expect(TokenType.IDENTIFIER).value

        parameters = []
        if self.match(TokenType.LPAREN):
            parameters = self.parse_parameters()

        self.expect(TokenType.SEMICOLON)

        variables = []
        if self.match(TokenType.VAR):
            variables = self.parse_var_section()

        body = self.parse_compound_statement()
        self.expect(TokenType.SEMICOLON)

        return Procedure(name, parameters, variables, body)

    def parse_function(self) -> Function:
        self.expect(TokenType.FUNCTION)
        name = self.expect(TokenType.IDENTIFIER).value

        parameters = []
        if self.match(TokenType.LPAREN):
            parameters = self.parse_parameters()

        self.expect(TokenType.COLON)
        return_type = self.parse_type()
        self.expect(TokenType.SEMICOLON)

        variables = []
        if self.match(TokenType.VAR):
            variables = self.parse_var_section()

        body = self.parse_compound_statement()
        self.expect(TokenType.SEMICOLON)

        return Function(name, parameters, return_type, variables, body)

    def parse_parameters(self) -> List[Parameter]:
        self.expect(TokenType.LPAREN)
        parameters = []

        if not self.match(TokenType.RPAREN):
            parameters.append(self.parse_parameter())

            while self.match(TokenType.SEMICOLON):
                self.advance()
                parameters.append(self.parse_parameter())

        self.expect(TokenType.RPAREN)
        return parameters

    def parse_parameter(self) -> Parameter:
        by_reference = False
        if self.match(TokenType.VAR):
            by_reference = True
            self.advance()

        names = [self.expect(TokenType.IDENTIFIER).value]

        while self.match(TokenType.COMMA):
            self.advance()
            names.append(self.expect(TokenType.IDENTIFIER).value)

        self.expect(TokenType.COLON)
        param_type = self.parse_type()

        return Parameter(names, param_type, by_reference)

    def parse_compound_statement(self) -> CompoundStatement:
        self.expect(TokenType.BEGIN)
        statements = []

        if not self.match(TokenType.END):
            statements.append(self.parse_statement())

            while self.match(TokenType.SEMICOLON):
                self.advance()
                if not self.match(TokenType.END):
                    statements.append(self.parse_statement())

        self.expect(TokenType.END)
        return CompoundStatement(statements)

    def parse_statement(self) -> Statement:
        if self.match(TokenType.BEGIN):
            return self.parse_compound_statement()

        if self.match(TokenType.IF):
            return self.parse_if_statement()

        if self.match(TokenType.WHILE):
            return self.parse_while_statement()

        if self.match(TokenType.REPEAT):
            return self.parse_repeat_statement()

        if self.match(TokenType.FOR):
            return self.parse_for_statement()

        if self.match(TokenType.CASE):
            return self.parse_case_statement()

        if self.match(TokenType.IDENTIFIER):
            return self.parse_assignment_or_call()

        return EmptyStatement()

    def parse_if_statement(self) -> IfStatement:
        self.expect(TokenType.IF)
        condition = self.parse_expression()
        self.expect(TokenType.THEN)
        then_stmt = self.parse_statement()

        else_stmt = None
        if self.match(TokenType.ELSE):
            self.advance()
            else_stmt = self.parse_statement()

        return IfStatement(condition, then_stmt, else_stmt)

    def parse_while_statement(self) -> WhileStatement:
        self.expect(TokenType.WHILE)
        condition = self.parse_expression()
        self.expect(TokenType.DO)
        body = self.parse_statement()

        return WhileStatement(condition, body)

    def parse_repeat_statement(self) -> RepeatStatement:
        self.expect(TokenType.REPEAT)
        statements = []

        statements.append(self.parse_statement())
        while self.match(TokenType.SEMICOLON):
            self.advance()
            if not self.match(TokenType.UNTIL):
                statements.append(self.parse_statement())

        self.expect(TokenType.UNTIL)
        condition = self.parse_expression()

        return RepeatStatement(CompoundStatement(statements), condition)

    def parse_for_statement(self) -> ForStatement:
        self.expect(TokenType.FOR)
        variable = self.expect(TokenType.IDENTIFIER).value
        self.expect(TokenType.ASSIGN)
        start_value = self.parse_expression()

        downto = False
        if self.match(TokenType.DOWNTO):
            downto = True
            self.advance()
        else:
            self.expect(TokenType.TO)

        end_value = self.parse_expression()
        self.expect(TokenType.DO)
        body = self.parse_statement()

        return ForStatement(variable, start_value, end_value, body, downto)

    def parse_case_statement(self) -> CaseStatement:
        self.expect(TokenType.CASE)
        expression = self.parse_expression()
        self.expect(TokenType.OF)

        branches = []
        branches.append(self.parse_case_branch())

        while self.match(TokenType.SEMICOLON):
            self.advance()
            if not self.match(TokenType.END, TokenType.ELSE):
                branches.append(self.parse_case_branch())

        else_stmt = None
        if self.match(TokenType.ELSE):
            self.advance()
            else_stmt = self.parse_statement()

        self.expect(TokenType.END)
        return CaseStatement(expression, branches, else_stmt)

    def parse_case_branch(self) -> tuple:
        values = [self.parse_expression()]

        while self.match(TokenType.COMMA):
            self.advance()
            values.append(self.parse_expression())

        self.expect(TokenType.COLON)
        statement = self.parse_statement()

        return (values, statement)

    def parse_assignment_or_call(self) -> Statement:
        name = self.expect(TokenType.IDENTIFIER).value

        # Проверка на индексированную переменную
        indices = []
        if self.match(TokenType.LBRACKET):
            self.advance()
            indices.append(self.parse_expression())

            while self.match(TokenType.COMMA):
                self.advance()
                indices.append(self.parse_expression())

            self.expect(TokenType.RBRACKET)

        if self.match(TokenType.ASSIGN):
            self.advance()
            expression = self.parse_expression()
            return AssignmentStatement(Variable(name, indices), expression)

        # Вызов процедуры
        arguments = []
        if self.match(TokenType.LPAREN):
            self.advance()
            if not self.match(TokenType.RPAREN):
                arguments.append(self.parse_expression())

                while self.match(TokenType.COMMA):
                    self.advance()
                    arguments.append(self.parse_expression())

            self.expect(TokenType.RPAREN)

        return ProcedureCall(name, arguments)

    def parse_expression(self) -> Expression:
        left = self.parse_simple_expression()

        if self.match(
            TokenType.EQUAL,
            TokenType.NOT_EQUAL,
            TokenType.LESS,
            TokenType.LESS_EQUAL,
            TokenType.GREATER,
            TokenType.GREATER_EQUAL,
        ):
            operator = self.current_token().value
            self.advance()
            right = self.parse_simple_expression()
            return BinaryOp(left, operator, right)

        return left

    def parse_simple_expression(self) -> Expression:
        sign = None
        if self.match(TokenType.PLUS, TokenType.MINUS):
            sign = self.current_token().value
            self.advance()

        left = self.parse_term()

        if sign:
            left = UnaryOp(sign, left)

        while self.match(TokenType.PLUS, TokenType.MINUS, TokenType.OR, TokenType.XOR):
            operator = self.current_token().value
            self.advance()
            right = self.parse_term()
            left = BinaryOp(left, operator, right)

        return left

    def parse_term(self) -> Expression:
        left = self.parse_factor()

        while self.match(
            TokenType.MULTIPLY,
            TokenType.DIVIDE,
            TokenType.DIV,
            TokenType.MOD,
            TokenType.AND,
        ):
            operator = self.current_token().value
            self.advance()
            right = self.parse_factor()
            left = BinaryOp(left, operator, right)

        return left

    def parse_factor(self) -> Expression:
        if self.match(TokenType.NOT):
            self.advance()
            return UnaryOp("not", self.parse_factor())

        if self.match(TokenType.LPAREN):
            self.advance()
            expr = self.parse_expression()
            self.expect(TokenType.RPAREN)
            return expr

        if self.match(TokenType.INT_LITERAL):
            value = self.current_token().value
            self.advance()
            return IntegerLiteral(value)

        if self.match(TokenType.REAL_LITERAL):
            value = self.current_token().value
            self.advance()
            return RealLiteral(value)

        if self.match(TokenType.STRING_LITERAL):
            value = self.current_token().value
            self.advance()
            return StringLiteral(value)

        if self.match(TokenType.CHAR_LITERAL):
            value = self.current_token().value
            self.advance()
            return CharLiteral(value)

        if self.match(TokenType.TRUE):
            self.advance()
            return BooleanLiteral(True)

        if self.match(TokenType.FALSE):
            self.advance()
            return BooleanLiteral(False)

        if self.match(TokenType.IDENTIFIER):
            name = self.current_token().value
            self.advance()

            # Индексация массива
            indices = []
            if self.match(TokenType.LBRACKET):
                self.advance()
                indices.append(self.parse_expression())

                while self.match(TokenType.COMMA):
                    self.advance()
                    indices.append(self.parse_expression())

                self.expect(TokenType.RBRACKET)
                return Variable(name, indices)

            # Вызов функции
            if self.match(TokenType.LPAREN):
                self.advance()
                arguments = []

                if not self.match(TokenType.RPAREN):
                    arguments.append(self.parse_expression())

                    while self.match(TokenType.COMMA):
                        self.advance()
                        arguments.append(self.parse_expression())

                self.expect(TokenType.RPAREN)
                return FunctionCall(name, arguments)

            return Variable(name)

        raise ParserError("Ожидается выражение", self.current_token())
