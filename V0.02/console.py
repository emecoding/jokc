class console:
	def __init__(self):
		self.__command = ""

	def set_command(self, command):
		self.__command = command
	
	def get_value_of_flag(self, flag_name):
		value = ""
		for flag in self.__command:
			s = flag.split("=")
			if s[0] == flag_name:
				return s[1]

		return value


CONSOLE = console()
