#!/usr/bin/python
# convert-turk-file-to-folders.py -- Converts the results of a turk submission to folders.
from __future__ import with_statement
import os, sys
from alphabetspaths import *
from recordsubmission import record_submission, get_alphabet_id_from_dict

SUCCESS_FILE = 'characterrequest.input.reject.success'
REJECT_FILE = 'characterrequest.input.reject'
REJECT_BAD_FILE = os.path.join(os.getcwd(), 'reject-bad.bat')


if not os.path.exists(TURK_POST_EXTRA_LIST_PATH):
    with open(TURK_POST_EXTRA_LIST_PATH, 'w') as f:
        pass
with open(TURK_POST_EXTRA_LIST_PATH, 'r') as f:
    EXTRA_SUBMISSION_LIST = map(str.strip, f.readlines())
EXTRA_SUBMISSION_LIST = [submission.split(' ') for submission in EXTRA_SUBMISSION_LIST if submission]
EXTRA_SUBMISSION_LIST = dict((submission[0],
                              dict(map((lambda s: s.split('=')), submission[1:]))) \
                             for submission in EXTRA_SUBMISSION_LIST)


rejects = {}

def make_reject_bad_file():
    success_file = SUCCESS_FILE
    reject_file = REJECT_FILE
    assignmentIdToRejectComment = '"Blank submission."'
    with open(REJECT_BAD_FILE, 'w') as f:
        f.write('SET i=%CD%\n')
        num_add = 0
        while rejects:
            num_add += 1
            reject_assignments = []
            f.write('ECHO hitid\thittypeid> %(success_file)s\n' % locals())
            f.write('ECHO assignmentIdToReject\tassignmentIdToRejectComment> %(reject_file)s\n' % locals())
            for hit_key in sorted(rejects.keys()):
                hitid, hittypeid = hit_key
                if sum(map(len, rejects[hit_key].values())) == num_add:
                    f.write('ECHO %(hitid)s\t%(hittypeid)s>> %(success_file)s\n' % locals())
                    for worker_id in rejects[hit_key]:
                        for assignmentIdToReject in rejects[hit_key][worker_id]:
                            f.write('ECHO %(assignmentIdToReject)s\t%(assignmentIdToRejectComment)s>> %(reject_file)s\n' % locals())
                    del rejects[hit_key]
            f.write(r"""PUSHD "D:\mech-turk-tools-1.3.0\bin"
ECHO %%i%%
START rejectWork -rejectfile "%%i%%\%(reject_file)s"
START extendHITs -successfile "%%i%%\%(success_file)s" -assignments %(num_add)d
POPD
PAUSE
""" % locals())

    

def note_bad_hit(submission_dict, ex=None):
    if submission_dict['reject'] != 'y':
        if ex:
            print('There was an error with assignment %s: %s' % (submission_dict['assignmentid'], repr(ex)))
        else:
            print('There was an error with assignment %s' % submission_dict['assignmentid'])
        print('Please visit %(viewhit)s and reject the worker with id %(workerid)s.' % submission_dict)
        hit_key = (submission_dict['hitid'], submission_dict['hittypeid'])
        worker_id = submission_dict['workerid']
        if hit_key not in rejects: rejects[hit_key] = {}
        if worker_id not in rejects[hit_key]: rejects[hit_key][worker_id] = []
        rejects[hit_key][worker_id].append(submission_dict['assignmentid'])
    else:
        print('Rejected empty submission not saved to folder.')

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
                line_sep='\n', data_sep='\t', pseudo=False):
    table = [line.split(data_sep) for line in hit.split(line_sep) if line.strip()]
    data = _parse_table(table)
##    check = map((lambda d: (get_alphabet_name(d), hash(d['ipAddress']), d['ipAddress'], d['reject'], d['viewhit'], d['workerid'])), data)
##    for i in check:
##        print(i)
##    raw_input()
##    for i in sorted(check):
##        raw_input(i)
##    raw_input()
    for submission_dict in data:
        print('Saving %s for %s...' % (repr(get_alphabet_id_from_dict(submission_dict)),
                                       repr(submission_dict['workerid'])))
        images_path, strokes_path, extra_info_path = get_submission_paths(submission_dict)
        try:
            record_submission(submission_dict, names=names, many_dirs=False, pseudo=pseudo,
                              images_path=images_path, strokes_path=strokes_path, extra_info_path=extra_info_path)
            raise_object_changed(images_path)
            raise_object_changed(strokes_path)
        except AttributeError, ex:
            note_bad_hit(submission_dict, ex)

def _parse_table(table):
    header, body = table[0], table[1:]
    left_header, right_header = header[:header.index('"answers[question_id answer_value]"')], header[header.index('"answers[question_id answer_value]"')+1:]
    def entry_to_tuple(entry):
        parts = entry.split('=')
        return (parts[0].strip('"'), '='.join(parts[1:]).strip('"'))
    def row_to_dict(row):
        left_row   = row[:len(left_header)]
        middle_row = row[len(left_header):-len(right_header)]
        right_row  = row[-len(right_header):]
        row_dict = {}
        for key, val in zip(left_header, left_row):
            row_dict[key.strip('"')] = val.strip('"')
        for key, val in zip(right_header, right_row):
            row_dict[key.strip('"')] = val.strip('"')
        update_dict = dict([entry_to_tuple(answer_part) for answer_part in middle_row])
        for key in update_dict:
            if key not in row_dict or not row_dict[key] or row_dict[key] == update_dict[key]:
                row_dict[key] = update_dict[key]
            else:
                row_dict[key] += '\n' + update_dict[key] # should be only for feedback
            #row_dict['answers']
        return row_dict
    rtn = [row_to_dict(row) for row in body]
    return rtn
    

if len(sys.argv) > 1:
    files_to_convert = sys.argv[1:]
else:
    files_to_convert = list(set([os.path.join(RESULTS_PATH, 'HIT-results.txt'), os.path.join(os.getcwd(), 'HIT-results.txt')]))


for file_name in files_to_convert:
    if os.path.exists(file_name) and os.path.isfile(file_name):
        print('Converting ' + file_name + '...')
        with open(file_name, 'r') as f:
            hit = f.read().replace('\r', '\n').replace('\n\n', '\n')
        convert_hit(hit, pseudo=False)#False)
    else:
        print('Invalid file name: ' + file_name)
make_reject_bad_file()
os.system('echo > ' + SUBMISSION_LOG_PATH) # clean up log, or else it'll get too big
