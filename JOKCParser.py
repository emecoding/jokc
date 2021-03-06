from ast import If, arg
from distutils.util import split_quoted
import os, shutil
from Arguments import *
from Console import *

class JOCKParser:
    def __init__(self):
        self.__file_to_parse = ""
        self.__file_to_pass_data = ""
        self.__exe_file_name = ""
        self.__include_directories = []

        self.__run_exe_stright: bool = False

        self.__EVERY_ATTRITUBE = []
        self.__EVERY_IMPORT = []
        self.__EVERY_INCLUDE_PATH = []
        

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
        if line.find(COMMENT_FLAG["name"]) != FIND_FAILED:
            return True
        return False

    def __checkForAttributeAssignment(self, Line: str, lineNum: int, finalLines: list):
        if Line.find(ASSING_VALUE_FLAG["name"]) != FIND_FAILED:
            splittedLine = Line.split(ASSING_VALUE_FLAG["name"])
            splittedLine0 = splittedLine[0].split(" ")
            if splittedLine0[-1] == "": splittedLine0.remove(splittedLine0[-1])
            
            if len(splittedLine0) == 2:
                type = splittedLine0[0]
                name = splittedLine0[1]

                lst = list(splittedLine[1])
                lst.remove(lst[0])
                value = self.__convertListToString(lst)
                value = value.replace(END_LINE_FLAG["name"], "")



                templateType = type.split("<")
                if len(templateType) > 1:
                    templateType = templateType[1].replace(">", "")
                else:
                    templateType = None
                
                for DATATYPE in EVERY_BUILT_IN_DATA_TYPE:
                    rt = type
                    if templateType != None:
                        rt = rt.replace(templateType, "")
                        rt = rt.replace(">", "")
                        rt = rt.replace("<", "")
                
                for DATATYPE in EVERY_BUILT_IN_DATA_TYPE:
                    if DATATYPE["name"] == templateType:
                        templateType = DATATYPE["compensation"]
                        break
                    
                for DATATYPE in EVERY_BUILT_IN_DATA_TYPE:
                    if DATATYPE["name"] == rt:
                        for IMPORT in DATATYPE["requiredImports"]:
                            if IMPORT not in self.__EVERY_IMPORT:
                                self.__EVERY_IMPORT.append(IMPORT)
                                finalLines.insert(0, IMPORT_FLAG["compensation"] + f" <{IMPORT}>{NEW_LINE_FLAG}")
                                break
                        attritube_str = ""
                        if DATATYPE["name"] == LIST["name"]:
                            attritube_str = f"{DATATYPE['compensation']}<{templateType}> {name} {ASSING_VALUE_FLAG['compensation']} {value}{END_LINE_FLAG['compensation']}{NEW_LINE_FLAG}"
                        else:    
                            attritube_str = f"{DATATYPE['compensation']} {name} {ASSING_VALUE_FLAG['compensation']} {value}{END_LINE_FLAG['compensation']}{NEW_LINE_FLAG}"

                        finalLines.insert(lineNum, attritube_str)
                        a = {"type": type, "templateType": str(templateType), "name": name, "value": value}
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
        if Line.find(IMPORT_FLAG["name"]) != FIND_FAILED:
            splittedLine = Line.split(IMPORT_FLAG["name"])
            importName = splittedLine[1]
            importName = importName.replace(" ", "")
            importName = importName.replace('"', "")

            return IMPORT_FLAG["compensation"] + '"' + importName + '"', importName.replace('"', "")
        
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
                    givenAttritubes = givenAttritubes.split(",")
                    if len(givenAttritubes) > 1:
                        a = 0
                        for attr in givenAttritubes:
                            if (attr[0] == "'" or attr[0] == '"'):
                                if (attr[-1] != "'" or attr[-1] != '"'):
                                    if (a + 1) >= len(givenAttritubes): 
                                        raiseInvalidFunctionDeclarationError(lineNum)
                                    else:
                                        attr2 = givenAttritubes[a + 1]
                                        givenAttritubes[a] = attr + " " + attr2
                                        givenAttritubes.remove(givenAttritubes[a + 1])
                                else:
                                    continue
                            else:
                                continue

                            a += 1

                    
                    if len(givenAttritubes) != len(args): raiseInvalidFunctionDeclarationError(lineNum)

                    for arg in range(len(args)):
                        finalFunc = finalFunc.replace(args[arg], givenAttritubes[arg])
                    
                    finalFunc = f"{finalFunc}{END_LINE_FLAG['compensation']}{NEW_LINE_FLAG}"
                    return finalFunc, imports


        return False, None

    def __isValidBuiltInType(self, arg, lineNum):
        for i in EVERY_BUILT_IN_DATA_TYPE:
            if i["name"] == arg:
                return True

        raiseNotProperDataTypeError(line_num=lineNum, data_type=arg)

    def __checkForLoop(self, Line, lineNum):
        splittedLine = Line.split(" ")
        lines = []
        if splittedLine[0].find(FOR_LOOP["name"]) != FIND_FAILED:
            argType = splittedLine[0].split(FOR_LOOP["name"])[1]
            argType = argType.replace("(", "")
            if self.__isValidBuiltInType(argType, lineNum):
                argName = splittedLine[1].replace(",", "")
                howLong = splittedLine[2].replace(")", "")
                howLong = howLong.replace("{", "")
                startingIterator = 0
                if Line.find(ASSING_VALUE_FLAG["name"]) != FIND_FAILED:
                    sp = Line.split(" ")
                    for i in range(len(sp)):
                        if sp[i] == ASSING_VALUE_FLAG["name"]:
                            if (i + 1) >= len(sp): raiseInvalidAttritubeAssignmentError(lineNum)
                            startingIterator = int(sp[i + 1].replace(",", ""))
                            howLong = splittedLine[-1]
                            howLong = howLong.replace(")", "")
                            howLong = howLong.replace("{", "")
                            break
                
                

                firstLine = f"{FOR_LOOP['compensation']}({argType} {argName} = {startingIterator}{END_LINE_FLAG['compensation']} {argName} < {howLong}{END_LINE_FLAG['compensation']} {argName}++)" + "{" + NEW_LINE_FLAG
                lines.insert(0, firstLine)
        elif splittedLine[0].find(WHILE_LOOP["name"]) != FIND_FAILED:
            l = self.__convertListToString(splittedLine) + NEW_LINE_FLAG
            lines.insert(0, l)

        if len(lines) != 0:
            return self.__convertListToString(lines)
        return None

    def __checkForIfStatement(self, Line, lineNum):
        splittedLine = Line.split(" ")
        if splittedLine[0] != IF_STATEMENT_FLAG["name"] and splittedLine[0] != ELSE_IF_STATEMENT_FLAG["name"] and splittedLine[0].find(ELSE_STATEMENT_FLAG["name"]) == FIND_FAILED:
            return False

        IS_IF = False
        IS_ELIF = False
        IS_ELSE = False

        if splittedLine[0] == IF_STATEMENT_FLAG["name"]:
            IS_IF = True
            IS_ELIF = False
            IS_ELSE = False
        elif splittedLine[0] == ELSE_IF_STATEMENT_FLAG["name"]:
            IS_ELIF = True
            IS_IF = False
            IS_ELSE = False
        elif splittedLine[0].find(ELSE_STATEMENT_FLAG["name"]) != FIND_FAILED:
            IS_ELSE = True
            IS_IF = False
            IS_ELIF = False
        else:
            print("Not implemented")
            return False

        if IS_ELSE == False:
            Line = Line.replace(NEW_LINE_FLAG, "")
            
            argument = splittedLine[1]
            isValid = splittedLine[2]
            compensation = splittedLine[3]
            compensation = compensation.replace("{", "")
            quotes = ["'", '"']

            if compensation[0] in quotes and compensation[-1] not in quotes:
                try:
                    for i in range(len(splittedLine)):
                        if splittedLine[i] == compensation:
                            for j in range(i + 1, len(splittedLine)):
                                compensation += " " + splittedLine[j]
                                compensation = compensation.replace("{", "")

                                if splittedLine[j][-1] in quotes:
                                    break
                except:
                    raiseInvalidAttritubeAssignmentError(lineNum)
                                    
            line = ""
            if IS_IF:
                line = f"{IF_STATEMENT_FLAG['compensation']}({argument} {isValid} {compensation})" + "{" + NEW_LINE_FLAG
            elif IS_ELIF:
                line = f"{ELSE_IF_STATEMENT_FLAG['compensation']}({argument} {isValid} {compensation})" + "{" + NEW_LINE_FLAG
            else:
                print("WHUT")

            return line

        else:
            line = ELSE_STATEMENT_FLAG["compensation"] + "{" + NEW_LINE_FLAG
            return line

    def __lineIsReturnStatement(self, Line, lineNum):
        splittedLine = Line.split(" ")
        if splittedLine[0].find(RETURN_STATEMENT_FLAG["name"]) != FIND_FAILED:
            newLine = f"{RETURN_STATEMENT_FLAG['compensation']} {splittedLine[1]}"
            return newLine
        
        return False

    def __parseLine(self, Line, lineNum, finalLines):
        Line = Line.replace(NEW_LINE_FLAG, "")
        spaces = 0
        j: int = 0
        finalLine = Line
        for i in Line:
            if i == " " or i == "": 
                spaces += 1
                l = list(finalLine)
                l.remove(l[0])
                finalLine = self.__convertListToString(l)
            else: 
                break

            j += 1

        Line = finalLine
        #print(spaces, lineNum, Line)
        if self.__lineIsCommented(Line) == False:
            lineIsImport, importName = self.__lineIsImport(Line)
            lineIsBuiltInFunction, requiredImports = self.__lineIsBuiltInFunction(Line, lineNum)
            lineIsLoop = self.__checkForLoop(Line, lineNum)
            lineIsIfStatement = self.__checkForIfStatement(Line, lineNum)
            lineIsReturnStatement = self.__lineIsReturnStatement(Line, lineNum)
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
            elif lineIsLoop:
                finalLines.insert(lineNum, lineIsLoop)
                return finalLines
            elif lineIsIfStatement != False:
                finalLines.insert(lineNum, lineIsIfStatement)
                return finalLines
            elif lineIsReturnStatement != False:
                finalLines.insert(lineNum, lineIsReturnStatement)
                return finalLines
                

            self.__checkForEndLineFlag(Line, lineNum)
            attritube, finalLines = self.__checkForAttributeAssignment(Line, lineNum, finalLines)

            if attritube == False:
                finalLines.insert(lineNum, Line + NEW_LINE_FLAG)


        return finalLines

    def __isFunctionReturnType(self, line):
        #for t in EVERY_BUILT_IN_FUNCTION_RETURN_TYPE:
        #    if line.find(t["name"]) != FIND_FAILED:
        #        return t

        splitted = line.split(" ")
        
        for t in EVERY_BUILT_IN_DATA_TYPE:
            if splitted[0].find(t["name"]) != FIND_FAILED:
                lstValue = ""
                lstValue = splitted[0]
                lstValue = lstValue.replace("<", "")
                lstValue = lstValue.replace(">", "")
                lstValue = lstValue.replace(t["name"], "")
                lstValue = convertBuiltInDataTypeNameToCompensation(lstValue)

                return t, lstValue
        
        return False, 0

    def __gatherFunctionLines(self, Lines: list, lineNum: int):
        funcLines = []
        funcName = ""
        for l in range(lineNum, len(Lines)):
            line = Lines[l]
            if line != "}" + END_LINE_FLAG["name"] and line != "}":
                funcReturnType, lstValue = self.__isFunctionReturnType(line)
                if funcReturnType != False:
                    splittedLine = line.split(" ")
                    funcName = splittedLine[1]

                    lst = funcName.split("(")
                    lst.remove(lst[-1])
                    funcName = self.__convertListToString(lst)
                    funcName = funcName.replace(NEW_LINE_FLAG, "")
                    funcName = funcName.replace("(", "")


                    attritubes = []
                    i: int = 0
                    '''for arg in splittedLine:
                        if arg not in getEveryBuiltInFunctionReturnTypeName():
                            ARG = arg
                            if ARG.find("(") != FIND_FAILED: ARG = ARG.replace(funcName + "(", "")
                            ARG = ARG.replace(NEW_LINE_FLAG, "")
                            if ARG in getEveryBuildInDataTypeName():
                                print("YES", ARG)
                                if (i + 1) >= len(splittedLine): raiseInvalidFunctionDeclarationError(lineNum)
                                dataType = ARG
                                dataType = convertBuiltInDataTypeNameToCompensation(dataType)
                                if dataType == None: raiseNotProperDataTypeError(lineNum, dataType)
                                attritubeName = splittedLine[i + 1]
                                attritubeName = attritubeName.replace("){", "")
                                attritubeName = attritubeName.replace(",", "")

                                LINE = f"{dataType} {attritubeName},"
                                attritubes.append(LINE)
                        i += 1'''

                    splittedWith = line.split("(")
                    for j in range(1, len(splittedWith)):
                        ln = splittedWith[j]
                        if ln == "){" + NEW_LINE_FLAG:
                            break
                        sp = ln.split(" ")
                        for x in range(len(sp)):
                            dataType = ""
                            value = ""
                            if sp[x] in getEveryBuildInDataTypeName():
                                if (x + 1) >= len(sp): raiseInvalidFunctionDeclarationError(lineNum)
                                dataType = convertBuiltInDataTypeNameToCompensation(sp[x])
                                value = sp[x + 1].replace("){", "")
                                value = value.replace(NEW_LINE_FLAG, "")
                                attritubes.insert(x, f"")#HERE

                            print(dataType, value)

                        

                    #print(attritubes, "AT")

                    FinalAttritubes = ""
                    if len(attritubes) > 0:
                        attritubes[-1] = attritubes[-1].replace(",", "")
                        FinalAttritubes = self.__convertListToString(attritubes)
                        FinalAttritubes = FinalAttritubes.replace(NEW_LINE_FLAG, "")                   

                    a = ""
                    if funcReturnType == LIST:
                        a = f"{funcReturnType['compensation']}<{lstValue}> {funcName}({FinalAttritubes})" + '{' + NEW_LINE_FLAG
                    else:
                        a = f"{funcReturnType['compensation']} {funcName}({FinalAttritubes})" + '{' + NEW_LINE_FLAG

                    #print(a, "A")

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
            if Line[-1] != "}" and Line[-1] != "}" + END_LINE_FLAG["name"]:
                hasEndLineFlag = (Line[-1] == END_LINE_FLAG["name"])
                if hasEndLineFlag == False: raiseNoLineEndFlagFoundError(lineNum)
            #if Line[-1] != "}" and Line[-1] != "}" + END_LINE_FLAG["name"]:
            #    raiseNoLineEndFlagFoundError(lineNum)
            #hasEndLineFlag = (Line[-1] == END_LINE_FLAG["name"])
            #if hasEndLineFlag == False: 

    def __getEveryIncludePath(self):
        files = os.listdir(self.__convertListToString(self.__include_directories))
        lst = [self.__convertListToString(self.__include_directories)]
        for i in files:
            lst.append(i)

        return lst

    def __copyIncludeFilesToProject(self):
        files = os.listdir(self.__convertListToString(self.__include_directories))
        newPath = self.__file_to_pass_data.split(os.sep)[0] + os.sep
        for file in files:
            shutil.copyfile(self.__EVERY_INCLUDE_PATH[0] + file, newPath + file)
            

    def setFileToParse(self, file):
        self.__file_to_parse = file

    def setFileToPassData(self, file):
        self.__file_to_pass_data = file

    def setRunExeStraight(self, b):
        self.__run_exe_stright = b

    def setExeFileName(self, name):
        self.__exe_file_name = name

    def addIncludeDirectory(self, path):
        self.__include_directories.append(path)

    def parse(self):
        print("Starting the parse....")
        Lines = self.__getLines()
        self.__EVERY_INCLUDE_PATH = self.__getEveryIncludePath()
        self.__copyIncludeFilesToProject()
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
                    if Line.find("}" + END_LINE_FLAG["name"]) == FIND_FAILED:
                        finalLines = self.__parseLine(Line, line_num, finalLines)
            line_num += 1
            if line_num >= len(Lines):
                break

        print("Parsing done...")
        #print(finalLines)
        self.__writeToCppFile(finalLines)
        