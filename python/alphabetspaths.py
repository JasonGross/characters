#!/usr/bin/python
# Filename: alphabetspaths.py
from __future__ import with_statement
import os
import sys
import re
import urllib
import python2to3patch
try:
    import cPickle as pickle
except ImportError:
    import pickle
try:
    from python3lib import relpath
except SyntaxError:
    from python25lib import relpath

__all__ = ['BASE_PATH', 'BASE_URL', 'UNREVIEWED_PATH', 'UNREVIEWED_URL', 'FILE_NAME_REGEX',
           'get_original_image_list',
           'get_unreviewed_extra_info_file_name', 'get_unreviewed_ids', 'get_unreviewed_image_list', 'get_unreviewed_stroke_list',
           'pop_dir', 'push_dir', 'PNGOUT_PATH', 'MOGRIFY_PATH', 'CONVERT_PATH', 'SUBMISSION_LOG_PATH', 'ALPHABET_LISTING_PATH',
           'CHARACTER_REQUEST_URL', 'PUBLIC_DATASET_PATHS', 'PUBLIC_DATASET_BETA_PATHS', 'FORM_SUBMISSION_URL',
           'MATLAB_MAT_FILE_NAME', 'MATLAB_DOWNSAMPLE_MAT_FILE_NAME', 'MATLAB_NO_STROKES_MAT_FILE_NAME', 'MATLAB_DOWNSAMPLE_NO_STROKES_MAT_FILE_NAME',
           'ACCEPTED_JAVASCRIPT_PATH', 'REJECTED_JAVASCRIPT_PATH', 'SCRIPTS_PATH', 'JAVASCRIPT_PATH', 'TURK_POST_EXTRA_LIST_PATH',
           'RESULTS_PATH', 'get_alphabet_name', 'get_alphabet_id_from_file_name',
           'STORED_ALPHABET_IMAGES_LIST_PATH',
           'CATEGORIZATION_RESULTS_PATH',
           'CATEGORIZATION_UNREVIEWED_PATH', 'CATEGORIZATION_UNREVIEWED_URL',
           'LOCAL_TEMP_PATH', 'LOCAL_TEMP_URL',
           'ANONYMOUS_IMAGES_PATH', 'ANONYMOUS_IMAGES_URL',
           'get_object', 'get_object_file_name', 'save_object',
           'get_hashed_images_dict']
 
_paths = {'ORIGINAL':(lambda s: 'originals' if s == 'images' else None),
          'ACCEPTED': (lambda s: ('accepted-%s' % s) if s != 'information' else None),
          'REJECTED': (lambda s: ('rejected-%s' % s) if s != 'information' else None),
          'TURK': (lambda s: ('turk-%s' % s) if s != 'information' else None),
          'TURK_REJECTED': (lambda s: ('turk-rejected-%s' % s) if s != 'information' else None),
          'TURK_ACCEPTED': (lambda s: ('turk-accepted-%s' % s) if s != 'information' else None),
          'EXTRA': (lambda s: ('extra-%s' % s) if s != 'information' else None),
          'CATEGORIZATION_ACCEPTED': (lambda s: ('categorization/accepted-%s' % s) if s == 'information' else None),
          'CATEGORIZATION_REJECTED': (lambda s: ('categorization/rejected-%s' % s) if s == 'information' else None),
          'CATEGORIZATION_TURK': (lambda s: ('categorization/turk-%s' % s) if s == 'information' else None),
          'CATEGORIZATION_TURK_REJECTED': (lambda s: ('categorization/turk-rejected-%s' % s) if s == 'information' else None),
          'CATEGORIZATION_TURK_ACCEPTED': (lambda s: ('categorization/turk-accepted-%s' % s) if s == 'information' else None),
          'CATEGORIZATION_EXTRA': (lambda s: ('categorization/extra-%s' % s) if s == 'information' else None)}

_image_stroke_dicts_names = ['unreviewed'] + [key.lower() for key in sorted(_paths.keys()) if 'CATEGORIZATION_' not in key]

FILE_NAME_REGEX = '(.*?)_([0-9]+)_([^._]+)'
FILE_NAME_REGEX_COMPILED = re.compile(FILE_NAME_REGEX)

_normal_path_names = [] + \
                     [_path for _path in sorted(_paths.keys()) \
                      if _path not in ('ORIGINAL', 'UNREVIEWED') and 'CATEGORIZATION_' not in _path]

BASE_PATH = os.path.join(os.path.expanduser('~'), 'web_scripts', 'alphabets')
BASE_URL = 'http://scripts.mit.edu/~jgross/alphabets/'

