#!/usr/bin/python
# Filename: library.py
import python2to3patch
import os, os.path
import glob

def walk(top, topdown=True, onerror=None, followlinks=True, separate_files=True):
    """Directory tree generator.

    For each directory in the directory tree rooted at top (including top
    itself, but excluding '.' and '..'), yields either a 3-tuple

        dirpath, dirnames, filenames

    if separate_files is True, or a 2-tuple,

        dirpath, names

    if separate_files is False.
    dirpath is a string, the path to the directory.  dirnames is a list of
    the names of the subdirectories in dirpath (excluding '.' and '..').
    filenames is a list of the names of the non-directory files in dirpath.
    names is a list of the names of the subdirectories and files in dirpath
    (excluding '.' and '..').
    Note that the names in the lists are just names, with no path components.
    To get a full path (which begins with top) to a file or directory in
    dirpath, do os.path.join(dirpath, name).

    If optional arg 'topdown' is true or not specified, the triple for a
    directory is generated before the triples for any of its subdirectories
    (directories are generated top down).  If topdown is false, the triple
    for a directory is generated after the triples for all of its
    subdirectories (directories are generated bottom up).

    When topdown is true, the caller can modify the dirnames list in-place
    (e.g., via del or slice assignment), and walk will only recurse into the
    subdirectories whose names remain in dirnames; this can be used to prune
    the search, or to impose a specific order of visiting.  Modifying
    dirnames when topdown is false is ineffective, since the directories in
    dirnames have already been generated by the time dirnames itself is
    generated.

    By default errors from the os.listdir() call are ignored.  If
    optional arg 'onerror' is specified, it should be a function; it
    will be called with one argument, an os.error instance.  It can
    report the error to continue with the walk, or raise the exception
    to abort the walk.  Note that the filename is available as the
    filename attribute of the exception object.

    By default, os.walk does not follow symbolic links to subdirectories on
    systems that support them.  In order to get this functionality, set the
    optional argument 'followlinks' to true.

    Caution:  if you pass a relative pathname for top, don't change the
    current working directory between resumptions of walk.  walk never
    changes the current directory, and assumes that the client doesn't
    either.

    Example:

    import os
    from os.path import join, getsize
    for root, dirs, files in walk('python/Lib/email'):
        print(root, "consumes", end="")
        print(sum([getsize(join(root, name)) for name in files]), end="")
        print("bytes in", len(files), "non-directory files")
        if 'CVS' in dirs:
            dirs.remove('CVS')  # don't visit CVS directories
    """

    from os.path import join, isdir, islink, normpath
    from os import listdir, error

    # We may not have read permission for top, in which case we can't
    # get a list of the files the directory contains.  walk
    # always suppressed the exception then, rather than blow up for a
    # minor reason when (say) a thousand readable directories are still
    # left to visit.  That logic is copied here.
    try:
        # Note that listdir and error are globals in this module due
        # to earlier import-*.
        top = normpath(top)
        if top[-1] not in r'\/': top += '/'
        names = glob.glob(join(top, '*'))
        if not names and not isdir(top):
            return
    except error as err:
        if onerror is not None:
            onerror(err)
        return

    if separate_files:
        dirs, nondirs = [], []
        for name in names:
            if isdir(join(top, name)):
                dirs.append(name)
            else:
                nondirs.append(name)
        if topdown:
            yield top, dirs, nondirs
        for name in dirs:
            path = join(top, name)
            if followlinks or not islink(path):
                for x in walk(path, topdown, onerror, followlinks, separate_files):
                    yield x
        if not topdown:
            yield top, dirs, nondirs
    else:
        if topdown:
            yield top, names
        for name in names:
            path = join(top, name)
            if followlinks or not islink(path):
                for x in walk(path, topdown, None, followlinks, separate_files):
                    yield x
        if not topdown:
            yield top, names
