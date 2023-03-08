from pseudotoken import Tokenizer
import pseudoyacc as Parser

file = open("Main.mayudo")
data = file.readlines()

for line in range(len(data)):
    data[line] = data[line].removesuffix("\n")

print("\nTokens:\n==========")
for line in range(len(data)):
    print(f"Line {line + 1}:")
    tokenList = list(Tokenizer.tokenize(data[line]))
    for token in tokenList: print(token)
    print("")
print("")

for line in data:
    parse = Parser.parse(line)
print("Transpiled python code:")
print("=========================")
print("--[BEGIN PYTHON CODE]--")
for line in parse[0]:
    print(line)
print("--[END  PYTHON  CODE]--\n\n")

print("Stack Trace:")
print("==============")
rootCount = 0
for trace in range(len(parse[1])):
    element = parse[1][-(trace+1)]
    if element == "p_root":
        if rootCount > 0:
            print("")
        rootCount += 1
        print(f"Line {rootCount + 1}:")
    print(element)
