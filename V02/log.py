from flags import *

NOT_CORRECT_FORMAT_ERROR = "your format was not correct"
NO_END_LINE_FLAG_FOUND_ERROR = f'no "{END_LINE}" found from the end of the line.'
NO_FINAL_FILE_LOCATION_DECLARED = "did not found final file location declared in your command."

def raiseError(msg, line_num):
	m = f"[PARSER ERROR]: '{msg}' at line {line_num}"
	raise Exception(m)


def raiseConsoleError(msg):
	m = f"[CONSOLE ERROR] '{msg}' in your command"
	raise Exception(m)
