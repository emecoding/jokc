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
        self.__EVERY_IMPORT = []

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
            print("Running the program...")
            print("--------------------------------------------")
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

        lines.insert(0, NEW_LINE_FLAG)
        lines[-1] += NEW_LINE_FLAG
        return lines

    def __lineIsCommented(self, line):
        if line.find(COMMENT_FLAG["name"]) != -1:
            return True
        return False

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
        else: return False, finalLines
    
    def __lineIsImport(self, Line):
        if Line.find(IMPORT_FLAG["name"]) != -1:
            splittedLine = Line.split(IMPORT_FLAG["name"])
            importName = splittedLine[1]
            importName = importName.replace(" ", "")
            return IMPORT_FLAG["compensation"] + importName, importName.replace('"', "")
        
        return False, None

    def __lineIsBuiltInFunction(self, Line, lineNum):
        splittedLine = Line.split("(")
        if len(splittedLine) == 2:
            funcName = splittedLine[0]
            for func in EVERY_BUILT_IN_FUNCTION:
                if func["name"] == funcName:
                    imports = func["requiredImports"]
                    args = func["args"]
                    finalFunc = func["compensation"]

                    
                    givenAttritubes = splittedLine[1]
                    givenAttritubes = givenAttritubes.replace(")", "")
                    givenAttritubes = givenAttritubes.replace(END_LINE_FLAG["name"], "")
                    givenAttritubes = givenAttritubes.replace(",", "")
                    givenAttritubes = givenAttritubes.split(" ")
                    
                    if len(givenAttritubes) != len(args): raiseInvalidFunctionDeclarationError(lineNum)

                    for arg in range(len(args)):
                        finalFunc = finalFunc.replace(args[arg], givenAttritubes[arg])
                    
                    finalFunc = f"{finalFunc}{END_LINE_FLAG['compensation']}{NEW_LINE_FLAG}"
                    return finalFunc, imports


        return False, None

    def __parseLine(self, Line, lineNum, finalLines):
        Line = Line.replace(NEW_LINE_FLAG, "")
        if self.__lineIsCommented(Line) == False:

            lineIsImport, importName = self.__lineIsImport(Line)
            lineIsBuiltInFunction, requiredImports = self.__lineIsBuiltInFunction(Line, lineNum)
            if lineIsImport:
                if importName not in self.__EVERY_IMPORT:
                    self.__EVERY_IMPORT.append(importName)
                    finalLines.insert(lineNum, lineIsImport + NEW_LINE_FLAG)
                return finalLines
            elif lineIsBuiltInFunction:
                for IMPORT in requiredImports:
                    if IMPORT not in self.__EVERY_IMPORT:
                        self.__EVERY_IMPORT.append(IMPORT)
                        r = f"{IMPORT_FLAG['compensation']} <{IMPORT}>{NEW_LINE_FLAG}"
                        finalLines.insert(0, r)

                finalLines.insert(lineNum, lineIsBuiltInFunction)

                return finalLines

            self.__checkForEndLineFlag(Line, lineNum)
            attritube, finalLines = self.__checkForAttributeAssignment(Line, lineNum, finalLines)

            if attritube == False:
                finalLines.insert(lineNum, Line + NEW_LINE_FLAG)


        return finalLines

    def __isFunctionReturnType(self, line):
        for t in EVERY_BUILT_IN_FUNCTION_RETURN_TYPE:
            if line.find(t["name"]) != -1:
                return t
        
        return False

    def __gatherFunctionLines(self, Lines: list, lineNum: int):
        funcLines = []
        funcName = ""
        for l in range(lineNum, len(Lines)):
            line = Lines[l]
            if line != "}" + END_LINE_FLAG["name"]:
                funcReturnType = self.__isFunctionReturnType(line)
                if funcReturnType != False:
                    splittedLine = line.split(" ")
                    funcName = splittedLine[1]
                    funcName = funcName.replace("(", "")
                    funcName = funcName.replace(")", "")
                    funcName = funcName.replace("{", "")
                    funcName = funcName.replace(NEW_LINE_FLAG, "")

                    a = f"{funcReturnType['compensation']} {funcName}()" + '{' + NEW_LINE_FLAG
                    funcLines.insert(l, a)
                else:
                    if line != NEW_LINE_FLAG:
                        line = line.replace(NEW_LINE_FLAG, "")
                        self.__parseLine(line, l, funcLines)

        #print(funcLines)

        #funcLines.append("}" + END_LINE_FLAG["compensation"])

        return funcLines


    def __checkForEndLineFlag(self, Line: str, lineNum: int):
        if len(Line) != 0:
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
            if Line != NEW_LINE_FLAG:
                Line = Line.replace(NEW_LINE_FLAG, "")
                funcReturnType = self.__isFunctionReturnType(Line)
                if funcReturnType != False: 
                    funcLines = self.__gatherFunctionLines(Lines, line_num)
                    #print(funcLines[1][-1], "LINES")
                    for funcLine in funcLines:
                        finalLines.insert(line_num, funcLine)
                        line_num += 1
                        if line_num >= len(Lines):
                            line_num = len(Lines) - 1
                    continue
                else:
                    if Line.find("};") == -1:
                        finalLines = self.__parseLine(Line, line_num, finalLines)
            line_num += 1
            if line_num >= len(Lines):
                break

        print("Parsing done...")
        #print(finalLines)
        self.__writeToCppFile(finalLines)
        