#!/usr/bin/python
# convert-recognition-rt-turk-file-to-folders.py -- Converts the results of a turk submission to folders.
from alphabetspaths import *
from turkconverter import main
from recordrecognitionrtsubmission import record_submission

if __name__ == '__main__':
    main(task_name='recognition-rt', unreviewed_path=RECOGNITION_RT_UNREVIEWED_PATH, record_submission=record_submission)
