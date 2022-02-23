EVERY_ARG = []

def addArg(arg: str, argName: str):
    global EVERY_ARG
    a = {"arg" : arg, "argName" : argName}
    EVERY_ARG.append(a)

    return a

FILE_NAME = addArg("-f", "file_name")
COMPILE_DIRECTORY = addArg("-d", "compile_directory")
EXE_NAME = addArg("-o", "name")

