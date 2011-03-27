#!/usr/bin/python
from __future__ import with_statement
import argparse
import os
from alphabetspaths import *
import re


parser = argparse.ArgumentParser(description='Gets the ids of turk users who have already submitted a hit')
parser.add_argument('--include-drawings', action='store_true',
                    help='Include turk submissions of initial drawings?')
parser.add_argument('--path', type=str, default=[CATEGORIZATION_UNREVIEWED_PATH, RECOGNITION_UNREVIEWED_PATH, RECOGNITION_RT_UNREVIEWED_PATH],
                    nargs='?', help='What folders should I look in for Turk submissions')

def _is_hash(string):
    if string[0] == 'm': string = '-' + string[1:]
    try:
        return str(int(string)) == string
    except ValueError:
        return False

_STUPID_REGEX = re.compile('^[A-Z0-9]+$')
def _is_worker_id(string):
    if _is_hash(string): return False
    string = string.upper()
    if not string.isalnum(): return False
    if string.isdigit(): return False
    if string in ('UNREVIEWED', 'BAD'): return False
    if string[0] != 'A': raw_input(string)
    return True



if __name__ == '__main__':
    args = parser.parse_args()
    rtn = set()
    if args.include_drawings:
        for get_dict in [get_accepted_ids, get_rejected_ids, get_extra_ids, get_turk_ids]:
            cur_dict = get_dict()
            for alphabet in cur_dict:
                rtn.update(_id.upper() for _id in cur_dict[alphabet])
    for path in args.path:
        if not os.path.exists(path) and path in globals():
            path = globals[path]
        for base, dirs, files in os.walk(path):
            rtn.update(path.upper() for path in dirs if _is_worker_id(path))
    print(','.join(list(sorted(rtn))))


