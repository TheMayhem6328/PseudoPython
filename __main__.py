from pseudotoken import Tokenizer
import pseudoyacc as Parser

file = open("Main.mayudo", encoding="utf8")
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

def stackTrace():
    print("Stack Trace:")
    print("==============")
    count = 0
    lineTrace = []
    newTrace  = []
    for trace in parse[1]:
        if trace in ["p_root [None]", "(Blank line)"]:
            print("----LINE----")
        else:
            print(trace)

# Uncomment below line to print out trace
stackTrace()
