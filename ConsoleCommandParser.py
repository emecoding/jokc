from Console import *
import os, sys

def createCppFile(name, exe_file_dir):
    EXE_FILE_DIRECTORY, EXE_FILE_FULL_DIRECTORY = exe_file_dir, ""
    n = name.replace(".jokc", ".cpp")
    FILE_TO_PASS_DATA = n
    EXE_FILE_FULL_DIRECTORY = (EXE_FILE_DIRECTORY + FILE_TO_PASS_DATA)
    print(FILE_TO_PASS_DATA)
    if os.path.isfile(EXE_FILE_FULL_DIRECTORY) == False:
        with open(EXE_FILE_FULL_DIRECTORY, "w+") as file:
            file.close()

    return EXE_FILE_DIRECTORY, EXE_FILE_FULL_DIRECTORY

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
    FILE_TO_PARSE, FILE_TO_PASS_DATA, EXE_FILE_DIRECTORY = "", "", ""
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

    EXE_FILE_DIRECTORY, EXE_FILE_FULL_DIRECTORY = createCppFile(FILE_TO_PARSE.split(os.sep)[-1], EXE_FILE_DIRECTORY)
    #print(FILE_TO_PARSE, EXE_FILE_DIRECTORY, EXE_FILE_NAME, EXE_FILE_FULL_DIRECTORY)
    return EXE_FILE_DIRECTORY, EXE_FILE_FULL_DIRECTORY, EXE_FILE_NAME, FILE_TO_PARSE