_self = sys.modules[globals()['__name__']]

SCRIPTS_PATH = os.path.join(BASE_PATH, 'scripts')
JAVASCRIPT_PATH = os.path.join(SCRIPTS_PATH, 'javascript')
ACCEPTED_JAVASCRIPT_PATH = os.path.join(JAVASCRIPT_PATH, 'accepted_alphabets.js')
REJECTED_JAVASCRIPT_PATH = os.path.join(JAVASCRIPT_PATH, 'rejected_alphabets.js')

_RELATIVE_RESULTS_PATH = 'results'
_RELATIVE_UNREVIEWED_PATH = os.path.join(_RELATIVE_RESULTS_PATH, 'unreviewed')

_RELATIVE_CATEGORIZATION_RESULTS_PATH = 'results/categorization'
_RELATIVE_CATEGORIZATION_UNREVIEWED_PATH = os.path.join(_RELATIVE_CATEGORIZATION_RESULTS_PATH, 'unreviewed')

_RELATIVE_LOCAL_TEMP_PATH = 'tmp'
_RELATIVE_ANONYMOUS_IMAGES_PATH = 'anonymous-images'

RESULTS_PATH = os.path.join(BASE_PATH, _RELATIVE_RESULTS_PATH)
UNREVIEWED_PATH = os.path.join(BASE_PATH, _RELATIVE_UNREVIEWED_PATH)

CATEGORIZATION_RESULTS_PATH = os.path.join(BASE_PATH, _RELATIVE_CATEGORIZATION_RESULTS_PATH)
CATEGORIZATION_UNREVIEWED_PATH = os.path.join(BASE_PATH, _RELATIVE_CATEGORIZATION_UNREVIEWED_PATH)

RESULTS_URL = urllib.parse.urljoin(BASE_URL, _RELATIVE_RESULTS_PATH)
UNREVIEWED_URL = urllib.parse.urljoin(BASE_URL, _RELATIVE_UNREVIEWED_PATH)

CATEGORIZATION_RESULTS_URL = urllib.parse.urljoin(BASE_URL, _RELATIVE_CATEGORIZATION_RESULTS_PATH)
CATEGORIZATION_UNREVIEWED_URL = urllib.parse.urljoin(BASE_URL, _RELATIVE_CATEGORIZATION_UNREVIEWED_PATH)

TURK_POST_EXTRA_LIST_PATH = os.path.join(RESULTS_PATH, 'turk-bad-submissions.txt')

STORED_ALPHABET_IMAGES_LIST_PATH = os.path.join(RESULTS_PATH, 'alphabets-images-list.txt')

LOCAL_TEMP_PATH = os.path.join(BASE_PATH, _RELATIVE_LOCAL_TEMP_PATH)
LOCAL_TEMP_URL = urllib.parse.urljoin(BASE_URL, _RELATIVE_LOCAL_TEMP_PATH)

ANONYMOUS_IMAGES_PATH = os.path.join(BASE_PATH, _RELATIVE_ANONYMOUS_IMAGES_PATH)
ANONYMOUS_IMAGES_URL = urllib.parse.urljoin(BASE_URL, _RELATIVE_ANONYMOUS_IMAGES_PATH)

for _path in _paths:
    for name_part, path_part in (('IMAGES', 'images'),
                                 ('STROKES', 'strokes'),
                                 ('EXTRA_INFO', 'extra-information'),
                                 ('INFO', 'information')):
        if _paths[_path](path_part):
            setattr(_self, '_RELATIVE_%s_%s_PATH' % (_path, name_part),
                    os.path.join(_RELATIVE_RESULTS_PATH, _paths[_path](path_part)))
            setattr(_self, '%s_%s_PATH' % (_path, name_part),
                    os.path.join(BASE_PATH, getattr(_self, '_RELATIVE_%s_%s_PATH' % (_path, name_part))))
            __all__.append('%s_%s_PATH' % (_path, name_part))
            setattr(_self, '%s_%s_URL' % (_path, name_part),
                    urllib.parse.urljoin(BASE_URL, getattr(_self, '_RELATIVE_%s_%s_PATH' % (_path, name_part))))
            __all__.append('%s_%s_URL' % (_path, name_part))

CHARACTER_REQUEST_URL = urllib.parse.urljoin(BASE_URL, 'CharacterRequest.shtml')
FORM_SUBMISSION_URL = urllib.parse.urljoin(BASE_URL, 'scripts/python/record-submission.py')

