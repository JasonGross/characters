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
             'images': [[anonymize_image(alphabets_dict[alphabet][uid][character_i], from_path=FROM_PATH, include_hash=False, include_original=False)
                         for alphabet, character_i, uid in group]
                        for group in task]
            }
            for task in tasks]

def make_task(foreground_fraction=0.75, verbose=True, random=random, **kwargs):
    if verbose: print('Getting list of alphabets...')
    alphabets_dict = get_accepted_image_list()

    alphabets_list = make_foreground_alphabets(random=random, verbose=verbose, alphabets_dict=alphabets_dict, foreground_fraction=foreground_fraction, **kwargs)

    return make_task_from_alphabets_list(alphabets_list, random=random, verbose=verbose, alphabets_dict=alphabets_dict, **kwargs)

def make_task_from_alphabets_list(alphabets_list, alphabets_dict=None, verbose=True, random=random, **kwargs):
    if alphabets_dict is None: alphabets_dict = get_accepted_image_list()

    groups_list = []
    for alphabet in alphabets_list:
        if verbose: print('Collecting characters from %s...' % alphabet)
        groups_list.append([(alphabet, character_i) for character_i in range(len(alphabets_dict[alphabet].values()[0]))])

    return make_task_from_groups_list(groups_list, alphabets_dict=alphabets_dict, verbose=verbose, random=random, **kwargs)

def make_task_from_groups_list(groups_list, example_class_count=1, example_per_class_count=1, task_count=200, unique_classes=True,
                               alphabets_dict=None, verbose=True, random=random, **kwargs):
    if alphabets_dict is None: alphabets_dict = get_accepted_image_list()

    if unique_classes:
        pre_classes = random.sample(groups_list, task_count)
    else:
        pre_classes = (random.choice(groups_list) for i in range(task_count))

    classes = (random.sample(group, example_class_count) for group in pre_classes)

    tasks = [[[(alphabet, character, uid) for uid in random.sample(alphabets_dict[alphabet].keys(), example_per_class_count)]
              for alphabet, character in group]
             for group in classes]

    return tasks_to_task_images(tasks, verbose=verbose, random=random, alphabets_dict=alphabets_dict)

def make_task_from_alphabet_set(alias, alphabets_dict=None, **kwargs):
    if alphabets_dict is None: alphabets_dict = get_accepted_image_list()
    def bad_alias():
        raise Exception("Character set with the given name does not exist.  Run construct-character-set.py to create it.")
    
    list_of_stuff = get_object('recognition-tasks_character-set_%s' % alias, bad_alias)
    if not isinstance(list_of_stuff[0], (list, tuple)):
        return make_task_from_alphabets_list(list_of_stuff, alphabets_dict=alphabets_dict, **kwargs)
    else: # is string
        return make_task_from_groups_list(list_of_stuff, alphabets_dict=alphabets_dict, **kwargs)
#    else:
#        print(list_of_stuff)
#        raw_input(list_of_stuff[0])
#        raise Exception("Character set with the given name is malformed.")


def create_first_task(form, args, verbose=False):
    passOnValues = {
                    'pauseToFirstHint':[500],
                    'pauseToSecondHint':[500],
                    'pauseToExample':[1000],
                    'pauseToNoise':[500],
                    'taskCount':-1,
                    'exampleClassCount':1,
                    'examplePerClassCount':1,
                    'uniqueClasses':True,
                    'characterSize':'100px',
                    'canvasSize':'100px',
                    'characterSet':''
                    }

    rtn = aggregate_values(passOnValues, args, form);

    rtn['imagesPerTask'] = rtn['exampleClassCount'] * rtn['examplePerClassCount'] * 2;

    if rtn['exampleClassCount'] > 1 or rtn['examplePerClassCount'] > 1: # untimed
        if rtn['taskCount'] == -1: # no value given
            rtn['taskCount'] = 15
        rtn['uniqueClasses'] = True # we should check to see if something is given...
    else:
        if rtn['taskCount'] == -1: # no value given
            rtn['taskCount'] = 15
        rtn['uniqueClasses'] = False # we should check to see if something is given...



    if rtn['characterSet']:
        rtn['tasks'] = make_task_from_alphabet_set(rtn['characterSet'], verbose=verbose,
                                                   example_class_count=rtn['exampleClassCount'], example_per_class_count=rtn['examplePerClassCount'],
                                                   task_count=rtn['taskCount'],
                                                   unique_classes=rtn['uniqueClasses'])
    else:
        rtn['tasks'] = make_task(verbose=verbose,
                                 example_class_count=rtn['exampleClassCount'], example_per_class_count=rtn['examplePerClassCount'],
                                 task_count=rtn['taskCount'],
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

parser = argparse.ArgumentParser(description='Get the characters duplication task')
parser.add_argument('--verbose', '-v', action='store_true',
                    help='print status on recreating tasks')
parser.add_argument('--character-set', '-s', dest='characterSet', type=str,
                    help='name of character set to use')
parser.add_argument('--no-unique', dest='unique', action='store_false',
                    help='unique characters?')
if __name__ == '__main__':
    main()
