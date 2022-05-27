NOT_CORRECT_FORMAT_ERROR = "your format was not correct"

def raiseError(msg, line_num):
	m = f"[PARSER ERROR]: '{msg}' at line {line_num}"
	raise Exception(msg)


def raiseConsoleError(msg):
	m = f"[CONSOLE ERROR] '{msg}' in your command"
	raise Exception(m)
