EVERY_COMPILE_ARG = []
EVERY_FLAG = []
EVERY_BUILT_IN_DATA_TYPE = []

def addBuiltInDataType(name):
    EVERY_BUILT_IN_DATA_TYPE.append(name)
    return name

def addFlag(name):
    EVERY_FLAG.append(name)
    return name

def addCommandArg(arg: str, argName: str):
    global EVERY_ARG
    a = {"arg" : arg, "argName" : argName}
    EVERY_COMPILE_ARG.append(a)

    return a

INT = addBuiltInDataType("int")
STRING = addBuiltInDataType("string")

ASSING_VALUE_FLAG = addFlag("=")

FILE_NAME = addCommandArg("-f", "file_name")
COMPILE_DIRECTORY = addCommandArg("-d", "compile_directory")
EXE_NAME = addCommandArg("-o", "name")