PNGOUT_PATH = os.path.join(BASE_PATH, 'scripts', 'pngout')
MOGRIFY_PATH = os.path.join(BASE_PATH, 'scripts', 'ImageMagick-6.6.2-6', 'utilities', 'mogrify')
CONVERT_PATH = os.path.join(BASE_PATH, 'scripts', 'ImageMagick-6.6.2-6', 'utilities', 'convert')

SUBMISSION_LOG_PATH = os.path.join(BASE_PATH, 'scripts', 'submission.log')

ALPHABET_LISTING_PATH = os.path.join(RESULTS_PATH, 'alphabets.txt')

##MATLAB_M_FILE_NAME = os.path.join(RESULTS_PATH, 'results.m')
MATLAB_MAT_FILE_NAME = os.path.join(RESULTS_PATH, 'results.mat')
MATLAB_DOWNSAMPLE_MAT_FILE_NAME = os.path.join(RESULTS_PATH, 'results-28x28.mat')
MATLAB_NO_STROKES_MAT_FILE_NAME = os.path.join(RESULTS_PATH, 'results-nostroke.mat')
MATLAB_DOWNSAMPLE_NO_STROKES_MAT_FILE_NAME = os.path.join(RESULTS_PATH, 'results-nostroke-28x28.mat')

PUBLIC_DATASET_PATHS = ('accepted-extra-information', 'accepted-images', 'accepted-strokes', 'originals', 'results*.mat',
                             'decompress-strokes_standalone.py', 'compress-strokes_standalone.py')
PUBLIC_DATASET_BETA_PATHS = ('accepted-extra-information', 'accepted-images', 'accepted-strokes', 'originals', 'rejected-extra-information',
                             'rejected-images', 'rejected-strokes', 'extra-extra-information',
                             'extra-images', 'extra-strokes', 'results*.mat', 'unreviewed',
                             'decompress-strokes_standalone.py', 'compress-strokes_standalone.py')

_ALPHABET_NAMES_FILE = os.path.join(RESULTS_PATH, 'alphabet-names.txt')

_dir_stack = []


    

def push_dir(new_dir, make_dirs=True):
    _dir_stack.append(os.getcwd())
    if make_dirs and not os.path.exists(new_dir):
        os.makedirs(new_dir)
    os.chdir(new_dir)

def pop_dir():
    os.chdir(_dir_stack.pop())

_alphabets_names_dict = {}

for _name in _image_stroke_dicts_names:
    setattr(_self, '_%s_images_dict' % _name, {})
    setattr(_self, '_%s_strokes_dict' % _name, {})


OBJECT_STORAGE_DIRECTORY = os.path.join(BASE_PATH, 'object-storage')
_save_object_call_backs = {}
def register_save_object_callback(name, method):
    if name not in _save_object_call_backs:
        _save_object_call_backs[name] = []
    _save_object_call_backs[name].append(method)

def get_object(name, object_maker, is_old=None, protocol=0):
    if os.path.exists(get_object_file_name(name)):
        try:
            with open(get_object_file_name(name), 'rb') as f:
                obj = pickle.load(f)
            if is_old is None or not is_old(obj):
                return obj
        except (IOError,): # add more as needed
            pass
    obj = object_maker()
    with open(get_object_file_name(name), 'wb') as f:
        pickle.dump(obj, f, protocol=protocol)
    return obj

def save_object(name, obj, protocol=0):
    with open(get_object_file_name(name), 'wb') as f:
        pickle.dump(obj, f, protocol=protocol)
    if name in _save_object_call_backs:
        for method in _save_object_call_backs[name]:
            _save_object_call_backs[name]()
    return obj

def get_object_file_name(name):
    return os.path.join(OBJECT_STORAGE_DIRECTORY, name + '.obj')


def get_alphabet_name(alphabet_id):
    global _alphabets_names_dict
    if not _alphabets_names_dict:
        _alphabets_names_dict = {}
        with open(_ALPHABET_NAMES_FILE, 'r') as f:
            for line in f:
                a_id, name = line.replace('\n', '').split(': ')
                _alphabets_names_dict[a_id.lower()] = name
    if alphabet_id.lower() in _alphabets_names_dict:
        return _alphabets_names_dict[alphabet_id.lower()]


def get_alphabet_id_from_file_name(file_name):
    actual_name = os.path.splitext(os.path.split(file_name)[-1])[0]
    match = FILE_NAME_REGEX_COMPILED.match(actual_name)
    if not match:
        raise ValueError("Invalid file name paseed for id: %s" % repr(file_name))
    return match.groups()[0]

