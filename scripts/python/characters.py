#!/usr/bin/python
# Filename: alphabets.py
from __future__ import with_statement
import os, sys, json, cgi, cgitb, subprocess, tempfile, shutil, random, urllib
cgitb.enable()
try:
    import cPickle as pickle
except ImportError:
    import pickle
from alphabetspaths import *
from alphabetsutil import png_to_uri
from image_anonymizer import anonymize_image 


FROM_PATH = BASE_PATH

images = None

def get_boolean_value(form, true_keys, false_keys=None, default=None, true_options=(True,'true','1',1,'','yes','on','y','t'),
                      false_options=(False,'false','0',0,'','no','off','n','f'),
                      if_both=None, if_neither=None, aggregate_true_keys=any, aggregate_false_keys=any):
    if isinstance(true_keys, str): true_keys = [true_keys]
    if isinstance(false_keys, str): false_keys = [true_keys]
    if true_keys is None: true_keys = []
    if false_keys is None: false_keys = []
    if if_both is None: if_both = (lambda:default)
    if if_neither is None: if_neither = (lambda:default)
    true_value = aggregate_true_keys(true_key in form and aggregate_true_keys(value in true_options for value in form.getlist(true_key)) for true_key in true_keys)
    false_value = aggregate_false_keys(false_key in form and aggregate_false_keys(value in false_options for value in form.getlist(false_key)) for false_key in false_keys)
    if true_value and false_value: return if_both()
    elif not true_value and not false_value: return if_neither()
    else: return true_value and not false_value

def get_list_of_values(form, keys):
    if isinstance(keys, str): keys = [keys]
    rtn = []
    for key in keys:
        for cur_value in form.getlist(key):
            if not cur_value:
                rtn.append('')
            else:
                cur_value = json.loads(cur_value)
                try:
                    rtn += cur_value
                except TypeError:
                    rtn.append(cur_value)
    return rtn

def is_nested_type(obj, *types):
    if not types: return True
    first, rest = types[0], types[1:]
    try:
        for type_tree in first:
            try:
                if is_nested_type(obj, *type_tree):
                    return True
            except TypeError:
                if is_instance(obj, type_tree):
                    return True
            return False
    except TypeError:
        if isinstance(obj, first):
            return is_nested_type(obj, *rest)
        else:
            return False



def create_first_task(form):
    NUMBER_OF_TASKS = int(form.getfirst('numberOfTasks', 5))
    TRAINING_IMAGES_PER_TASK = int(form.getfirst('trainingImagesPerTask', 1))
    TEST_IMAGES_PER_TASK = int(form.getfirst('testImagesPerTask', 10))
    SAME_ALPHABET_DISTRASTORS_PER_TASK = int(form.getfirst('sameAlphabetDistractorsPerTask', 3))
    OTHER_ALPHABET_DISTRASTORS_PER_TASK = int(form.getfirst('otherAlphabetDistractorsPerTask', 2))
    DISTINCT_ALPHABETS = get_boolean_value(form, 'distinctTaskAlphabets')

    TOTAL_DISTRACTORS_PER_TASK = SAME_ALPHABET_DISTRASTORS_PER_TASK + OTHER_ALPHABET_DISTRASTORS_PER_TASK
    TRUE_TEST_IMAGES_PER_TASK = TEST_IMAGES_PER_TASK - TOTAL_DISTRACTORS_PER_TASK
    
    alphabets = get_accepted_image_list(from_path=FROM_PATH)

    all_characters = [(alphabet, image_num) for alphabet in alphabets for image_num in range(len(alphabets[alphabet].values()[0]))]
    
    if DISTINCT_ALPHABETS:
        training_characters = [(alphabet, random.choice(range(len(alphabets[alphabet].values()[0])))) for alphabet in random.sample(alphabets.keys(), NUMBER_OF_TASKS)]
    else:
        training_characters = random.sample(all_characters, NUMBER_OF_TASKS)

    tasks = []
    for i, (alphabet, character_num) in enumerate(training_characters):
        same_uids = sorted(alphabets[alphabet].keys())
        same_alphabet_same_characters = [alphabets[alphabet][uid][character_num]
                                         for uid in same_uids]
        same_alphabet_other_characters = [alphabets[alphabet][uid][num]
                                          for num in range(len(alphabets[alphabet][uid]))
                                          if (alphabet, num) not in training_characters
                                          for uid in sorted(alphabets[alphabet].keys())]
        other_alphabet_other_characters = [alphabets[alphabet][uid][num]
                                           for alphabet in sorted(alphabets.keys())
                                           for uid in sorted(alphabets[alphabet].keys())
                                           for num in range(len(alphabets[alphabet][uid]))
                                           if (alphabet, num) not in training_characters]
        random.shuffle(same_alphabet_same_characters)
        random.shuffle(same_alphabet_other_characters)
        random.shuffle(other_alphabet_other_characters)
        tasks.append({'training alphabet':alphabet,
                      'training character number':character_num,
                      'training characters':list(map(anonymize_image, same_alphabet_same_characters[:TRAINING_IMAGES_PER_TASK])),
                      'test characters': list(map(anonymize_image,
                                                  random.sample((same_alphabet_same_characters[TRAINING_IMAGES_PER_TASK:TRAINING_IMAGES_PER_TASK+TRUE_TEST_IMAGES_PER_TASK] +
                                                                 same_alphabet_other_characters[:SAME_ALPHABET_DISTRASTORS_PER_TASK] +
                                                                 other_alphabet_other_characters[:OTHER_ALPHABET_DISTRASTORS_PER_TASK]),
                                                                TEST_IMAGES_PER_TASK)))
                      })
    return tasks


def main():
    form = cgi.FieldStorage()
    non_existant_variable = form.getvalue('variableDoesNotExistString')
    if 'getObject' in form:
        objects = dict((name,
                        (globals()[name] if name in globals() else non_existant_variable)) \
                       for name in form.getlist('getObject'))
        print('Content-type: text/json\n')
        print(json.dumps(objects))
    else:
        rtn = create_first_task(form)
        print('Content-type: text/json\n')
        print(json.dumps(rtn))

if __name__ == '__main__':
    main()
        
