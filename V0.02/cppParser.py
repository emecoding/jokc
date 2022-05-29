from parserSkeleton import parserSkeleton

class cppParser(parserSkeleton):
	def __init__(self, file_name):
		super().__init__(file_name)
		

	def parse(self):
		print("CPP", self.get_file_name())
