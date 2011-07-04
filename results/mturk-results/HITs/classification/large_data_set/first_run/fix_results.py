#!/usr/bin/python
from __future__ import with_statement
import os, sys
import re
if __name__ == '__main__':
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r') as f:
            hit = f.read()
        line_sep, data_sep = '\n' '\t'
        reg = re.compile('%s(feedback=.*?)%s[^"]' % (data_sep, data_sep), re.DOTALL)
        for rep in reg.findall(hit):
            print((rep, rep.replace(line_sep, re.escape(line_sep)).replace(data_sep, re.escape(data_sep))))
            hit = hit.replace(rep, rep.replace(line_sep, re.escape(line_sep)).replace(data_sep, re.escape(data_sep)))
        with open(sys.argv[1], 'w') as f:
            f.write(hit)
            
