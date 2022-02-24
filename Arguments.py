EVERY_COMPILE_ARG = []
EVERY_FLAG = []
EVERY_BUILT_IN_DATA_TYPE = []
EVERY_BUILD_IN_FUNCTION = []

def addBuiltInDataType(name, compensation:str=""):
    if compensation == "":
        compensation = name
    f = {"name": name, "compensation": compensation}
    EVERY_BUILT_IN_DATA_TYPE.append(f)
    return f

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

def addBuiltIntFunction(name, compensation, args):
    global EVERY_BUILD_IN_FUNCTION
    func = {"name": name, "compensation": compensation, "args": args}
    EVERY_BUILD_IN_FUNCTION.append(func)
    return func

INT = addBuiltInDataType("int")
STRING = addBuiltInDataType("string", compensation="std::string")

ASSING_VALUE_FLAG = addFlag("=")
END_LINE_FLAG = addFlag(";")
COMMENT_FLAG = addFlag("//")
FUNCTION_FLAG = addFlag("def", compensation="void")
IMPORT_FLAG = addFlag("import", compensation="#include")


FILE_NAME = addCommandArg("-f", "file_name")
COMPILE_DIRECTORY = addCommandArg("-d", "compile_directory")
EXE_NAME = addCommandArg("-o", "name")

