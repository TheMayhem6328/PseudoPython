import ply.yacc as yacc
from pseudotoken import Tokenizer
from utils import *
import inspect
tokens = Tokenizer.tokens
lexer = Tokenizer.lexer
stackTrace = []
parseLines = []

def p_root(p):
    """root : comment
            | assign
            | print"""
    stackTrace.append(inspect.stack()[0][3])

def p_comment(p):
    """comment : COMMENT"""
    stackTrace.append(inspect.stack()[0][3])
    parseLines.append(f"#{str(escapedString(p[1])).removeprefix('//')}")
    
def p_assign(p):
    """assign : ID ASSIGN expr
              | ID ASSIGN datatypes"""
    stackTrace.append(inspect.stack()[0][3])
    parseLines.append(f"{p[1]} = {p[3]}")

def p_print(p):
    """print : OUTPUT expr
             | OUTPUT ID
             | OUTPUT datatypes"""
    stackTrace.append(inspect.stack()[0][3])
    if type(p[2]) == str:
        parseLines.append(f"print({escapedString(p[2])})")

# Arithmetic Operations
def p_expr_arithmetic(p):
    """expr : expr '+' expr
            | expr '-' expr
            | expr '*' expr
            | expr '/' expr
            | expr DIV expr
            | expr MOD expr"""
    stackTrace.append(inspect.stack()[0][3])
    if p[2] == '+':
        p[0] = p[1] + p[3]
    elif p[2] == '-':
        p[0] = p[1] - p[3]
    elif p[2] == '*':
        p[0] = p[1] * p[3]
    elif p[2] == '/':
        p[0] = p[1] / p[3]
    elif p[2] == 'DIV':
        p[0] = p[1] // p[3]
    elif p[2] == 'MOD':
        p[0] = p[1] % p[3]

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

def parse(text : str = "") -> tuple[list, list]:
    parser.parse(text)
    return (parseLines, stackTrace)