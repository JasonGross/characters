#!/usr/bin/python
# recordsimilaritysubmission.py -- Stores the data from the  submission
from __future__ import with_statement
import os, re
import sys
import shutil
import traceback
from alphabetspaths import *
from matlabutil import format_for_matlab
from image_anonymizer import deanonymize_image
import turkutil
try:
    import cPickle as pickle
except ImportError:
    import pickle

def _make_folder_for_submission(uid, path=SIMILARITY_UNREVIEWED_PATH, return_num=True):
    return turkutil.make_folder_for_submission(uid, path, return_num=return_num)


_BOOL_DICT = {'true':True, 'false':False, 'True':True, 'False':False, '0':False, '1':True, 0:False, 1:True, 'Did Not See':None, 'did not see':None}

def _make_summary(properties):
    rtn = []
    rtn.append('Summary:')
    task_regex = re.compile('^task-([0-9]+)-time-of-do-task$')
    task_start_time = 'task-%d-time-of-do-task'
    task_end_time = 'task-%d-time-of-finish-task'
    task_desc = '%%(task-%(task)d-image-0-alphabet)s, %%(task-%(task)d-image-0-character-number)s, %%(task-%(task)d-image-0-id)s, ' + \
                '%%(task-%(task)d-image-1-alphabet)s, %%(task-%(task)d-image-1-character-number)s, %%(task-%(task)d-image-1-id)s, ' + \
                '%%(task-%(task)d-answer)s'

    task_numbers = list(sorted(int(task_regex.match(key).groups()[0]) for key in properties if '-time-of-do-task' in key))

    right_count, wrong_count = 0, 0
    for i in task_numbers:
        desc = task_desc % {'task':i}
        while '%(' in desc:
            desc = desc % properties
        rtn.append('\nTask %d: %s' % (i, desc))
        if (task_end_time % i) in properties and properties[task_end_time % i]:
            start_time = int(properties[task_start_time % i])
            end_time = int(properties[task_end_time % i])
            rtn.append('\nTask %d duration: %d' % (i, end_time - start_time))
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
            if 'task_' in use_key:
                tag = use_key[:len('task_')+use_key.index('task_')-1]
                rest = use_key[len(tag)+1:].split('_')
                use_key = '%s(%d).%s' % (tag, int(rest[0]) + 1, '_'.join(rest[1:]))
            rtn.append('results.for_%s(%d).%s = %s;' % (uid, zero_based_num+1, use_key, 
                format_for_matlab(turkutil.string_to_object(properties[key]))))
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


def record_submission(form_dict, many_dirs=True, path=SIMILARITY_UNREVIEWED_PATH,
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
    if verbose: print('Done<br>')
    if verbose: print('Done<br>Storing your responses...')
    form_dict = turkutil.fix_str_dict(form_dict)
    form_dict = turkutil.deanonymize_urls(form_dict)
    turkutil.put_properties(path, form_dict, _make_file_name(uid), quiet=quiet)
    if not pseudo:
        if verbose: print('Done<br>Summarizing your responses...')
        _put_summary(path, form_dict, _make_file_name(uid, summary=True), quiet=quiet)
        if verbose: print('Done<br>Making a matlab file for your responses...')
        _put_matlab(path, form_dict, _make_file_name(uid, matlab=True), uid, quiet=quiet, zero_based_num=results_num)
    if many_dirs:
        turkutil.log_success(path)
    if verbose: print('Done<br>You may now leave this page.<br>')
    if verbose: print('<a href="http://scripts.mit.edu/~jgross/alphabets/">Return to home page</a>')
