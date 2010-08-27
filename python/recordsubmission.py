#!/usr/bin/python
# recordsubmission.py -- Stores the data from the submission
from __future__ import with_statement
import cgi
import os, re
import urllib
import sys
from alphabetspaths import *
from alphabetsutil import stroke_to_list, compress_images


import warnings
##
##def deprecated(func):
##    """This is a decorator which can be used to mark functions
##    as deprecated. It will result in a warning being emmitted
##    when the function is used."""
##    def newFunc(*args, **kwargs):
##        warnings.warn("Call to deprecated function %s." % func.__name__,
##                      category=DeprecationWarning)
##        return func(*args, **kwargs)
##    newFunc.__name__ = func.__name__
##    newFunc.__doc__ = func.__doc__
##    newFunc.__dict__.update(func.__dict__)
##    return newFunc
##
##@deprecated #???
##def get_alphabet_name(form_dict, id_reg='^character([0-9]+)Id'):
##    return get_alphabet_id_from_dict(form_dict, id_reg=id_reg)
###deprecated(get_alphabet_name)

def _make_folder_for_submission(uid, path=UNREVIEWED_PATH):
    if not isinstance(uid, str):
        uid = str(uid)
    push_dir(path)
    if not os.path.exists(uid.replace('-', 'm')):
        os.mkdir(uid.replace('-', 'm'))
    os.chdir(uid.replace('-', 'm'))
    existing = map(int, [i for i in os.listdir(os.getcwd()) if os.path.isdir(i)] + [-1])
    new_dir = str(1 + max(existing))
    os.mkdir(new_dir)
    pop_dir()
    return os.path.join(path, uid.replace('-', 'm'), new_dir)

def _put_properties(folder, properties, file_name='responses.txt',
                   not_use=('^image[0-9]+', '^character_', '^character[0-9]+Id', '^ipAddress',
                            '^annotation', '^assignmentaccepttime', '^assignmentapprovaltime',
                            '^assignmentduration', '^assignmentrejecttime', '^assignments',
                            '^assignmentstatus', '^assignmentsubmittime', '^autoapprovaldelay',
                            '^autoapprovaltime', '^creationtime', '^deadline', '^description',
                            '^hitlifetime', '^hitstatus', '^hittypeid', '^keywords',
                            '^numavailable', '^numcomplete', '^numpending', '^reviewstatus',
                            '^reward', '^title', '^hitid', '^assignmentid')):
    push_dir(folder)
    write_to_file = ''
    def can_use(key):
        for bad_key in not_use:
            if re.match(bad_key, key):
                return False
        return True
    for key in sorted(properties.keys()):
        if can_use(key):
            write_to_file += '%s: %s\n' % (key, properties[key].replace('\n', '\\n'))
    with open(file_name, 'w') as f:
        f.write(write_to_file)
    pop_dir()

def get_alphabet_id_from_dict(form_dict, id_reg='^character([0-9]+)Id', name_reg='^(.*?)_[Pp]age_[0-9]+'):
    id_reg = re.compile(id_reg)
    name_reg = re.compile(name_reg)
    for key in sorted(form_dict.keys()):
        match = id_reg.match(key)
        if match:
            return name_reg.match(form_dict[key]).groups()[0]
    raise ValueError

def _get_image_dict_list(form_dict, id_reg='^character([0-9]+)Id'):
    original_image_names = []
    image_dict = {}
    id_reg = re.compile(id_reg)
    image_reg = re.compile('<img\\s+src="+(.*?)"+\\s*/>')
    rtn = []
    for key in sorted(form_dict.keys()):
        match = id_reg.match(key)
        if match:
            image_dict[int(match.groups()[0])] = {'id':form_dict[key]}
    for image_num in image_dict:
        for key in sorted(form_dict.keys()):
            if image_dict[image_num]['id'] in key:
                if '_stroke' in key:
                    image_dict[image_num]['stroke'] = _fix_strokes(form_dict[key])
                elif '_image' in key:
                    if not image_reg.search(form_dict[key]):
                        print('Error: key: %s, value: %s' % (cgi.escape(key), cgi.escape(form_dict[key])))
                    image_dict[image_num]['image'] = image_reg.search(form_dict[key]).groups()[0]
    for image_num in image_dict:
        image_dict[image_num]['name'] = image_dict[image_num]['id'].replace('_Page', '').replace('_page', '').replace('.png', '')
    for image_num in sorted(image_dict.keys()):
        rtn.append(image_dict[image_num])
    return rtn

