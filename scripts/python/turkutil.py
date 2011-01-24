#!/usr/bin/python
# convert-turk-file-to-folders.py -- Converts the results of a turk submission to folders.
from __future__ import with_statement
import os, sys
from alphabetspaths import *

rejects = {}

def make_reject_bad_file(success_file, reject_file, reject_bad_file='reject-bad', assignmentIdToRejectComment='"Blank submission."'):
    with open(reject_bad_file + '.bat', 'w') as wf:
        with open(reject_bad_file + '.sh', 'w') as lf:
            wf.write('SET i=%CD%\n')
            lf.write(r"""#/bin/bash
export JAVA_HOME=/usr
SCRIPTPATH=`dirname $(readlink -f $0)`
export MTURK_CMD_HOME=~/web_scripts/alphabets/results/mturk-results/aws-mturk-clt-1.3.0
""")
        num_add = 0
        while rejects:
            num_add += 1
            reject_assignments = []
            wf.write('ECHO hitid\thittypeid> %(success_file)s\n' % locals())
            wf.write('ECHO assignmentIdToReject\tassignmentIdToRejectComment> %(reject_file)s\n' % locals())
            lf.write('echo hitid\thittypeid> %(success_file)s\n' % locals())
            lf.write('echo assignmentIdToReject\tassignmentIdToRejectComment> %(reject_file)s\n' % locals())
            for hit_key in sorted(rejects.keys()):
                hitid, hittypeid = hit_key
                if sum(map(len, rejects[hit_key].values())) == num_add:
                    wf.write('ECHO %(hitid)s\t%(hittypeid)s>> %(success_file)s\n' % locals())
                    lf.write('echo %(hitid)s\t%(hittypeid)s>> %(success_file)s\n' % locals())
                    for worker_id in rejects[hit_key]:
                        for assignmentIdToReject in rejects[hit_key][worker_id]:
                            wf.write('ECHO %(assignmentIdToReject)s\t%(assignmentIdToRejectComment)s>> %(reject_file)s\n' % locals())
                            lf.write('echo %(assignmentIdToReject)s\t%(assignmentIdToRejectComment)s>> %(reject_file)s\n' % locals())
                    del rejects[hit_key]
            wf.write(r"""PUSHD "D:\mech-turk-tools-1.3.0\bin"
ECHO %%i%%
START rejectWork -rejectfile "%%i%%\%(reject_file)s"
START extendHITs -successfile "%%i%%\%(success_file)s" -assignments %(num_add)d
POPD
PAUSE
""" % locals())
            lf.write(r"""pushd $MTURK_CMD_HOME/bin
echo $SCRIPTPATH
./rejectWork -rejectfile $SCRIPTPATH/%(reject_file)s &
./extendHITs.sh -successfile $SCRIPTPATH/%(success_file)s -assignments %(num_add)d
popd
""")

    

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

def convert_hit(hit, record_submission, message=(lambda submission_dict: 'Saving for %s...' % repr(submission_dict['workerid'])),
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
        print(message(submission_dict))
        try:
            record_submission(submission_dict, pseudo=pseudo)
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
    
