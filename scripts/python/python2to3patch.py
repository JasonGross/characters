#!/usr/bin/python
# Filename: python2to3patch.py
import os, sys, urllib

if not hasattr(os.path, 'relpath'):
    if os.name == 'posix':
        from os.path import abspath, sep, commonprefix, pardir, curdir, join
        def relpath(path, start=curdir):
            """Return a relative version of a path"""

            if not path:
                raise ValueError("no path specified")

            start_list = abspath(start).split(sep)
            path_list = abspath(path).split(sep)

            # Work out how much of the filepath is shared by start and path.
            i = len(commonprefix([start_list, path_list]))

            rel_list = [pardir] * (len(start_list)-i) + path_list[i:]
            if not rel_list:
                return curdir
            return join(*rel_list)

    elif os.name in ('nt', 'ce') or (os.name == 'os2' and sys.version.find('EMX GCC') == -1):
        from os.path import abspath, sep, splitunc, pardir, curdir, join
        def relpath(path, start=curdir):
            """Return a relative version of a path"""

            if not path:
                raise ValueError("no path specified")
            start_list = abspath(start).split(sep)
            path_list = abspath(path).split(sep)
            if start_list[0].lower() != path_list[0].lower():
                unc_path, rest = splitunc(path)
                unc_start, rest = splitunc(start)
                if bool(unc_path) ^ bool(unc_start):
                    raise ValueError("Cannot mix UNC and non-UNC paths (%s and %s)"
                                                                        % (path, start))
                else:
                    raise ValueError("path is on drive %s, start on drive %s"
                                                        % (path_list[0], start_list[0]))
            # Work out how much of the filepath is shared by start and path.
            for i in range(min(len(start_list), len(path_list))):
                if start_list[i].lower() != path_list[i].lower():
                    break
            else:
                i += 1

            rel_list = [pardir] * (len(start_list)-i) + path_list[i:]
            if not rel_list:
                return curdir
            return join(*rel_list)

    else:
        raise ImportError('relpath is not available on this os: ' + os.name)
    os.path.relpath = relpath
    del relpath
try:
    import urllib.parse
except ImportError: # we are not in python 3.x
    import urlparse
    urllib.parse = urlparse
    for method in ('quote', 'unquote'):
        setattr(urllib.parse, method, getattr(urllib, method))

if hasattr(sys.version_info, 'major'):
    major = sys.version_info.major
else:
    major = sys.version_info[0]
if major < 3:
    global input
    input = raw_input

