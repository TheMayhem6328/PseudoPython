from pseudotoken import Tokenizer

lexer = Tokenizer.lexer

# tokenList = list(lexer.tokenize("PRINT 2 + 3"))
tokenList = list(Tokenizer.tokenize(filename = "Main.mayudo"))
for token in tokenList:
    #print(f"Type: -|{token.type}|- ||| Line: {token.lineno} ||| Char: {token.lexpos} ||| Val : -|{token.value}|-")
    print(token)