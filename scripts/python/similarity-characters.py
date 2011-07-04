#!/usr/bin/python
# Filename: similarity-characters.py
from __future__ import with_statement
#import warnings
#warnings.simplefilter('ignore') #make cgitb work correctly
import cgi, cgitb
cgitb.enable(format='nohtml')
import os, sys, json, subprocess, tempfile, shutil, random, urllib, random
import itertools
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
from characters import make_foreground_alphabets, aggregate_values

FROM_PATH = ACCEPTED_IMAGES_PATH

def tasks_to_task_images(tasks, verbose=True, random=random, alphabets_dict=None):
    if alphabets_dict is None: alphabets_dict = get_accepted_image_list(from_path=FROM_PATH)
    return [{
             'images': [anonymize_image(alphabets_dict[alphabet][uid][character_i], from_path=FROM_PATH, include_hash=False, include_original=False)
                        for alphabet, character_i, uid in task],
             'areSame': task[0][0] == task[1][0] and task[0][1] == task[1][1]
            }
            for task in tasks]

def make_task(foreground_fraction=0.75, verbose=True, random=random, **kwargs):

    if verbose: print('Getting list of alphabets...')
    alphabets_dict = get_accepted_image_list()

    alphabets_list = make_foreground_alphabets(random=random, verbose=verbose, alphabets_dict=alphabets_dict, foreground_fraction=foreground_fraction, **kwargs)

    return make_task_from_alphabets_list(alphabets_list, random=random, verbose=verbose, alphabets_dict=alphabets_dict, **kwargs)

def make_task_from_alphabets_list(alphabets_list, alphabets_dict=None, verbose=True, random=random, **kwargs):
    if alphabets_dict is None: alphabets_dict = get_accepted_image_list()

    characters_list = []
    for alphabet in alphabets_list:
        if verbose: print('Collecting characters from %s...' % alphabet)
        characters_list.extend((alphabet, character_i) for character_i in range(len(alphabets_dict[alphabet].values()[0])))

    return make_task_from_characters_list(characters_list, alphabets_dict=alphabets_dict, verbose=verbose, random=random, **kwargs)

