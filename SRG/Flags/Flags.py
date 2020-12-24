import glob
import os


Flags = []


def getflags():
    i=0
    Flags = []
    for file in glob.glob(__file__.removesuffix("Flags.py")+"*.jpg"):
        name=file.removesuffix(".jpg")
        name=name.removeprefix(__file__.removesuffix("Flags.py"))
        Flag = [i, name, os.path.abspath(file)]
        Flags.append(Flag)
        i += 1

    return Flags


def __init__():
    global Flags
    Flags = getflags()


__init__()
