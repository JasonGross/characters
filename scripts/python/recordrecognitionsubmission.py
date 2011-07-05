#!/usr/bin/python
# recordcategorizationsubmission.py -- Stores the data from the categorization submission
import re
from alphabetspaths import *
import turkutil

_BOOL_DICT = {'true':True, 'false':False, 'True':True, 'False':False, '0':False, '1':True, 0:False, 1:True, 'Did Not See':None, 'did not see':None}

def _fix_url_tags(properties):
    for key in sorted(properties.keys()):
        if key[:len('task-')] == 'task-' and key[-len('-url'):] == '-url':
            properties[key.replace('-url', '-anonymous_url')] = properties[key]
    return properties

def _make_summary(properties, uid=None):
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
                          'example-alphabet': properties['task-%d-example-alphabet' % task_number],
                          'example-character-number': properties['task-%d-example-character-number' % task_number],
                          'example-id': properties['task-%d-example-id' % task_number],
                          'test-alphabet': properties['task-%d-test-alphabet' % task_number],
                          'test-character-number': properties['task-%d-test-character-number' % task_number],
                          'test-id': properties['task-%d-test-id' % task_number],
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


def record_submission(form_dict, path=RECOGNITION_UNREVIEWED_PATH, **kwargs):
    turkutil.record_submission(form_dict, path=path, make_summary=_make_summary, prepreprocess_form=_fix_url_tags, **kwargs)
