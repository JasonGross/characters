#!/usr/bin/python
# record-submission.py -- Stores the data from the submission
from __future__ import with_statement
import cgi, cgitb
cgitb.enable(format="html")
from recordsubmission import record_submission

if __name__ == '__main__':
    form = cgi.FieldStorage()
    #print("Content-Type: text/plain")
    print("Content-type: text/html")    # HTML is following
    print                               # blank line, end of headers
    print('Converting form to dict...')
    form_dict = dict((key, form.getvalue(key)) for key in form.keys())
    print('Done<br>')
    record_submission(form_dict, many_dirs=True)
##    print(BASE_PATH)
##    for key in sorted(form.keys()):
##        print('%s: %s<br>' % (key, cgi.escape(form.getvalue(key)[:50])))



