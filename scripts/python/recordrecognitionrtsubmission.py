#!/usr/bin/python
# recordrecognitionrtsubmission.py -- Stores the data from the recognition rt submission
import re
from alphabetspaths import *
import turkutil

_BOOL_DICT = {'true':True, 'false':False, 'True':True, 'False':False, '0':False, '1':True, 0:False, 1:True, 'Did Not See':None, 'did not see':None}

def _make_summary(properties, uid=None):
    rtn = []
    rtn.append('Summary:')
    calibration_task_regex = re.compile('^calibration_task-([0-9]+)-time-of-showCharacters$')
    task_regex = re.compile('^task-([0-9]+)-time-of-showCharacters$')
    calibration_start_time = 'calibration_task-%d-time-of-showCharacters'
    calibration_end_time = 'calibration_task-%d-time-of-keypress'
    task_start_time = 'task-%d-time-of-showCharacters'
    task_end_time = 'task-%d-time-of-keypress'
    task_desc = '%%(task-%(task)d-character-0-alphabet)s, %%(task-%(task)d-character-0-character-number)s, %%(task-%(task)d-character-0-id)s VS. ' + \
            '%%(task-%(task)d-character-1-alphabet)s, %%(task-%(task)d-character-1-character-number)s, %%(task-%(task)d-character-1-id)s'

    calibration_numbers = list(sorted(int(calibration_task_regex.match(key).groups()[0]) for key in properties
        if 'calibration' in key and '-time-of-showCharacters' in key))
    task_numbers = list(sorted(int(task_regex.match(key).groups()[0]) for key in properties
        if 'calibration' not in key and '-time-of-showCharacters' in key))
    
    rtn.append('\nCalibration:')
    total_time, task_count = 0, 0
    for i in calibration_numbers:
        task_count += 1
        cur_time = int(properties[calibration_end_time % i]) - int(properties[calibration_start_time % i])
        total_time += cur_time
        rtn.append('\n%d' % cur_time)
    rtn.append('\nAverage: %d\n\n' % int(total_time / task_count))
    
    rtn.append('\nTasks:')
    for i in task_numbers:
        rtn.append('\nTask %d: %s' % (i, ((task_desc % {'task':i}) % properties)))
        is_correct = _BOOL_DICT[properties['task-%d-is-correct-answer' % i]]
        are_same = _BOOL_DICT[properties['task-%d-are-same' % i]]
        rtn.append('\nTask %d: ' % i)
        if is_correct: rtn.append('Right, ')
        else: rtn.append('Wrong, ')
        if are_same: rtn.append('Are Same')
        else: rtn.append('Are Different')
        if (task_end_time % i) in properties and properties[task_end_time % i]:
            start_time = int(properties[task_start_time % i])
            end_time = int(properties[task_end_time % i])
            rtn.append('\nTask %d RT: %d' % (i, end_time - start_time))
    return ''.join(rtn)

    


def _record_reaction_times(properties, overwrite=True, tags=('task-', 'calibration_task-'),
        start_time_end='-time-of-showCharacters', end_time_end='-time-of-keypress', find_nums='-time-of-showCharacters',
        if_none=-1):
    if not overwrite: properties = dict(properties)
    for tag in tags:
        cur_regex = re.compile('^%s([0-9]+)' % tag)
        pre_nums = (cur_regex.match(key) for key in properties if tag in key and find_nums in key)
        nums = list(sorted(set(int(match.groups()[0]) for match in pre_nums if match)))
        start_time_key = '%s%%d%s' % (tag, start_time_end)
        end_time_key = '%s%%d%s' % (tag, end_time_end)
        for i in nums:
            if (start_time_key % i) in properties and (end_time_key % i) in properties and \
               properties[start_time_key % i] and properties[end_time_key % i]:
                properties['%s%d-reaction-time' % (tag, i)] = str(int(properties[end_time_key % i]) - int(properties[start_time_key % i]))
            else:
                properties['%s%d-reaction-time' % (tag, i)] = str(if_none)
    return properties

def record_submission(form_dict, path=RECOGNITION_RT_UNREVIEWED_PATH, **kwargs):
    turkutil.record_submission(form_dict, path=path, make_summary=_make_summary, preprocess_form=_record_reaction_times, **kwargs)
