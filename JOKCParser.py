
from Arguments import *
from Console import *

class JOCKParser:
    def __init__(self):
        self.__file_to_parse = ""

    def __getLines(self):
        lines = []
        with open(self.__file_to_parse, "r") as file:
            lines = file.readlines()
            file.close()

        return lines

    def __checkForAttributeAssignment(self, Line: str):
        splittedLine = Line.split(ASSING_VALUE_FLAG["name"])
        print(splittedLine)

    def __checkForEndLineFlag(self, Line: str, lineNum: int):
        hasEndLineFlag = (Line[-1] == END_LINE_FLAG["name"])
        if hasEndLineFlag == False: raiseNoLineEndFlagFoundError(lineNum)

    def setFileToParse(self, file):
        self.__file_to_parse = file


    def parse(self):
        Lines = self.__getLines()

        line_num = 0
        for L in range(len(Lines)):
            Line = Lines[line_num]
            self.__checkForEndLineFlag(Line, line_num)


            line_num += 1
        