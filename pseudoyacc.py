import ply.yacc as yacc
from pseudotoken import Tokenizer
import inspect
tokens = Tokenizer.tokens
lexer = Tokenizer.lexer
stackTrace = []
parseLines = []
indentCount = 0
def addLine(text: str) : parseLines.append(" "*indentCount +  text)
def addTrace(text: str): stackTrace.append(text)
def incrementDepth(depth : int = 1): global indentCount ;indentCount += 4 * depth
def decrementDepth(depth : int = 1): global indentCount ;indentCount -= 4 * depth

# Starting rule
def p_root(p):
    """root : comment
            | if
            | loop
            | declare
            | assign
            | fileops
            | constant
            | input
            | output"""
    stackTrace.append(inspect.stack()[0][3])



# == Miscellaneous

# Comment parsing
def p_comment(p):
    """comment : COMMENT"""
    addTrace(inspect.stack()[0][3])
    addLine(f"#{str(p[1]).removeprefix('//')}")



# == Conditional selection


# If...else...endif statements

def p_if(p):
    """if : ifstart
          | then
          | else
          | endif"""

def p_ifstart(p):
    """ifstart : IF boolexpr THEN
               | IF boolexpr"""
    addTrace(inspect.stack()[0][3])
    addLine(f"if {p[2]}:")
    incrementDepth()

def p_then(p):
    """then : THEN"""
    addTrace(inspect.stack()[0][3])

def p_else(p):
    """else : ELSE"""
    addTrace(inspect.stack()[0][3])
    decrementDepth()
    addLine("else:")
    incrementDepth()

def p_endif(p):
    """endif : ENDIF"""
    addTrace(inspect.stack()[0][3])
    decrementDepth()



# == Loops

# Catch-all loop handling
def p_loop(p):
    """loop : for
            | while
            | repeatuntil"""
    addTrace(inspect.stack()[0][3])


# For loops

def p_for(p):
    """for : forstart
           | endfor"""
    addTrace(inspect.stack()[0][3])

def p_forstart(p):
    """forstart : FOR ID ASSIGN RANGETYPE"""
    addTrace(inspect.stack()[0][3])
    addLine(f"for {p[2]} in {p[4]}")
    incrementDepth()

def p_endfor(p):
    """endfor : ENDFOR
              | NEXT ID"""
    addTrace(inspect.stack()[0][3])
    decrementDepth()


# While loops

def p_while(p):
    """while : whilestart
             | endwhile"""
    addTrace(inspect.stack()[0][3])
    
def p_whilestat(p):
    """whilestart : WHILE boolexpr"""
    addTrace(inspect.stack()[0][3])
    addLine(f"while {p[2]}:")
    incrementDepth()

def p_endwhile(p):
    """endwhile : ENDWHILE"""
    addTrace(inspect.stack()[0][3])
    decrementDepth()


# Repeat-Until loops

def p_repeatuntil(p):
    """repeatuntil : repeat
                   | until"""
    addTrace(inspect.stack()[0][3])

def p_repeat(p):
    """repeat : REPEAT"""
    addTrace(inspect.stack()[0][3])
    addLine(f"while True:")
    incrementDepth()

def p_until(p):
    """until : UNTIL boolexpr"""
    addTrace(inspect.stack()[0][3])
    addLine(f"if {p[2]}: break")
    decrementDepth()



# == Data flow

# Declaration statements
def p_declare(p):
    """declare : DECLARE ID ':' typenames"""
    addTrace(inspect.stack()[0][3])
    if   p[4] == "DATE"    : addLine(f"{p[2]} = datetime.datetime(1970, 1, 1)")
    elif p[4] == "REAL"    : addLine(f"{p[2]} = float()")
    elif p[4] == "INTEGER" : addLine(f"{p[2]} = int()")
    elif p[4] == "CHAR"    : addLine(f"{p[2]} = str() # Should be char")
    elif p[4] == "STRING"  : addLine(f"{p[2]} = str()")
    elif p[4] == "BOOLEAN" : addLine(f"{p[2]} = bool()")

# Constant assignment
def p_constant(p):
    """constant : CONSTANT ID EQUALTO datatypes"""
    addTrace(inspect.stack()[0][3])
    addLine(f"{p[2]} = {p[4]} # Constant")

# Assign statements
def p_assign(p):
    """assign : ID ASSIGN expr
              | ID ASSIGN boolexpr
              | ID ASSIGN datatypes"""
    addTrace(inspect.stack()[0][3])
    addLine(f"{p[1]} = {p[3]}")



# == I/O

# File operations

def p_fileops(p):
    """fileops : openfile
               | readfile
               | writefile
               | closefile"""
    addTrace(inspect.stack()[0][3])

