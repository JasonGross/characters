#!/usr/bin/python
# record-duplication-submission.py -- Stores the data from the duplication task submission
from __future__ import with_statement
import cgi, cgitb
import argparse
import os
cgitb.enable(format="html")
from recordduplicationsubmission import record_submission
from alphabetspaths import DUPLICATION_UNREVIEWED_PATH

DEFAULT_PATH = DUPLICATION_UNREVIEWED_PATH

parser = argparse.ArgumentParser(description='Stores data from the duplication task submission')
parser.add_argument('--path', type=str, default=DEFAULT_PATH,
                    help='What folder should should the tasks go in')

if __name__ == '__main__':
    args, argv = parser.parse_known_args()
    form = cgi.FieldStorage(keep_blank_values=False)
    print("Content-type: text/html")    # HTML is following
    print                               # blank line, end of headers
    print('Converting form to dict...')
    form_dict = dict((key, form.getvalue(key)) for key in form.keys())
    print('Done<br>')
    record_submission(form_dict, many_dirs=True, path=os.path.join(DEFAULT_PATH, args.path))



