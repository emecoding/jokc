import sys
from Console import *
from Arguments import *

#jokc -f main.jokc -d Compiles/ -o test_run

FILE_TO_PARSE: str = ""

def createCppFile(name):
    n = name.replace(".jokc", ".cpp")
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
    for l in line:
        print(l, EVERY_BUILT_IN_DATA_TYPE)
        if l in EVERY_BUILT_IN_DATA_TYPE:
            

            return Attribute
        else:
            raiseNotProperDataTypeError(line_number + 1, l)

    return Attribute


def parseJOKCFile():
    global FILE_TO_PARSE
    lines = []
    with open(FILE_TO_PARSE, "r") as file:
        lines = file.readlines()
        file.close()

    line_num = 0
    for line in lines:
        splitted_line = line.split(" ")
        if ASSING_VALUE_FLAG in splitted_line:
            attribute = createAttritubeFromLine(splitted_line, line_num)  
            print(attribute)          


        line_num += 1


if __name__ == "__main__":
    compileCommands()
    if FILE_TO_PARSE == "":
        raiseNoCompileFileFoundError()
    else:
        parseJOKCFile()



