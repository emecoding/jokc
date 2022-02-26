import os
from Arguments import *
from Console import *

class JOCKParser:
    def __init__(self):
        self.__file_to_parse = ""
        self.__file_to_pass_data = ""
        self.__exe_file_name = ""

        self.__run_exe_stright: bool = False

        self.__EVERY_ATTRITUBE = []

    def __getCompileCppToExeCommands(self):
        #cmd = 'g++ -g $(find . -type f -iregex ".*\.cpp") glad.c -o idk -lglfw -ldl -lGL -I/home/eme/C++/OpenGl/Test/include'
        cmd1 = f'g++ {self.__file_to_pass_data} -o {self.__exe_file_name}'
        cmd2 = f'./{self.__exe_file_name}'

        return cmd1, cmd2

    def __convertListToString(self, lst: list):
        s: str = ""
        for i in lst:
            s += i

        return s

    def __compileCppFile(self):
        cmd1, cmd2 = self.__getCompileCppToExeCommands()
        print("Starting to compile to .exe file...")
        os.system(cmd1)
        print("Compiling to .exe done...")
        if self.__run_exe_stright:
            os.system(cmd2)

    def __writeToCppFile(self, lines):
        print("Starting to write to .cpp file...")
        self.__file_to_pass_data = self.__file_to_pass_data.replace(" ", "")

        with open(self.__file_to_pass_data, "w") as file:
            file.write(self.__convertListToString(lines))
            file.close()

        print("Writing to .cpp file done...")

        self.__compileCppFile()

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

    def setFileToPassData(self, file):
        self.__file_to_pass_data = file

    def setRunExeStraight(self, b):
        self.__run_exe_stright = b

    def setExeFileName(self, name):
        self.__exe_file_name = name

    def parse(self):
        print("Starting the parse....")
        Lines = self.__getLines()
        finalLines: list = []
        line_num = 0
        for L in range(len(Lines)):
            Line = Lines[line_num]
            Line = Line.replace(NEW_LINE_FLAG, "")

            self.__checkForEndLineFlag(Line, line_num)
            attritube, finalLines = self.__checkForAttributeAssignment(Line, line_num, finalLines)
            line_num += 1

        print("Parsing done...")
        self.__writeToCppFile(finalLines)
        