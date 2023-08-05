# Import handling
from ply import lex, yacc
import pseudotoken as tokenizer
import inspect


# Initialize necessary values
tokens = tokenizer.tokens
lexer = tokenizer.lexer
stackTrace = []
parseLines = []
indentCount = 0


# Define utility functions
def add_line(text: str):
    parseLines.append(" " * indentCount + text)


def add_trace(text: str, p: any):
    if p is not None and type(p) != lex.LexToken:
        stackTrace.append(text + str(list(p)[1:]))
    else:
        stackTrace.append(text)


def increment_depth(depth: int = 1):
    global indentCount
    indentCount += 4 * depth


def decrement_depth(depth: int = 1):
    global indentCount
    indentCount -= 4 * depth


def add_line_if_not_found(utility_line: str):
    try:
        parseLines.index(utility_line)
    except ValueError:
        add_line(utility_line)


# Starting rule
def p_root(p):
    """root : comment
    | if
    | loop
    | declare
    | subroutine
    | assign
    | file_operation
    | constant
    | input
    | output"""
    add_trace(inspect.stack()[0][3], p)
    p[0] = p[1]


# == Miscellaneous


# Comment parsing
def p_comment(p):
    """comment : COMMENT"""
    add_trace(inspect.stack()[0][3], p)
    add_line(f"#{str(p[1]).removeprefix('//')}")


# == Conditional selection


# If...else...endif statements


def p_if(p):
    """if : if_start
    | then
    | else
    | end_if"""
    p[0] = p[1]


def p_if_start(p):
    """if_start : IF boolean_expression THEN
    | IF boolean_expression"""
    add_trace(inspect.stack()[0][3], p)
    add_line(f"if {p[2]}:")
    increment_depth()


def p_then(p):
    """then : THEN"""
    add_trace(inspect.stack()[0][3], p)


def p_else(p):
    """else : ELSE"""
    add_trace(inspect.stack()[0][3], p)
    decrement_depth()
    add_line("else:")
    increment_depth()


def p_end_if(p):
    """end_if : ENDIF"""
    add_trace(inspect.stack()[0][3], p)
    decrement_depth()


# == Loops


# Catch-all loop handling
def p_loop(p):
    """loop : for
    | while
    | repeat_until"""
    add_trace(inspect.stack()[0][3], p)


# For loops


def p_for(p):
    """for : for_start
    | end_for"""
    add_trace(inspect.stack()[0][3], p)


def p_for_start(p):
    """for_start : FOR ID ASSIGN range_for"""
    add_trace(inspect.stack()[0][3], p)
    add_line(f"for {p[2]} in {p[4]}")
    increment_depth()


def p_range_for(p):
    """range_for : expression TO expression"""
    add_trace(inspect.stack()[0][3], p)
    p[0] = f"range({p[1]}, {p[3]} + 1):"


def p_end_for(p):
    """end_for : ENDFOR
    | NEXT ID"""
    add_trace(inspect.stack()[0][3], p)
    decrement_depth()


# While loops


def p_while(p):
    """while : while_start
    | end_while"""
    add_trace(inspect.stack()[0][3], p)


def p_while_start(p):
    """while_start : WHILE boolean_expression"""
    add_trace(inspect.stack()[0][3], p)
    add_line(f"while {p[2]}:")
    increment_depth()


def p_end_while(p):
    """end_while : ENDWHILE"""
    add_trace(inspect.stack()[0][3], p)
    decrement_depth()


# Repeat-Until loops


def p_repeat_until(p):
    """repeat_until : repeat
    | until"""
    add_trace(inspect.stack()[0][3], p)


def p_repeat(p):
    """repeat : REPEAT"""
    add_trace(inspect.stack()[0][3], p)
    add_line(f"while True:")
    increment_depth()


def p_until(p):
    """until : UNTIL boolean_expression"""
    add_trace(inspect.stack()[0][3], p)
    add_line(f"if {p[2]}: break")
    decrement_depth()


# == Data flow