def make_get_list(reg_string, default_from_path, use_dict, name):
    def get_list(alphabet_id=None, from_path=default_from_path):
        reg = re.compile(reg_string)
        if not use_dict:
            def make_dict():
                use_dict = {}
                for base, dirs, files in os.walk(default_from_path):
                    print(base)
                    for file_name in sorted(files):
                        match = reg.match(file_name)
                        if match:
                            name = match.groups()[0]
                            if name not in use_dict:
                                use_dict[name] = []
                            use_dict[name].append(os.path.join(default_from_path, file_name))
                return use_dict
            use_dict.update(get_object(name, make_dict))
        if alphabet_id is None:
            return use_dict.copy()
        if alphabet_id not in use_dict:
            return []
        return [relpath(i, from_path) for i in use_dict[alphabet_id]]
    return get_list

def make_get_optional_id_list(reg_string, default_from_path, use_dict, name, base_dir=None):
    if base_dir is None: base_dir = default_from_path
    reg = re.compile(reg_string)
    def get_list(alphabet_id=None, id_=None, from_path=default_from_path):
        if not use_dict:
            def make_dict():
                use_dict = {}
                for base, dirs, files in os.walk(base_dir):
                    print(base)
                    for file_name in sorted(files):
                        match = reg.match(file_name)
                        if match:
                            name, number, cur_id = match.groups()
                            name = name
                            if name not in use_dict: use_dict[name] = {}
                            if cur_id not in use_dict[name]: use_dict[name][cur_id] = []
                            use_dict[name][cur_id].append(os.path.join(base, file_name))
                return use_dict
            use_dict.update(get_object(name, make_dict))
        if alphabet_id is None:
            rtn = {}
            if id_ is None:
                for alphabet_id in use_dict:
                    rtn[alphabet_id] = {}
                    for id_ in use_dict[alphabet_id]:
                        rtn[alphabet_id][id_] = [relpath(i, from_path) for i in use_dict[alphabet_id][id_]]
            else:
                rtn = {}
                for alphabet_id in use_dict:
                    if id_ in use_dict[alphabet_id]:
                        rtn[alphabet_id] = [relpath(i, from_path) for i in use_dict[alphabet_id][id_]]
            return rtn
        else:
            if id_ is None:
                if alphabet_id not in use_dict: return {}
                rtn = {}
                for cur_id in use_dict[alphabet_id]:
                    rtn[cur_id] = [relpath(i, from_path) for i in use_dict[alphabet_id][cur_id]]
                return rtn
            else:
                if alphabet_id not in use_dict: return []
                return [relpath(i, from_path) for i in use_dict[alphabet_id][id_]]
    return get_list

def make_get_ids(get_image_list):
    def get_ids(alphabet_id=None, id_=None):
        images = get_image_list(alphabet_id=alphabet_id, id_=id_)
        if alphabet_id is None:
            if id_ is None:
                rtn = {}
                for alphabet_id in images:
                    rtn[alphabet_id] = sorted(images[alphabet_id].keys())
            else:
                rtn = {}
                for alphabet_id in images:
                    rtn[alphabet_id] = ([id_] if images[alphabet_id] else [])
            return rtn
        else:
            if id_ is None:
                return sorted(images.keys())
            else:
                return ([id_] if images else [])
    return get_ids

def make_get_extra_info_file_name(get_ids, location_path, default_from_path=RESULTS_PATH):
    def get_extra_info_file_name(alphabet_id=None, id_=None, from_path=default_from_path):
        ids = get_ids(alphabet_id=alphabet_id, id_=id_)
        if alphabet_id is None:
            rtn = {}
            if id_ is None:
                for alphabet_id in ids:
                    if alphabet_id not in rtn:
                        rtn[alphabet_id] = {}
                    for id_ in ids[alphabet_id]: # ids[alphabet_id] is a list of ids
                        rtn[alphabet_id][id_] = relpath(os.path.join(location_path, '%s_%s.results.txt' % (alphabet_id, id_)),
                                                                from_path)
            else:
                for alphabet_id in ids:
                    if ids[alphabet_id]:
                        for id_ in ids[alphabet_id]: # ids[alphabet_id] is a list of ids
                            rtn[alphabet_id] = relpath(os.path.join(location_path, '%s_%s.results.txt' % (alphabet_id, id_)),
                                                               from_path)
            return rtn
        else:
            if id_ is None:
                rtn = {}
                for id_ in ids:
                    rtn[id_] = relpath(os.path.join(location_path, '%s_%s.results.txt' % (alphabet_id, id_)),
                                               from_path)
                return rtn
            else:
                return (relpath(from_path,
                                        os.path.join(location_path, '%s_%s.results.txt' % (alphabet_id, id_))) if ids else None)
    return get_extra_info_file_name