def make_task_from_characters_list(characters_list, unique=True, same_character_fraction=0.5, different_alphabet_fraction=-1, task_count=200,
                                   alphabets_dict=None, verbose=True, random=random, **kwargs):
    if same_character_fraction < 0: same_character_fraction = None
    if different_alphabet_fraction < 0: different_alphabet_fraction = None
    if alphabets_dict is None: alphabets_dict = get_accepted_image_list()

    random.shuffle(characters_list)

    tasks_left = task_count

    tasks = []

    if same_character_fraction is not None:
        same_character_count = int(same_character_fraction * task_count)
        tasks_left -= same_character_count
        if unique:
            same_characters = characters_list[:same_character_count]
            characters_list = characters_list[same_character_count:]
        else:
            same_characters = random.sample(characters_list, same_character_count)

        tasks.extend(((alphabet, character, uid_0), (alphabet, character, uid_1))
                     for alphabet, character in same_characters
                     for uid_0, uid_1 in [random.sample(alphabets_dict[alphabet].keys(), 2)])

    if unique:
        if different_alphabet_fraction is None:
            pairs = zip(characters_list[:tasks_left], characters_list[tasks_left:]) # truncation will cut the second list to size
        else:
            different_alphabet_count = int(different_alphabet_fraction * task_count)
            def make_pairs(different_alphabet_count, same_alphabet_count):
                i, j = 0, 1
                while True:
                    if j >= len(characters_list):
                        i += 1
                        j = i + 1
                    if i >= len(characters_list) - 1:
                        return
                    first, second = characters_list[i], characters_list[j]
                    if first[0] != second[0] and different_alphabet_count > 0:
                        different_alphabet_count -= 1
                        del characters_list[i], characters_list[j]
                        i, j = 0, 1
                        yield (first, second)
                    elif first[0] == second[0] and same_alphabet_count > 0:
                        same_alphabet_count -= 1
                        del characters_list[i], characters_list[j]
                        i, j = 0, 1
                        yield (first, second)
                    else:
                        j += 1
            pairs = make_pairs(different_alphabet_count, tasks_left - different_alphabet_count)
    else:
        pairs = ((random.choice(characters_list), random.choice(characters_list))
                 for i in itertools.count()) 
        if same_character_fraction is not None:
            old_pairs_s = pairs
            pairs = (((alphabet_0, character_0), (alphabet_1, character_1))
                     for (alphabet_0, character_0), (alphabet_1, character_1) in old_pairs_s
                     if alphabet_0 != alphabet_1 or character_0 != character_1)
        if different_alphabet_fraction is not None:
            old_pairs_0 = pairs
            pairs_diff = (((alphabet_0, character_0), (alphabet_1, character_1))
                          for (alphabet_0, character_0), (alphabet_1, character_1) in old_pairs_0
                          if alphabet_0 != alphabet_1)
            pairs_same = (((alphabet_0, character_0), (alphabet_1, character_1))
                          for (alphabet_0, character_0), (alphabet_1, character_1) in old_pairs_0
                          if alphabet_0 == alphabet_1)
            pairs = itertools.chain(itertools.islice(pairs_diff, int(different_alphabet_fraction * task_count)),
                                    pairs_same)
    
    tasks.extend(((alphabet_0, character_0, random.choice(alphabets_dict[alphabet_0].keys())),
                  (alphabet_1, character_1, random.choice(alphabets_dict[alphabet_1].keys())))
                 for (alphabet_0, character_0), (alphabet_1, character_1) in itertools.islice(pairs, tasks_left))

    if len(tasks) < task_count: raise Exception("Not enough characters")

    random.shuffle(tasks)

    return tasks_to_task_images(tasks, verbose=verbose, random=random, alphabets_dict=alphabets_dict)

def make_task_from_alphabet_set(alias, alphabets_dict=None, **kwargs):
    if alphabets_dict is None: alphabets_dict = get_accepted_image_list()
    def bad_alias():
        raise Exception("Character set with the given name does not exist.  Run construct-character-set.py to create it.")
    
    list_of_stuff = get_object('recognition-tasks_character-set_%s' % alias, bad_alias)
    if not isinstance(list_of_stuff[0], (list, tuple)):
        return make_task_from_alphabets_list(list_of_stuff, alphabets_dict=alphabets_dict, **kwargs)
    else: # is string
        return make_task_from_characters_list(list_of_stuff, alphabets_dict=alphabets_dict, **kwargs)
#    else:
#        print(list_of_stuff)
#        raw_input(list_of_stuff[0])
#        raise Exception("Character set with the given name is malformed.")


def create_first_task(form, args, verbose=False):
    passOnValues = {
                    'tasksPerFeedbackGroup':[10],
                    'pauseToNextGroup':[-1],
                    'displayProgressBarDuringTask':False,
                    'allowDidNotSeeCount':[1],
                    'taskCount':210,
                    'differentAlphabetFraction':-1,
                    'sameFraction':0.5,
                    'unique':True,
                    'confirmToContinue':True,
                    'characterSize':'100px',
                    'characterSet':''
                    }

    rtn = aggregate_values(passOnValues, args, form);

    rtn['imagesPerTask'] = 2

    if rtn['characterSet']:
        rtn['tasks'] = make_task_from_alphabet_set(rtn['characterSet'], verbose=verbose, same_character_fraction=rtn['sameFraction'],
                                                   different_alphabet_fraction=rtn['differentAlphabetFraction'], task_count=rtn['taskCount'],
                                                   unique=rtn['unique'])
    else:
        rtn['tasks'] = make_task(verbose=verbose, same_character_fraction=rtn['sameFraction'], different_alphabet_fraction=rtn['differentAlphabetFraction'],
                                 task_count=rtn['taskCount'], unique=rtn['unique'])
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
