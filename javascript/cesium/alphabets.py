#!/usr/bin/python
# Filename: alphabets.py
from __future__ import with_statement
import os, sys, json, cgi, cgitb, subprocess, tempfile, shutil, random
cgitb.enable()
try:
    import cPickle as pickle
except ImportError:
    import pickle
from alphabetspaths import *


FROM_PATH = BASE_PATH

_random = random.Random()

def get_boolean_value(form, true_keys, false_keys=None, default=None, true_options=(True,'true','1',1,'','yes','on','y','t'),
                      false_options=(False,'false','0',0,'','no','off','n','f'),
                      if_both=(lambda:default), if_neither=(lambda:default), aggregate_true_keys=any, aggregate_false_keys=any):
    if isinstance(true_keys, str): true_keys = [true_keys]
    if isinstance(false_keys, str): false_keys = [true_keys]
    if true_keys is None: true_keys = []
    if false_keys is None: false_keys = []
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
                

def update_alphabets_file(now=False): # because I need a way for this to not take any time
    if now or '--update-alphabets-file' in sys.argv:
        images = get_accepted_image_list(from_path=FROM_PATH)
        f = tempfile.NamedTemporaryFile(delete=False)
        pickle.dump(images, f, protocol=2)
        f.close()
        shutil.move(f.name, STORED_ALPHABET_IMAGES_LIST_PATH)
        return images
    else:
        p = subprocess.Popen(args=[__file__, '--update-alphabets-file'], shell=True)

def get_alphabets():
    if os.path.exists(STORED_ALPHABET_IMAGES_LIST_PATH):
        try:
            with open(STORED_ALPHABET_IMAGES_LIST_PATH, 'rb') as f:
                images = pickle.load(f)
                #update_alphabets_file()
        except ValueError:
            images = update_alphabets_file(now=True)
    else:
        images = update_alphabets_file(now=True)
    return images

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

def create_first_task(form, images):
    GROUP_COUNT = 5
    ALPHABETS_PER_GROUP = 10
    alphabet_ids = tuple(_random.sample(images.keys(), GROUP_COUNT * ALPHABETS_PER_GROUP))
    TRAINING_CHARACTERS_PER_ALPHABET = 2 #int(form.getvalue('trainingCharactersPerAlphabet', 2))
    groups = [{'alphabets':dict((alphabet_id, []) for alphabet_id in alphabet_ids[ALPHABETS_PER_GROUP*i:ALPHABETS_PER_GROUP*(i+1)])} for i in range(GROUP_COUNT)]
    for group in groups:
        asking_alphabet_id = _random.choice(list(group['alphabets'].keys()))
        for alphabet_id in group['alphabets']:
            uids = list(images[alphabet_id].keys())
            image_numbers = list(range(len(images[alphabet_id][uids[0]])))
            use_uids = _random.sample(uids, TRAINING_CHARACTERS_PER_ALPHABET)
            use_image_numbers = _random.sample(image_numbers, TRAINING_CHARACTERS_PER_ALPHABET)
            group['alphabets'][alphabet_id] = [images[alphabet_id][uid][image_num] for uid, image_num in zip(use_uids, use_image_numbers)]
            if alphabet_id == asking_alphabet_id:
                uid, image_num = None, None
                while uid is None or uid in use_uids:
                    uid = _random.choice(uids)
                while image_num is None or image_num in use_image_numbers:
                    image_num = _random.choice(image_numbers)
                group['ask_for'] = [images[alphabet_id][uid][image_num]]
    return groups
    
    

