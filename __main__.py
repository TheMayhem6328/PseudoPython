from pseudotoken import Tokenizer

tokenList = list(Tokenizer.tokenize("Main.mayudo"))
for token in tokenList:
    print(f"Type: {token.type} ||| Line: {token.lineno} ||| Char: {token.lexpos} ||| Val : {token.value}")