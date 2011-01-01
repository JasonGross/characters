#!/usr/bin/python
# serve-random-alphabet.py
from __future__ import with_statement
import cgi, cgitb
cgitb.enable(format="html")
import os, re, sys
import random
import urllib
import python2to3patch
from alphabetspaths import *

size_upper_bound = 1 << 31

def process_options():
    form = cgi.FieldStorage()
    global size_upper_bound
    for key in ('count_upper_bound', 'length_upper_bound', 'max_count',
                'max_length', 'max_letter_count', 'max_size',
                'size_upper_bound', 'upper_bound'):
        if key in form.keys():
            try:
                size_upper_bound = int(form.getvalue(key))
                break
            except ValueError:
                pass

def make_listing(folder, file_name):
    listing = {}
    reg = re.compile('(.*?)_[Pp]age_([0-9]+).png')
    push_dir(folder)
    for image in os.listdir(os.getcwd()):
        match = reg.match(image)
        if match:
            name, number = match.groups()
            if name in listing: listing[name] += 1
            else: listing[name] = 1
    file_listing = '\n'.join('%s --- %d' % (alphabet, listing[alphabet]) for alphabet in sorted(listing.keys()))
    with open(file_name, 'w') as f:
        f.write(file_listing)
    pop_dir()

def pick_random_alphabet_url(folder, file_name, size_upper_bound=50):
    push_dir(folder)
    if not os.path.exists(file_name):
        make_listing('.', file_name)
    with open(file_name, 'r') as f:
        contents = f.read()
    listing = old_listing = [i.split(' --- ') for i in contents.split('\n')]
    listing = [(name, int(number)) for name, number in listing if int(number) <= size_upper_bound]
    if not listing:
        min_num = min(int(number) for name, number in old_listing)
        listing = [(name, int(number)) for name, number in old_listing if int(number) <= min_num]
    choice = random.choice(listing)
    url = 'image%(number)d=%(name)s_page_%(number+1)02d.png&character%(number)dId=%(name)s_page_%(number+1)02d'
    rtn = 'globalImageHeight=100px&submitTo=' + urllib.parse.quote(CHARACTER_REQUEST_SUBMISSION_URL) + '&' + '&'.join(url % {'name':choice[0], 'number':number, 'number+1':number+1} for number in range(choice[1]))
    return rtn


if __name__ == '__main__':
    process_options()
    new_url = CHARACTER_REQUEST_URL + '?' + \
              pick_random_alphabet_url(ORIGINAL_IMAGES_PATH, ALPHABET_LISTING_PATH, size_upper_bound=size_upper_bound)
    #print("Content-Type: text/plain")
    print("Content-type: text/html")    # HTML is following
    print                               # blank line, end of headers
    print('<script type="text/javascript"><!--')
    print("location.replace('" + new_url + "');")
    print('//-->')
    print('</script>')
    sys.exit(0)
        
