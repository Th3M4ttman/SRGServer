import glob
import os
from pathlib import Path


FlagsList = []
FlagNameList = []

def getflags(namesonly=False):
    i=0
    Flags = []
    scriptname =str(__file__)
    if scriptname.endswith("Flagdir.py"):
        scriptname = scriptname[:-10]
    for file in glob.glob(scriptname+"*.jpg"):
        name=os.path.abspath(file)

        if namesonly:
            Flag = Path(name).stem
        else:
            Flag = [i, Path(name).stem, os.path.abspath(file)]
        Flags.append(Flag)
        i += 1

    return Flags

def __init__():
    global FlagsList
    global FlagNameList
    FlagsList = getflags()
    FlagNameList = getflags(True)

__init__()
