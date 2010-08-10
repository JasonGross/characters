#!/usr/bin/python
# Filename: alphabetspaths.py
import os, re
import python2to3patch

_RELPATH_ERROR_REG = re.compile(r'path is on drive [A-Z]:, start on drive [A-Z]:')

def relpath(path, start='.'):
    """
    Return a relative version of a path.  If the paths are on
    different drives, return the absolute path.
    """
    try:
        return os.path.relpath(path, start)
    except ValueError, ex:
        if _RELPATH_ERROR_REG.match(ex.message):
            return os.path.abspath(path)
        else:
            raise ex
