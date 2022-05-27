from config import *
from log import *

class parser:
	def __init__(self):
		self.__file_name = ""
		self.__format = ""

	def set_file_name(self, name):
		self.__file_name = name

	def set_format(self, format):
		self.__format = format
	
	def __parse_to_python(self):
		print(self.__format)
	
	def __parse_to_cpp(self):
		print(self.__format)

	def parse(self):
		if self.__format == PYTHON_FORMAT:
			self.__parse_to_python()
		elif self.__format == CPP_FORMAT:
			self.__parse_to_cpp()
		else:
			raiseConsoleError(NOT_CORRECT_FORMAT_ERROR)

PARSER = parser()
