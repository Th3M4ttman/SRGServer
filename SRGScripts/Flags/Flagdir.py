import glob
import os


FlagsList = []


def getflags():
    i=0
    Flags = []
    for file in glob.glob(__file__.removesuffix("Flagdir.py")+"*.jpg"):
        name=file.removesuffix(".jpg")
        name=name.removeprefix(__file__.removesuffix("Flagdir.py"))
        Flag = [i, name, os.path.abspath(file)]
        Flags.append(Flag)
        i += 1

    return Flags


def __init__():
    global Flags
    Flags = getflags()


__init__()
