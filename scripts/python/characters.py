#!/usr/bin/python
# Filename: characters.py
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
from objectstorage import get_object, save_object

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
    _random = get_object('characters_random', (lambda: random.Random()))
    NUMBER_OF_ALPHAHBETS = int(form.getfirst('numberOfAlphabets', 40))
    EXAMPLE_CHARACTERS_PER_ALPHABET = int(form.getfirst('exampleCharactersPerAlphabet', 10))
    SAME_TEST_CHARACTERS_PER_ALPHABET = int(form.getfirst('sameTestCharactersPerAlphabet', 10))
    DIFFERENT_TEST_CHARACTERS_PER_ALPHABET = int(form.getfirst('differentTestCharactersPerAlphabet', 10))
    DIFFERENT_ALPHABET_CHARACTERS_PER_ALPHABET = int(form.getfirst('differentAlphabetTestCharactersPerAlphabet', 20))
    DISTRACT_WITH_ALL = get_boolean_value(form, 'distractWithAll')
    
    alphabets = get_accepted_image_list(from_path=FROM_PATH)
    alphabets = dict((alphabet, alphabets[alphabet]) for alphabet in alphabets
                     if len(alphabets[alphabet].values()[0]) > max((EXAMPLE_CHARACTERS_PER_ALPHABET,
                                                                    DIFFERENT_TEST_CHARACTERS_PER_ALPHABET,
                                                                    DIFFERENT_ALPHABET_CHARACTERS_PER_ALPHABET)))
    
    if DISTRACT_WITH_ALL:
        use_alphabets = _random.sample(alphabets.keys(), NUMBER_OF_ALPHAHBETS)

    if not DISTRACT_WITH_ALL:
        use_alphabets = _random.sample(alphabets.keys(), NUMBER_OF_ALPHAHBETS)

    tasks = []

    for alphabet in use_alphabets:
        this_characters = zip(_random.sample(alphabets[alphabet].keys(), EXAMPLE_CHARACTERS_PER_ALPHABET),
                              _random.sample(range(len(alphabets[alphabet].values()[0])), EXAMPLE_CHARACTERS_PER_ALPHABET))
        for uid, character_num in this_characters:
            all_other_uids = [d_uid for d_uid in alphabets[alphabet].keys() if d_uid != uid]
            all_other_uids = _random.sample(all_other_uids, len(all_other_uids))
            
            other_uid_same_character = all_other_uids[:SAME_TEST_CHARACTERS_PER_ALPHABET]
            other_characters_same_alphabet = [alphabets[alphabet]]
            other_characters_same_alphabet = [i[u]
                                              for u in all_other_uids[SAME_TEST_CHARACTERS_PER_ALPHABET:SAME_TEST_CHARACTERS_PER_ALPHABET+DIFFERENT_TEST_CHARACTERS_PER_ALPHABET]
                                              for i in other_characters_same_alphabet]
            other_characters_same_alphabet = [i[n]
                                              for n in _random.sample([i for i in range(len(alphabets[alphabet][uid])) if i != character_num],
                                                                      DIFFERENT_TEST_CHARACTERS_PER_ALPHABET)
                                              for i in other_characters_same_alphabet]
            other_alphabets = _random.sample([a for a in use_alphabets if a != alphabet], DIFFERENT_ALPHABET_CHARACTERS_PER_ALPHABET)

            other_characters_other_alphabet = [alphabets[a]
                                               [_random.choice(alphabets[a].keys())]
                                               [_random.randrange(len(alphabets[a].values()[0]))] for a in other_alphabets]


            this_character_url = anonymize_image(alphabets[alphabet][uid][character_num])
            tasks.extend([(this_character_url,
                           anonymize_image(alphabets[alphabet][u][character_num])) for u in other_uid_same_character])
            tasks.extend([(this_character_url,
                           anonymize_image(image)) for image in other_characters_same_alphabet])
            tasks.extend([(this_character_url,
                           anonymize_image(image)) for image in other_characters_other_alphabet])
    random.shuffle(tasks)
    tasks = [(example, test, 'http://www.quasimondo.com/hydra/sineNoise1.jpg')
             for example, test in tasks]
    return tasks


def main():
    form = cgi.FieldStorage()
    non_existant_variable = form.getvalue('&=variableDoesNotExistString=&')
    rtn = create_first_task(form)
    print('Content-type: text/json\n')
    print(json.dumps(rtn))

if __name__ == '__main__':
    main()
        
