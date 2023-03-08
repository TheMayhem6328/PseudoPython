def escapedString(string : str) -> str:
    newString = ""
    for pos in range(len(string)):
        if   string[pos] == "\"" : newString += '\\"'
        elif string[pos] == "\'" : newString += "\\'"
        elif string[pos] == "\n" : newString += "\\n"
        elif string[pos] == "\t" : newString += "\\t"
        elif string[pos] == "\\" : newString += "\\\\"
        else: newString += string[pos]
    return newString
