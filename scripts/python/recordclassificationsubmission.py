#!/usr/bin/python
# recordclassificationsubmission.py -- Stores the data from the classification submission
from alphabetspaths import *
import turkutil


def record_submission(form_dict, path=CLASSIFICATION_UNREVIEWED_PATH, **kwargs):
    desc =  'GIVEN %%(task-%(task)d-anchor-image-0-alphabet)s, %%(task-%(task)d-anchor-image-0-character-number)s, %%(task-%(task)d-anchor-image-0-id)s, ' + \
            'CHOSE %%%%(task-%(task)d-class-%%(task-%(task)d-chosen-class)s-image-0-alphabet)s, %%%%(task-%(task)d-class-%%(task-%(task)d-chosen-class)s-image-0-character-number)s, %%%%(task-%(task)d-class-%%(task-%(task)d-chosen-class)s-image-0-id)s'
    make_summary = turkutil.make_default_make_summary(desc, start_time_postfix='-time-of-show-classes')
    turkutil.record_submission(form_dict, path=path, make_summary=make_summary, **kwargs)