def p_openfile(p):
    """openfile : OPENFILE fileid FOR filemodes"""
    addTrace(inspect.stack()[0][3])
    for modeTranslate in [["READ", "rt"], ["WRITE", "wt"], ["APPEND", "at"]]:
        if p[4] == modeTranslate[0]: mode = modeTranslate[1]
    utilLine = "fileDict = dict() # Utility dictionary, from transpiler"
    try : parseLines.index(utilLine)
    except ValueError : addLine(utilLine)
    braceBound = bb = ["{", "}"]
    addLine(f"fileDict.update({bb[0]}{p[2]}: open({p[2]}, '{mode}'){bb[1]})")

def p_readfile(p):
    """readfile : READFILE fileid ',' ID"""
    addTrace(inspect.stack()[0][3])
    addLine(f"{p[4]} = fileDict[{p[2]}].readline()")    

def p_writefile(p):
    """writefile : WRITEFILE fileid ',' boolexpr
                 | WRITEFILE fileid ',' expr
                 | WRITEFILE fileid ',' ID
                 | WRITEFILE fileid ',' datatypes"""
    addTrace(inspect.stack()[0][3])
    addLine(f"fileDict[{p[2]}].write(str({p[4]}) + '\\n')")

def p_closefile(p):
    """closefile : CLOSEFILE fileid"""
    addTrace(inspect.stack()[0][3])
    addLine(f"fileDict[{p[2]}].close()")

def p_filemappings(p):
    """filemodes : READ
                 | WRITE
                 | APPEND
    fileid : STRINGTYPE
           | ID"""
    addTrace(inspect.stack()[0][3])
    p[0] = p[1]


# Console operations

# Input statements
def p_input(p):
    """input : INPUT ID"""
    addTrace(inspect.stack()[0][3])
    addLine(f"{p[2]} = input()")

# Output statements
def p_output(p):
    """output : OUTPUT expr
              | OUTPUT boolexpr
              | OUTPUT ID
              | OUTPUT datatypes"""
    addTrace(inspect.stack()[0][3])
    addLine(f"print({p[2]})")



# == Operand parsing

# Booleans Operations
def p_boolexpr_operands(p):
    """boolexpr : boolexpr EQUALTO boolexpr
                | boolexpr NOTEQUALTO boolexpr
                | boolexpr GREATEQUAL boolexpr
                | boolexpr LESSEQUAL boolexpr
                | boolexpr GREAT boolexpr
                | boolexpr LESS boolexpr"""
    addTrace(inspect.stack()[0][3])
    if   p[2] == "="  : operator = "=="
    elif p[2] == "<>" : operator = "!="
    else            : operator = p[2]
    p[0] = f"{p[1]} {operator} {p[3]}"

# Arithmetic Operations
def p_expr_operands(p):
    """expr : expr '+' expr
            | expr '-' expr
            | expr '*' expr
            | expr '/' expr
            | expr DIV expr
            | expr MOD expr"""
    addTrace(inspect.stack()[0][3])
    if   p[2] == "DIV": operator = "//"
    elif p[2] == "MOD": operator = "%"
    else              : operator = p[2]
    p[0] = f"{p[1]} {operator} {p[3]}"



# == Data type handling

# Boolean expression terms
def p_boolexpr_terms(p):
    """boolexpr : BOOLEANTYPE
                | ID
                | expr"""
    addTrace(inspect.stack()[0][3])
    p[0] = p[1]

# Arithmetic expression terms
def p_expr_terms(p):
    """expr : INTEGERTYPE
            | REALTYPE
            | ID"""
    addTrace(inspect.stack()[0][3])
    p[0] = p[1]

# Data types
def p_datatypes(p):
    """datatypes : STRINGTYPE
                 | CHARTYPE
                 | DATETYPE"""
    addTrace(inspect.stack()[0][3])
    p[0] = p[1]

# Data type names
def p_typenames(p):
    """typenames : DATE
                 | REAL
                 | INTEGER
                 | CHAR
                 | STRING
                 | BOOLEAN"""
    addTrace(inspect.stack()[0][3])
    p[0] = p[1]

# Braket support for expressions
def p_expr_group(p):
    """expr : '(' expr ')'"""
    addTrace(inspect.stack()[0][3])
    p[0] = f"({p[2]})"

# Braket support for boolean expressions
def p_boolexpr_group(p):
    """boolexpr : '(' boolexpr ')'"""
    addTrace(inspect.stack()[0][3])
    p[0] = f"({p[2]})"

# Error handling
def p_error(p):
    addTrace(inspect.stack()[0][3])
    if p == None:
        stackTrace[-1] += " (Blank line)"
        addLine("")
    else:
        print(f"Syntax error in input! Token in context: {p}")
        addLine(f"#=== ERROR PARSING {p} ===#")



# Build parser
parser = yacc.yacc()

# Function to parse given string
def parse(text : str = "") -> tuple[list, list]:
    """Parses parameter string and transpiles pseudocode to python.
    Returns a tuple with list of parsed lines and another list with stack trace
    
    Args:
    - `text` (str): Text to parse
    
    Returns:
    - tuple[`parseLines`, `stackTrace`]
    - `parseLines` (list): A list with transpiled python lines"""
    parser.parse(text)
    return (parseLines, stackTrace)
