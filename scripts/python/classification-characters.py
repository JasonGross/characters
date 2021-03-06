#!/usr/bin/python
# Filename: classification-characters.py
from __future__ import with_statement
#import warnings
#warnings.simplefilter('ignore') #make cgitb work correctly
import cgi, cgitb
cgitb.enable(format='nohtml')
import os, sys, json, subprocess, tempfile, shutil, random, urllib, random
from itertools import islice
import argparse
try:
  import urllib.parse
except ImportError:
  pass
from cgiutil import get_boolean_value, get_list_of_values, is_nested_type
from alphabetspaths import *
import alphabetspopularity
from alphabetsutil import png_to_uri
from image_anonymizer import anonymize_image 
from objectstorage import get_object, save_object
import sequencer
from characters import make_foreground_alphabets

FROM_PATH = ACCEPTED_IMAGES_PATH

PLUS_MINUS_CHAR = '\u00B1'
PLUS_MINUS_STRINGS = ('+-', '-+', '+', PLUS_MINUS_CHAR)

_STROKE_NOISES = get_stroke_noises(from_path=BASE_PATH)

def anchor_classes_to_tasks(anchor_classes_list, verbose=True, random=random, alphabets_dict=None, anchor_count=1):
    if alphabets_dict is None: alphabets_dict = get_accepted_image_list()
    tasks = []

    for anchor, classes in anchor_classes_list:
        if verbose: print('Constructing trials for set ' + str((anchor, classes)))
        anchor_alphabet, anchor_character_i = anchor
        ids = random.sample(alphabets_dict[anchor_alphabet].keys(), anchor_count + 1);
        task_anchor = (anchor_alphabet, anchor_character_i, tuple(ids[1:]))
        task_classes = [((anchor_alphabet, anchor_character_i, ids[0]), True)] + \
                       [((alphabet, character_i, random.choice(alphabets_dict[alphabet].keys())), False)
                        for alphabet, character_i in classes]
        random.shuffle(task_classes)
        tasks.append((task_anchor, task_classes))

    random.shuffle(tasks)
    return tasks

def tasks_to_task_images(tasks, verbose=True, random=random):
    alphabets_dict = get_accepted_image_list(from_path=FROM_PATH)
    return [{
             'anchors' :[anonymize_image(alphabets_dict[alphabet][uid][character_i], from_path=FROM_PATH, include_hash=False, include_original=False)
                         for alphabet, character_i, ids in [anchor] # kludge to unpack values from anchor
                         for uid in ids],
             'classes':[([anonymize_image(alphabets_dict[alphabet][uid][character_i], from_path=FROM_PATH, include_hash=False, include_original=False)],
                         are_same)
                        for character_class, are_same in classes
                        for alphabet, character_i, uid in [character_class]]
            }
            for anchor, classes in tasks]

def make_task(foreground_fraction=0.75, verbose=True, random=random, **kwargs):

    if verbose: print('Getting list of alphabets...')
    alphabets_dict = get_accepted_image_list()

    alphabets_use = make_foreground_alphabets(random=random, verbose=verbose, alphabets_dict=alphabets_dict, foreground_fraction=foreground_fraction, **kwargs)

    return make_task_from_alphabet_list(alphabets_use, random=random, verbose=verbose, alphabets_dict=alphabets_dict, **kwargs)

def make_task_from_alphabet_list(alphabets_use, alphabets_dict=None,
                                 verbose=True, random=random, **kwargs):
    if alphabets_dict is None: alphabets_dict = get_accepted_image_list()

    remaining_characters_use = []
    for alphabet in alphabets_use:
        if verbose: print('Collecting characters from %s...' % alphabet)
        remaining_characters_use.extend((alphabet, character_i) for character_i in range(len(alphabets_dict[alphabet].values()[0])))

    return make_task_from_characters_list(remaining_characters_use, alphabets_dict=alphabets_dict, verbose=verbose, random=random, **kwargs)

