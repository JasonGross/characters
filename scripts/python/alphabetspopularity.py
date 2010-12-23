#!/usr/bin/python
from alphabetspaths import *
import objectstorage
from google import search
import re

__all__ = ['get_popularity']

_polularity_dict = objectstorage.get_object('alphabetspopularity-popularity_dict', (lambda: {}))

_popularity_override = {}

_polularity_dict.update(_popularity_override)
temp = ''
_reg = re.compile(r'<div id="resultStats">\s*About ([0-9]+) results\s*<nobr>')
def get_popularity(alphabet, reset=False, transform=(lambda s:re.sub(r'(.*?) \((.*?)\)', r'"\1" OR "\2"', s.lower().replace('-','')))):
    possibilities = (alphabet, get_alphabet_name(alphabet))
    if not reset:
        for poss in possibilities:
            if poss.lower() in _polularity_dict:
                return _polularity_dict[poss.lower()]
    else:
        for poss in possibilities:
            if poss.lower() in _popularity_override:
                return _popularity_override[poss.lower()]
    if get_alphabet_name(alphabet): alphabet_name = get_alphabet_name(alphabet)
    else: alphabet_name = alphabet
    _polularity_dict[alphabet_name.lower()] = get_number_of_results(alphabet_name.replace('-', ''))
    if transform(alphabet_name) not in (alphabet_name.lower(), alphabet_name, alphabet_name.replace('-', ''), alpahbet_name.lower().replace('-', '')):
        _polularity_dict[alphabet_name.lower()] = max((_polularity_dict[alphabet_name.lower()], get_number_of_results(transform(alphabet_name))))
    objectstorage.save_object('alphabetspopularity-popularity_dict', _polularity_dict)
    return _polularity_dict[alphabet_name.lower()]
    
