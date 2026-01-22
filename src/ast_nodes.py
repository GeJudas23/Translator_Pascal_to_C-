"""
Классы узлов абстрактного синтаксического дерева (AST)
Представляют структуру программы на Pascal
"""

from dataclasses import dataclass
from typing import List, Optional, Any


# Базовый класс для всех узлов AST
@dataclass
class ASTNode:
    pass


# Программа
@dataclass
class Program(ASTNode):
    name: str
    variables: List["VarDeclaration"]
    subprograms: List["Subprogram"]
    body: "CompoundStatement"


# Объявление переменной
@dataclass
class VarDeclaration(ASTNode):
    names: List[str]
    var_type: "Type"


# Типы данных
@dataclass
class Type(ASTNode):
    name: str


@dataclass
class ArrayType(Type):
    element_type: Type
    dimensions: List[tuple]  # [(start, end), ...]


# Подпрограммы
@dataclass
class Subprogram(ASTNode):
    pass


@dataclass
class Procedure(Subprogram):
    name: str
    parameters: List["Parameter"]
    variables: List[VarDeclaration]
    body: "CompoundStatement"


@dataclass
class Function(Subprogram):
    name: str
    parameters: List["Parameter"]
    return_type: Type
    variables: List[VarDeclaration]
    body: "CompoundStatement"


@dataclass
class Parameter(ASTNode):
    names: List[str]
    param_type: Type
    by_reference: bool = False


# Операторы
@dataclass
class Statement(ASTNode):
    pass


@dataclass
class CompoundStatement(Statement):
    statements: List[Statement]


@dataclass
class AssignmentStatement(Statement):
    variable: "Variable"
    expression: "Expression"


@dataclass
class IfStatement(Statement):
    condition: "Expression"
    then_statement: Statement
    else_statement: Optional[Statement] = None


@dataclass
class WhileStatement(Statement):
    condition: "Expression"
    body: Statement


@dataclass
class RepeatStatement(Statement):
    body: CompoundStatement
    condition: "Expression"


@dataclass
class ForStatement(Statement):
    variable: str
    start_value: "Expression"
    end_value: "Expression"
    body: Statement
    downto: bool = False


@dataclass
class CaseStatement(Statement):
    expression: "Expression"
    branches: List[tuple]  # [(values, statement), ...]
    else_statement: Optional[Statement] = None


@dataclass
class ProcedureCall(Statement):
    name: str
    arguments: List["Expression"]


# Выражения
@dataclass
class Expression(ASTNode):
    pass


@dataclass
class BinaryOp(Expression):
    left: Expression
    operator: str
    right: Expression


@dataclass
class UnaryOp(Expression):
    operator: str
    operand: Expression


@dataclass
class Variable(Expression):
    name: str
    indices: List[Expression] = None

    def __post_init__(self):
        if self.indices is None:
            self.indices = []


@dataclass
class IntegerLiteral(Expression):
    value: int


@dataclass
class RealLiteral(Expression):
    value: float


@dataclass
class StringLiteral(Expression):
    value: str


@dataclass
class CharLiteral(Expression):
    value: str


@dataclass
class BooleanLiteral(Expression):
    value: bool


@dataclass
class FunctionCall(Expression):
    name: str
    arguments: List[Expression]


# Пустой оператор
@dataclass
class EmptyStatement(Statement):
    pass