# Declaration statements
def p_declare(p):
    """declare : declare_array
    | declare_variable"""
    add_trace(inspect.stack()[0][3], p)


# 2D Arrays
def p_declare_array__2d(p):
    """declare_array : DECLARE declare_id ':' ARRAY '[' expression ':' expression ',' expression ':' expression ']' OF type_names"""
    add_trace(inspect.stack()[0][3], p)
    declaration_type = ""
    count_row = int(p[8]) - (int(p[6]) - 1)
    count_col = int(p[12]) - (int(p[10]) - 1)
    if p[15] == "DATE":
        add_line_if_not_found(
            "from datetime import date # Added by transpiler to add date support"
        )
        declaration_type = f"[[date(1970, 1, 1)] * {count_col}] * {count_row}"
    elif p[15] == "REAL":
        declaration_type = f"[[float()] * {count_col}] * {count_row}"
    elif p[15] == "INTEGER":
        declaration_type = f"[[int()] * {count_col}] * {count_row}"
    elif p[15] == "CHAR":
        declaration_type = f"[[str()] * {count_col}] * {count_row} # Should be char"
    elif p[15] == "STRING":
        declaration_type = f"[[str()] * {count_col}] * {count_row}"
    elif p[15] == "BOOLEAN":
        declaration_type = f"[[bool()] * {count_col}] * {count_row}"
    add_line(f"{p[2]} = {declaration_type} # Declaration")


# 1D Arrays
def p_declare_array__1d(p):
    """declare_array : DECLARE declare_id ':' ARRAY '[' expression ':' expression ']' OF type_names"""
    add_trace(inspect.stack()[0][3], p)
    declaration_type = ""
    count = int(p[8]) - (int(p[6]) - 1)
    if p[11] == "DATE":
        add_line_if_not_found(
            "from datetime import date # Added by transpiler to add date support"
        )
        declaration_type = f"[date(1970, 1, 1)] * {count}"
    elif p[11] == "REAL":
        declaration_type = f"[float()] * {count}"
    elif p[11] == "INTEGER":
        declaration_type = f"[int()] * {count}"
    elif p[11] == "CHAR":
        declaration_type = f"[str()] * {count} # Should be char"
    elif p[11] == "STRING":
        declaration_type = f"[str()] * {count}"
    elif p[11] == "BOOLEAN":
        declaration_type = f"[bool()] * {count}"
    add_line(f"{p[2]} = {declaration_type} # Declaration")


def p_declare_variable(p):
    """declare_variable : DECLARE declare_id ':' type_names"""
    add_trace(inspect.stack()[0][3], p)
    declaration_type = ""
    if p[4] == "DATE":
        add_line_if_not_found(
            "from datetime import date # Not in source, but added to add support for date data_types"
        )
        declaration_type = "date(1970, 1, 1)"
    elif p[4] == "REAL":
        declaration_type = "float()"
    elif p[4] == "INTEGER":
        declaration_type = "int()"
    elif p[4] == "CHAR":
        declaration_type = "str() # Should be char"
    elif p[4] == "STRING":
        declaration_type = "str()"
    elif p[4] == "BOOLEAN":
        declaration_type = "bool()"
    add_line(f"{p[2]} = {declaration_type} # Declaration")


def p_declare_id(p):
    """declare_id : ID"""
    add_trace(inspect.stack()[0][3], p)
    p[0] = p[1]


# Constant assignment
def p_constant(p):
    """constant : CONSTANT ID EQUALTO data_types"""
    add_trace(inspect.stack()[0][3], p)
    add_line(f"{p[2]} = {p[4]} # Constant")


# Assign statements
def p_assign(p):
    """assign : symbol_reference ASSIGN expression
    | symbol_reference ASSIGN boolean_expression
    | symbol_reference ASSIGN data_types"""
    add_trace(inspect.stack()[0][3], p)
    add_line(f"{p[1]} = {p[3]}")


# == Subroutines


def p_subroutine(p):
    """subroutine : procedure
    | function"""
    add_trace(inspect.stack()[0][3], p)


# Procedures


