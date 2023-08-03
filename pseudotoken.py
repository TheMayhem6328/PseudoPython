# ------------------------------------------------------------
# pseudotoken.py
#
# A WIP library for interpreting cambridge pseudocode
# ------------------------------------------------------------
import ply.lex  as lex
from datetime import date

class Tokenizer:
    # List of reserved words:
    reserved = [
        # Array Keywords
        'ARRAY',
        'OF',
        # Arithmetic Operators
        'DIV',
        'MOD',
        # Boolean Operators
        'AND',
        'OR',
        'NOT',
        # Data Flow
        'DECLARE',
        # Data Types
        'DATE',
        'REAL',
        'INTEGER',
        'CHAR',
        'STRING',
        'BOOLEAN',
        'CONSTANT',
        # IF Definition
        'IF',
        'THEN',
        'ELSE',
        'ENDIF',
        # FOR Definition
        'FOR',
        'TO',
        'NEXT',
        'ENDFOR',
        # WHILE Definition
        'WHILE',
        'ENDWHILE',
        # REPEAT-UNTIL Definition
        'REPEAT',
        'UNTIL',
        # PROCEDURE Definition
        'PROCEDURE',
        'BYREF',
        'BYVAL',
        'ENDPROCEDURE',
        'CALL',
        # String Functions Definition
        'LEFT',
        'RIGHT',
        'LENGTH',
        'MID',
        'LCASE',
        'UCASE',
        # Numeric Functions Definition
        'INT',
        'RAND',
        # FUNCTION Definition
        'FUNCTION',
        'RETURNS',
        'RETURN',
        'ENDFUNCTION',
        # File Operation Keywords
        'OPENFILE',
        'READ',
        'WRITE',
        'APPEND',
        'READFILE',
        'WRITEFILE',
        'CLOSEFILE',
         # I/O Keywords
        'INPUT',
        'OUTPUT',
    ]
    
    # List of token names
    # In order of priority - highest ones first
    tokens = [
        # Miscellaneous
        'COMMENT',
        'ASSIGN',
        # Data Types
        'DATETYPE',
        'REALTYPE',
        'INTEGERTYPE',
        'CHARTYPE',
        'STRINGTYPE',
        'BOOLEANTYPE',
        # Logical Operators
        'EQUALTO',
        'NOTEQUALTO',
        'GREATEQUAL',
        'LESSEQUAL',
        'GREAT',
        'LESS',
        # Miscellaneous
        'ID'
     ] + reserved
    
    # Literal handling
    literals = r"+-*/(){}[],:."
    
    # Logical Operators
    t_EQUALTO    = r'\='
    t_NOTEQUALTO = r'\<\>'
    t_GREATEQUAL = r'\>\='
    t_LESSEQUAL  = r'\<\='
    t_LESS       = r'\<'
    t_GREAT      = r'\>'
    
    # Miscellaneous
    t_COMMENT = r'\/\/.*'
    
    def t_ASSIGN(t):
        r'\<\-|←'
        return t
    
    # def t_INDENT(t):
    #     r'\ \ \ |\ \ \ \ '
    #     return t
    
    def t_SPACE(t):
        r'\ '
    
    def t_DATETYPE(t):
        r'\d{2}/\d{2}/\d{4}'
        temp = t.value
        t.value =   "date("
        t.value += f"{ int(temp[6:10])},"
        t.value += f" {int(temp[3:5])},"
        t.value += f" {int(temp[0:2])}"
        t.value +=  ")"
        return t
        
    def t_REALTYPE(t):
        r'\d+\.\d+'
        t.value = float(t.value)    
        return t

    def t_INTEGERTYPE(t):
        r'\d+'
        t.value = int(t.value)    
        return t
    
    def t_CHARTYPE(t):
        r'\'.\''
        t.value = str(t.value)
        return t
    
    def t_STRINGTYPE(t):
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
        if t.value == "PRINT" or t.value == "OUTPUT":
            t.type = "OUTPUT"
        elif Tokenizer.reserved.count(t.value) > 0:
            t.type = t.value
        return t
    
    # Track line numbers
    def t_newline(t):
        r'\n|\r|\r\n'
        t.lexer.lineno += len(t.value)
        # t.type = "NEWLINE"
        # return t

    # Ignore these characters
    t_ignore  = '\t'

    # Error handler
    def t_error(t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1) 
    
    # Build lexer
    lexer = lex.lex()

    # Tokenize
    def tokenize(text : str = "", filename : str = "") -> list[lex.LexToken]:
        if text == "" and filename != "":
            with open(filename, "r") as file:
                text = file.read()
        
        # Give the lexer some input
        Tokenizer.lexer.input(text)
        
        # Tokenize
        tokens = []
        for tok in Tokenizer.lexer:
            tokens.append(tok)
            
        return tokens
