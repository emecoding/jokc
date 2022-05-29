from config import *
from flags import *
from log import *
import os

from parserSkeleton import parserSkeleton

class pythonParser(parserSkeleton):
	def __init__(self, file_name):
		super().__init__(file_name)
		self.__format = PYTHON_FORMAT

	def _is_variable_assignment(self, line):
		if EQUALS[PYTHON_FORMAT] in line:
			try:
				splitted = line.split(" ")
				value = splitted[-1].replace(END_LINE, "")
				data_type, required_imports = is_data_type(splitted[0], self.__format)
				if data_type != None: #new variable
					new_line = f"{splitted[1]}: {data_type} {EQUALS[PYTHON_FORMAT]} {value}"
					return new_line
				else:
					new_line = f"{splitted[0]} {EQUALS[PYTHON_FORMAT]} {value}"
					return new_line

			except Exception as e:
				print(e)
		

	def _edit_line_to_proper_format(self, line, line_num):
		if line.split()[-1][-1] != END_LINE: raiseError(NO_END_LINE_FLAG_FOUND_ERROR, line_num)
	

		new_line = line.replace(NEW_LINE[PYTHON_FORMAT], "")
		return new_line

	def parse(self):
		#python3 jokc.py file_name="jocks/main.jokc" format="py"
#		print(os.path.isfile(self.get_file_name()))
#		print(self.get_file_data_as_lines())
#		print(EQUALS)
		
		lines = self.get_file_data_as_lines()
		line_num = 1
		final_lines = ""
		for line in lines:
			line = self._edit_line_to_proper_format(line, line_num)
			line = self._is_variable_assignment(line)


			line += NEW_LINE[PYTHON_FORMAT]
			final_lines += line
			line_num += 1


		self.set_final_data(final_lines)
		self._write_to_final_file(PYTHON_FORMAT)
