#!/usr/bin/python
# move-turk-to-approved.py -- Moves the turk results to the approved folders
from __future__ import with_statement
import os
import sys
from alphabetspaths import *


MOVE_ALL = False
if '--all' in sys.argv:
    MOVE_ALL = True

##turk_image_list = get_turk_image_list(from_path=os.getcwd())
##turk_strokes_list = get_turk_stroke_list(from_path=os.getcwd())
##turk_extra_info_file_name = get_turk_extra_info_file_name(from_path=os.getcwd())
##turk_rejected_image_list = get_turk_rejected_image_list(from_path=os.getcwd())
##turk_rejected_stroke_list = get_turk_rejected_stroke_list(from_path=os.getcwd())
##turk_rejected_extra_info_file_name = get_turk_rejected_extra_info_file_name(from_path=os.getcwd())
##turk_accepted_image_list = get_turk_accepted_image_list(from_path=os.getcwd())
##turk_accepted_strokes_list = get_turk_accepted_stroke_list(from_path=os.getcwd())
##turk_accepted_extra_info_file_name = get_turk_accepted_extra_info_file_name(from_path=os.getcwd())


dict_list = [{'get_list':get_turk_rejected_image_list, 'old path':TURK_REJECTED_IMAGES_PATH, 'path':REJECTED_IMAGES_PATH,
              'name':'rejected images', 'obj name':'get_turk_rejected_image_list'},
             {'get_list':get_turk_rejected_stroke_list, 'old path':TURK_REJECTED_STROKES_PATH, 'path':REJECTED_STROKES_PATH,
              'name':'rejected strokes', 'obj name':'get_turk_rejected_stroke_list'},
             {'get_list':get_turk_rejected_extra_info_file_name, 'old path':TURK_REJECTED_EXTRA_INFO_PATH, 'path':REJECTED_EXTRA_INFO_PATH,
              'name':'rejected info', 'obj name':'get_turk_rejected_extra_info_file_name'},
             {'get_list':get_turk_accepted_image_list, 'old path':TURK_ACCEPTED_IMAGES_PATH, 'path':ACCEPTED_IMAGES_PATH,
              'name':'accepted images', 'obj name':'get_turk_accepted_image_list'},
             {'get_list':get_turk_accepted_stroke_list, 'old path':TURK_ACCEPTED_STROKES_PATH, 'path':ACCEPTED_STROKES_PATH,
              'name':'accepted strokes', 'obj name':'get_turk_accepted_stroke_list'},
             {'get_list':get_turk_accepted_extra_info_file_name, 'old path':TURK_ACCEPTED_EXTRA_INFO_PATH, 'path':ACCEPTED_EXTRA_INFO_PATH,
              'name':'accepted info', 'obj name':'get_turk_accepted_extra_info_file_name'}]

if MOVE_ALL:
    dict_list += [{'get_list':get_turk_image_list, 'old path':TURK_IMAGES_PATH, 'path':EXTRA_IMAGES_PATH,
                   'name':'extra images', 'obj name':'get_turk_image_list'},
                  {'get_list':get_turk_stroke_list, 'old path':TURK_STROKES_PATH, 'path':EXTRA_STROKES_PATH,
                   'name':'extra strokes', 'obj name':'get_turk_stroke_list'},
                  {'get_list':get_turk_extra_info_file_name, 'old path':TURK_EXTRA_INFO_PATH, 'path':EXTRA_EXTRA_INFO_PATH,
                   'name':'extra info', 'obj name':'get_turk_extra_info_file_name'}]

for cur_dict in dict_list:
    cur_list = cur_dict['get_list'](from_path=os.getcwd())
    cur_path = cur_dict['path']
    raise_object_changed(cur_dict['get_list'])
    raise_object_changed(cur_dict['path'])
    for alphabet_id in cur_list:
        for id_ in cur_list[alphabet_id]:
            if isinstance(cur_list[alphabet_id][id_], str):
                old = os.path.abspath(cur_list[alphabet_id][id_])
                new = old.lower().replace(cur_dict['old path'].lower(), cur_dict['path'])
                print('Moving %s to %s...' % (os.path.relpath(old), os.path.relpath(new)))
                if not os.path.exists(os.path.split(new)[0]):
                    os.makedirs(os.path.split(new)[0])
                os.rename(old, new)
            else:
                for file_name in cur_list[alphabet_id][id_]:
                    old = os.path.abspath(file_name)
                    new = old.lower().replace(cur_dict['old path'].lower(), cur_dict['path'])
                    print('Moving %s to %s...' % (os.path.relpath(old), os.path.relpath(new)))
                    if not os.path.exists(os.path.split(new)[0]):
                        os.makedirs(os.path.split(new)[0])
                    os.rename(old, new)



