from posixpath import splitext
from stat import FILE_ATTRIBUTE_ARCHIVE
import sys, os
from xml.dom.minidom import Attr
from Console import *
from Arguments import *

#jokc -f jockcs/Attribute.jokc -d Compiles/ -o test_run

FILE_TO_PARSE: str = ""
FILE_TO_PASS_DATA: str = ""
EXE_FILE_NAME: str = ""
EXE_FILE_DIRECTORY: str = ""
EXE_FILE_FULL_DIRECTORY: str = ""

EVERY_ATTRIBUTE = []

def createCppFile(name):
    global FILE_TO_PASS_DATA, EXE_FILE_DIRECTORY, EXE_FILE_FULL_DIRECTORY
    n = name.replace(".jokc", ".cpp")
    FILE_TO_PASS_DATA = n
    EXE_FILE_FULL_DIRECTORY = (EXE_FILE_DIRECTORY + FILE_TO_PASS_DATA)
    if os.path.isfile(EXE_FILE_FULL_DIRECTORY) == False:
        with open(EXE_FILE_FULL_DIRECTORY, "w+") as file:
            file.write("I")
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
    global FILE_TO_PARSE, FILE_TO_PASS_DATA, EXE_FILE_DIRECTORY
    args = sys.argv
    args.remove(args[0])
    
    line = 0
    for i in range(len(args)):
        arg = args[line]
        a = argIsInEVERY_ARG(arg)
        if a != None:
            if i >= len(args) - 1:
                raiseCommandArgumentError(a)

            #print(getArgumentValue(arg, args))
            if arg == FILE_NAME["arg"]:
                FILE_TO_PARSE = getArgumentValue(arg, args)
                line += 2
            elif arg == COMPILE_DIRECTORY["arg"]:
                EXE_FILE_DIRECTORY = getArgumentValue(arg, args)
                line += 2
            elif arg == EXE_NAME["arg"]:
                EXE_FILE_NAME = getArgumentValue(arg, args)
                line += 2
                if line >= len(args):
                    break
        else:
            raiseInvalidCompilerArgumentError(arg)    

    print(FILE_TO_PARSE, EXE_FILE_DIRECTORY, EXE_FILE_NAME)
    createCppFile(FILE_TO_PARSE.split(os.sep)[-1])
    
    


if __name__ == "__main__":
    compileCommands()
    if FILE_TO_PARSE == "":
        raiseNoCompileFileFoundError()
    else:
        #parseJOKCFile()
        pass



