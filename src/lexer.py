"""
Лексический анализатор для транслятора Pascal → C++
Разбивает исходный код на последовательность токенов
"""

import re
from enum import Enum
from dataclasses import dataclass
from typing import List, Optional


class TokenType(Enum):
    # Ключевые слова
    PROGRAM = "program"
    VAR = "var"
    BEGIN = "begin"
    END = "end"
    IF = "if"
    THEN = "then"
    ELSE = "else"
    WHILE = "while"
    DO = "do"
    REPEAT = "repeat"
    UNTIL = "until"
    FOR = "for"
    TO = "to"
    DOWNTO = "downto"
    CASE = "case"
    OF = "of"
    PROCEDURE = "procedure"
    FUNCTION = "function"

    # Логические операции
    AND = "and"
    OR = "or"
    NOT = "not"
    XOR = "xor"
    DIV = "div"
    MOD = "mod"

    # Типы данных
    INTEGER = "integer"
    REAL = "real"
    BOOLEAN = "boolean"
    CHAR = "char"
    STRING = "string"
    ARRAY = "array"

    # Литералы
    TRUE = "true"
    FALSE = "false"

    # Встроенные функции
    READ = "read"
    READLN = "readln"
    WRITE = "write"
    WRITELN = "writeln"
    ABS = "abs"
    SQR = "sqr"
    SQRT = "sqrt"
    SIN = "sin"
    COS = "cos"
    LN = "ln"
    EXP = "exp"
    LENGTH = "length"

    # Идентификаторы и литералы
    IDENTIFIER = "IDENTIFIER"
    INT_LITERAL = "INT_LITERAL"
    REAL_LITERAL = "REAL_LITERAL"
    STRING_LITERAL = "STRING_LITERAL"
    CHAR_LITERAL = "CHAR_LITERAL"

    # Операторы
    PLUS = "+"
    MINUS = "-"
    MULTIPLY = "*"
    DIVIDE = "/"
    ASSIGN = ":="
    EQUAL = "="
    NOT_EQUAL = "<>"
    LESS = "<"
    LESS_EQUAL = "<="
    GREATER = ">"
    GREATER_EQUAL = ">="

    # Разделители
    DOT = "."
    COMMA = ","
    SEMICOLON = ";"
    COLON = ":"
    LPAREN = "("
    RPAREN = ")"
    LBRACKET = "["
    RBRACKET = "]"
    RANGE = ".."

    # Специальные
    EOF = "EOF"
    NEWLINE = "NEWLINE"


@dataclass
class Token:
    type: TokenType
    value: any
    line: int
    column: int

    def __repr__(self):
        return f"Token({self.type.name}, {self.value!r}, {self.line}:{self.column})"


class LexerError(Exception):
    def __init__(self, message: str, line: int, column: int):
        self.message = message
        self.line = line
        self.column = column
        super().__init__(f"Lexer error at {line}:{column}: {message}")


