import sys
from CommandArguments import *
from Console import *

def argIsInEVERY_ARG(arg):
    for i in EVERY_ARG:
        if i["arg"] == arg:
            return i

    return None

args = sys.argv
args.remove(args[0])

for i in range(len(args)):
    arg = args[i]
    a = argIsInEVERY_ARG(arg)
    if a != None:
        if i >= len(args) - 1:
            raiseCommandArgumentError(a)

