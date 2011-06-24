#!/usr/bin/python
# Filename: image_anonymizer.py
from __future__ import with_statement
import os, sys, json, subprocess, tempfile, shutil, urllib, re
import warnings

##try:
##    import cPickle as pickle
##except ImportError:
##    import pickle
from alphabetspaths import *
from alphabetsutil import png_to_uri

hashed_images = get_hashed_images_dict()

##images_dict = get_object('image_anonymizer_iamges_dict', (lambda: {}))

##def _update_dict():
##    save_object('image_anonymizer_iamges_dict', images_dict)
    
##def deanonymize_image(id, from_path=BASE_PATH):
##    original_name = images_dict[os.path.split(id)[-1]]['original']
##    return os.path.relpath(original_name, from_path)
##
##def get_image_path(id, from_path=BASE_PATH):
##    file_name = images_dict[id]['new path']
##    return os.path.relpath(file_name, from_path)
##
##def anonymize_path(path):
##    if path:
##        base, cur = os.path.split(path)
##        return os.path.join(anonymize_path(base), str(hash(cur)).replace('-', 'm'))
##    return ''
##
##def anonymize_image(original_file_name, new_from_path=BASE_PATH, old_from_path=BASE_PATH, check=True):
##    old_path = os.path.join(old_from_path, original_file_name)
##    new_name = anonymize_path(os.path.relpath(old_path, BASE_PATH)) + '.png'
##    new_path = os.path.join(ANONYMOUS_IMAGES_PATH, new_name)
##    new_url = urllib.parse.urljoin(ANONYMOUS_IMAGES_URL, new_name)
##    if not os.path.exists(new_path) or \
##       (check and os.stat(new_path) != os.stat(old_path)):
##        shutil.copy2(old_path, new_path)
##        images_dict[old_path] = images_dict[os.path.split(new_path)[-1]] = \
##                                {'new path':new_path,
##                                 'new url': new_url,
##                                 'original':old_path,
##                                 'new name':new_name,
##                                 'id':      os.path.split(new_path)[-1]
##                                 }
##        _update_dict()
##    return os.path.relpath(new_path, new_from_path)

_image_reg = re.compile(r'([a-z_]+?)_([0-9]+)_([a-z0-9]+)\.png')
def anonymize_image(image_path, from_path=BASE_PATH, from_url=BASE_URL, desired_base_path=BASE_PATH, include_data_uri=False, include_hash=True, include_original=True, **kwargs):
    name = os.path.split(image_path)[-1]
    image_path = os.path.relpath(os.path.join(from_path, image_path), desired_base_path)
    alphabet, number, uid = _image_reg.match(name).groups()
    first, second, third, fourth = (alphabet + 'a')[:4]
    uid_first, uid_second, uid_third, uid_fourth, uid_rest = uid[:2], uid[2:4], uid[4:6], uid[6:8], uid[8:]
##    print('RewriteRule ^results/accepted-images/(..)%(first)s(..)%(second)s(..)%(third)s([0-9][0-9])([^\.]+)\.png /~jgross/alphabets/results/accepted-images/%(alphabet)s/%(alphabet)s_$4_$1$2$3$5.png' % locals())
    rtn = {
           'anonymous url':urllib.parse.urljoin(ACCEPTED_IMAGES_URL, '%(uid_first)s%(first)s%(uid_second)s%(second)s%(uid_third)s%(third)s%(uid_fourth)s%(fourth)s%(number)s%(uid_rest)s.png' % locals())
          }
    if include_data_uri:
        rtn['data uri'] = png_to_uri(os.path.join(from_path, image_path))
    if include_hash:
        rtn['hash'] = hash(name)
    if include_original:
        rtn['original url'] = urllib.parse.urljoin(from_url, image_path)
    return rtn
    
_REWRITE_DICT = {}
for alphabet in sorted(os.listdir(ACCEPTED_IMAGES_PATH)):
    _REWRITE_DICT[(alphabet + 'a')[:4]] = alphabet

def deanonymize_image(anonymous_url):
    base, image = os.path.split(anonymous_url)
    return {
            'alphabet': _REWRITE_DICT['%s%s%s%s' % (image[2], image[5], image[8], image[11])],
            'character-number': image[12:14],
            'id': '%s%s%s%s%s' % (image[:2], image[3:5], image[6:8], image[9:11], image[15:-4])
           }
    return rtn
#    return '%s%s%s%s_%s_%s%s%s%s%s' % (image[2], image[5], image[8], image[11], image[12:14], image[0:2], image[3:5], image[6:8], image[9:11], image[15:])
    #return hashed_images[int(hash_code)]
##def parse_images(anonymize_images=[], deanonymize_images=[]):
##    rtn = {}
##    for image in anonymize_images:
##        rtn[image] = urllib.parse.urljoin(BASE_URL, anonymize_image(image))
##    for image in deanonymize_images:
##        rtn[image] = urllib.parse.urljoin(BASE_URL, deanonymize_image(image))
##    return rtn
##
##
##if __name__ == '__main__':
##    form = cgi.FieldStorage()
##    rtn = {}
##    anonymize_images = list(form.getfirst('anonymizeImages', []))
##    deanonymize_images = list(form.getfirst('deanonymizeImages', []))
##    rtn = parse_images(anonymize_images, deanonymize_images)
##    print('Content-type: text/json\n')
##    print(json.dumps(rtn))
