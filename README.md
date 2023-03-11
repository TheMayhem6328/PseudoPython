# PseudoPython

## Introduction

This is a transpiler for translating Cambridge's definition of pseudocode (which has been defined in [this](CambridgeGuide.pdf) guide) into Python code. Transpiled code is nearly always a one-on-one transpilation of the source code. I've been making this using Python - parsed with the help of the library [PLY (Python-Lex-Yacc)](https://github.com/dabeaz/ply).

## Installation

To install, simply clone the repository, open the resulting the directory in a terminal session and run [\_\_main\_\_.py](__main__.py).  
To edit the source pseudocode, simply edit [Main.mayudo](main.mayudo), enter your pseudocode there and save it. Then run [\_\_main\_\_.py](__main__.py) again. Further simplification en-route.

## Rationale

Pseudocode is by definition simply a series of code-like statements written using arbitrary syntax. Cambridge has a highly comprehensive guideline [(here)](CambridgeGuide.pdf) which outlines a rendition of pseudocode that is more akin to a complete, production-ready programming language. As per the same guide, in pseudocode-related questions, candidates are tested for their algorithm design and not for conforming to the Cambridge's outlined syntax - some schools tend to enforce it in their examinations regardless.

I personally learnt Python primarily through the means of experimenting with its syntax. I used to make random scripts and projects written in Python. Unfortunately, the same is not possible for pseudocode. Since pseudocode is not even a real language, no compiler or interpreter exist for it. This posed to be a challenge for me - I used to forget Cambridge's syntax very often. Also, I would appreciate pseudocode being functional one day.

That is why I set out to make a transpiler for pseudocode. I initially wanted to create an interpreter, but apparently directly executing the code is a tad bit more difficult than just translating it to Python line-by-line and then executing the general code - both served the same goal of making pseudocode executable, so since it was easier to process the latter while nSot impacting functionality, I went with that.

## Progress

So far, here's a checklist of what's complete and what's not:

- [X] **1** || Pseudocode in examined components
  - [X] **1.1** || Font style and size  
    Doesn't affect implementation
  - [X] **1.2** || Indentation  
    Handled using opening and closing keywords - for example,
    `IF` increases indent, whereas `ENDIF` decreases indent
  - [X] **1.3** || Case  
    Doesn't affect implementation
  - [X] **1.4** || Lines and line numbering  
    Doesn't affect implementation
  - [X] **1.5** || Comments  
    Inline comments not yet supported
- [X] **2** || Variables, constants and data types
  - [X] **2.1** || Data Types
    - [X] `INTEGER`
    - [X] `REAL`
    - [X] `CHAR`
    - [X] `STRING`
    - [X] `BOOLEAN`
    - [X] `DATE`  
    We handle dates by utilizing module `datetime`
  - [X] **2.2** || Literals
    - [X] Integer
    - [X] Real
    - [X] Char
    - [X] String
    - [X] Boolean
    - [X] Date  
    We handle dates by utilizing module `datetime`
  - [X] **2.3** || Identifiers  
    Due to how variables work in Python, a slight deviation
    from guideline: identifiers *are* case-sensitive
  - [X] **2.4** || Variable declarations  
    We just create a variable with blank value of the given data type
     instead. For example, we translate pseudocode statement
    `DECLARE Counter : INTEGER` to
    `Counter = int()`
  - [X] **2.5** || Constants  
    We just assign `<value>` to `<identifier>` and add a comment
    to indicate that this was a constant (we don't have the idea of
    constants in python, as far as I know). For example, we translate
    the pseudocode statement `CONSTANT HourlyRate = 6.50`
    to `HourlyRate = 6.50 # Constant`
  - [X] **2.6** || Assignments
    - [X] Operator variants
      - [X] `<-`
      - [X] `←`
- [ ] **3** || Arrays
  - [ ] **3.1** || Declaring arrays
    - [ ] Declaration
      - [ ] One-Dimensional
      - [ ] Two-Dimensional
  - [ ] **3.2** || Using arrays
    - [ ] Index reference
      - [ ] One-Dimensional
      - [ ] Two-Dimensional
- [ ] **4** || User-defined data types
  - [ ] **4.1** || Defining user-defined
    - [ ] Non-composite data types
      - [ ] Enumerated
      - [ ] Pointer
    - [ ] Composite data type
  - [ ] **4.2** || Using user-defined data types
- [ ] **5** || Common operations
  - [X] **5.1** || Input and output
    - [X] `INPUT`
    - [X] `OUTPUT`
  - [X] **5.2** || Arithmetic operations
    - [X] `+` Addition
    - [X] `-` Subtraction
    - [X] `*` Multiplication
    - [X] `/` Division
    - [X] `DIV` Integer division
    - [X] `MOD` Modulus
  - [X] **5.3** || Relational operations
    - [X] `>` Greater than
    - [X] `<` Less than
    - [X] `>=` Greater than or equal to
    - [X] `<=` Less than or equal to
    - [X] `=` Equal to
    - [X] `<>` Not equal to
  - [ ] **5.4** || Logic operations
    - [ ] AND
    - [ ] OR
    - [ ] NOT
  - [ ] **5.5** || String functions and operations
    - [ ] String functions
      - [ ] `RIGHT(ThisString : STRING, x : INTEGER) RETURNS STRING`
      - [ ] `LENGTH(ThisString : STRING) RETURNS INTEGER`
      - [ ] `MID(ThisString : STRING, x : INTEGER, y : INTEGER) RETURNS STRING`
      - [ ] `LCASE(ThisChar : CHAR) RETURNS CHAR`
      - [ ] `UCASE(ThisChar : CHAR) RETURNS CHAR`
    - [ ] Concatenation operator (&)
  - [ ] **5.6** || Numeric functions
    - [ ] `INT(x : REAL) RETURNS INTEGER`
    - [ ] `RAND(x : INTEGER) RETURNS REAL`
- [ ] **6** || Selection
  - [X] **6.1** || IF statements  
    Fortunately in pseudocode, for block-like logic, we have keywords
    more akin to opening and closing tags found in HTML. For example,
    `IF` always needs to be closed with `ENDIF`. We utilize this to know
    when to indent and not to indent. We could just use source indentation,
    but we don't. Let's say we have 12 spaces to indicate indentation.
    The guideline states that indents can be indicated by
    three or four spaces per level of indent depth - knowing that, is
    12 spaces three indents (since `12 / 4 = 3`)
    or four indents (since `12 / 3 = 4`) ? To avoid this ambiguity, we
    simply use the open-tag-close-tag concept as aforementioned.
    - [X] IF
    - [X] ELSE
    - [X] ENDIF
  - [ ] **6.2** || CASE statements
- [X] **7** || Iteration (repetition)
  - [X] **7.1** || Count-controlled (FOR) loops
  - [X] **7.2** || Post-condition (REPEAT) loops
  - [X] **7.3** || Pre-condition (WHILE) loops
- [ ] **8** || Procedures and functions
  - [X] **8.1** || Defining and calling procedures
    - [X] Definition
    - [X] Subroutine call (using keyword `CALL`)
  - [X] **8.2** || Defining and calling functions
    - [X] Definition
    - [ ] Subroutine call (inline)
  - [X] **8.3** || Passing parameters by value or by reference  
    We just ignore the presence of the keywords `BYREF` and `BYVAL`,
    since every passed parameter in Python (to my knowledge) is
    passed by reference
- [ ] **9** || File handling
  - [ ] **9.1** || Handling text files
    - [X] `OPENFILE` directive
    - [X] File modes
      - [X] `READ`
      - [X] `WRITE`
      - [X] `APPEND`
    - [X] `READFILE` directive
    - [ ] `EOF` function
    - [X] `WRITEFILE` directive
    - [X] `CLOSEFILE` directive
  - [ ] **9.2** || Handling random files
    - [ ] `RANDOM` file mode
    - [ ] `SEEK` directive
    - [ ] `GETRECORD` directive
    - [ ] `PUTRECORD` directive
- [ ] **10** || Object-oriented Programming
  - [ ] **10.1** || Methods and Properties
    - [ ] Declaration
    - [ ] Property access levels
      - [ ] Private
      - [ ] Public
  - [ ] **10.2** || Constructors and Inheritance
    - [ ] Constructors
    - [ ] Inheritance
