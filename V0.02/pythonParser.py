from config import *
from log import *

from parserSkeleton import parserSkeleton

class pythonParser(parserSkeleton):
	def __init__(self, file_name):
		super().__init__(file_name)
		

	def parse(self):
		print(self.get_file_name())
