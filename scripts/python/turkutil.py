#!/usr/bin/python
# convert-turk-file-to-folders.py -- Converts the results of a turk submission to folders.
from __future__ import with_statement
import os, sys
import re
from alphabetspaths import *
from image_anonymizer import deanonymize_image

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

def preparse_hit(hit, line_sep='\n', data_sep='\t'):
    reg = re.compile('%s(feedback=.*?)%s[^"]' % (data_sep, data_sep), re.DOTALL)
    for rep in reg.findall(hit):
        hit = hit.replace(rep, rep.replace(line_sep, '\\n').replace(data_sep, '\\t'))
    return hit

def convert_hit(hit, record_submission, message=(lambda submission_dict: 'Saving for %s...' % repr(submission_dict['workerid'])),
                line_sep='\n', data_sep='\t', pseudo=False, **kwargs):
    hit = preparse_hit(hit, line_sep=line_sep, data_sep=data_sep)
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
            record_submission(submission_dict, pseudo=pseudo, **kwargs)
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

def get_accepted_rejected_status(submission_dict, extra_submission_dict=tuple()):
    rejected = (submission_dict['reject'] == 'y')
    accepted = (submission_dict['assignmentstatus'].lower() == 'Approved'.lower())
    if submission_dict['assignmentid'] in extra_submission_dict:
        props = extra_submission_dict[submission_dict['assignmentid']]
        rejected = 'rejected' in props and props['rejected'].lower() not in ('0', 'false', 'no', 'off')
        accepted = 'accepted' in props and props['accepted'].lower() not in ('0', 'false', 'no', 'off')
    return accepted, rejected

def get_submission_paths(submission_dict, rejected_return, accepted_return, unreviewed_return, extra_submission_dict=tuple()):
    accepted, rejected = get_accepted_rejected_status(submission_dict, extra_submission_dict=extra_submission_dict)
    if rejected: return rejected_return
    elif accepted: return accepted_return
    else: return unreviewed_return

    
def make_folder_for_submission(uid, path, return_num=True):
    if not isinstance(uid, str):
        uid = str(uid)
    push_dir(path)
    if not os.path.exists(uid.replace('-', 'm')):
        os.mkdir(uid.replace('-', 'm'))
    os.chdir(uid.replace('-', 'm'))
    existing = map(int, [i for i in os.listdir(os.getcwd()) if os.path.isdir(i)] + [-1])
    new_dir = str(1 + max(existing))
    os.mkdir(new_dir)
    pop_dir()
    rtn = os.path.join(path, uid.replace('-', 'm'), new_dir)
    if return_num: return rtn, int(new_dir)
    else: return rtn

def put_summary(folder, properties, file_name, make_summary, quiet=True):
    push_dir(folder)
    summary = make_summary(properties)
    if not quiet and os.path.exists(file_name):
        input("The file `%s' in `%s' already exists.  Press enter to continue, or ^c (ctrl + c) to break." % (file_name, folder))
    with open(file_name, 'w') as f:
        f.write(summary)
    pop_dir()

def put_properties(folder, properties, file_name,
                   not_use=('^ipAddress',
                            '^annotation', '^assignmentaccepttime', '^assignmentapprovaltime',
                            '^assignmentduration', '^assignmentrejecttime', '^assignments',
                            '^assignmentstatus', '^assignmentsubmittime', '^autoapprovaldelay',
                            '^autoapprovaltime', '^creationtime', '^deadline', '^description',
                            '^hitlifetime', '^hitstatus', '^hittypeid', '^keywords',
                            '^numavailable', '^numcomplete', '^numpending', '^reviewstatus',
                            '^reward', '^title', '^hitid', '^assignmentid'),
                    quiet=True):
    push_dir(folder)
    write_to_file = ''
    def can_use(key):
        for bad_key in not_use:
            if re.match(bad_key, key):
                return False
        return True
    for key in sorted(properties.keys()):
        if can_use(key):
            write_to_file += '%s: %s\n' % (key, properties[key].replace('\n', '\\n'))
    if not quiet and os.path.exists(file_name):
        input("The file `%s' in `%s' already exists.  Press enter to continue, or ^c (ctrl + c) to break." % (file_name, folder))
    with open(file_name, 'w') as f:
        f.write(write_to_file)
    pop_dir()

def deanonymize_urls(properties, tail_tag='-anonymous_url')):
    rtn = dict(properties)
    for key in sorted(rtn.keys()):
        if key[-len(tail_tag):] == tail_tag:
            values = deanonymize_image(rtn[key])
            rtn[key.replace(tail_tag, '-alphabet')] = values['alphabet']
            rtn[key.replace(tail_tag, '-character-number')] = values['character-number']
            rtn[key.replace(tail_tag, '-id')] = values['id']
    return rtn

def log_success(folder):
    push_dir(folder)
    with open('success.log', 'w') as f:
        f.write('')
    pop_dir()

def make_uid(form_dict):
    if 'workerid' in form_dict and form_dict['workerid']:
        return form_dict['workerid']
    else:
        return str(hash(form_dict['ipAddress']))
