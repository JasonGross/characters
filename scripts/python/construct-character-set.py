#!/usr/bin/python
# Filename: construct-character-set.py
from __future__ import with_statement
import cgi, cgitb
cgitb.enable(format='nohtml')
import os, sys, json, subprocess, tempfile, shutil, random, urllib, random
import argparse
try:
  import urllib.parse
except ImportError:
  pass
from cgiutil import get_boolean_value, get_list_of_values, is_nested_type
from alphabetspaths import *
from objectstorage import get_object, save_object

CHARACTER_SET_NAME_FORMAT = 'recognition-tasks_character-set_%s'

def construct_character_set(form, args, reset=False, verbose=False, help=False):
    if get_boolean_value(form, 'help', default=help):
        print('Content-type: text/html\n')
        print("""<p>You may any of the following permissible url parameters:</p>
<ul>
  <li>
    <b>characters</b> - A list of characters that must be used, in the form [<em>alphabet</em>, <em>number</em>], where <em>number</em> is a 
    one-based index.  For example, <tt>?characters=[["latin", 1], ["latin", 2], ["greek", 10]]</tt>.  
    <span style="color:red"><strong>Note that the quotes (") are mandatory.</strong></span>
  </li>
  <li>
    <b>alphabets</b> - A list of alphabets from which to draw the characters.  For example, 
    <tt>?constructCharacterSet&amp;alphabets=["latin", "greek", "hebrew"]</tt>.  Does not work well with <b>nonAlphabets</b>.
    <span style="color:red"><strong>Note that the quotes (") are mandatory.</strong></span>
  </li>
  <li>
    <b>nonAlphabets</b> - A list of alphabets from which characters may not be drawn.  For example, 
    <tt>?constructCharacterSet&amp;nonAlphabets=["latin", "greek", "hebrew"]</tt>.  Does not work well with <b>alphabets</b>.
    <span style="color:red"><strong>Note that the quotes (") are mandatory.</strong></span>
  </li>
  <li><b>totalCharacters</b> - the total number of characters to draw. </li>
  <li><b>alias</b> - the name of the structure.  If you do not choose an alias, you will be given a hash code. </li>
  <li><b>overwrite</b> - whether or not an already existent character set should be overwritten.  Either <tt>true</tt> or <tt>false</tt>.</li>
  <li><b>get</b> - If you want to see the current contents of a character set, use this parameter.  For example, <tt>?get=small</tt>.</li>
</ul>""")
        return False
    try:
        get_alias = form.getfirst('get', args.get)
        if get_alias:
            def do_error():
                raise ValueError('No structure with alias "%s" exists.' % get_alias)
            return get_object(CHARACTER_SET_NAME_FORMAT % get_alias, do_error, is_old=(lambda x: False))
        characters = get_list_of_values(form, 'characters', args.characters)
        alphabets = get_list_of_values(form, 'alphabets', args.alphabets)
        non_alphabets = get_list_of_values(form, 'nonAlphabets', args.non_alphabets)
        totalCharacters = int(form.getfirst('totalCharacters', args.total_characters))
        alias = form.getfirst('alias', args.alias)
        overwrite = get_boolean_value(form, 'overwrite', default=((not args.no_overwrite) and (args.overwrite or (alias is None)))) 
        if characters:
            rtn = [(alphabet, int(ch_num) - 1) for alphabet, ch_num in characters]
        elif alphabets:
            rtn = alphabets
        elif non_alphabets:
            rtn = [alphabet for alphabet in get_accepted_image_list() 
                   if alphabet not in nonAlphabets and alphabet.lower() not in nonAlphabets]
        else:
            raise Exception("Insufficient parameters for decision")
        rtn.sort()
        if not alias:
            alias = str(hash(rtn))
    except Exception:
        construct_character_set(form, args, help=True)
        raise
    if rtn != get_object(CHARACTER_SET_NAME_FORMAT % alias, (lambda: rtn), is_old=(lambda x: overwrite)):
        raise Exception('Structure with given alias (%s) already exists.  Pick a new alias.' % alias)
    return {'alias':alias}





def main():
    form = cgi.FieldStorage(keep_blank_values=True)
    non_existant_variable = form.getvalue('&=variableDoesNotExistString=&')
    if 'help' in sys.argv[1:] and get_boolean_value(form, 'help'): # so that a web call with ?help works, since parser normally calls sys.exit if it doesn't understand the arguments
        return construct_character_set(form, None, help=True)
    args = parser.parse_args()
    rtn = construct_character_set(form, args, verbose=args.verbose)
    if rtn:
        print('Content-type: text/plain\n')
        print(json.dumps(rtn))

def str2alphabet_tuple(string):
    lst = str2list(string)
    if len(lst) != 2: raise ValueError('value should be an (alphabet, character number) pair: %s' % string)
    return (lst[0], int(lst[1]))

def str2list(string):
    if (string[0], string[-1]) not in (('[', ']'), ('(', ')')):
        raise ValueError('invalid start/end delimiters for list: %s and %s' % (string[0], string[-1]))
    return string[1:-1].replace(', ', ',').split(',')

parser = argparse.ArgumentParser(description='Create a new character set with a given alias or hash code')
parser.add_argument('--verbose', '-v', action='store_true',
                    help='print status on recreating tasks')
parser.add_argument('--characters', metavar='[A,N]', type=str2alphabet_tuple, nargs='*',
                    help='Characters that must be used, in the form "[alphabet, number]", where "number" is a one-based index.')
parser.add_argument('--alphabets', metavar='A', type=str, nargs='*',
                    help='Alphabets from which to draw the characters')
parser.add_argument('--non-alphabets', metavar='A', type=str, nargs='*',
                    help='alphabets from which characters may not be drawn')
parser.add_argument('--total-characters', metavar='N', type=int, nargs='?',
                    default=-1,
                    help='the total number of characters to draw')
parser.add_argument('--alias', type=str, nargs='?',
                    default=None,
                    help='the name of the structure.  If you do not choose an alias, you will be given a hash code.')
parser.add_argument('--overwrite', action='store_true',
                    help='overwrite already existing character sets')
parser.add_argument('--no-overwrite', action='store_true',
                    help='do not overwrite already existing character sets')
parser.add_argument('--get', metavar='ALIAS', type=str,
                    help='the alias or hash code of which to see the data structure')
if __name__ == '__main__':
    main()
        
