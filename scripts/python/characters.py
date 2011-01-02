#!/usr/bin/python
# Filename: characters.py
from __future__ import with_statement
import cgi#, cgitb
#cgitb.enable(format='nohtml')
import os, sys, json, subprocess, tempfile, shutil, random, urllib, random
import argparse
try:
  import urllib.parse
except ImportError:
  pass
from alphabetspaths import *
import alphabetspopularity
from alphabetsutil import png_to_uri
from image_anonymizer import anonymize_image 
from objectstorage import get_object, save_object
import sequencer

FROM_PATH = ACCEPTED_IMAGES_PATH

PLUS_MINUS_CHAR = '\u00B1'
PLUS_MINUS_STRINGS = ('+-', '-+', '+', '-', PLUS_MINUS_CHAR)

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


def make_task(most_popular_number=6, min_characters=20, same_character_distractors_count=5, same_alphabet_distractors_count=5,
              other_alphabet_distractors_count=10, num_experiments=50, foreground_fraction=0.6, verbose=True, random=random.Random):
    originals_count = 1

    if verbose: print('Getting list of alphabets...')
    alphabets_dict = get_accepted_image_list()
    alphabets_list = alphabets_dict.keys()
    if verbose: print('Getting alphabet popularities...')
    popularities = [(alphabetspopularity.get_popularity(alphabet), alphabet) for alphabet in alphabets_list]
    popularities.sort(reverse=True)
    if verbose: print('Separating alphabet list into background and foreground sets...')
    alphabets_background = [alphabet for popularity, alphabet in popularities[:most_popular_number]]
    popularities = popularities[most_popular_number:]
    too_small = [alphabet for popularity, alphabet in popularities if len(alphabets_dict[alphabet].values()[0]) < min_characters]
    alphabets_background += too_small
    alphabets_left = [alphabet for popularity, alphabet in popularities if alphabet not in too_small]
    random.shuffle(alphabets_left)

    alphabets_use = alphabets_left[:int(0.5 + len(alphabets_list) * foreground_fraction)]
    alphabets_background += alphabets_left[int(0.5 + len(alphabets_list) * foreground_fraction):]
    alphabets_use.sort()
    #random.shuffle(alphabets_background)


    if verbose: print('Separating characters into two sets...')
    character_sets = [[], []]
    remaining_characters_use = []
    for alphabet in alphabets_use:
        if verbose: print('Separating characters from %s into sets...' % alphabet)
        characters = list(range(len(alphabets_dict[alphabet].values()[0])))
        random.shuffle(characters)
        character_sets[0].extend((alphabet, character_i) for character_i in characters[:1+same_alphabet_distractors_count])
        character_sets[1].extend((alphabet, character_i) for character_i in characters[1+same_alphabet_distractors_count:2*(1+same_alphabet_distractors_count)])
        remaining_characters_use.extend((alphabet, character_i) for character_i in characters[2*(1+same_alphabet_distractors_count):])
    random.shuffle(remaining_characters_use)
    character_sets[0] += remaining_characters_use[:int(len(remaining_characters_use)/2)]
    character_sets[1] += remaining_characters_use[int(len(remaining_characters_use)/2):]
    for set_i, cur_set in enumerate(character_sets):
        cur_dict = {}
        for alphabet, character_i in cur_set:
            if character_i >= len(alphabets_dict[alphabet].values()[0]):
                print(cur_set)
                raw_input((alphabet, character_i, len(alphabets_dict[alphabet].values()[0])))
            if alphabet not in cur_dict: cur_dict[alphabet] = []
            cur_dict[alphabet].append(character_i)
            for alphabet in cur_dict:
                for character_j in cur_dict[alphabet]:
                    if character_j >= len(alphabets_dict[alphabet].values()[0]):
                        print(cur_dict[alphabet])
                        raw_input((alphabet, character_j, character_i, len(alphabets_dict[alphabet].values()[0])))
        character_sets[set_i] = cur_dict

                
    if verbose: print('Done separating characters into sets.')
            
    trials_sets = [[], []]
    experiments_sets = [[], []]
    for set_i, character_set in enumerate(character_sets):
        if verbose: print('Constructing trials for set %d...' % set_i)
        for alphabet in sorted(character_set.keys()):
            if verbose: print('Making dict of characters not in alphabet %s...' % alphabet)
            other_alphabet_characters = [(other_alphabet, character_i)
                                         for other_alphabet in character_set
                                         if other_alphabet != alphabet
                                         for character_i in character_set[other_alphabet]]
            for character_i in character_set[alphabet]:
