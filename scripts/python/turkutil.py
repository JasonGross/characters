#!/usr/bin/python
# convert-turk-file-to-folders.py -- Converts the results of a turk submission to folders.
from __future__ import with_statement
import os, sys
import re
import shutil
import traceback
from alphabetspaths import *
from matlabutil import format_for_matlab
from image_anonymizer import deanonymize_image

rejects = {}

DEFAULT_NOT_USE_PROPERTIES = ('^ipAddress', '^annotation',
                              '^assignmentaccepttime',
                              '^assignmentapprovaltime', '^assignmentduration',
                              '^assignmentrejecttime', '^assignments',
                              '^assignmentstatus', '^assignmentsubmittime',
                              '^autoapprovaldelay', '^autoapprovaltime',
                              '^creationtime', '^deadline', '^description',
                              '^hitlifetime', '^hitstatus', '^hittypeid',
                              '^keywords', '^numavailable', '^numcomplete',
                              '^numpending', '^reviewstatus', '^reward',
                              '^title', '^hitid', '^assignmentid')

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
        except (AttributeError, KeyError) as ex:
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

def get_accepted_rejected_status(submission_dict, extra_submission_dict=tuple(), exclude_ids=tuple()):
    rejected = (submission_dict.get('reject') == 'y')
    accepted = (submission_dict.get('assignmentstatus', '').lower() == 'Approved'.lower())
    if submission_dict.get('assignmentid', '') in extra_submission_dict:
        props = extra_submission_dict[submission_dict['assignmentid']]
        rejected = 'rejected' in props and props['rejected'].lower() not in ('0', 'false', 'no', 'off')
        accepted = 'accepted' in props and props['accepted'].lower() not in ('0', 'false', 'no', 'off')
    if submission_dict.get('assignmentid', '') in exclude_ids:
        rejected = True
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

_BOOL_DICT = {'true':True, 'false':False, 'True':True, 'False':False, '0':False, '1':True, 0:False, 1:True, 'Did Not See':None, 'did not see':None}

def make_default_make_summary(description, prefix='task-', regex_postfix='-time-of-do-task', start_time_postfix='-time-of-do-task',
                              end_time_postfix='-time-of-finish-task', count_correct=True):
    def default_make_summary(properties, uid):
        rtn = []
        rtn.append('Summary:')
        task_regex = re.compile('^%s([0-9]+)%s$' % (prefix, regex_postfix))
        task_start_time = '%s%%d%s' % (prefix, start_time_postfix)
        task_end_time = '%s%%d%s' % (prefix, end_time_postfix)
        task_desc = description

        task_numbers = list(sorted(int(task_regex.match(key).groups()[0]) for key in properties if regex_postfix in key and prefix in key))
        
        right_count, wrong_count = 0, 0
        bad = 0
        for i in task_numbers:
            desc = task_desc % {'task':i}
            try:
                while '%(' in desc:
                    desc = desc % properties
            except KeyError:
                bad += 1
            rtn.append('\nTask %d: %s' % (i, desc))
            rtn.append('\nTask %d: ' % i)
            if count_correct:
                is_correct = _BOOL_DICT[properties['task-%d-is-correct-answer' % i]]
                if is_correct:
                    right_count += 1
                    rtn.append('Right')
                else:
                    wrong_count += 1
                    rtn.append('Wrong')
            if (task_end_time % i) in properties and properties[task_end_time % i]:
                start_time = int(properties[task_start_time % i])
                end_time = int(properties[task_end_time % i])
                rtn.append('\nTask %d duration: %d' % (i, end_time - start_time))
        if bad:
            print('Bad %d HIT: %s, %s' % (bad, properties.get('assignmentid', ''), uid))
        if count_correct:
            rtn.append('\n\nNumber Right: %d\nNumber Wrong: %d\nPercent Right: %d%%' % (right_count, wrong_count, 100.0 * right_count / (right_count + wrong_count)))
        rtn.append('\nDuration: %s' % properties['duration'].replace('0y 0d ', '').replace('0h ', ''))
        rtn.append('\nComments: %s' % (properties['feedback'] if 'feedback' in properties else ''))
        return ''.join(rtn)

    return default_make_summary