##def parse_options(form, images):
##    MAX_ALPHABET_COUNT = int(form.getfirst('maximumAlphabetCount', len(images)))
##    DEFAULT_IS_UNIQUE = get_boolean_value(form, 'generallyUnique', 'generallyNotUnique',
##    True) ALPHABETS_ARE_UNIQUE = get_boolean_value(form,
##    'uniqueAlphabets', 'notUniqueAlphabets', DEFAULT_IS_UNIQUE)
##    potential_alphabet_ids = set(images.keys()) for _id in
##    get_list_of_values(form, ['excludeAlphabet', 'excludeAlphabets']):
##    if _id in potential_alphabet_ids:
##    potential_alphabet_ids.remove(_id) elif _id.lower() in
##    potential_alphabet_ids: potential_alphabet_ids.remove(_id.lower())
##    require_alphabet_ids = [] for _id in get_list_of_values(form,
##    ['requireAlphabet', 'requireAlphabets']): if _id in
##    potential_alphabet_ids: require_alphabet_ids.append(_id) elif
##    _id.lower() in potential_alphabet_ids:
##    require_alphabet_ids.append(_id.lower()) alphabet_ids =
##    require_alphabet_ids[:] # I want a copy potential_alphabet_ids =
##    tuple(sorted(_id for _id in alphabet_ids if not
##    ALPHABETS_ARE_UNIQUE or _id not in alphabet_ids))
##    MAX_ALPHABET_COUNT -= len(alphabet_ids) MAX_ALPHABET_COUNT =
##    max((0, MAX_ALPHABET_COUNT)) if ALPHABETS_ARE_UNIQUE:
##    MAX_ALPHABET_COUNT = min((MAX_ALPHABET_COUNT,
##    len(potential_alphabet_ids))) alphabet_ids +=
##    list(_random.sample(potential_alphabet_ids, MAX_ALPHABET_COUNT))
##    else: alphabet_ids += list(_random.choice(alphabet_ids) for i in
##    range(MAX_ALPHABET_COUNT)) alphabet_ids = tuple(alphabet_ids)
##    MAX_ALPHABET_COUNT = len(alphabet_ids)
##    
##    DEFAULT_NUMBER_OF_ALPHABETS_PER_GROUP = int(form.getfirst('alphabetsPerGroup', -1))
##    DEFAULT_NUMBER_OF_GROUPS = int(form.getfirst('groupCount', -1))
##    if DEFAULT_NUMBER_OF_ALPHABETS_PER_GROUP <= 0 and DEFAULT_NUMBER_OF_GROUPS <= 0:
##       DEFAULT_NUMBER_OF_ALPHABETS_PER_GROUP = 10
##       DEFAULT_NUMBER_OF_GROUPS = MAX_ALPHABET_COUNT / DEFAULT_NUMBER_OF_ALPHABETS_PER_GROUP
##    elif DEFAULT_NUMBER_OF_ALPHABETS_PER_GROUP <= 0:
##        DEFAULT_NUMBER_OF_ALPHABETS_PER_GROUP = MAX_ALPHABET_COUNT / DEFAULT_NUMBER_OF_GROUPS
##    elif DEFAULT_NUMBER_OF_GROUPS <= 0:
##        DEFAULT_NUMBER_OF_GROUPS = MAX_ALPHABET_COUNT / DEFAULT_NUMBER_OF_ALPHABETS_PER_GROUP
##
##    alphabet_id_groups = []
##    if any(key in form for key in ('group', 'groups', 'alphabetGroup', 'alphabetGroups')):
##        initial_groups = get_list_of_values(form, ('group', 'groups', 'alphabetGroup', 'alphabetGroups'))
##        if all(isinstance(group, str) for group in initial_groups):
##            alphabet_id_groups = initial_groups
##        elif is_nested_type(initial_groups, list, str): # it's a single group of alphabet ids
##            alphabet_id_groups.append(initial_groups)
##        elif is_nested_type(initial_groups, list, list, str): # it's a list of groups of alphabet ids
##            alphabet_id_groups += initial_groups
##        elif is_nested_type(initial_groups, list, dict, (str, int, [list, (str, int)], [dict, (str, int)])): # it's a list of groups of alphabet ids, which are dicts to ids
##            alphabet_id_groups += [group.keys() for group in initial_groups]
##        elif is_nested_type(initial_groups, dict, (str, [list, (str, int)])): # it's a group of alphabet ids, which are dicts to ids or character numbers
##            alphabet_id_groups.append(initial_groups.keys())
##        else:
##            raise ValueError('Invalid parameter passed for the structure of the groups: %s' % initial_groups)
##    APPEND_TO_GROUPS_TO_GET_UP_TO_LENGTH = get_boolean_value(form, 'increaseSpecifiedGroups', 'doNotIncreaseSpecifiedGroups', False)
##    if ALPHABETS_ARE_UNIQUE:
##        for group in alphabet_id_groups:
##            for alphabet_id in group:
##                if alphabet_id in alphabet_ids:
##                    alphabet_ids.remove(alphabet_id)
##                elif alphabet_id.lower() in alphabet_ids:
##                    alphabet_ids.remove(alphabet_id.lower())
##                if alphabet_id in require_alphabet_ids:
##                    require_alphabet_ids.remove(alphabet_id)
##                elif alphabet_id.lower() in require_alphabet_ids:
##                    require_alphabet_ids.remove(alphabet_id.lower())
##    if APPEND_TO_GROUPS_TO_GET_UP_TO_LENGTH:
##        for group_i, group in enumerate(alphabet_id_groups):
##            if len(group) < DEFAULT_NUMBER_OF_ALPHABETS_PER_GROUP:
##                alphabet_id_groups[group_i] += alphabet_ids[:DEFAULT_NUMBER_OF_ALPHABETS_PER_GROUP - len(group)]
##                alphabet_ids = alphabet_ids[DEFAULT_NUMBER_OF_ALPHABETS_PER_GROUP - len(group):]
##                require_alphabet_ids = alphabet_ids[DEFAULT_NUMBER_OF_ALPHABETS_PER_GROUP - len(group):]
##    while require_alphabet_ids or (len(groups) < DEFAULT_NUMBER_OF_GROUPS and alphabet_ids):
##        alphabet_id_groups.append(alphabet_ids[:DEFAULT_NUMBER_OF_ALPHABETS_PER_GROUP])
##        alphabet_ids = alphabet_ids[DEFAULT_NUMBER_OF_ALPHABETS_PER_GROUP:]
##        require_alphabet_ids = alphabet_ids[DEFAULT_NUMBER_OF_ALPHABETS_PER_GROUP:]
##    alphabet_id_groups = tuple(list(map(tuple, alphabet_id_groups)))
##
##
##
##    DEFAULT_NUMBER_OF_CHARACTERS_PER_ALPHABET = int(form.getfirst('charactersPerAlphabet', 3))
##
##    character_number_groups = [dict((alphabet, []) for alphabet in group) for group in alphabet_id_groups]
##    for group in alphabet_id_groups:
##        for alphabet in group:
##            if DEFAULT_NUMBER_OF_CHARACTERS_PER_ALPHABET < 0:
##                group[alphabet] = _random.sample(range(len(images[alphabet].values()[0])), len(images[alphabet].values()[0]))
##            else:
##                group[alphabet] = _random.sample(range(len(images[alphabet].values()[0])), DEFAULT_NUMBER_OF_CHARACTERS_PER_ALPHABET)

    




    


    
        
       
    
    
    

def main():
    form = cgi.FieldStorage()
    non_existant_variable = form.getvalue('variableDoesNotExistString')
    print('Content-type: text/json\n')
    if 'getObject' in form:
        objects = dict((name,
                        (globals()[name] if name in globals() else non_existant_variable)) \
                       for name in form.getlist('getObject'))
        print(json.dumps(objects))
    else:
        images = get_alphabets()
        print(json.dumps(create_first_task(form, images)))
        #print(json.dumps(images))

if __name__ == '__main__':
    if '--update-alphabets-file' in sys.argv:
        update_alphabets_file()
    else:
        main()
        
