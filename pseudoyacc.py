import ply.yacc as yacc
from pseudotoken import Tokenizer
from utils import *
import inspect
tokens = Tokenizer.tokens
lexer = Tokenizer.lexer
stackTrace = []
parseLines = []
indentCount = 0
def addLine(text: str) : parseLines.append(" "*indentCount +  text)
def addTrace(text: str): stackTrace.append(text)

# Starting rule
def p_root(p):
    """root : comment
            | assign
            | declare
            | input
            | output"""
    stackTrace.append(inspect.stack()[0][3])


# == Statement handling

# Comment parsing
def p_comment(p):
    """comment : COMMENT"""
    addTrace(inspect.stack()[0][3])
    addLine(f"#{str(escapedString(p[1])).removeprefix('//')}")

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

# Assign statements
def p_assign(p):
    """assign : ID ASSIGN expr
              | ID ASSIGN datatypes"""
    addTrace(inspect.stack()[0][3])
    addLine(f"{p[1]} = {p[3]}")


# == I/O

def p_input(p):
    """input : INPUT ID"""
    addTrace(inspect.stack()[0][3])
    addLine(f"{p[2]} = input()")

# Output statements
def p_output(p):
    """output : OUTPUT expr
              | OUTPUT ID
              | OUTPUT datatypes"""
    addTrace(inspect.stack()[0][3])
    addLine(f"print({p[2]})")

# == Miscellaneous

# Arithmetic Operations
def p_expr_arithmetic(p):
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


# == Basic type handling

# Expression terms
def p_expr_num(p):
    """expr : INTEGERTYPE
            | REALTYPE
            | ID"""
    addTrace(inspect.stack()[0][3])
    p[0] = p[1]

# Data types
def p_datatypes(p):
    """datatypes : STRINGTYPE
                 | CHARTYPE
                 | DATETYPE
                 | BOOLEANTYPE"""
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

# Error handling
def p_error(p):
    addTrace(inspect.stack()[0][3])
    if p == None:
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
