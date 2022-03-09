from shutil import ExecError
from Arguments import *

def raiseCommandArgumentError(argument: dict):
    MSG = f"No value found for argument '{argument['arg']}'({argument['argName']})"
    raise Exception(MSG)    

def raiseNoCompileFileFoundError():
    MSG = "Wasn't able to find the file you were looking for..."
    raise Exception(MSG)

def raiseNotProperDataTypeError(line_num, data_type):
    MSG = f"Couldn't find '{data_type}' type... (line {line_num + 1})"
    raise Exception(MSG)

def raiseNoLineEndFlagFoundError(line_num):
    MSG = f"Couldn't find '{END_LINE_FLAG['name']}' from line {line_num + 1}"
    raise Exception(MSG)

def raiseInvalidFunctionDeclarationError(line_num):
    MSG = f"Invalid function declaration(line {line_num + 1})"
    raise Exception(MSG)

def raiseInvalidImportDeclarationError(line_num):
    MSG = f"Invalid import declaration(line {line_num + 1})"
    raise Exception(MSG)

def raiseInvalidCompilerArgumentError(arg):
    MSG = f"'{arg}' is not a regonized argument for jokc compiler..."
    raise Exception(MSG)

def raiseInvalidAttritubeAssignmentError(line_num):
    MSG = f"Invalid attritube assigment at line {line_num + 1}"
    raise Exception(MSG)

def raiseInvalidIfStatementError(lineNum):
    MSG = f"Invalid If statement on line {lineNum + 1}"
    raise Exception(MSG)