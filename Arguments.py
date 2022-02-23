EVERY_COMPILE_ARG = []
EVERY_FLAG = []
EVERY_BUILT_IN_DATA_TYPE = []

def addBuiltInDataType(name):
    EVERY_BUILT_IN_DATA_TYPE.append(name)
    return name

def addFlag(name, compensation:str=""):
    if compensation == "":
        compensation = name
    f = {"name": name, "compensation": compensation}
    EVERY_FLAG.append(f)
    return f

def addCommandArg(arg: str, argName: str):
    global EVERY_ARG
    a = {"arg" : arg, "argName" : argName}
    EVERY_COMPILE_ARG.append(a)

    return a

INT = addBuiltInDataType("int")
STRING = addBuiltInDataType("string")
CHAR = addBuiltInDataType("char")


ASSING_VALUE_FLAG = addFlag("=")
END_LINE_FLAG = addFlag(";")
COMMENT_FLAG = addFlag("//")
FUNCTION_FLAG = addFlag("def", compensation="void")

FILE_NAME = addCommandArg("-f", "file_name")
COMPILE_DIRECTORY = addCommandArg("-d", "compile_directory")
EXE_NAME = addCommandArg("-o", "name")

