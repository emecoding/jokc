import os
from log import *

class parserSkeleton:
	def __init__(self, file_name):
		self.__file_name = file_name
		self.__final_file_location = ""
		self.__final_data = ""

	def get_file_name(self): return self.__file_name
	
	def get_abs_path(self): return os.path.abspath(self.get_file_name())

	def get_file_data_as_lines(self):
		data = []
		with open(self.get_abs_path(), "r") as file:
			data = file.readlines()
			file.close()

		return data

	def get_final_file_location(self):
		if self.__final_file_location == "":
			raiseConsoleError(NO_FINAL_FILE_LOCATION_DECLARED)
			

		return self.__final_file_location

	def set_final_file_location(self, ffl):
		self.__final_file_location = ffl	
	
	def set_final_data(self, data):
		self.__final_data = data
			

	def parse(self): pass
	
	
	def _is_variable_assignment(self, line): pass

	def _edit_line_to_proper_format(self, line): pass

	def _write_to_final_file(self, format):
		print(self.__final_data)
		with open(self.get_final_file_location() + self.__file_name.split("/")[-1].replace("jokc", "") + format, "w+") as file:
			file.write(self.__final_data)
			file.close()
