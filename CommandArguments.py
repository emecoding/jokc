EVERY_ARG = []

def addArg(arg: str, argName: str):
    global EVERY_ARG
    a = {"arg" : arg, "argName" : argName}
    EVERY_ARG.append(a)

    return a

EXE_NAME = addArg("-o", "name")

