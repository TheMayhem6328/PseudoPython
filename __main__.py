from pseudotoken import Tokenizer

lexer = Tokenizer()
lexer.build()

tokenList = list(lexer.tokenize("Main.mayudo"))
for token in tokenList:
    #print(f"Type: -|{token.type}|- ||| Line: {token.lineno} ||| Char: {token.lexpos} ||| Val : -|{token.value}|-")
    print(token)