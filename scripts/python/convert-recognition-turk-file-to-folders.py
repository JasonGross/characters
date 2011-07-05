#!/usr/bin/python
# convert-recognition-turk-file-to-folders.py -- Converts the results of a turk submission to folders.
from __future__ import with_statement
from alphabetspaths import *
from turkconverter import main
from recordrecognitionsubmission import record_submission

if __name__ == '__main__':
    main(task_name='recognition', unreviewed_path=RECOGNITION_UNREVIEWED_PATH, record_submission=record_submission)
