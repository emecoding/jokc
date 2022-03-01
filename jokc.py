
from Console import *
from Arguments import *
from ConsoleCommandParser import *
from JOKCParser import *

#jokc -f jockcs/Attribute.jokc -d Compiles/ -o test_run

FILE_TO_PARSE: str = ""
FILE_TO_PASS_DATA: str = ""
EXE_FILE_NAME: str = ""
EXE_FILE_DIRECTORY: str = ""
EXE_FILE_FULL_DIRECTORY: str = ""

EVERY_ATTRIBUTE = []

PARSER = JOCKParser()
PARSER.setRunExeStraight(False)


if __name__ == "__main__":
    #EXE_FILE_DIRECTORY, EXE_FILE_FULL_DIRECTORY, EXE_FILE_NAME, FILE_TO_PASS_DATA, FILE_TO_PARSE = compileCommands()
    EXE_FILE_DIRECTORY, EXE_FILE_FULL_DIRECTORY, EXE_FILE_NAME, FILE_TO_PARSE = compileCommands()
    print(EXE_FILE_DIRECTORY, EXE_FILE_FULL_DIRECTORY, EXE_FILE_NAME, FILE_TO_PARSE)
    if FILE_TO_PARSE == "":
        raiseNoCompileFileFoundError()
    else:
        #parseJOKCFile()
        PARSER.setFileToParse(FILE_TO_PARSE)
        PARSER.setFileToPassData(EXE_FILE_FULL_DIRECTORY)
        PARSER.setExeFileName(EXE_FILE_NAME)
        PARSER.parse()



