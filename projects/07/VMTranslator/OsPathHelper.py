import os


def removeExtension(path: str):
    return path.rsplit(os.extsep, maxsplit=1)[0].strip()


def getExtension(path: str):
    return path.rsplit(os.extsep, maxsplit=1)[-1].strip()