def make_task_from_characters_list(remaining_characters_use, unique=True, unique_classes=True, anchor_count=1, class_count=20,
                                   same_alphabet_class_count=-1, task_count=50,
                                   alphabets_dict=None, verbose=True, random=random, **kwargs):
    if same_alphabet_class_count < 0: same_alphabet_class_count = None
    if alphabets_dict is None: alphabets_dict = get_accepted_image_list()
    if same_alphabet_class_count is not None and unique_classes: raise Exception("Cannot have multiple identical classes and have them all be distinct.")

    random.shuffle(remaining_characters_use)

    if unique: 
        anchor_characters = remaining_characters_use[:task_count]
        remaining_characters_use = remaining_characters_use[task_count:]
    else:
        anchor_characters = random.sample(remaining_characters_use, task_count)

    tasks = []
    class_count -= 1

    for anchor in anchor_characters:
        classes = []
        if same_alphabet_class_count is None:
            if unique_classes:
                if unique:
                    i = 0
                    used_alphabets = set([anchor[0]])
                    while len(classes) < class_count:
                        if i >= len(remaining_characters_use): raise Exception("Not enough characters")
                        if remaining_characters_use[i][0] not in used_alphabets:
                            used_alphabets.add(remaining_characters_use[i][0])
                            classes.append(remaining_characters_use[i])
                            del remaining_characters_use[i]
                        else:
                            i += 1
                else:
                    i = 0
                    used_alphabets = set([anchor[0]])
                    while len(classes) < class_count:
                        if i >= len(remaining_characters_use): raise Exception("Not enough characters")
                        if remaining_characters_use[i][0] not in used_alphabets:
                            used_alphabets.add(remaining_characters_use[i][0])
                            classes.append(remaining_characters_use[i])
                        i += 1
                    random.shuffle(remaining_characters_use)
            else:
                if unique:
                    if len(remaining_characters_use) < class_count: raise Exception("Not enough characters")
                    classes.extend(remaining_characters_use[:class_count])
                    remaining_characters_use = remaining_characters_use[class_count:]
                else: # exclude characters identical to the anchor
                    classes.extend(islice((character for character in remaining_characters_use if character != anchor), class_count))
                    random.shuffle(remaining_characters_use)
        else:
            if unique:
                if len(remaining_characters_use) < class_count: raise Exception("Not enough characters")
                i = 0
                same_alphabet_count, different_alphabet_count = 0, 0
                while len(classes) < class_count:
                    if remaining_characters_use[i][0] == anchor[0] and same_alphabet_count < same_alphabet_class_count:
                        same_alphabet_count += 1
                        classes.append(remaining_characters_use[i])
                        del remaining_characters_use[i]
                    elif remaining_characters_use[i][0] == anchor[0] and different_alphabet_count < class_count - same_alphabet_class_count:
                        different_alphabet_count += 1
                        classes.append(remaining_characters_use[i])
                        del remaining_characters_use[i]
                    else:
                        i += 1
            else:
                classes.extend(islice((character for character in remaining_characters_use if character[0] != anchor[0]), same_alphabet_class_count))
                classes.extend(islice((character for character in remaining_characters_use if character[0] == anchor[0] and character != anchor),
                                      class_count - same_alphabet_class_count))
                random.shuffle(remaining_characters_use)
        tasks.append((anchor, classes))


    tasks = anchor_classes_to_tasks(tasks, random=random, verbose=verbose, alphabets_dict=alphabets_dict, anchor_count=anchor_count)
    return tasks_to_task_images(tasks, verbose=verbose, random=random)

def make_task_from_alphabet_set(alphabet_set, alphabets_dict=None, **kwargs):
    if alphabets_dict is None: alphabets_dict = get_accepted_image_list()
    def bad_alias():
        raise Exception("Character set with the given name does not exist.  Run construct-character-set.py to create it.")
    
    list_of_stuff = get_object('recognition-tasks_character-set_%s' % alphabet_set, bad_alias)
    if not isinstance(list_of_stuff[0], (list, tuple)):
        return make_task_from_alphabet_list(list_of_stuff, alphabets_dict=alphabets_dict, **kwargs)
    else: # is string
        return make_task_from_characters_list(list_of_stuff, alphabets_dict=alphabets_dict, **kwargs)
