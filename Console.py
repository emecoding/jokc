
def raiseCommandArgumentError(argument: dict):
    MSG = f"No value found for argument '{argument['arg']}'({argument['argName']})"
    raise Exception(MSG)    

def raiseNoCompileFileFoundError():
    MSG = "Wasn't able to find the file you were looking for..."
    raise Exception(MSG)