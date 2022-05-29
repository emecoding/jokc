from config import *

END_LINE = ";"

EQUALS = {PYTHON_FORMAT:"=", CPP_FORMAT:"="}
NEW_LINE = {PYTHON_FORMAT:"\n", CPP_FORMAT:"\n"}


INT = {"valids": ["int", "it"], "compensation": {PYTHON_FORMAT:"int", CPP_FORMAT:"int"}, "required_imports":{PYTHON_FORMAT:None, CPP_FORMAT:None}}
FLOAT = {"valids": ["float", "flt"], "compensation": {PYTHON_FORMAT:"float", CPP_FORMAT: "float"}, "required_imports": {PYTHON_FORMAT:None, CPP_FORMAT:None}}
STRING = {"valids": ["string", "str"], "compensation": {PYTHON_FORMAT: "str", CPP_FORMAT: "std::string"}, "required_imports": {PYTHON_FORMAT:None, CPP_FORMAT:"iostream"}}


DATA_TYPES = [INT, FLOAT, STRING]

def is_data_type(type: str, format: str):
	global DATA_TYPES
	for i in DATA_TYPES:
		for j in i["valids"]:
			if j == type:
				return i["compensation"][format], i["required_imports"][format]

	return None, None
