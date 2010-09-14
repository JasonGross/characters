#!/usr/bin/python
# recordcategorizationsubmission.py -- Stores the data from the categorization submission
from __future__ import with_statement
import os, re
import sys
from alphabetspaths import *


def _make_folder_for_submission(uid, path=CATEGORIZATION_UNREVIEWED_PATH):
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

def _make_summary(properties):
    rtn = []
    rtn.append('\n\nSummary:')
    regex = re.compile('question_([0-9]+)-group_([0-9]+)-questionImagePath')
    training_image_reg = 'alphabet_([0-9]+)-group_%d-alphabetGlobalNum_([0-9]+)-imagePath'
    question_images = (list(map(int, regex.match(key).groups())) + [properties[key]] for key in properties if '-questionImagePath' in key)
    groups = {}
    for question_image in question_images:
        if question_image[1] not in groups:
            groups[question_image[1]] = {}
        groups[question_image[1]][question_image[0]] = {'question image': question_image[-1]}
    for group_num in groups:
        group = groups[group_num]
        regex = re.compile(training_image_reg % group_num)
        for question_num in group:
            question = group[question_num]
            question['real alphabet id'] = get_alphabet_id_from_file_name(question['question image'])
            choice_alphabets = (list(map(int, regex.match(key).groups())) + [properties[key]] \
                                for key in properties if regex.match(key))
            choice_alphabets = dict((alphabet[1], get_alphabet_id_from_file_name(alphabet[-1])) for alphabet in choice_alphabets)
            question['choice alphabet ids'] = list(choice_alphabets[key] for key in sorted(list(choice_alphabets.keys())))
            selection_regex = re.compile('alphabet_group_%d_number_test_%d' % (group_num, question_num))
            question['selected alphabet id'] = [choice_alphabets[int(properties[key])] for key in properties if selection_regex.match(key)][0]
            question['correct'] = question['selected alphabet id'] == question['real alphabet id']
            del question['question image']
    right_count = 0
    wrong_count = 0
    for group_num in sorted(list(groups.keys())):
        for question_num in sorted(list(groups[group_num].keys())):
            question = groups[group_num][question_num]
            cur_line = []
            if question['correct']:
                cur_line.append('Right: Selected "')
                cur_line.append(get_alphabet_name(question['selected alphabet id']))
                right_count += 1
            else:
                cur_line.append('Wrong: Selected "')
                cur_line.append(get_alphabet_name(question['selected alphabet id']))
                cur_line.append('" instead of "')
                cur_line.append(get_alphabet_name(question['real alphabet id']))
                wrong_count += 1
            cur_line.append('" from options "')
            cur_line.append('", "'.join(map(get_alphabet_name, question['choice alphabet ids'])))
            cur_line.append('"')
            rtn.append(''.join(cur_line))
    rtn.append('\nTotals:')
    rtn.append('Correct: %d\nIncorrect: %d' % (right_count, wrong_count))
    rtn.append('\nDuration: %s' % properties['duration'].replace('0y 0d ', '').replace('0h ', ''))
    return '\n'.join(rtn)
            
def _put_summary(folder, properties, file_name, quiet=True):
    push_dir(folder)
    summary = _make_summary(properties)
    if not quiet and os.path.exists(file_name):
        input("The file `%s' in `%s' already exists.  Press enter to continue, or ^c (ctrl + c) to break." % (file_name, folder))
    with open(file_name, 'w') as f:
        f.write(summary)
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

def _make_file_name(uid, summary=False):
    if summary:
        return uid.replace('-', 'm') + '_summary.txt'
    return uid.replace('-', 'm') + '_results.txt'

def record_categorization_submission(form_dict, many_dirs=False, path=CATEGORIZATION_UNREVIEWED_PATH,
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
    if many_dirs:
        _log_success(path)
    if verbose: print('Done<br>You may now leave this page.<br>')
    if verbose: print('<a href="http://scripts.mit.edu/~jgross/alphabets/">Return to home page</a>')