#    else:
#        print(list_of_stuff)
#        raw_input(list_of_stuff[0])
#        raise Exception("Character set with the given name is malformed.")


def create_first_task(form, args, verbose=False):
    passOnValues = {'pauseToFirstHint':[500],
                    'pauseToSecondHint':[500],
                    'pauseToAnchor':[1000],
                    'pauseToNoise':[-1],
                    'pauseToTest':[1000],
                    'tasksPerFeedbackGroup':[10],
                    'pauseToNextGroup':[-1],
                    'displayProgressBarDuringTask':False,
                    'allowDidNotSeeCount':[1],
                    'taskCount':50,
                    'anchorCount':1,
                    'classCount':20,
                    'unique':False,
                    'uniqueClasses':True,
                    'confirmToContinue':True,
                    'anchorPosition':'above',
                    'sameAlphabetClassCount':-1,
                    'characterSize':'50px',
                    'characterSet':''
                    }
    for key in passOnValues:
        if hasattr(args, key) and getattr(args, key) is not None:
            if isinstance(passOnValues[key], (list, tuple)) and not isinstance(getattr(args, key), (list, tuple)):
                passOnValues[key] = [getattr(args, key)]
            else:
                passOnValues[key] = getattr(args, key)

    rtn = {}

    for key in passOnValues:
        if isinstance(passOnValues[key], bool): rtn[key] = get_boolean_value(form, key, default=passOnValues[key])
        else: rtn[key] = form.getfirst(key, passOnValues[key])
        if isinstance(rtn[key], str) and any(sign_char in rtn[key] for sign_char in PLUS_MINUS_STRINGS):
            for sign_char in PLUS_MINUS_STRINGS:
                rtn[key] = rtn[key].replace(sign_char, PLUS_MINUS_CHAR)
            rtn[key] = rtn[key].split(PLUS_MINUS_CHAR)
            rtn[key] = list(map(int, rtn[key]))
        elif isinstance(rtn[key], (tuple, list)):
            rtn[key] = list(map(int, rtn[key]))
        elif isinstance(rtn[key], bool):
            pass
        elif isinstance(passOnValues[key], (list, tuple)):
            rtn[key] = [int(rtn[key])]
        elif isinstance(passOnValues[key], int):
            rtn[key] = int(rtn[key])
        elif isinstance(passOnValues[key], float):
            rtn[key] = float(rtn[key])
        if isinstance(rtn[key], list) and len(rtn[key]) < 2:
            rtn[key].append(0)
    
    rtn['imagesPerTask'] = 2 * rtn['anchorCount'] + rtn['classCount']

    if rtn['characterSet']:
        rtn['tasks'] = make_task_from_alphabet_set(rtn['characterSet'], verbose=verbose, anchor_count=rtn['anchorCount'], class_count=rtn['classCount'],
                                                   same_alphabet_class_count=rtn['sameAlphabetClassCount'], task_count=rtn['taskCount'], 
                                                   unique=rtn['unique'], unique_classes=rtn['uniqueClasses'])
    else:
        rtn['tasks'] = make_task(verbose=verbose, anchor_count=rtn['anchorCount'], class_count=rtn['classCount'], 
                                 same_alphabet_class_count=rtn['sameAlphabetClassCount'], task_count=rtn['taskCount'], unique=rtn['unique'],
                                 unique_classes=rtn['uniqueClasses'])
    return rtn

def main():
    form = cgi.FieldStorage(keep_blank_values=True)
    non_existant_variable = form.getvalue('&=variableDoesNotExistString=&')
    args, argv = parser.parse_known_args()
    rtn = create_first_task(form, args, verbose=args.verbose)
#    rtn = create_first_task(form)
    print('Content-type: text/json\n')
    print(json.dumps(rtn))

parser = argparse.ArgumentParser(description='Get the characters classification task')
parser.add_argument('--verbose', '-v', action='store_true',
                    help='print status on recreating tasks')
parser.add_argument('--character-set', '-s', dest='characterSet', type=str,
                    help='name of character set to use')
parser.add_argument('--no-unique', dest='unique', action='store_false',
                    help='unique characters?')
if __name__ == '__main__':
    main()
