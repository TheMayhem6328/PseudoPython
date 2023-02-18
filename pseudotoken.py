# ------------------------------------------------------------
# pseudotoken.py
#
# tokenizer for a simple expression evaluator for
# numbers and +,-,*,/
# ------------------------------------------------------------
import ply.lex as lex
import datetime

class Tokenizer:
    # List of token names
    # In order of priority - highest ones first
    tokens = (
       # Data types
       'DATE',
       'REAL',
       'INTEGER',
       'CHAR',
       'STRING',
       'BOOLEAN',
       # Arithmetic Operators
       'PLUS',
       'MINUS',
       'TIMES',
       'DIVIDE',
       # Commands
       # Parenthesis
       'LPAREN1',
       'RPAREN1',
       'LPAREN2',
       'RPAREN2',
       'LPAREN3',
       'RPAREN3',
       # Miscellaneous
       'SPACE',
    )
    
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
    t_SPACE    = r'\ '


    # Data Types
    def t_DATE(t):
        r'\d{2}/\d{2}/\d{4}'
        t.value = datetime.datetime(
            int(t.value[6:10]),
            int(t.value[3:5]),
            int(t.value[0:2])
        )
        return t
        
    def t_REAL(t):
        r'\d+\.\d+'
        t.value = float(t.value)    
        return t

    def t_INTEGER(t):
        r'\d+'
        t.value = int(t.value)    
        return t
    
    def t_CHAR(t):
        r'\'.\''
        t.value = str(t.value)
        return t
    
    def t_STRING(t):
        r'\".*\"'
        t.value = str(t.value)
        return t
    
    def t_BOOLEAN(t):
        r'TRUE|FALSE'
        if t.value == "TRUE":
            t.value = bool(True)
        elif t.value == "FALSE":
            t.value = bool(False)
        return t
    

    # Track line numbers
    def t_newline(t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    # Ignore these characters
    t_ignore  = '\t'

    # Error handler
    def t_error(t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    # Build lexer
    lexer = lex.lex()

    # Tokenize
    def tokenize(filename : str, lexer : lex.Lexer = lexer) -> list[lex.LexToken]:
        with open(filename, "r") as file:
            data = file.read()
        
        # Give the lexer some input
        lexer.input(data)
        
        # Tokenize
        tokens = []
        for tok in lexer:
            tokens.append(tok)
            
        return tokens