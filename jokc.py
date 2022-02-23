import sys
from CommandArguments import *
from Console import *

#jokc -o name

FILE_TO_PARSE: str = ""

def createCppFile(name):
    n = name.replace(".jokc", ".cpp")
    with open(n, "w+") as file:
        file.close()

def argIsInEVERY_ARG(arg):
    for i in EVERY_ARG:
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

def parseJOKCFile():
    global FILE_TO_PARSE
    lines = []
    with open(FILE_TO_PARSE, "r") as file:
        lines = file.readlines()
        file.close()

    print(lines)


if __name__ == "__main__":
    compileCommands()
    if FILE_TO_PARSE == "":
        raiseNoCompileFileFoundError()
    else:
        parseJOKCFile()



