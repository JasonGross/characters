#!/usr/bin/python
from __future__ import with_statement
import os, sys
import argparse
from alphabetspaths import *
import turkutil

def main(task_name, unreviewed_path, record_submission):
    SUCCESS_FILE = '%s.input.reject.success' % task_name
    REJECT_FILE = '%s.input.reject' % task_name
    UNREVIEWED_PATH = unreviewed_path

    def make_reject_bad_file():
        turkutil.make_reject_bad_file(success_file=SUCCESS_FILE, reject_file=REJECT_FILE)

    def convert_hit(hit, line_sep='\n', data_sep='\t', pseudo=False, **kwargs):
        def do_record_submission(submission_dict, pseudo=pseudo):
            record_submission(submission_dict, many_dirs=True, pseudo=pseudo, **kwargs)
        turkutil.convert_hit(hit, record_submission=do_record_submission, 
                             line_sep=line_sep, data_sep=data_sep, pseudo=pseudo)

    parser = argparse.ArgumentParser(description='Converts results of a turk recognition submission to folders')
    parser.add_argument('--path', type=str, default=UNREVIEWED_PATH,
                        help='What folder should should the tasks go in')
    parser.add_argument('files_to_convert', metavar='FILE', type=str, nargs='*',
                        help='what files get converted to folders')
    parser.add_argument('--exclude-rejected', dest='exclude_rejected', action='store_true',
                        help='do not save the rejected HITs')
    parser.add_argument('--exclude', dest='exclude_ids', metavar='FILE_OR_ID', type=str, nargs='*',
                        help='rejected ids, or files to take rejected ids from')

    args = parser.parse_args()
    rejected_ids = set()
    if args.exclude_ids is None: args.exclude_ids = []
    for ids in args.exclude_ids:
        if os.path.exists(ids) and os.path.isfile(ids):
            with open(ids, 'r') as f:
                ids = f.read().replace('\r', '\n').replace('\n\n', '\n').replace('\n', ',')
        rejected_ids = rejected_ids.union(ids.split(','))
    if '' in rejected_ids: rejected_ids.remove('')
    for file_name in args.files_to_convert:
        if os.path.exists(file_name) and os.path.isfile(file_name):
            print('Converting ' + file_name + '...')
            with open(file_name, 'r') as f:
                hit = f.read().replace('\r', '\n').replace('\n\n', '\n')
                convert_hit(hit, pseudo=False, path=os.path.join(UNREVIEWED_PATH, args.path), exclude_rejected=args.exclude_rejected, exclude_ids=rejected_ids)#False)
        else:
            print('Invalid file name: ' + file_name)
    turkutil.make_reject_bad_file(SUCCESS_FILE, REJECT_FILE)
    os.system('echo > ' + SUBMISSION_LOG_PATH) # clean up log, or else it'll get too big
