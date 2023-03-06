import ply.yacc as yacc
from pseudotoken import Tokenizer
from utils import *
import inspect
tokens = Tokenizer.tokens
lexer = Tokenizer.lexer

variableState = dict(TestVariable = "Unchanged")
stackTrace    = []

def p_assign(p):
    """assign : ID ASSIGN expr
              | ID ASSIGN datatypes"""
    stackTrace.append(inspect.stack()[0][3])
    print(f"{p[1]} = {p[3]}")

def p_print(p):
    """print : OUTPUT expr
             | OUTPUT datatypes"""
    stackTrace.append(inspect.stack()[0][3])
    if type(p[2]) == str:
        print(f"print(\"{escapedString(p[2])}\")")

# Arithmetic Operations
def p_expr_arithmetic(p):
    """expr : expr '+' expr
            | expr '-' expr
            | expr '*' expr
            | expr '/' expr"""
    stackTrace.append(inspect.stack()[0][3])
    if p[2] == '+':
        p[0] = p[1] + p[3]
    elif p[2] == '-':
        p[0] = p[1] - p[3]
    elif p[2] == '*':
        p[0] = p[1] * p[3]
    elif p[2] == '/':
        p[0] = p[1] / p[3]

def p_expr_num(p):
    """expr : INTEGERTYPE
            | REALTYPE"""
    stackTrace.append(inspect.stack()[0][3])
    p[0] = p[1]

def p_datatypes(p):
    """datatypes : STRINGTYPE
                 | CHARTYPE
                 | DATETYPE
                 | BOOLEAN"""
    stackTrace.append(inspect.stack()[0][3])
    p[0] = p[1]

def p_expr_group(p):
    """expr : '(' expr ')'"""
    stackTrace.append(inspect.stack()[0][3])
    p[0] = p[2]

def p_error(p):
    stackTrace.append(inspect.stack()[0][3])
    print(f"Syntax error in input! Token in context: {p}")

parser = yacc.yacc()

def parse(text : str = "", filename : str = "") -> list[str]:
    if text == "" and filename != "":
        with open(filename, "r") as file:
            text = file.read()

    parser.parse(text)
    return stackTrace