class Lexer:
    KEYWORDS = {
        "program",
        "var",
        "begin",
        "end",
        "if",
        "then",
        "else",
        "while",
        "do",
        "repeat",
        "until",
        "for",
        "to",
        "downto",
        "case",
        "of",
        "procedure",
        "function",
        "and",
        "or",
        "not",
        "xor",
        "div",
        "mod",
        "integer",
        "real",
        "boolean",
        "char",
        "string",
        "array",
        "true",
        "false",
        "read",
        "readln",
        "write",
        "writeln",
        "abs",
        "sqr",
        "sqrt",
        "sin",
        "cos",
        "ln",
        "exp",
        "length",
    }

    def __init__(self, source: str):
        self.source = source
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens: List[Token] = []

    def current_char(self) -> Optional[str]:
        if self.pos >= len(self.source):
            return None
        return self.source[self.pos]

    def peek_char(self, offset: int = 1) -> Optional[str]:
        pos = self.pos + offset
        if pos >= len(self.source):
            return None
        return self.source[pos]

    def advance(self):
        if self.pos < len(self.source):
            if self.source[self.pos] == "\n":
                self.line += 1
                self.column = 1
            else:
                self.column += 1
            self.pos += 1

    def skip_whitespace(self):
        while self.current_char() and self.current_char() in " \t\r\n":
            self.advance()

    def skip_comment(self):
        # Комментарии в Pascal: { } или (* *)
        if self.current_char() == "{":
            self.advance()
            while self.current_char() and self.current_char() != "}":
                self.advance()
            if self.current_char() == "}":
                self.advance()
            else:
                raise LexerError("Незавершенный комментарий", self.line, self.column)

        elif self.current_char() == "(" and self.peek_char() == "*":
            self.advance()
            self.advance()
            while True:
                if not self.current_char():
                    raise LexerError(
                        "Незавершенный комментарий", self.line, self.column
                    )
                if self.current_char() == "*" and self.peek_char() == ")":
                    self.advance()
                    self.advance()
                    break
                self.advance()

        elif self.current_char() == "/" and self.peek_char() == "/":
            while self.current_char() and self.current_char() != "\n":
                self.advance()

    def read_number(self) -> Token:
        start_line = self.line
        start_column = self.column
        num_str = ""

        while self.current_char() and self.current_char().isdigit():
            num_str += self.current_char()
            self.advance()

        # Проверка на вещественное число
        if (
            self.current_char() == "."
            and self.peek_char()
            and self.peek_char().isdigit()
        ):
            num_str += self.current_char()
            self.advance()

            while self.current_char() and self.current_char().isdigit():
                num_str += self.current_char()
                self.advance()

            # Экспоненциальная форма
            if self.current_char() and self.current_char().upper() == "E":
                num_str += self.current_char()
                self.advance()

                if self.current_char() and self.current_char() in "+-":
                    num_str += self.current_char()
                    self.advance()

                if not (self.current_char() and self.current_char().isdigit()):
                    raise LexerError(
                        "Неверный формат экспоненты", self.line, self.column
                    )

                while self.current_char() and self.current_char().isdigit():
                    num_str += self.current_char()
                    self.advance()

            return Token(
                TokenType.REAL_LITERAL, float(num_str), start_line, start_column
            )

        return Token(TokenType.INT_LITERAL, int(num_str), start_line, start_column)

    def read_string(self) -> Token:
        start_line = self.line
        start_column = self.column
        quote = self.current_char()
        self.advance()

        string_val = ""
        while self.current_char() and self.current_char() != quote:
            if self.current_char() == "\n":
                raise LexerError(
                    "Незавершенный строковый литерал", self.line, self.column
                )
            string_val += self.current_char()
            self.advance()

        if not self.current_char():
            raise LexerError("Незавершенный строковый литерал", self.line, self.column)

        self.advance()  # Закрывающая кавычка

        if quote == "'":
            if len(string_val) == 1:
                return Token(
                    TokenType.CHAR_LITERAL, string_val, start_line, start_column
                )
            return Token(TokenType.STRING_LITERAL, string_val, start_line, start_column)
        else:
            return Token(TokenType.STRING_LITERAL, string_val, start_line, start_column)

    def read_identifier(self) -> Token:
        start_line = self.line
        start_column = self.column
        ident = ""

        while self.current_char() and (
            self.current_char().isalnum() or self.current_char() == "_"
        ):
            ident += self.current_char()
            self.advance()

        ident_lower = ident.lower()

        if ident_lower in self.KEYWORDS:
            token_type = TokenType[ident_lower.upper()]
            return Token(token_type, ident_lower, start_line, start_column)

        return Token(TokenType.IDENTIFIER, ident, start_line, start_column)

    def tokenize(self) -> List[Token]:
        while self.current_char():
            self.skip_whitespace()

            if not self.current_char():
                break

            # Комментарии
            if (
                self.current_char() == "{"
                or (self.current_char() == "(" and self.peek_char() == "*")
                or (self.current_char() == "/" and self.peek_char() == "/")
            ):
                self.skip_comment()
                continue

            start_line = self.line
            start_column = self.column
            char = self.current_char()

            # Числа
            if char.isdigit():
                self.tokens.append(self.read_number())
                continue

            # Строки
            if char in ("'", '"'):
                self.tokens.append(self.read_string())
                continue

            # Идентификаторы и ключевые слова
            if char.isalpha() or char == "_":
                self.tokens.append(self.read_identifier())
                continue

            # Двухсимвольные операторы
            if char == ":" and self.peek_char() == "=":
                self.advance()
                self.advance()
                self.tokens.append(
                    Token(TokenType.ASSIGN, ":=", start_line, start_column)
                )
                continue

            if char == "<" and self.peek_char() == ">":
                self.advance()
                self.advance()
                self.tokens.append(
                    Token(TokenType.NOT_EQUAL, "<>", start_line, start_column)
                )
                continue

            if char == "<" and self.peek_char() == "=":
                self.advance()
                self.advance()
                self.tokens.append(
                    Token(TokenType.LESS_EQUAL, "<=", start_line, start_column)
                )
                continue

            if char == ">" and self.peek_char() == "=":
                self.advance()
                self.advance()
                self.tokens.append(
                    Token(TokenType.GREATER_EQUAL, ">=", start_line, start_column)
                )
                continue

            if char == "." and self.peek_char() == ".":
                self.advance()
                self.advance()
                self.tokens.append(
                    Token(TokenType.RANGE, "..", start_line, start_column)
                )
                continue

            # Односимвольные операторы и разделители
            single_char_tokens = {
                "+": TokenType.PLUS,
                "-": TokenType.MINUS,
                "*": TokenType.MULTIPLY,
                "/": TokenType.DIVIDE,
                "=": TokenType.EQUAL,
                "<": TokenType.LESS,
                ">": TokenType.GREATER,
                ".": TokenType.DOT,
                ",": TokenType.COMMA,
                ";": TokenType.SEMICOLON,
                ":": TokenType.COLON,
                "(": TokenType.LPAREN,
                ")": TokenType.RPAREN,
                "[": TokenType.LBRACKET,
                "]": TokenType.RBRACKET,
            }

            if char in single_char_tokens:
                self.advance()
                self.tokens.append(
                    Token(single_char_tokens[char], char, start_line, start_column)
                )
                continue

            raise LexerError(f"Недопустимый символ '{char}'", self.line, self.column)

        self.tokens.append(Token(TokenType.EOF, None, self.line, self.column))
        return self.tokens
