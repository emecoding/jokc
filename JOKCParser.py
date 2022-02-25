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

    def setFileToParse(self, file):
        self.__file_to_parse = file


    

    def parse(self):
        print(self.__getLines())
        