from enum import Enum


class TokenList(Enum):
    any = "Any"
    reserved = "Reserved Word"
    predefined = "Predefined Word"
    identifier = "Identifier"
    integer = "Integer"
    integer_16 = "Integer (format 16)"
    integer_8 = "Integer (format 8)"
    integer_2 = "Integer (format 2)"
    real = "Real"
    real_e = "Real (Float Point): e"
    real_plus_minus = "Real (Float Point): plus-minus"
    real_degree = "Real (Float Point): degree"
    string = "String"
    operation = "Operation"
    separator = "Separator"
    assignment = "Assignment"
    comment = "Comment"
    directive = "Directive"
    error = "Error"