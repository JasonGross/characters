#!/usr/bin/python
# recordrecognitionrtsubmission.py -- Stores the data from the recognition rt submission
from __future__ import with_statement
import os, re
import sys
import shutil
from alphabetspaths import *
from matlabutil import format_for_matlab
from image_anonymizer import deanonymize_image
import turkutil


#def get_submission_paths(submission_dict, if_rejected=TURK_RECOGNITION_REJECTED_PATH, if_accepted=TURK_RECOGNITION_PATH, if_none=TURK_RECOGNITION_UNREVIEWED_PATH):
#    return turkutil.get_submission_paths(submission_dict, if_rejected, if_accepted, if_none)


def _make_folder_for_submission(uid, path=RECOGNITION_RT_UNREVIEWED_PATH, return_num=True):
    return turkutil.make_folder_for_submission(uid, path, return_num=return_num)


_BOOL_DICT = {'true':True, 'false':False, 'True':True, 'False':False, '0':False, '1':True, 0:False, 1:True, 'Did Not See':None, 'did not see':None}

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
            response['%s-id' % image_type] = '%s%s%s%s%s' % (url[:2], url[3:5], url[6:8], url[9:11], url[15:-4])
    percent_correct = right_count * 100 / (right_count + wrong_count) if right_count + wrong_count else -1
    percent_same_correct = right_same_count * 100 / (right_same_count + wrong_same_count) if right_same_count + wrong_same_count else -1
    percent_different_correct = right_different_count * 100 / (right_different_count + wrong_different_count) if right_different_count + wrong_different_count else -1
    
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
    rtn.append('\nComments: %s' % (properties['feedback'] if 'feedback' in properties else ''))
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
                 quiet=True, zero_based_num=0):
    rtn = []
    uid = uid.replace('-', 'm')
    def can_use(key):
        for bad_key in not_use:
            if re.match(bad_key, key):
                return False
        return True
    for key in sorted(properties.keys()):
        if can_use(key):
            use_key = key.replace('-', '_')
            if use_key[:len('task_')] == 'task_':
                use_key = use_key.split('_')
                use_key = '%s(%d).%s' % (use_key[0], int(use_key[1]) + 1, '_'.join(use_key[2:]))
            rtn.append('results.for_%s(%d).%s = %s;' % (uid, zero_based_num+1, use_key, format_for_matlab(properties[key])))
    return '\n'.join(rtn)
    

def _put_summary(folder, properties, file_name, quiet=True):
    turkutil.put_summary(folder, properties, file_name, _make_summary, quiet=quiet)
    
def _put_matlab(folder, properties, file_name, uid, quiet=True, **kwargs):
    push_dir(folder)
    matlab = _make_matlab(properties, uid, quiet=quiet, **kwargs)
    if not quiet and os.path.exists(file_name):
        input("The file `%s' in `%s' already exists.  Press enter to continue, or ^c (ctrl + c) to break." % (file_name, folder))
    with open(file_name, 'w') as f:
        f.write(matlab)
    pop_dir()
    

def _make_file_name(uid, summary=False, matlab=False):
    if summary:
        return uid.replace('-', 'm') + '_summary.txt'
    elif matlab:
        return uid.replace('-', 'm') + '_matlab.m'
    else:
        return uid.replace('-', 'm') + '_results.txt'


def record_submission(form_dict, many_dirs=True, path=RECOGNITION_RT_UNREVIEWED_PATH,
                      verbose=True, pseudo=False, quiet=True, exclude_rejected=False):
    accepted, rejected = turkutil.get_accepted_rejected_status(form_dict)
    if rejected and exclude_rejected:
        print('Submission rejected.')
        return False
    if verbose: print('Hashing IP address...')
    uid = turkutil.make_uid(form_dict)
    results_num = 0
    if many_dirs:
        if verbose: print('Done.  It\'s %s.<br>Making folder for your submission...' % uid)
        path, results_num = _make_folder_for_submission(uid, path=path, return_num=True)
    if verbose: print('Done<br>Storing your responses...')
    form_dict = turkutil.deanonymize_urls(form_dict)
    try:
        turkutil.put_properties(path, form_dict, _make_file_name(uid), quiet=quiet)
        if not pseudo:
            if verbose: print('Done<br>Summarizing your responses...')
            _put_summary(path, form_dict, _make_file_name(uid, summary=True), quiet=quiet)
            if verbose: print('Done<br>Making a matlab file for your responses...')
            _put_matlab(path, form_dict, _make_file_name(uid, matlab=True), uid, quiet=quiet, zero_based_num=results_num)
        if many_dirs:
            turkutil.log_success(path)
    except KeyError as ex:
        print('<br />  <strong>Error</strong>: %s. Failed to save.  Moving data to bad subdirectory.' % ex)
        new_path = os.path.join(path, '../../BAD')
        if not os.path.exists(new_path):
            os.makedirs(new_path)
        shutil.move(path, new_path)
    if verbose: print('Done<br>You may now leave this page.<br>')
    if verbose: print('<a href="http://scripts.mit.edu/~jgross/alphabets/">Return to home page</a>')
