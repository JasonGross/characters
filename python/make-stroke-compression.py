#!/usr/bin/python
# Filename: make-stroke-compression.py
from __future__ import with_statement
import os, glob, re
import python2to3patch
PRE_HEADER = r"""#!/usr/bin/python
# File name: %s
from __future__ import with_statement"""

IMPORTS = tuple('import ' + s for s in ('os', 'math', 'glob', 're'))

FIRST_FILES = ('alphabetsutil.py', 'stroke_compression.py')
SHARED_CONSTS = ('BIG_BYTE_PLUS_ONE',)
SHARED_METHODS = ('stroke_to_list', 'uint_encode', 'uint_decode',
                  'compress_stroke', 'decompress_stroke')

COMPRESSION_METHODS = ('compress_all_strokes_in_current_directory',)
DECOMPRESSION_METHODS = ('decompress_all_strokes_in_current_directory',)

COMPRESSION_MAIN = 'compress_all_strokes_in_current_directory()'
DECOMPRESSION_MAIN = 'decompress_all_strokes_in_current_directory()'

def find_const_in_file(file_name, const_name):
    with open(file_name, 'r') as f:
        body = f.read()
    if const_name in body:
        reg = re.compile('\n%s\\s*=\\s*(.*?)\n' % const_name)
        match = reg.search(body)
        if match:
            return '%s = %s' % (const_name, match.groups()[0])

def find_method_in_file(file_name, method_name):
    with open(file_name, 'r') as f:
        body = f.read()
    if '\ndef ' + method_name in body:
        start_with = body[body.index('def ' + method_name):].split('\n')
        rtn = [start_with[0]]
        del start_with[0]
        while start_with and start_with[0][:1] in (' \t#'):
            rtn.append(start_with[0])
            del start_with[0]
        return '\n'.join(rtn)

def find_object(name, finder=find_method_in_file, search_first=tuple(), search_glob='*.py'):
    done = set()
    for file_name in search_first:
        rtn = finder(file_name, name)
        if rtn: return rtn
    for file_name in glob.glob(search_glob):
        rtn = finder(file_name, name)
        if rtn: return rtn

def make_file(file_name, imports, consts, methods, main, search_first=tuple()):
    body = [PRE_HEADER % file_name] + list(imports)
    for things, thing_finder in ((consts, find_const_in_file),
                                 (methods, find_method_in_file)):
        for thing_name in things:
            cur_code = find_object(thing_name, finder=thing_finder,
                                   search_first=search_first)
            if cur_code:
                body.append('')
                body.append(cur_code)
            else:
                input('Error: code for %s not found.' % thing_name)
    body.append("if __name__ == '__main__':")
    body.append('   ' + main.replace('\n', '\n    '))
    body = '\n'.join(body)
    with open(file_name, 'wb') as f:
        f.write(body)
##    with open(file_name, 'rb') as f:
##        body = f.read()
##    if not isinstance(body, str): # assuming bytes
##        body = ''.join(map(chr, list(body)))
##    body = body.replace('\r\n', '\n').replace('\r', '\n')
##    with open(file_name, 'wb') as f:
##        f.write(body)

if __name__ == '__main__':
    make_file('compress-strokes_standalone.py', IMPORTS, SHARED_CONSTS,
              SHARED_METHODS + COMPRESSION_METHODS, COMPRESSION_MAIN,
              search_first=FIRST_FILES)
    make_file('decompress-strokes_standalone.py', IMPORTS, SHARED_CONSTS,
              SHARED_METHODS + DECOMPRESSION_METHODS, DECOMPRESSION_MAIN,
              search_first=FIRST_FILES)
    
                
    