##                if verbose: print('Making trials for character %d of alphabet %s...' % (character_i, alphabet))
                this_ids = random.sample(alphabets_dict[alphabet].keys(), originals_count + same_character_distractors_count)

                original = [(alphabet, character_i, this_id) for this_id in this_ids[:originals_count]][0] # I force originals to be 1
                same_character_distractors = [(alphabet, character_i, this_id) for this_id in this_ids[originals_count:]]
                
                same_alphabet_distractors = random.sample(character_set[alphabet], same_alphabet_distractors_count + 1)
                if character_i in same_alphabet_distractors:
                    same_alphabet_distractors = [i for i in same_alphabet_distractors if i != character_i]
                else:
                    same_alphabet_distractors = same_alphabet_distractors[:-1]
                same_alphabet_distractors = [(alphabet, i, random.choice(alphabets_dict[alphabet].keys()))
                                             for i in same_alphabet_distractors]
                
                other_alphabet_distractors = [(other_alphabet, i, random.choice(alphabets_dict[other_alphabet].keys()))
                                              for other_alphabet, i in random.sample(other_alphabet_characters, other_alphabet_distractors_count)]
                trials_sets[set_i] += [(original, test)
                                       for tests in (same_character_distractors, same_alphabet_distractors, other_alphabet_distractors)
                                       for test in tests]

        if verbose: print('Done making trials for set %d.' % set_i)
        random.shuffle(trials_sets[set_i])
        trials_per_experiment = int(len(trials_sets[set_i])) / num_experiments
        while len(experiments_sets[set_i]) < num_experiments:
##            if verbose: print('Selecting trials for experiment %d / %d...' % (len(experiments_sets[set_i]) + 1, num_experiments))
            cur_experiment = []
            used = set()
            left = []
            while len(cur_experiment) < trials_per_experiment:
                cur_trial = trials_sets[set_i][0]
                if tuple(cur_trial[0][:2]) not in used and tuple(cur_trial[1][:2]) not in used:
                    cur_experiment.append(cur_trial)
                else:
                    left.append(cur_trial)
                del trials_sets[set_i][0]
                if verbose: print ('\rSelected %03d / %03d of the trials, %04d left to choose from, for experiment %d / %d.' % (len(cur_experiment), trials_per_experiment, len(trials_sets[set_i]), len(experiments_sets[set_i]) + 1, num_experiments)),
            trials_sets[set_i] += left
            experiments_sets[set_i].append(cur_experiment)
##            if verbose: print('\nDone selecting trials for experiment %d.' % len(experiments_sets[set_i]))
        if verbose: print('\nDone making experiments for set %d.' % set_i)
    return experiments_sets


def get_a_task(task_group_index, reset=False, verbose=False, reset_database=False, reset_on_run_out=True):
    _random = get_object('characters_random', (lambda: random.Random()))
    is_old = ((lambda x:reset) if reset else None)
    tasks = get_object('recognition-tasks', (lambda *args, **kargs: make_task(*args, random=_random, verbose=verbose, **kargs)), is_old=is_old)[task_group_index]
    return tasks[sequencer.pop('recognition_characters_%d' % task_group_index, reset_sequence=reset,
                               reset_database=reset_database, reset_on_run_out=reset_on_run_out, length=len(tasks))]
    

_STROKE_NOISES = get_stroke_noises(from_path=BASE_PATH)

