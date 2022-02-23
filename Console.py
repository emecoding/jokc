
def raiseCommandArgumentError(argument: dict):
    MSG = f"No value found for argument '{argument['arg']}'({argument['argName']})"
    raise Exception(MSG)    