def p_procedure(p):
    """procedure : start_procedure
    | end_procedure
    | call"""
    add_trace(inspect.stack()[0][3], p)


def p_start_procedure__parameter_free(p):
    """start_procedure : PROCEDURE ID '(' ')'"""
    add_trace(inspect.stack()[0][3], p)
    add_line(f"def {p[2]}():")
    increment_depth()


def p_start_procedure__parameter_inclusive(p):
    """start_procedure : PROCEDURE ID '(' parameter_definition ')'"""
    add_trace(inspect.stack()[0][3], p)
    add_line(f"def {p[2]}({p[4]}):")
    increment_depth()


def p_end_procedure(p):
    """end_procedure : ENDPROCEDURE"""
    add_trace(inspect.stack()[0][3], p)
    decrement_depth()


def p_call_parameter_free(p):
    """call : CALL ID"""
    add_trace(inspect.stack()[0][3], p)
    add_line(f"{p[2]}()")


def p_call_parameter_inclusive(p):
    """call : CALL ID '(' parameter_feed ')'"""
    add_trace(inspect.stack()[0][3], p)
    add_line(f"{p[2]}({p[4]})")


# Functions


def p_function(p):
    """function : start_function
    | return
    | end_function
    | inline_call"""
    add_trace(inspect.stack()[0][3], p)


def p_start_function__parameter_free(p):
    """start_function : FUNCTION ID '(' ')' RETURNS type_names"""
    add_trace(inspect.stack()[0][3], p)
    data_type = ""
    if p[6] == "DATE":
        add_line_if_not_found(
            "from datetime import date # Added by transpiler to add date support"
        )
        data_type = "datetime.date"
    elif p[6] == "REAL":
        data_type = "float"
    elif p[6] == "INTEGER":
        data_type = "int"
    elif p[6] == "CHAR":
        data_type = "str"
    elif p[6] == "STRING":
        data_type = "str"
    elif p[6] == "BOOLEAN":
        data_type = "bool"
    elif p[6] == "ARRAY":
        data_type = "list"
    add_line(f"def {p[2]}() -> {data_type}:")
    increment_depth()


def p_start_function_parameter_inclusive(p):
    """start_function : FUNCTION ID '(' parameter_definition ')' RETURNS type_names"""
    add_trace(inspect.stack()[0][3], p)
    data_type = ""
    if p[7] == "DATE":
        add_line_if_not_found(
            "from datetime import date # Added by transpiler to add date support"
        )
        data_type = "datetime.date"
    elif p[7] == "REAL":
        data_type = "float"
    elif p[7] == "INTEGER":
        data_type = "int"
    elif p[7] == "CHAR":
        data_type = "str"
    elif p[7] == "STRING":
        data_type = "str"
    elif p[7] == "BOOLEAN":
        data_type = "bool"
    add_line(f"def {p[2]}({p[4]}) -> {data_type}:")
    increment_depth()


def p_return(p):
    """return : RETURN expression
    | RETURN boolean_expression
    | RETURN ID
    | RETURN data_types"""
    add_trace(inspect.stack()[0][3], p)
    add_line(f"return {p[2]}")


def p_end_function(p):
    """end_function : ENDFUNCTION"""
    add_trace(inspect.stack()[0][3], p)
    decrement_depth()


def p_inline_call_builtin(p):
    """inline_call : builtin_functions"""
    add_trace(inspect.stack()[0][3], p)
    p[0] = p[1]


def p_inline_call__parameter_free(p):
    """inline_call : ID '('  ')'"""
    add_trace(inspect.stack()[0][3], p)
    p[0] = f"{p[1]}()"


def p_inline_call_parameter_inclusive(p):
    """inline_call : ID '(' parameter_feed ')'"""
    add_trace(inspect.stack()[0][3], p)
    p[0] = f"{p[1]}({p[3]})"


# Parameter flow parsing


def p_parameter_definition_recursion(p):
    """parameter_definition : parameter_definition ',' parameter_definition"""
    add_trace(inspect.stack()[0][3], p)
    p[0] = f"{p[1]}, {p[3]}"