def _fix_strokes(stroke_string):
    rtn = stroke_to_list(stroke_string)
    min_t = int(rtn[0][0]['t'])
    for stroke in rtn:
        for point in stroke:
            point['t'] = int(point['t']) - min_t
    return '[' + ','.join('[' + ','.join("{'x':%(x)s,'y':%(y)s,'t':%(t)d}" % point for point in stroke) + ']' for stroke in rtn) + ']'

def _save_images(image_dict_list, uid, images_path, strokes_path, make_base_file_name=None):
    raise_object_changed(images_path)
    raise_object_changed(strokes_path)
    if not make_base_file_name:
        def make_base_file_name(image_name, uid):
            return image_name + '_' + uid
    push_dir(images_path)
    rtn = []
    for image in image_dict_list:
        base_file_name = make_base_file_name(image['name'], uid)
        path = os.path.split(base_file_name)[0]
        if path and not os.path.exists(path):
            os.makedirs(path)
        if os.path.exists(base_file_name + '.png'):
            raw_input('The image `' + base_file_name + '.png' + "' already exists.  Press enter to continue and overwrite it, or press ^c (ctrl + c) to break.")
        urllib.urlretrieve(image['image'], base_file_name + '.png')
        rtn.append(base_file_name + '.png')
    pop_dir()
    push_dir(strokes_path)
    for image in image_dict_list:
        base_file_name = make_base_file_name(image['name'], uid)
        path = os.path.split(base_file_name)[0]
        if path and not os.path.exists(path):
            os.makedirs(path)
        with open(base_file_name + '.stroke', 'w') as f:
            f.write(image['stroke'])
    pop_dir()
    return rtn

def _log_success(folder):
    push_dir(folder)
    with open('success.log', 'w') as f:
        f.write('')
    pop_dir()

def make_uid(form_dict):
    if 'workerid' in form_dict and form_dict['workerid']:
        return form_dict['workerid']
    else:
        return str(hash(form_dict['ipAddress']))

alphabet_id = None

def record_submission(form_dict, names=('get_unreviewed_image_list', 'get_unreviewed_stroke_list'),
                      many_dirs=False, path=UNREVIEWED_PATH,
                      images_path=TURK_IMAGES_PATH, strokes_path=TURK_STROKES_PATH, extra_info_path=TURK_EXTRA_INFO_PATH,
                      verbose=True, pseudo=False):
    if names:
        for name in names:
            if os.path.exists(get_object_file_name(name)):
                os.remove(get_object_file_name(name))
    if verbose: print('Hashing IP address...')
    uid = make_uid(form_dict)
    if many_dirs:
        print('Done<br>Making folder for your submission...')
        images_path = strokes_path = extra_info_path = folder = _make_folder_for_submission(uid, path=path)
    if verbose: print('Done<br>Retrieving and processing your drawings...')
    image_dict_list = _get_image_dict_list(form_dict)
    if verbose: print('Done<br>Saving your stroke and image data...')
    if many_dirs:
        make_base_file_name = None
    else:
        def make_base_file_name(image_name, uid):
            global alphabet_id
            if not alphabet_id or image_name[:len(alphabet_id)] != alphabet_id:
                alphabet_id = get_alphabet_id_from_file_name(image_name + '_' + uid)
            return os.path.join(alphabet_id, image_name + '_' + uid)
    image_list = _save_images(image_dict_list, uid, images_path, strokes_path, make_base_file_name=make_base_file_name)
    if verbose: print('Done<br>Storing your non-image responses...')
    if many_dirs:
        _put_properties(extra_info_path, form_dict)
    else:
        file_name = get_alphabet_id_from_dict(form_dict) + '_' + uid + '.results.txt'
        _put_properties(extra_info_path, form_dict, file_name=file_name)
    if not pseudo:
        if verbose: print('Done<br>Compressing your image data...')
        compress_images(folder=images_path, image_list=image_list)
    if many_dirs:
        _log_success(folder)
    if verbose: print('Done<br>You may now leave this page.<br>')
    if verbose: print('<a href="http://scripts.mit.edu/~jgross/alphabets/">Return to home page</a>')
