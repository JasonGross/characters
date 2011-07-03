#!/usr/bin/python
# Filename: cgiutil.py
import json

def get_boolean_value(form, true_keys, false_keys=None, default=None, true_options=(True,'true','1',1,'','yes','on','y','t'),
                      false_options=(False,'false','0',0,'','no','off','n','f'),
                      if_both=None, if_neither=None, aggregate_true_keys=any, aggregate_false_keys=any):
    if isinstance(true_keys, str): true_keys = [true_keys]
    if isinstance(false_keys, str): false_keys = [true_keys]
    if true_keys is None: true_keys = []
    if false_keys is None: false_keys = []
    if if_both is None: if_both = (lambda:default)
    if if_neither is None: if_neither = (lambda:default)
    true_value = (aggregate_true_keys(true_key in form and 
                                      aggregate_true_keys(value in true_options 
                                                          for value in form.getlist(true_key))
                                      for true_key in true_keys) or
                  aggregate_true_keys(false_key in form and
                                      aggregate_true_keys(value in false_options
                                                          for value in form.getlist(false_key))
                                      for false_key in false_keys))
    false_value = (aggregate_false_keys(false_key in form and
                                        aggregate_false_keys(value in true_options
                                                             for value in form.getlist(false_key))
                                        for false_key in false_keys) or
                   aggregate_false_keys(true_key in form and
                                        aggregate_false_keys(value in false_options
                                                             for value in form.getlist(true_key))
                                        for true_key in true_keys))
    if true_value and false_value: return if_both()
    elif not true_value and not false_value: return if_neither()
    else: return true_value and not false_value

def get_list_of_values(form, keys, default=None):
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
    if default and not rtn: return default
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