get_original_image_list = make_get_list(reg_string='(.*?)_[Pp]age_([0-9]+).png',
                                        default_from_path=ORIGINAL_IMAGES_PATH, use_dict=_original_images_dict,
                                        name='get_original_image_list')

get_unreviewed_image_list = make_get_optional_id_list(reg_string=FILE_NAME_REGEX+'.png',
                                                      default_from_path=UNREVIEWED_PATH, use_dict=_unreviewed_images_dict,
                                                      name='get_unreviewed_image_list')
get_unreviewed_ids = make_get_ids(get_unreviewed_image_list)
get_unreviewed_stroke_list = make_get_optional_id_list(reg_string=FILE_NAME_REGEX+'.c?stroke',
                                                       default_from_path=UNREVIEWED_PATH, use_dict=_unreviewed_strokes_dict,
                                                       name='get_unreviewed_stroke_list')

def get_unreviewed_extra_info_file_name(alphabet_id=None, id_=None, from_path=UNREVIEWED_PATH):
    images = get_unreviewed_image_list(alphabet_id=alphabet_id, id_=id_, from_path=from_path)
    if alphabet_id is None:
        rtn = {}
        if id_ is None:
            for alphabet_id in images:
                for id_ in images[alphabet_id]: # images[alphabet_id] is a dict with ids as keys
                    base = os.path.split(images[alphabet_id][id_][0])[0]
                    rtn[alphabet_id][id_] = os.path.join(base, 'responses.txt')
        else:
            for alphabet_id in images:
                if images[alphabet_id]:
                    base = os.path.split(images[alphabet_id][0])[0]
                    rtn[alphabet_id] = os.path.join(base, 'responses.txt')
        return rtn
    else:
        if id_ is None:
            rtn = {}
            for id_ in images:
                if images[id_]:
                    base = os.path.split(images[id_][0])[0]
                    rtn[id_] = os.path.join(base, 'responses.txt')
            return rtn
        else:
            if images:
                base = os.path.split(images[id_][0])[0]
                return os.path.join(base, 'responses.txt')
            else:
                return None

for _name in _normal_path_names:
    setattr(_self, 'get_%s_image_list' % _name.lower(),
            make_get_optional_id_list(reg_string=FILE_NAME_REGEX+'.png',
                                      default_from_path=getattr(_self, '%s_IMAGES_PATH' % _name.upper()),
                                      use_dict=getattr(_self, '_%s_images_dict' % _name.lower()),
                                      name=('get_%s_image_list' % _name.lower())))
    __all__.append('get_%s_image_list' % _name.lower())
    setattr(_self, 'get_%s_ids' % _name.lower(),
            make_get_ids(getattr(_self, 'get_%s_image_list' % _name.lower())))
    __all__.append('get_%s_ids' % _name.lower())
    setattr(_self, 'get_%s_extra_info_file_name' % _name.lower(),
            make_get_extra_info_file_name(getattr(_self, 'get_%s_ids' % _name.lower()),
                                          getattr(_self, '%s_EXTRA_INFO_PATH' % _name.upper())))
    __all__.append('get_%s_extra_info_file_name' % _name.lower())
    setattr(_self, 'get_%s_stroke_list' % _name.lower(),
            make_get_optional_id_list(reg_string=FILE_NAME_REGEX+'.c?stroke',
                                      default_from_path=getattr(_self, '%s_STROKES_PATH' % _name.upper()),
                                      use_dict=getattr(_self, '_%s_strokes_dict' % _name.lower()),
                                      name=('get_%s_stroke_list' % _name.lower())))
    __all__.append('get_%s_stroke_list' % _name.lower())
    


def _make_hashed_images_dict():
    rtn = {}
    images = get_accepted_image_list()
    for alphabet in images:
        for id_ in images[alphabet]:
            for image in images[alphabet][id_]:
                rtn[hash(image)] = image
    return rtn
def _remake_hashed_images_dict():
    rtn = _make_hashed_images_dict()
    save_object('get_hashed_images_dict', rtn)
    return rtn
register_save_object_callback('get_accepted_image_list', _remake_hashed_images_dict)
def get_hashed_images_dict():
    return get_object('get_hashed_images_dict', _make_hashed_images_dict)
