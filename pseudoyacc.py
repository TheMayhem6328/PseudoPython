import ply.yacc as yacc
from pseudotoken import Tokenizer
tokens = Tokenizer.tokens
lexer = Tokenizer.lexer

def p_print(p):
    """print : OUTPUT expr
             | OUTPUT STRINGTYPE
             | OUTPUT CHARTYPE
             | OUTPUT DATETYPE
             | OUTPUT BOOLEAN"""
    print(p[2])

def p_statement_expr(p):
    'statement : expr'

# Arithmetic Operations
def p_expr_arithmetic(p):
    """expr : expr '+' expr
            | expr '-' expr
            | expr '*' expr
            | expr '/' expr"""
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
    p[0] = p[1]

def p_expr_group(p):
    """expr : '(' expr ')'"""
    p[0] = p[2]

def p_error(p):
    print(f"Syntax error in input! Token in context: {p}")

parser = yacc.yacc()
file = open("Main.mayudo")
data = file.read()
print(f"\n\nContent:\n==========\n[BEGIN FILE]\n{data}\n[END FILE]")
print("\n\nTokens:\n==========")
tokenList = list(Tokenizer.tokenize(filename = "Main.mayudo"))
for token in tokenList: print(token)
print("\nOutput:\n==========")
parser.parse(data)