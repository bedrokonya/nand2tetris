import os


def remove_extension(path: str):
    return path.rsplit(os.extsep, maxsplit=1)[0].strip()


def get_extension(path: str):
    return path.rsplit(os.extsep, maxsplit=1)[-1].strip()
