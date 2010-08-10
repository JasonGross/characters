#!/usr/bin/python
# display-dataset.py
from __future__ import with_statement
import cgi, cgitb
cgitb.enable(format="html")
import os, re, sys, base64
import datetime
from alphabetspaths import *
from alphabetsutil import png_to_uri

use_uri = True
include_originals = True
include_unreviewed = True
include_rejected = True

def process_options():
    form = cgi.FieldStorage()
    global use_uri
    global include_originals
    global include_unreviewed
    global include_rejected
    use_uri = process_option('use_uri', form, use_uri)
    include_originals = process_option('include_originals', form, include_originals)
    include_unreviewed = process_option('include_unreviewed', form, include_unreviewed)
    include_rejected = process_option('include_rejected', form, include_rejected)

def process_option(option_name, form, default_value):
    if option_name in form.keys():
        return string_to_boolean(form.getvalue(option_name), default_value=default_value)
    return default_value

def string_to_boolean(string_value, default_value=False,
                      true_strings=('1','-1','true','t','y','yes','on'),
                      false_strings=('','0','false','f','no','n','off')):
    true_strings = map(str.lower, true_strings)
    true_strings = map(str.strip, true_strings)
    false_strings = map(str.lower, false_strings)
    false_strings = map(str.strip, false_strings)
    string_value = string_value.lower().strip()
    if string_value in true_strings and string_value not in false_strings:
        return True
    elif string_value in false_strings and string_value not in true_strings:
        return False
    else:
        return default_value
    

output = []


def default_print(string):
    print(string)

def serve_dataset(include_originals=True, include_unreviewed=True, include_rejected=True, print_method=default_print, use_uri=True, verbose=None):
    if verbose is None: verbose = use_uri
    def print_image(image_path, image_url):
        if use_uri:
            print_method('<img src="' + png_to_uri(image_path) + '" height=100px />')
        else:
            print_method('<img src="' + image_url + '" height=100px />')
    def print_alphabets(path, get_ids, get_image_list, get_original_image_list=get_original_image_list):
        for alphabet_id in sorted(get_image_list().keys()):
            if verbose: print('Obtaining ' + alphabet_id + '...<br />')
            if include_originals:
                if verbose: print('  Obtaining originals...<br />')
                print_method('<tr>')
                print_method('<td>')
                print_method(alphabet_id.replace('_', ' '))
                print_method(' Originals')
                print_method('</td>')
                for image_name in get_original_image_list(alphabet_id=alphabet_id, from_path=ORIGINAL_IMAGES_PATH):
                    print_method('<td>')
                    print_image(os.path.join(ORIGINAL_IMAGES_PATH, image_name), os.path.join(ORIGINAL_IMAGES_URL, image_name))
                    print_method('</td>')
                print_method('</tr>')
            for id_number in get_ids(alphabet_id=alphabet_id):
                if verbose: print('  Obtaining for ' + id_number + '...<br />')
                print_method('<tr>')
                print_method('<td>')
                print_method(alphabet_id.replace('_', ' '))
                print_method('</td>')
                for image_name in get_image_list(alphabet_id=alphabet_id, id_=id_number, from_path=path):
                    print_method('<td id="%s %s %s">' % (alphabet_id, image_name, id_number))
                    print_image(os.path.join(path, image_name),
                                os.path.join(BASE_URL, os.path.relpath(path, BASE_PATH), image_name))
                    print_method('</td>')
                print_method('</tr>')
##    push_dir(ACCEPTED_IMAGES_PATH)
    print_method('<h1>Reviewed and accepted results</h1>')
    print_method('<table border=1><tbody>')
    print_alphabets(path=ACCEPTED_IMAGES_PATH, get_ids=get_accepted_ids, get_image_list=get_accepted_image_list)
    print_method('</tbody></table>')
##    pop_dir()
            
    if include_unreviewed:
        print_method('<h1>Unreviewed results</h1>')
##        push_dir(UNREVIEWED_PATH)
        print_method('<table border=1><tbody>')
        print_alphabets(path=UNREVIEWED_PATH, get_ids=get_unreviewed_ids, get_image_list=get_unreviewed_image_list)
        print_method('</tbody></table>')
##        pop_dir()
    if include_rejected:
        print_method('<h1>Rejected results</h1>')
##        push_dir(REJECTED_IMAGES_PATH)
        print_method('<table border=1><tbody>')
        print_alphabets(path=REJECTED_IMAGES_PATH, get_ids=get_rejected_ids, get_image_list=get_rejected_image_list)
        print_method('</tbody></table>')
##        pop_dir()

if __name__ == '__main__':
    print("Content-type: text/html")    # HTML is following
    print                               # blank line, end of headers
    process_options()
    if use_uri: name = 'dataset-uri.html'
    else: name = 'dataset.html'
##    print('Please wait while I build the data set display...')
    push_dir(os.path.join(BASE_PATH, 'working-directory'))
    with open(name, 'r') as f:
        document = f.read()
    pop_dir()
    print(document.replace('</body>', '').replace('</html>', '').replace('<body>', """<body><div id="wait_update" name="wait_update">
  I am currently updating the data set display.
  In the meantime, here is the last version of the data set.
  A link to the updated version will appear at the top of the page when its creation is finished.
  You may need to click on this link for the options you choose to appear.</div><br />"""))
    def append_to_output(string):
        global output
        output.append(string)
    serve_dataset(print_method=append_to_output, use_uri=use_uri,
                  include_originals=include_originals,
                  include_unreviewed=include_unreviewed,
                  include_rejected=include_rejected, verbose=False)
    push_dir(os.path.join(BASE_PATH, 'working-directory'))
    with open(name, 'w') as f:
        f.write('<html><head><title>Alphabets Data Set</title></head><body>')
        f.write('\n'.join(output))
        f.write('</body></html>')
    pop_dir()
    print('<script type="text/javascript"><!--')
    print("document.getElementById('wait_update').innerHTML = 'The updated version is finished.  Please <a href=\"" + \
          os.path.join(BASE_URL, 'working-directory', name) + """">click here</a> to navigate to the updated version.<br />';""")
    print('//-->')
    print('</script>')
    print('</body></html>')
##    print('<script type="text/javascript"><!--')
##    print("location.replace('" + os.path.join(BASE_URL, 'working-directory', name) + "');")
##    print('//-->')
##    print('</script>')
