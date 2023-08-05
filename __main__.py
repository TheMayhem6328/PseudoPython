import pseudotoken as tokenizer
import pseudoyacc as parser

file = open("Main.mayudo", encoding="utf8")
data = file.readlines()

for line in range(len(data)):
    data[line] = data[line].removesuffix("\n")

print("\nTokens:\n==========")
for line in range(len(data)):
    print(f"Line {line + 1}:")
    tokenList = list(tokenizer.tokenize(data[line]))
    for token in tokenList:
        print(token)
    print("")
print("")

parse = ([], [])
for line in data:
    parse = parser.parse(line)
print("Transpiled python code:")
print("=========================")
print("--[BEGIN PYTHON CODE]--")
for line in parse[0]:
    print(line)
print("--[END  PYTHON  CODE]--\n\n")


def stack_trace():
    print("Stack Trace:")
    print("==============")
    for trace in parse[1]:
        if trace in ["p_root[None]", "p_error(Blank line)"]:
            print("----LINE----")
        else:
            print(trace)


# Uncomment below line to print out trace
# stack_trace()
