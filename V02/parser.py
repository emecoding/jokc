from log import *
from config import *

from pythonParser import pythonParser
from cppParser import cppParser

class parser:
	def __init__(self):
		self.__file_name = ""
		self.__format = ""
		self.__final_file_location = ""
		self.__real_parser = None

	def set_file_name(self, file_name):
		self.__file_name = file_name

	def set_final_file_location(self, ffl):
		self.__final_file_location = ffl

	def set_format(self, format):
		self.__format = format

	def parse(self):
		if self.__format == PYTHON_FORMAT:
			self.__parse_to_python()
		elif self.__format == CPP_FORMAT:
			self.__parse_to_cpp()
		else:
			raiseConsoleError(NOT_CORRECT_FORMAT_ERROR)
		
	def __parse_to_python(self):
		self.__real_parser = pythonParser(self.__file_name)
		self.__real_parser.set_final_file_location(self.__final_file_location)
		self.__real_parser.parse()

	def __parse_to_cpp(self):
		self.__real_parser = cppParser(self.__file_name)
		self.__real_parser.set_final_file_location(self.__final_file_location)
		self.__real_parser.parse()

PARSER = parser()
