from BuiltInFunctionContents import *

EVERY_COMPILE_ARG = []
EVERY_FLAG = []
EVERY_BUILT_IN_DATA_TYPE = []
EVERY_BUILT_IN_FUNCTION = []
EVERY_BUILT_IN_FUNCTION_RETURN_TYPE = []

def addBuiltInDataType(name, compensation:str="", requiredImports:list=[]):
    if compensation == "":
        compensation = name
    f = {"name": name, "compensation": compensation, "requiredImports": requiredImports}
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

def addBuiltIntFunction(name:str, compensation:str, args:list, requiredImports: list):
    global EVERY_BUILT_IN_FUNCTION
    func = {"name": name, "compensation": compensation, "args": args, "requiredImports": requiredImports}
    EVERY_BUILT_IN_FUNCTION.append(func)
    return func

def addFunctionReturnType(name, compensation:str=""):
    if compensation == "":
        compensation = name
    f = {"name": name, "compensation": compensation}
    EVERY_BUILT_IN_FUNCTION_RETURN_TYPE.append(f)
    return f


NEW_LINE_FLAG = "\n"

INT = addBuiltInDataType("int")
STRING = addBuiltInDataType("str", compensation="std::string", requiredImports=["string"])
FLOAT = addBuiltInDataType("flt", compensation="float")
LIST = addBuiltInDataType("lst", compensation="std::vector", requiredImports=["vector"])
DOUBLE = addBuiltInDataType("db", compensation="double")

PRINT_FUNCTION = addBuiltIntFunction("print", compensation=PRINT, args=["a1"], requiredImports=["iostream"])
GET_INPUT_FUNCTION = addBuiltIntFunction("input", compensation=INPUT, args=["result", "text"], requiredImports=["iostream"])

ASSING_VALUE_FLAG = addFlag("=")
END_LINE_FLAG = addFlag(";")
COMMENT_FLAG = addFlag("//")
IMPORT_FLAG = addFlag("import", compensation="#include")

FUNCTION_VOID_FLAG = addFunctionReturnType("def", compensation="void")
FUNCTION_INT_FLAG = addFunctionReturnType("dif", compensation="int")




FILE_NAME = addCommandArg("-f", "file_name")
COMPILE_DIRECTORY = addCommandArg("-d", "compile_directory")
EXE_NAME = addCommandArg("-o", "name")
INCLUDE_DIRECTORY = addCommandArg("-i", "include_directory")

