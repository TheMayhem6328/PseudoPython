import ply.yacc as yacc
from pseudotoken import Tokenizer
tokens = Tokenizer.tokens

lexer = Tokenizer()
lexer.build()

def p_expr_plus(p):
    'expr : expr SPACE "+" SPACE term'
    p[0] = p[1] + p[5]

def p_expr_minus(p):
    'expr : expr SPACE "-" SPACE term'
    p[0] = p[1] - p[5]

def p_expr_term(p):
    'expr : term'
    p[0] = p[1]

def p_term_times(p):
    'term : term SPACE "*" SPACE fact'
    p[0] = p[1] * p[5]

def p_term_div(p):
    'term : term SPACE "/" SPACE fact'
    p[0] = p[1] / p[5]

def p_term_fact(p):
    'term : fact'
    p[0] = p[1]

def p_fact_num(p):
    '''fact : INTEGERTYPE
              | REALTYPE'''
    p[0] = p[1]

def p_fact_expr(p):
    'fact : "(" expr ")"'
    p[0] = p[2]

def p_error(p):
    print(f"Syntax error in input! Token in context: {p}")

parser = yacc.yacc()
print(parser.parse("2+4"))