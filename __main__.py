from pseudotoken import Tokenizer
import pseudoyacc as Parser

file = open("Main.mayudo")
data = file.read()

print(f"\nContent:\n==========\n[BEGIN FILE]\n{data}\n[END FILE]")
print("\nTokens:\n==========")
tokenList = list(Tokenizer.tokenize(data))
for token in tokenList: print(token)
print("\nOutput:\n==========")
stackTrace = Parser.parse(data)
print("\nTrace:\n==========")
for traceElement in stackTrace: print(traceElement)
print("\n")

file.close()