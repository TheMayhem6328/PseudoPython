# ------------------------------------------------------------
# pseudotoken.py
#
# tokenizer for a simple expression evaluator for
# numbers and +,-,*,/
# ------------------------------------------------------------
import ply.lex as lex


class Tokenizer:
    # List of token names
    # In order of priority - highest ones first
    tokens = (
        # Data types
       'REAL',
       'INTEGER',
        # Operators
       'PLUS',
       'MINUS',
       'TIMES',
       'DIVIDE',
        # Parenthesis
       'LPAREN1',
       'RPAREN1',
       'LPAREN2',
       'RPAREN2',
       'LPAREN3',
       'RPAREN3',
    )

    # Regex for simpler tokens
    
    # Operators
    t_PLUS    = r'\+'
    t_MINUS   = r'-'
    t_TIMES   = r'\*'
    t_DIVIDE  = r'/'
    # Parenthesis
    t_LPAREN1  = r'\('
    t_RPAREN1  = r'\)'
    t_LPAREN2  = r'\{'
    t_RPAREN2  = r'\}'
    t_LPAREN3  = r'\['
    t_RPAREN3  = r'\]'

    # Real numbers
    def t_REAL(t):
        r'\d+\.\d+'
        t.value = float(t.value)    
        return t
    
    # Integer values
    def t_INTEGER(t):
        r'\d+'
        t.value = int(t.value)    
        return t

    # Define a rule so we can track line numbers
    def t_newline(t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    # A string containing ignored characters (spaces and tabs)
    t_ignore  = ' \t'

    # Error handling rule
    def t_error(t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    # Build the lexer
    lexer = lex.lex()

    # Test it out
    def tokenize(filename : str, lexer : lex.Lexer = lexer) -> list[lex.LexToken]:
        file = open(filename, "r")
        data = file.read()

        # Give the lexer some input
        lexer.input(data)
        
        # Tokenize
        tokens = []
        for tok in lexer:
            tokens.append(tok)
            
        return tokens