# ------------------------------------------------------------
# pseudotoken.py
#
# A WIP library for interpreting cambridge pseudocode
# ------------------------------------------------------------
import ply.lex as lex
import datetime

class Tokenizer:
    # List of reserved words:
    reserved = [
        # Data Flow
        'DECLARE',
        'TYPE',
        'ENDTYPE',
        # CASE Directive
        'CASE',
        'OF',
        'OTHERWISE',
        'ENDCASE',
        # IF Directive
        'IF',
        'THEN',
        'ELSE',
        'ENDIF',
        # I/O Keywords
        'INPUT',
        'OUTPUT',
        'PRINT'
    ]
    
    # List of token names
    # In order of priority - highest ones first
    tokens = [
        # Miscellaneous
        'COMMENT',
        'ASSIGN',
        # Data Types
        'RANGE',
        'DATE',
        'REAL',
        'INTEGER',
        'CHAR',
        'STRING',
        'BOOLEAN',
        # Logical Operators
        'EQUALTO',
        'NOTEQUALTO',
        'GREATEQUAL',
        'LESSEQUAL',
        'LESS',
        'GREAT',
        # Arithmetic Operators
        'PLUS',
        'MINUS',
        'TIMES',
        'DIVIDE',
        'DIVIDEINTEGER',
        'MODULUS',
        'EQUAL',
        # Parenthesis
        'LPAREN1',
        'RPAREN1',
        'LPAREN2',
        'RPAREN2',
        'LPAREN3',
        'RPAREN3',
        # Miscellaneous
        'INDENT',
        'SPACE',
        'COMMA',
        'COLON',
        'DOT',
        'ID'
     ] + reserved
    
    # Logical Operators
    t_EQUALTO    = r'\=\='
    t_NOTEQUALTO = r'\<\>'
    t_GREATEQUAL = r'\>\='
    t_LESSEQUAL  = r'\<\='
    t_LESS       = r'\<'
    t_GREAT      = r'\>'
    
    # Arithmetic Operators
    t_PLUS          = r'\+'
    t_MINUS         = r'-'
    t_TIMES         = r'\*'
    t_DIVIDE        = r'/'
    t_DIVIDEINTEGER = r'[DIV]'
    t_MODULUS       = r'[MOD]'
    t_EQUAL         = r'\='
    
    # Parenthesis
    t_LPAREN1  = r'\('
    t_RPAREN1  = r'\)'
    t_LPAREN2  = r'\{'
    t_RPAREN2  = r'\}'
    t_LPAREN3  = r'\['
    t_RPAREN3  = r'\]'
    
    # Miscellaneous
    t_ASSIGN  = r'\<\-'
    t_COMMENT = r'\/\/.*'
    t_DOT     = r'\.'
    t_COMMA   = r'\,'
    t_COLON   = r'\:'
    t_INDENT  = r'\A[ ]{3,4}'
    t_SPACE   = r'\ '
    
    # Data Types
    def t_RANGE(t):
        '\d+\ TO\ \d+'
        value = t.value.split(" TO ")
        t.value = range(int(value[0]), int(value[1]) + 1)
        return t
    
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
    
    # Reserved keywords + Identifiers
    def t_ID(t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        if Tokenizer.reserved.count(t.value) > 0:
            if t.value == "PRINT" or t.value == "OUTPUT":
                t.type == "OUTPUT"
            else:
                t.type = t.value
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