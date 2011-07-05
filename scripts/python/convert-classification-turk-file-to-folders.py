#!/usr/bin/python
# convert-classification-turk-file-to-folders.py -- Converts the results of a turk submission to folders.
from alphabetspaths import *
from recordclassificationsubmission import record_submission
from turkconverter import main

if __name__ == '__main__':
    main(task_name='classification', unreviewed_path=CLASSIFICATION_UNREVIEWED_PATH, record_submission=record_submission)
