#!/usr/bin/python
# record-recognition-submission.py -- Stores the data from the recognition task submission
from __future__ import with_statement
import cgi, cgitb
cgitb.enable(format="html")
from recordrecognitionsubmission import record_submission

if __name__ == '__main__':
    form = cgi.FieldStorage(keep_blank_values=False)
    print("Content-type: text/html")    # HTML is following
    print                               # blank line, end of headers
    print('Converting form to dict...')
    form_dict = dict((key, form.getvalue(key)) for key in form.keys())
    print('Done<br>')
    record_submission(form_dict, many_dirs=True)