def p_parameter_definition__pass_by(p):
    """parameter_definition : BYREF parameter_definition
    | BYVAL parameter_definition"""
    p[0] = p[2]


def p_parameter_definition_init(p):
    """parameter_definition : ID ':' type_names"""
    add_trace(inspect.stack()[0][3], p)
    data_type = ""
    if p[3] == "DATE":
        util_line = "import datetime"
        try:
            parseLines.index(util_line)
        except ValueError:
            add_line(util_line)
        data_type = "datetime.date"
    elif p[3] == "REAL":
        data_type = "float"
    elif p[3] == "INTEGER":
        data_type = "int"
    elif p[3] == "CHAR":
        data_type = "str"
    elif p[3] == "STRING":
        data_type = "str"
    elif p[3] == "BOOLEAN":
        data_type = "bool"
    p[0] = f"{p[1]} : {data_type}"


def p_parameter_feed_recursion(p):
    """parameter_feed : parameter_feed ',' parameter_feed"""
    add_trace(inspect.stack()[0][3], p)
    p[0] = f"{p[1]}, {p[3]}"


def p_parameter_feed_init(p):
    """parameter_feed : expression
    | boolean_expression
    | symbol_reference
    | data_types
    | inline_call"""
    add_trace(inspect.stack()[0][3], p)
    p[0] = str(p[1])


# == Built-in functions


# Catch-all builtin function handling
def p_builtin_functions(p):
    """builtin_functions : string_functions
    | number_functions"""
    add_trace(inspect.stack()[0][3], p)
    p[0] = p[1]


# String functions
def p_string_functions(p):
    """string_functions : left_string_function
    | right_string_function
    | mid_string_function
    | one_parameter_string_function"""
    add_trace(inspect.stack()[0][3], p)
    p[0] = p[1]


def p_left_string_function(p):
    """left_string_function : LEFT '(' string_reference ',' expression ')'"""
    add_trace(inspect.stack()[0][3], p)
    p[0] = f"{p[3]}[:{p[5]}]"


def p_right_string_function(p):
    """right_string_function : RIGHT '(' string_reference ',' expression ')'"""
    add_trace(inspect.stack()[0][3], p)
    p[0] = f"{p[3]}[len({p[3]}) - ({p[5]}):]"


def p_mid_string_function(p):
    """mid_string_function : MID '(' string_reference ',' expression ',' expression ')'"""
    add_trace(inspect.stack()[0][3], p)
    p[0] = f"{p[3]}[({p[5]}-1):(({p[5]}-1)+{p[7]})]"


def p_one_parameter_string_function(p):
    """one_parameter_string_function : one_parameter_string_function_cases '(' string_reference ')'"""
    add_trace(inspect.stack()[0][3], p)
    if p[1] == "LENGTH":
        p[0] = f"len({p[3]})"
    elif p[1] == "LCASE":
        p[0] = f"{p[3]}.lower()"
    elif p[1] == "UCASE":
        p[0] = f"{p[3]}.upper()"


def p_one_parameter_string_function_cases(p):
    """one_parameter_string_function_cases : LENGTH
    | LCASE
    | UCASE"""
    add_trace(inspect.stack()[0][3], p)
    p[0] = p[1]


# Numeric functions
def p_number_functions(p):
    """number_functions : int_number_function
    | rand_number_function"""
    add_trace(inspect.stack()[0][3], p)
    p[0] = p[1]


def p_int_number_function(p):
    """int_number_function : INT '(' expression ')'"""
    add_trace(inspect.stack()[0][3], p)
    p[0] = f"int({p[3]})"


def p_rand_number_function(p):
    """rand_number_function : RAND '(' expression ')'"""
    add_trace(inspect.stack()[0][3], p)
    add_line_if_not_found(
        "from random import randint as rand # Added by transpiler to add random support"
    )
    p[0] = f"rand(1, {p[3]})"


# == I/O

# File operations


