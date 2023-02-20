# ------------------------------------------------------------
# pseudotoken.py
#
# A WIP library for interpreting cambridge pseudocode
# ------------------------------------------------------------
import ply.lex as lex
import datetime

class Tokenizer(object):
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
        'DIVIDEINTEGER',
        'MODULUS',
        # Miscellaneous
        'ID'
     ] + reserved
    
    # Literal handling
    literals = r"+-*/=(){}[],:. "
    
    # Logical Operators
    t_EQUALTO    = r'\=\='
    t_NOTEQUALTO = r'\<\>'
    t_GREATEQUAL = r'\>\='
    t_LESSEQUAL  = r'\<\='
    t_LESS       = r'\<'
    t_GREAT      = r'\>'
    
    # Arithmetic Operators
    t_DIVIDEINTEGER = r'[DIV]'
    t_MODULUS       = r'[MOD]'
    
    # Miscellaneous
    t_ASSIGN  = r'\<\-'
    t_COMMENT = r'\/\/.*'
    
    # Data Types
    def t_RANGE(self, t):
        '\d+\ TO\ \d+'
        value = t.value.split(" TO ")
        t.value = range(int(value[0]), int(value[1]) + 1)
        return t
    
    def t_DATE(self, t):
        r'\d{2}/\d{2}/\d{4}'
        t.value = datetime.datetime(
            int(t.value[6:10]),
            int(t.value[3:5]),
            int(t.value[0:2])
        )
        return t
        
    def t_REAL(self, t):
        r'\d+\.\d+'
        t.value = float(t.value)    
        return t

    def t_INTEGER(self, t):
        r'\d+'
        t.value = int(t.value)    
        return t
    
    def t_CHAR(self, t):
        r'\'.\''
        t.value = str(t.value)
        return t
    
    def t_STRING(self, t):
        r'\".*\"'
        t.value = str(t.value)
        return t
    
    def t_BOOLEAN(self, t):
        r'TRUE|FALSE'
        if t.value == "TRUE":
            t.value = bool(True)
        elif t.value == "FALSE":
            t.value = bool(False)
        return t
    
    # Reserved keywords + Identifiers
    def t_ID(self, t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        if Tokenizer.reserved.count(t.value) > 0:
            if t.value == "PRINT" or t.value == "OUTPUT":
                t.type == "OUTPUT"
            else:
                t.type = t.value
        return t
    

    # Track line numbers
    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    # Ignore these characters
    t_ignore  = '\t'

    # Error handler
    def t_error(self, t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    # Build lexer
    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

    # Tokenize
    def tokenize(self, filename : str) -> list[lex.LexToken]:
        with open(filename, "r") as file:
            data = file.read()
        
        # Give the lexer some input
        self.lexer.input(data)
        
        # Tokenize
        tokens = []
        for tok in self.lexer:
            tokens.append(tok)
            
        return tokens