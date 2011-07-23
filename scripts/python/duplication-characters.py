#!/usr/bin/python
# Filename: duplication-characters.py
from __future__ import with_statement
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
                        for alphabet, character_i, uid in task]
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

def make_task_from_characters_list(characters_list, unique=True, example_count=1, task_count=200,
                                   alphabets_dict=None, verbose=True, random=random, **kwargs):
    if same_character_fraction < 0: same_character_fraction = None
    if different_alphabet_fraction < 0: different_alphabet_fraction = None
    if alphabets_dict is None: alphabets_dict = get_accepted_image_list()

    if example_count != 1: raise Exception("We don't handle large example counts yet.")

    random.shuffle(characters_list)

    if len(characters_list) < task_count * example_count: raise Exception("Not enough characters")

    tasks = [[(alphabet, character, random.choice(alphabets_dict[alphabet].keys()))
              for alphabet, character in characters_list[i*example_count:(i+1)*example_count]]
             for i in range(task_count)]

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
                    'pauseToFirstHint':[500],
                    'pauseToSecondHint':[500],
                    'pauseToExample':[1000],
                    'pauseToNoise':[50],
                    'pauseToTest':[1000],
                    'tasksPerFeedbackGroup':[10],
                    'pauseToNextGroup':[-1],
                    'displayProgressBarDuringTask':False,
                    'allowDidNotSeeCount':[1],
                    'taskCount':20,
                    'exampleClassCount':1,
                    'examplePerClassCount':1,
                    'uniqueClasses':False,
                    'characterSize':'100px',
                    'characterSet':''
                    }

    rtn = aggregate_values(passOnValues, args, form);

    rtn['imagesPerTask'] = rtn['exampleClassCount'] * rtn['examplePerClassCount'] * 2;

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

parser = argparse.ArgumentParser(description='Get the characters duplication task')
parser.add_argument('--verbose', '-v', action='store_true',
                    help='print status on recreating tasks')
parser.add_argument('--character-set', '-s', dest='characterSet', type=str,
                    help='name of character set to use')
parser.add_argument('--no-unique', dest='unique', action='store_false',
                    help='unique characters?')
if __name__ == '__main__':
    main()
