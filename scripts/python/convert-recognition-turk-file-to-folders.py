#!/usr/bin/python
# convert-recognition-turk-file-to-folders.py -- Converts the results of a turk submission to folders.
from __future__ import with_statement
import os, sys
import argparse
from alphabetspaths import *
from recordrecognitionsubmission import record_submission
import turkutil

SUCCESS_FILE = 'recognition.input.reject.success'
REJECT_FILE = 'recognition.input.reject'


def make_reject_bad_file():
    turkutil.make_reject_bad_file(success_file=SUCCESS_FILE, reject_file=REJECT_FILE)

def get_submission_paths(submission_dict):
    rejected = (submission_dict['reject'] == 'y')
    accepted = (submission_dict['assignmentstatus'].lower() == 'Approved'.lower())
    if submission_dict['assignmentid'] in EXTRA_SUBMISSION_LIST:
        props = EXTRA_SUBMISSION_LIST[submission_dict['assignmentid']]
        rejected = 'rejected' in props and props['rejected'].lower() not in ('0', 'false', 'no', 'off')
        accepted = 'accepted' in props and props['accepted'].lower() not in ('0', 'false', 'no', 'off')
    if rejected:
        return TURK_REJECTED_IMAGES_PATH, TURK_REJECTED_STROKES_PATH, TURK_REJECTED_EXTRA_INFO_PATH
    elif accepted:
        return TURK_ACCEPTED_IMAGES_PATH, TURK_ACCEPTED_STROKES_PATH, TURK_ACCEPTED_EXTRA_INFO_PATH
    else:
        return TURK_IMAGES_PATH, TURK_STROKES_PATH, TURK_EXTRA_INFO_PATH

def convert_hit(hit, names=('get_turk_accepted_image_list', 'get_turk_accepted_stroke_list', 'get_turk_image_list',
                            'get_turk_stroke_list', 'get_turk_rejected_image_list', 'get_turk_rejected_stroke_list'),
                line_sep='\n', data_sep='\t', pseudo=False, **kwargs):
    def do_record_submission(submission_dict, pseudo=pseudo):
        record_submission(submission_dict, many_dirs=True, pseudo=pseudo, **kwargs)
    turkutil.convert_hit(hit, record_submission=do_record_submission, 
            line_sep=line_sep, data_sep=data_sep, pseudo=pseudo)

parser = argparse.ArgumentParser(description='Converts results of a turk recognition submission to folders')
parser.add_argument('--path', type=str, default=RECOGNITION_UNREVIEWED_PATH,
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
            convert_hit(hit, pseudo=False, path=os.path.join(RECOGNITION_UNREVIEWED_PATH, args.path), exclude_rejected=args.exclude_rejected)#False)
        else:
            print('Invalid file name: ' + file_name)
    turkutil.make_reject_bad_file(SUCCESS_FILE, REJECT_FILE)
    os.system('echo > ' + SUBMISSION_LOG_PATH) # clean up log, or else it'll get too big
