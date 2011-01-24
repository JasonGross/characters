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

def construct_character_set(form, reset=False, verbose=False, help=False):
    if get_boolean_value(form, 'help') or help:
        print('Content-type: text/html\n')
        print("""<p>You may any of the following permissible url parameters:</p>
<ul>
  <li>
    <b>characters</b> - A list of characters that must be used, in the form [<em>alphabet</em>, <em>number</em>], where <em>number</em> is a 
    one-based index.  For example, <tt>?constructCharacterSet&amp;characters=[["latin", 1], ["latin", 2], ["greek", 10]]</tt>.  
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
  <li><b>overwrite</b> - whether or not an already existent character set should be overwritten.  Either <tt>true</tt> or <tt>false</tt>.
</ul>""")
        return False
    try:
        characters = get_list_of_values(form, 'characters')
        alphabets = get_list_of_values(form, 'alphabets')
        non_alphabets = get_list_of_values(form, 'nonAlphabets')
        totalCharacters = int(form.getfirst('totalCharacters', -1))
        alias = form.getfirst('alias', None)
        overwrite = get_boolean_value(form, 'overwrite', default=(alias is None)) 
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
        construct_character_set(form, help=True)
        raise
    if rtn != get_object('recognition-tasks_character-set_%s' % alias, (lambda: rtn), is_old=(lambda x: overwrite)):
        raise Exception('Structure with given alias (%s) already exists.  Pick a new alias.' % alias)
    return {'alias':alias}





def main():
    form = cgi.FieldStorage()
    non_existant_variable = form.getvalue('&=variableDoesNotExistString=&')
    args = parser.parse_args()
    rtn = construct_character_set(form, verbose=args.verbose)
    print('Content-type: text/json\n')
    print(json.dumps(rtn))

parser = argparse.ArgumentParser(description='Create a new character set with a given alias or hash code')
parser.add_argument('--verbose', '-v', action='store_true',
                    help='print status on recreating tasks')
if __name__ == '__main__':
    main()
        
