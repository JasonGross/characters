#!/usr/bin/python
# recordcategorizationsubmission.py -- Stores the data from the categorization submission
import re
from alphabetspaths import *
import turkutil

def _make_summary(properties, uid=None):
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

def record_categorization_submission(form_dict, path=CATEGORIZATION_UNREVIEWED_PATH, **kwargs):
    turkutil.record_submission(form_dict, path=path, make_summary=_make_summary, **kwargs)
