
from typing import List, final
from Arguments import *
from Console import *

class JOCKParser:
    def __init__(self):
        self.__file_to_parse = ""

        self.__EVERY_ATTRITUBE = []

    def __convertListToString(self, lst: list):
        s: str = ""
        for i in lst:
            s += i

        return s

    def __getLines(self):
        lines = []
        with open(self.__file_to_parse, "r") as file:
            lines = file.readlines()
            file.close()

        return lines

    def __checkForAttributeAssignment(self, Line: str, lineNum: int, finalLines: list):
        if Line.find(ASSING_VALUE_FLAG["name"]) != -1:
            splittedLine = Line.split(ASSING_VALUE_FLAG["name"])
            splittedLine0 = splittedLine[0].split(" ")
            if splittedLine0[-1] == "": splittedLine0.remove(splittedLine0[-1])
            
            if len(splittedLine0) == 2:
                type = splittedLine0[0]
                name = splittedLine0[1]
                value = splittedLine[1].replace(" ", "")
                value = value.replace(END_LINE_FLAG["name"], "")
                #print(f"Type: {type}, Name: {name}, Value: {value}")
                
                for DATATYPE in EVERY_BUILT_IN_DATA_TYPE:
                    if DATATYPE["name"] == type:
                        attritube_str = f"{DATATYPE['compensation']} {name} {ASSING_VALUE_FLAG['compensation']} {value}{END_LINE_FLAG['compensation']}{NEW_LINE_FLAG}"
                        finalLines.insert(lineNum, attritube_str)
                        a = {"type": type, "name": name, "value": value}
                        self.__EVERY_ATTRITUBE.append(a)
                        return attritube_str, finalLines

                raiseNotProperDataTypeError(lineNum, type)

            elif len(splittedLine0) == 1:
                #Update attritube
                name = splittedLine0[0]
                value = splittedLine[1].replace(" ", "")
                value = value.replace(END_LINE_FLAG["name"], "")

                for attritube in self.__EVERY_ATTRITUBE:
                    if attritube["name"] == name:
                        attritube["value"] = value
                        attritube_str = f"{attritube['name']} {ASSING_VALUE_FLAG['compensation']} {attritube['value']}{END_LINE_FLAG['compensation']}{NEW_LINE_FLAG}"
                        finalLines.insert(lineNum, attritube_str)
                        return attritube_str, finalLines
            else:
                raiseInvalidAttritubeAssignmentError(lineNum)
        else: return False, None
        

    def __checkForEndLineFlag(self, Line: str, lineNum: int):
        hasEndLineFlag = (Line[-1] == END_LINE_FLAG["name"])
        if hasEndLineFlag == False: raiseNoLineEndFlagFoundError(lineNum)

    def setFileToParse(self, file):
        self.__file_to_parse = file


    def parse(self):
        Lines = self.__getLines()
        finalLines: list = []
        line_num = 0
        for L in range(len(Lines)):
            Line = Lines[line_num]
            Line = Line.replace(NEW_LINE_FLAG, "")

            self.__checkForEndLineFlag(Line, line_num)
            attritube, finalLines = self.__checkForAttributeAssignment(Line, line_num, finalLines)
            line_num += 1

        print(self.__convertListToString(finalLines))
        