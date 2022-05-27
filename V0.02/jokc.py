from console import CONSOLE
from parser import PARSER
import sys

def main():
	print("Starting parsing...")

	CONSOLE.set_command(sys.argv)
	file_name = CONSOLE.get_value_of_flag("file_name")
	format = CONSOLE.get_value_of_flag("format")
	PARSER.set_file_name(file_name)
	PARSER.set_format(format)

	PARSER.parse()
	


if __name__ == "__main__":
	main()
