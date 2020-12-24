import glob
import os


FlagsList = []


def getflags():
    i=0
    Flags = []
    scriptname =str(__file__)
    if scriptname.endswith("Flagdir.py"):
        scriptname = scriptname[:-10]
    for file in glob.glob(scriptname+"*.jpg"):
        name=os.path.abspath(file)
        name = name.split("\\")
        name = name[len(name)-1]
        name = name.split(".")
        name = name[0]
        Flag = [i, name, os.path.abspath(file)]
        Flags.append(Flag)
        i += 1

    return Flags


def __init__():
    global FlagsList
    FlagsList = getflags()


__init__()