def p_file_operation(p):
    """file_operation : open_file
    | read_file
    | write_file
    | close_file"""
    add_trace(inspect.stack()[0][3], p)


def p_open_file(p):
    """open_file : OPENFILE file_id FOR file_modes"""
    mode = str()
    add_trace(inspect.stack()[0][3], p)
    for modeTranslate in [["READ", "rt"], ["WRITE", "wt"], ["APPEND", "at"]]:
        if p[4] == modeTranslate[0]:
            mode = modeTranslate[1]
    add_line_if_not_found("fileDict = dict() # Utility dictionary, from transpiler")
    bb = ["{", "}"]
    add_line(f"fileDict.update({bb[0]}{p[2]}: open({p[2]}, '{mode}'){bb[1]})")


def p_read_file(p):
    """read_file : READFILE file_id ',' symbol_reference"""
    add_trace(inspect.stack()[0][3], p)
    add_line(f"{p[4]} = fileDict[{p[2]}].readline()")


def p_write_file(p):
    """write_file : WRITEFILE file_id ',' boolean_expression
    | WRITEFILE file_id ',' expression
    | WRITEFILE file_id ',' symbol_reference
    | WRITEFILE file_id ',' data_types"""
    add_trace(inspect.stack()[0][3], p)
    add_line(f"fileDict[{p[2]}].write(str({p[4]}) + '\\n')")


def p_close_file(p):
    """close_file : CLOSEFILE file_id"""
    add_trace(inspect.stack()[0][3], p)
    add_line(f"fileDict[{p[2]}].close()")


def p_file_mappings(p):
    """file_modes : READ
                 | WRITE
                 | APPEND
    file_id : STRINGTYPE
           | symbol_reference"""
    add_trace(inspect.stack()[0][3], p)
    p[0] = p[1]


# Console operations


# Input statements
def p_input(p):
    """input : INPUT symbol_reference"""
    add_trace(inspect.stack()[0][3], p)
    add_line(f"{p[2]} = input()")


# Output statements
def p_output(p):
    """output : OUTPUT output_types"""
    add_trace(inspect.stack()[0][3], p)
    add_line(f"print({p[2]})")


def p_output_multi(p):
    """output : OUTPUT output_multiple"""
    add_trace(inspect.stack()[0][3], p)
    add_line(f"print({p[2]}, sep='')")


def p_output_multiple(p):
    """output_multiple : output_multiple ',' output_multiple
    | output_types ',' output_types"""
    add_trace(inspect.stack()[0][3], p)
    p[0] = f"{p[1]}, {p[3]}"


# == Operand parsing

# Booleans Operations


def p_boolean_expression_operators__relational(p):
    """boolean_expression : boolean_expression EQUALTO boolean_expression
    | boolean_expression NOTEQUALTO boolean_expression
    | boolean_expression GREATEQUAL boolean_expression
    | boolean_expression LESSEQUAL boolean_expression
    | boolean_expression GREAT boolean_expression
    | boolean_expression LESS boolean_expression"""
    add_trace(inspect.stack()[0][3], p)
    if p[2] == "=":
        operator = "=="
    elif p[2] == "<>":
        operator = "!="
    else:
        operator = p[2]
    p[0] = f"{p[1]} {operator} {p[3]}"


def p_boolean_expression_operators__logical_and_or(p):
    """boolean_expression : boolean_expression AND boolean_expression
    | boolean_expression OR boolean_expression"""
    add_trace(inspect.stack()[0][3], p)
    if p[2] == "AND":
        p[0] = f"{p[1]} and {p[3]}"
    elif p[2] == "OR":
        p[0] = f"{p[1]} or {p[3]}"


def p_boolean_expression_operators__logical_not_01(p):
    """boolean_expression : boolean_expression NOT '(' boolean_expression ')'"""
    add_trace(inspect.stack()[0][3], p)
    p[0] = f"{p[1]} not ({p[4]})"


def p_boolean_expression_operators__logical_not_02(p):
    """boolean_expression : NOT '(' boolean_expression ')'"""
    add_trace(inspect.stack()[0][3], p)
    p[0] = f"not ({p[3]})"