def create_first_task(form, reset=False, verbose=False):
    if 'taskGroupIndex' in form.keys(): task_group_index = int(form.getfirst('taskGroupIndex'))
    else: task_group_index = 0
    tasks = get_a_task(task_group_index, reset=reset, verbose=verbose)
    passOnValues = {'pauseToFirstHint':500,
                    'pauseToSecondHint':500,
                    'pauseToExample':1000,
                    'pauseToNoise':100,
                    'pauseToTest':1000,
                    'tasksPerFeedbackGroup':10,
                    'tasksPerWaitGroup':1000,
                    'pauseToGroup':1000
                    }
    alphabets = get_accepted_image_list(from_path=FROM_PATH)
    tasks = [(anonymize_image(alphabets[task[0][0]][task[0][2]][task[0][1]], from_path=FROM_PATH),
              anonymize_image(alphabets[task[1][0]][task[1][2]][task[1][1]], from_path=FROM_PATH),
              task[0][0] == task[1][0] and task[0][1] == task[1][1])
             for task in tasks]
            
    rtn = {}

    for key in passOnValues:
      rtn[key] = form.getfirst(key, passOnValues[key])
      if isinstance(rtn[key], str) and any(sign_char in rtn[key] for sign_char in PLUS_MINUS_STRINGS):
        for sign_char in PLUS_MINUS_STRINGS:
            rtn[key] = rtn[key].replace(sign_char, PLUS_MINUS_CHAR)
        rtn[key] = rtn[key].split(PLUS_MINUS_CHAR)
        rtn[key] = list(map(int, rtn[key]))
      elif isinstance(rtn[key], (tuple, list)):
        rtn[key] = list(map(int, rtn[key]))
      else:
        rtn[key] = [int(rtn[key])]
      if len(rtn[key]) < 2:
        rtn[key].append(0)

    tasks = [(example, test, urllib.parse.urljoin(BASE_URL, random.choice(_STROKE_NOISES)), correct_answer) #http://www.quasimondo.com/hydra/sineNoise1.jpg')
             for example, test, correct_answer in tasks]
    rtn['tasks'] = tasks
    return rtn
    
##    
##    
##    tasks = 
##
##    for alphabet in use_alphabets:
##        this_characters = zip(_random.sample(alphabets[alphabet].keys(), EXAMPLE_CHARACTERS_PER_ALPHABET),
##                              _random.sample(range(len(alphabets[alphabet].values()[0])), EXAMPLE_CHARACTERS_PER_ALPHABET))
##        for uid, character_num in this_characters:
##            all_other_uids = [d_uid for d_uid in alphabets[alphabet].keys() if d_uid != uid]
##            all_other_uids = _random.sample(all_other_uids, len(all_other_uids))
##            
##            other_uid_same_character = all_other_uids[:SAME_TEST_CHARACTERS_PER_ALPHABET]
##            other_characters_same_alphabet = [alphabets[alphabet][u][n]
##                                              for u in all_other_uids[SAME_TEST_CHARACTERS_PER_ALPHABET:SAME_TEST_CHARACTERS_PER_ALPHABET+DIFFERENT_TEST_CHARACTERS_PER_ALPHABET]
##                                              for n in _random.sample([i for i in range(len(alphabets[alphabet][uid])) if i != character_num],
##                                                                      DIFFERENT_TEST_CHARACTERS_PER_ALPHABET)]
##            other_alphabets = _random.sample([a for a in use_alphabets if a != alphabet], DIFFERENT_ALPHABET_CHARACTERS_PER_ALPHABET)
##
##            other_characters_other_alphabet = [alphabets[a]
##                                               [_random.choice(alphabets[a].keys())]
##                                               [_random.randrange(len(alphabets[a].values()[0]))] for a in other_alphabets]
##
##
##            this_character_url = anonymize_image(alphabets[alphabet][uid][character_num])
##            tasks.extend([(this_character_url,
##                           anonymize_image(alphabets[alphabet][u][character_num], from_path=FROM_PATH)) for u in other_uid_same_character])
##            tasks.extend([(this_character_url,
##                           anonymize_image(image, from_path=FROM_PATH)) for image in other_characters_same_alphabet])
##            tasks.extend([(this_character_url,
##                           anonymize_image(image, from_path=FROM_PATH)) for image in other_characters_other_alphabet])
##    random.shuffle(tasks)
##    tasks = [(example, test, urllib.parse.urljoin(BASE_URL, 'images/sineNoise1.jpg')) #http://www.quasimondo.com/hydra/sineNoise1.jpg')
##             for example, test in tasks]
##    rtn['tasks'] = tasks
##    return rtn

def main():
    form = cgi.FieldStorage()
    non_existant_variable = form.getvalue('&=variableDoesNotExistString=&')
    args = parser.parse_args()
    rtn = create_first_task(form, reset=args.reset, verbose=args.verbose)
#    rtn = create_first_task(form)
    print('Content-type: text/json\n')
    print(json.dumps(rtn))

parser = argparse.ArgumentParser(description='Get the characters recognition task')
parser.add_argument('--reset', '-r', action='store_true',
                    help='recreate the tasks from scratch and reset the database')
parser.add_argument('--verbose', '-v', action='store_true',
                    help='print status on recreating tasks')

if __name__ == '__main__':
    main()
        
