from pseudotoken import Tokenizer
import pseudoyacc as Parser

file = open("Main.mayudo")
data = file.readlines()

for line in range(len(data)):
    data[line] = data[line].removesuffix("\n")

for line in data:
    parse = Parser.parse(line)
print("Converted to python code:")
print("=========================")
print("[BEGIN PYTHON CODE]")
for line in parse[0]:
    print(line)
print("[END  PYTHON  CODE]")