# Arithmetic Operations
def p_expression_operands(p):
    """expression : expression '+' expression
    | expression '-' expression
    | expression '*' expression
    | expression '/' expression
    | expression DIV expression
    | expression MOD expression
    | expression '&' expression"""
    add_trace(inspect.stack()[0][3], p)
    if p[2] == "DIV":
        operator = "//"
    elif p[2] == "MOD":
        operator = "%"
    elif p[2] == "&":
        operator = "+"
    else:
        operator = p[2]
    p[0] = f"{p[1]} {operator} {p[3]}"


# == Data type handling


# Boolean expression terms
def p_boolean_expression__terms(p):
    """boolean_expression : BOOLEANTYPE
    | symbol_reference
    | BOOLEAN
    | expression"""
    add_trace(inspect.stack()[0][3], p)
    p[0] = p[1]


# Arithmetic expression terms
def p_expression_terms(p):
    """expression : symbol_reference
    | INTEGERTYPE
    | REALTYPE
    | inline_call"""
    add_trace(inspect.stack()[0][3], p)
    p[0] = p[1]


# Output data type handling
def p_output_types(p):
    """output_types : boolean_expression
    | symbol_reference
    | data_types
    | expression"""
    add_trace(inspect.stack()[0][3], p)
    p[0] = p[1]


# Primitive data types
def p_data_types(p):
    """data_types : string_reference
    | CHARTYPE
    | DATETYPE"""
    add_trace(inspect.stack()[0][3], p)
    p[0] = p[1]


# Data type names
def p_type_names(p):
    """type_names : DATE
    | REAL
    | INTEGER
    | CHAR
    | STRING
    | BOOLEAN"""
    add_trace(inspect.stack()[0][3], p)
    p[0] = p[1]


# Bracket support for expressions
def p_expression_group(p):
    """expression : '(' expression ')'"""
    add_trace(inspect.stack()[0][3], p)
    p[0] = f"({p[2]})"


# Bracket support for boolean expressions
def p_boolean_expression__group(p):
    """boolean_expression : '(' boolean_expression ')'"""
    add_trace(inspect.stack()[0][3], p)
    p[0] = f"({p[2]})"


# String handling
def p_string_reference__base(p):
    """string_reference : STRINGTYPE
    | symbol_reference"""
    add_trace(inspect.stack()[0][3], p)
    p[0] = p[1]


def p_string_reference__concat(p):
    """string_reference : string_reference '&' string_reference"""
    add_trace(inspect.stack()[0][3], p)
    p[0] = f"{p[1]}+{p[3]}"


# Identifier resolution
def p_symbol_reference(p):
    """symbol_reference : ID
    | array_reference"""
    add_trace(inspect.stack()[0][3], p)
    p[0] = p[1]


def p_array_reference__2d(p):
    """array_reference : ID '[' expression ',' expression ']'"""
    add_trace(inspect.stack()[0][3], p)
    p[0] = f"{p[1]}[{p[3]} - 1][{p[5]} - 1]"


def p_array_reference__1d(p):
    """array_reference : ID '[' expression ']'"""
    add_trace(inspect.stack()[0][3], p)
    p[0] = f"{p[1]}[{p[3]} - 1]"


# Error handling
def p_error(p):
    add_trace(inspect.stack()[0][3], p)
    if p is None:
        stackTrace[-1] += "(Blank line)"
        add_line("")
    else:
        print(f"Syntax error in input! Token in context: {p}")
        add_line(f"#=== ERROR PARSING {p} ===#")


# Build parser
parser = yacc.yacc()

# Function to parse given string


def parse(text: str = "") -> tuple[list, list]:
    """Parses parameter string and transpiles pseudocode to python.
    Returns a tuple with list of parsed lines and another list with stack trace

    Args:
    - `text` (str): Text to parse

    Returns:
    - tuple[`parseLines`, `stackTrace`]
    - `parseLines` (list): A list with transpiled python lines"""
    parser.parse(text)
    return parseLines, stackTrace
