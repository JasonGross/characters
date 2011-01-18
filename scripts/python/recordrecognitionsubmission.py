#!/usr/bin/python
# recordcategorizationsubmission.py -- Stores the data from the categorization submission
from __future__ import with_statement
import os, re
import sys
from alphabetspaths import *
from matlabutil import format_for_matlab


def _make_folder_for_submission(uid, path=RECOGNITION_UNREVIEWED_PATH):
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
    return os.path.join(path, uid.replace('-', 'm'), new_dir)


_BOOL_DICT = {'true':True, 'false':False, 'True':True, 'False':False, '0':False, '1':True, 0:False, 1:True}

_REWRITE_DICT = {}
for alphabet in sorted(os.listdir(ACCEPTED_IMAGES_PATH)):
    _REWRITE_DICT[(alphabet + 'a')[:4]] = alphabet

def _make_summary(properties):
    rtn = []
    rtn.append('\n\nSummary:')
    is_correct_regex = re.compile('task-([0-9]+)-is-correct-answer')
    regex = re.compile('^task-([0-9]+)_question$')
    task_numbers = list(sorted(int(regex.match(key).groups()[0]) for key in properties if '_question' in key))

    responses = []
    for task_number in task_numbers:
        responses.append({'task-number':task_number,
                          'duration':int(properties['task-%d-duration-of-see-test' % task_number]),
                          'said-are-same': _BOOL_DICT[properties['task-%d_question' % task_number]],
                          'example-url': os.path.split(properties['task-%d-example-url' % task_number])[1],
                          'test-url': os.path.split(properties['task-%d-test-url' % task_number])[1],
                          'is-correct': _BOOL_DICT[properties['task-%d-is-correct-answer' % task_number]]})
    right_count = 0
    wrong_count = 0
    right_same_count = 0
    wrong_same_count = 0
    right_different_count = 0
    wrong_different_count = 0

    for response in responses:
        if response['is-correct']: 
            right_count += 1
            if response['said-are-same']: right_same_count += 1
            else: right_different_count += 1
        else: 
            wrong_count += 1
            if response['said-are-same']: wrong_different_count += 1
            else: wrong_same_count += 1
        for image_type in ('example', 'test'):
            url = response['%s-url' % image_type]
            response['%s-alphabet' % image_type] = _REWRITE_DICT['%s%s%s%s' % (url[2], url[5], url[8], url[11])]
            response['%s-character-number' % image_type] = int(url[12:14])
            response['%s-id' % image_type] = url[15:-4]
    percent_correct = right_count * 100 / (right_count + wrong_count)
    percent_same_correct = right_same_count * 100 / (right_same_count + wrong_same_count)
    percent_different_correct = right_different_count * 100 / (right_different_count + wrong_different_count)
    
    rtn.append("""Short Summary:
Correct: %(right_count)d
Incorrect: %(wrong_count)d
Percent Correct: %(percent_correct)d

Same Correct: %(right_same_count)d
Same Incorrect: %(wrong_same_count)d
Percent Same Correct: %(percent_same_correct)d

Different Correct: %(right_different_count)d
Different Incorrect: %(wrong_different_count)d
Percent Different Correct: %(percent_different_correct)d

Long Summary:
""" % locals())
    
    for response in responses:
        rtn.append('Task %(task-number)d: ' % response)
        if not response['is-correct']: rtn.append('in')
        rtn.append('correctly said that ')
        rtn.append('(%(example-alphabet)s, %(example-character-number)d, %(example-id)s) and ' % response)
        rtn.append('(%(test-alphabet)s, %(test-character-number)d, %(test-id)s) are ' % response)
        if not response['said-are-same']: rtn.append('not ')
        rtn.append('the same in %(duration)d ms.\n' % response)
    rtn.append('\nDuration: %s' % properties['duration'].replace('0y 0d ', '').replace('0h ', ''))
    return ''.join(rtn)

def _make_matlab(properties, uid,
                 not_use=('^ipAddress',
                          '^annotation', '^assignmentaccepttime', '^assignmentapprovaltime',
                          '^assignmentduration', '^assignmentrejecttime', '^assignments',
                          '^assignmentstatus', '^assignmentsubmittime', '^autoapprovaldelay',
                          '^autoapprovaltime', '^creationtime', '^deadline', '^description',
                          '^hitlifetime', '^hitstatus', '^hittypeid', '^keywords',
                          '^numavailable', '^numcomplete', '^numpending', '^reviewstatus',
                          '^reward', '^title', '^hitid', '^assignmentid'),
                 quiet=True):
    rtn = []
    uid = uid.replace('-', 'm')
    def can_use(key):
        for bad_key in not_use:
            if re.match(bad_key, key):
                return False
        return True
    for key in sorted(properties.keys()):
        if can_use(key):
            rtn.append('results.for_%s.%s = %s;' % (uid, key, format_for_matlab(properties[key])))
    return '\n'.join(rtn)
    

def _put_summary(folder, properties, file_name, quiet=True):
    push_dir(folder)
    summary = _make_summary(properties)
    if not quiet and os.path.exists(file_name):
        input("The file `%s' in `%s' already exists.  Press enter to continue, or ^c (ctrl + c) to break." % (file_name, folder))
    with open(file_name, 'w') as f:
        f.write(summary)
    pop_dir()
    
def _put_matlab(folder, properties, file_name, quiet=True):
    push_dir(folder)
    matlab = _make_matlab(properties, uid, quiet=quiet)
    if not quiet and os.path.exists(file_name):
        input("The file `%s' in `%s' already exists.  Press enter to continue, or ^c (ctrl + c) to break." % (file_name, folder))
    with open(file_name, 'w') as f:
        f.write(matlab)
    pop_dir()
    

def _put_properties(folder, properties, file_name,
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

def _log_success(folder):
    push_dir(folder)
    with open('success.log', 'w') as f:
        f.write('')
    pop_dir()

def make_uid(form_dict):
    if 'workerid' in form_dict and form_dict['workerid']:
        return form_dict['workerid']
    else:
        return str(hash(form_dict['ipAddress']))

def _make_file_name(uid, summary=False, matlab=False):
    if summary:
        return uid.replace('-', 'm') + '_summary.txt'
    elif matlab:
        return uid.replace('-', 'm') + '_matlab.m'
    else:
        return uid.replace('-', 'm') + '_results.txt'

def record_submission(form_dict, many_dirs=True, path=RECOGNITION_UNREVIEWED_PATH,
                      verbose=True, pseudo=False, quiet=True):
    if verbose: print('Hashing IP address...')
    uid = make_uid(form_dict)
    if many_dirs:
        if verbose: print('Done.  It\'s %s.<br>Making folder for your submission...' % uid)
        path = _make_folder_for_submission(uid, path=path)
    if verbose: print('Done<br>Storing your responses...')
    _put_properties(path, form_dict, _make_file_name(uid), quiet=quiet)
    if not pseudo:
        if verbose: print('Done<br>Summarizing your responses...')
        _put_summary(path, form_dict, _make_file_name(uid, summary=True), quiet=quiet)
        if verbose: print('Done<br>Making a matlab file for your responses...')
        _put_matlab(path, form_dict, _make_file_name(uid, matlab=True), quiet=quiet)
    if many_dirs:
        _log_success(path)
    if verbose: print('Done<br>You may now leave this page.<br>')
    if verbose: print('<a href="http://scripts.mit.edu/~jgross/alphabets/">Return to home page</a>')
