#!/usr/bin/python
# convert-recognition-rt-turk-file-to-folders.py -- Converts the results of a turk submission to folders.
from __future__ import with_statement
import os, sys
import argparse
from alphabetspaths import *
from recordrecognitionrtsubmission import record_submission
import turkutil

SUCCESS_FILE = 'recognition-rt.input.reject.success'
REJECT_FILE = 'recognition-rt.input.reject'


def make_reject_bad_file():
    turkutil.make_reject_bad_file(success_file=SUCCESS_FILE, reject_file=REJECT_FILE)

def convert_hit(hit, line_sep='\n', data_sep='\t', pseudo=False, **kwargs):
    def do_record_submission(submission_dict, pseudo=pseudo):
        record_submission(submission_dict, many_dirs=True, pseudo=pseudo, **kwargs)
    turkutil.convert_hit(hit, record_submission=do_record_submission, 
            line_sep=line_sep, data_sep=data_sep, pseudo=pseudo)

parser = argparse.ArgumentParser(description='Converts results of a turk recognition submission to folders')
parser.add_argument('--path', type=str, default=RECOGNITION_RT_UNREVIEWED_PATH,
                    help='What folder should should the tasks go in')
parser.add_argument('files_to_convert', metavar='FILE', type=str, nargs='*',
                    help='what files get converted to folders')
parser.add_argument('--exclude-rejected', dest='exclude_rejected', action='store_true',
                    help='do not save the rejected HITs')

if __name__ == '__main__':
    args = parser.parse_args()
    for file_name in args.files_to_convert:
        if os.path.exists(file_name) and os.path.isfile(file_name):
            print('Converting ' + file_name + '...')
            with open(file_name, 'r') as f:
                hit = f.read().replace('\r', '\n').replace('\n\n', '\n')
            convert_hit(hit, pseudo=False, path=os.path.join(RECOGNITION_RT_UNREVIEWED_PATH, args.path), exclude_rejected=args.exclude_rejected)#False)
        else:
            print('Invalid file name: ' + file_name)
    turkutil.make_reject_bad_file(SUCCESS_FILE, REJECT_FILE)
    os.system('echo > ' + SUBMISSION_LOG_PATH) # clean up log, or else it'll get too big