def put_summary(folder, properties, file_name, make_summary, uid, quiet=True):
    push_dir(folder)
    summary = make_summary(properties, uid)
    if not quiet and os.path.exists(file_name):
        input("The file `%s' in `%s' already exists.  Press enter to continue, or ^c (ctrl + c) to break." % (file_name, folder))
    with open(file_name, 'w') as f:
        f.write(summary)
    pop_dir()

def put_properties(folder, properties, file_name,
                   not_use=DEFAULT_NOT_USE_PROPERTIES, quiet=True):
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

def put_matlab(folder, properties, file_name, uid,
               not_use=DEFAULT_NOT_USE_PROPERTIES, quiet=True, zero_based_num=0):
    matlab_lines = []
    uid = uid.replace('-', 'm')
    def can_use(key):
        for bad_key in not_use:
            if re.match(bad_key, key):
                return False
        return True
    for key in sorted(properties.keys()):
        if can_use(key):
            use_key = key.replace('-', '_')
            if 'task_' in use_key:
                tag = use_key[:len('task_')+use_key.index('task_')-1]
                rest = use_key[len(tag)+1:].split('_')
                use_key = '%s(%d).%s' % (tag, int(rest[0]) + 1, '_'.join(rest[1:]))
            matlab_lines.append('results.for_%s(%d).%s = %s;' % (uid, zero_based_num+1, use_key,
                                format_for_matlab(string_to_object(properties[key]))))
    push_dir(folder)
    matlab = '\n'.join(matlab_lines)
    if not quiet and os.path.exists(file_name):
        input("The file `%s' in `%s' already exists.  Press enter to continue, or ^c (ctrl + c) to break." % (file_name, folder))
    with open(file_name, 'w') as f:
        f.write(matlab)
    pop_dir()

def deanonymize_urls(properties, tail_tag='-anonymous_url'):
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

def fix_str_dict(properties):
    weirdness = []
    for key in properties:
        if not isinstance(properties[key], str):
            weirdness.append(str((key, type(properties[key]), str(properties[key]))))
            print('<br>Your submission is weird: %s has a %s for a value: %s<br>' % (key, type(properties[key]), str(properties[key])))
            properties[key] = str(properties[key])
    if weirdness:
        properties['weirdness'] = ';'.join(weirdness)
    return properties

_OBJECT_DICT = {'true':True, 'false':False}
def string_to_object(string):
    if string in _OBJECT_DICT:
        return _OBJECT_DICT[string]
    try:
        return int(string)
    except ValueError:
        pass
    return string

def make_file_name(uid, summary=False, matlab=False):
    if summary:
        return uid.replace('-', 'm') + '_summary.txt'
    elif matlab:
        return uid.replace('-', 'm') + '_matlab.m'
    else:
        return uid.replace('-', 'm') + '_results.txt'


def record_submission(form_dict, path, make_summary, preprocess_form=None, prepreprocess_form=None, many_dirs=True,
                      verbose=True, pseudo=False, quiet=True, exclude_rejected=False, exclude_ids=tuple()):
    accepted, rejected = get_accepted_rejected_status(form_dict, exclude_ids=exclude_ids)
    if rejected and exclude_rejected:
        print('Submission rejected.')
        return False
    if verbose: print('Hashing IP address...')
    uid = make_uid(form_dict)
    results_num = 0
    if many_dirs:
        if verbose: print('Done.  It\'s %s.<br>Making folder for your submission...' % uid)
        path, results_num = make_folder_for_submission(uid, path=path, return_num=True)
    if verbose: print('Done<br>')
    if verbose: print('Done<br>Storing your responses...')
    if prepreprocess_form: form_dict = prepreprocess_form(form_dict)
    form_dict = fix_str_dict(form_dict)
    form_dict = deanonymize_urls(form_dict)
    if preprocess_form: form_dict = preprocess_form(form_dict)
    put_properties(path, form_dict, make_file_name(uid), quiet=quiet)
    if not pseudo:
        if verbose: print('Done<br>Summarizing your responses...')
        put_summary(path, form_dict, make_file_name(uid, summary=True), make_summary, uid, quiet=quiet)
        if verbose: print('Done<br>Making a matlab file for your responses...')
        put_matlab(path, form_dict, make_file_name(uid, matlab=True), uid, quiet=quiet, zero_based_num=results_num)
    if many_dirs:
        log_success(path)
    if verbose: print('Done<br>You may now leave this page.<br>')
    if verbose: print('<a href="http://jgross.scripts.mit.edu/alphabets/">Return to home page</a>')
