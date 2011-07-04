#!/usr/bin/python
# record-recognition-submission.py -- Stores the data from the task submission
from __future__ import with_statement
import os, sys, glob
if __name__ == '__main__':
    if len(sys.argv) > 1:
        combined_file = sys.argv[1]
    else:
        combined_file = 'matlab_results.m'
    real_combined_file = os.path.realpath(combined_file)
    rtn = []
    for dirpath, dirnames, filenames in os.walk(os.getcwd()):
        for file_name in filenames:
            if file_name[-2:] == '.m' and os.path.realpath(os.path.join(dirpath, file_name)) != real_combined_file:
                rtn.append('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Data for ' + os.path.join(dirpath, file_name) + ' %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
                with open(os.path.join(dirpath, file_name), 'r') as f:
                    rtn.append(f.read())
                rtn.append('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
    rtn = '\n'.join(rtn)
    with open(combined_file, 'w') as f:
        f.write(rtn)

