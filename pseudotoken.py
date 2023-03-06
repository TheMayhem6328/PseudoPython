# ------------------------------------------------------------
# pseudotoken.py
#
# A WIP library for interpreting cambridge pseudocode
# ------------------------------------------------------------
import ply.lex  as lex
import ply.yacc as yacc
import datetime

class Tokenizer:
    # List of reserved words:
    reserved = [
        # Arithmetic Operators
        'DIV',
        'MOD',
        # Data Flow
        'DECLARE',
        'TYPE',
        'ENDTYPE',
        # Data Types
        'RANGE',
        'DATE',
        'REAL',
        'INTEGER',
        'CHAR',
        'STRING',
        'BOOLEAN',
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
    ]
    
    # List of token names
    # In order of priority - highest ones first
    tokens = [
        # Miscellaneous
        'COMMENT',
        'ASSIGN',
        # Data Types
        'RANGETYPE',
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
        # 'INDENT',
        'SPACE',
        'ID',
        'NEWLINE'# ,
        # 'EOF'
     ] + reserved
    
    # Literal handling
    literals = r"+-*/=(){}[],:."
    
    # Logical Operators
    t_EQUALTO    = r'\=\='
    t_NOTEQUALTO = r'\<\>'
    t_GREATEQUAL = r'\>\='
    t_LESSEQUAL  = r'\<\='
    t_LESS       = r'\<'
    t_GREAT      = r'\>'
    
    # Miscellaneous
    t_COMMENT = r'\/\/.*'
    
    def t_ASSIGN(t):
        r'\<\-'
        return t
    
    # def t_INDENT(t):
    #     r'\ \ \ |\ \ \ \ '
    #     return t
    
    def t_SPACE(t):
        r'\ '
    
    # Data Types
    def t_RANGETYPE(t):
        '\d+\ TO\ \d+'
        value = t.value.split(" TO ")
        t.value = range(int(value[0]), int(value[1]) + 1)
        return t
    
    def t_DATETYPE(t):
        r'\d{2}/\d{2}/\d{4}'
        t.value = datetime.datetime(
            int(t.value[6:10]),
            int(t.value[3:5]),
            int(t.value[0:2])
        )
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
        t.value = str(t.value).replace("'", "")
        return t
    
    def t_STRINGTYPE(t):
        r'\".*\"'
        t.value = str(t.value).replace('"', '')
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
        t.type = "NEWLINE"
        return t

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


# Parser