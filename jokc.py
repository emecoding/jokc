from posixpath import splitext
import sys, os
from Console import *
from Arguments import *

#jokc -f main.jokc -d Compiles/ -o test_run

FILE_TO_PARSE: str = ""
FILE_TO_PASS_DATA: str = ""

EVERY_ATTRIBUTE = []

def createCppFile(name):
    global FILE_TO_PASS_DATA
    n = name.replace(".jokc", ".cpp")
    FILE_TO_PASS_DATA = n
    if os.path.isfile(n) == False:
        with open(n, "w+") as file:
            file.close()

def argIsInEVERY_ARG(arg):
    for i in EVERY_COMPILE_ARG:
        if i["arg"] == arg:
            return i

    return None

def getArgumentValue(arg, args):
    j = 0
    for i in args:
        if i == arg:
            return args[j + 1]
        j += 1

def compileCommands():
    global FILE_TO_PARSE
    args = sys.argv
    args.remove(args[0])

    for i in range(len(args)):
        arg = args[i]
        a = argIsInEVERY_ARG(arg)
        if a != None:
            if i >= len(args) - 1:
                raiseCommandArgumentError(a)

            if a["arg"] == FILE_NAME["arg"]:
                path = getArgumentValue(COMPILE_DIRECTORY["arg"], args)
                createCppFile(path + args[i + 1])
            if a["arg"] == FILE_NAME["arg"]:
                FILE_TO_PARSE = args[i + 1]

def createAttritubeFromLine(line, line_number):
    Attribute: str = ""
    i = 0
    for l in line:
        if l in EVERY_BUILT_IN_DATA_TYPE:
            dataType = line[i]
            name = line[i + 1]
            value = line[1 + 2]
            Attribute = f"{dataType} {name} = {value}"
            a = {"type": dataType, "name": name, "value": value}
            EVERY_ATTRIBUTE.append(a)
            return Attribute
        else:
            for attribute in EVERY_ATTRIBUTE:
                name = line[i]
                value = line[i + 2]
                if attribute["name"] == name:
                    Attribute = f"{attribute['name']} = {value}"
                    a = {"type": attribute["type"], "name": name, "value": value}
                    EVERY_ATTRIBUTE.append(a)
                    return Attribute
                else:
                    raiseNotProperDataTypeError(line_number + 1, l)
    i += 1

    return Attribute

def convertListToString(lst):
    s: str = ""
    for i in lst:
        s += i

    return s

def functionHasBrackets(function):
    brackets = 0
    for i in function:
        if i == "(": brackets += 1
        elif i == ")":
            brackets += 1
            break

    if brackets == 2: return True
    else: return False



def createFunction(lines, line_num):
    finalLines = []
    ln = line_num
    for line in range(len(lines)):
        splitted_line = lines[line].split(" ")
        if FUNCTION_FLAG["name"] in splitted_line[0]:
            splitted_line[-1] = splitted_line[-1].replace("\n", "")
            n = splitted_line[1].replace("(", "")
            n = n.replace(")", "")
            n = n.replace("{", "")
            functionName = n
            if functionHasBrackets(splitted_line[1]):
                l = FUNCTION_FLAG["compensation"] + " " + functionName + "(){\n"
                finalLines.insert(ln, l)
            else:
                raiseInvalidFunctionDeclarationError(ln)
        else:
            finalLines.insert(ln, lines[line])
            ln += 1
        

    finalLinesStr = convertListToString(finalLines)
    return finalLinesStr, finalLines

def parseJOKCFile():
    global FILE_TO_PARSE, FILE_TO_PASS_DATA
    lines = []
    with open(FILE_TO_PARSE, "r") as file:
        lines = file.readlines()
        file.close()

    finalLines = []
    for line_num in range(len(lines)):
        line = lines[line_num]
        splitted_line = line.split(" ")
        if splitted_line[0] != "\n":
            isCommented = splitted_line[0].find(COMMENT_FLAG["name"])
            functioned = False
            if isCommented == -1:
                hasLineEnd = splitted_line[-1].find(END_LINE_FLAG["name"])
                if FUNCTION_FLAG["name"] in splitted_line:
                    functioned = True
                    ls = []
                    for i in range(line_num, len(lines)):
                        splitted = lines[i].split(" ")
                        if splitted[0] != "\n":
                            if splitted[0] != "};\n":
                                ls.append(lines[i])
                            else:
                                function, functionLines = createFunction(ls, line_num)
                                finalLines.insert(line_num, function)
                                break
                    continue
                if hasLineEnd == -1:
                    raiseNoLineEndFlagFoundError(line_num)
                elif ASSING_VALUE_FLAG["name"] in splitted_line:
                    if functioned == False:
                        print(splitted_line, line_num)
                        attribute = createAttritubeFromLine(splitted_line, line_num)           
                        finalLines.insert(line_num, attribute)
                else:
                    attribute = convertListToString(line)
                    finalLines.insert(line_num, attribute)
            else:
                attribute = convertListToString(line)
                finalLines.insert(line_num, attribute)

    #print(finalLines)
    finalString: str = convertListToString(finalLines)

    with open(FILE_TO_PASS_DATA, "w+") as file:
        file.write(finalString)
        file.close()

if __name__ == "__main__":
    compileCommands()
    if FILE_TO_PARSE == "":
        raiseNoCompileFileFoundError()
    else:
        parseJOKCFile()



