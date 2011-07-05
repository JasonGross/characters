#!/usr/bin/python
# recordsimilaritysubmission.py -- Stores the data from the  submission
from alphabetspaths import *
import turkutil

def record_submission(form_dict, path=SIMILARITY_UNREVIEWED_PATH, **kwargs):
    desc =  'GIVEN %%(task-%(task)d-anchor-image-0-alphabet)s, %%(task-%(task)d-anchor-image-0-character-number)s, %%(task-%(task)d-anchor-image-0-id)s, ' + \
            'CHOSE %%%%(task-%(task)d-class-%%(task-%(task)d-chosen-class)s-image-0-alphabet)s, %%%%(task-%(task)d-class-%%(task-%(task)d-chosen-class)s-image-0-character-number)s, %%%%(task-%(task)d-class-%%(task-%(task)d-chosen-class)s-image-0-id)s'
    task_desc = '%%(task-%(task)d-image-0-alphabet)s, %%(task-%(task)d-image-0-character-number)s, %%(task-%(task)d-image-0-id)s, ' + \
                '%%(task-%(task)d-image-1-alphabet)s, %%(task-%(task)d-image-1-character-number)s, %%(task-%(task)d-image-1-id)s, ' + \
                '%%(task-%(task)d-answer)s'
    make_summary = turkutil.make_default_make_summary(task_desc, count_correct=False)
    turkutil.record_submission(form_dict, path=path, make_summary=make_summary, **kwargs)
