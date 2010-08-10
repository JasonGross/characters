#!/usr/bin/python

# build-public-dataset.py -- Compresses the appropriate images into .tar.gz and .zip formats.

from __future__ import with_statement

import os, re, sys, datetime
from alphabetspaths import *

def log(log_string):
    with open(os.path.join(RESULTS_PATH, 'dataset.log'), 'a') as f:
        f.write(log_string + '\n')

def make_public_dataset():
    print('Making public dataset archive...')
    old_dir = os.getcwd()
    try:
        os.chdir(RESULTS_PATH)
    except OSError:
        print('I am in %s, and I am having trouble finiding the results directory, "%s".' % (os.getcwd(), RESULTS_FOLDER))
        raise
    log(datetime.datetime.now().isoformat())
    for cmd in (#'tar -zcvf dataset.tar.gz ' + ' '.join(PUBLIC_DATASET_PATHS) + ' > dataset.tar.gz.log',
                #'zip -rq dataset.zip ' + ' '.join(PUBLIC_DATASET_PATHS),
                'tar -jcvf dataset.tar.bz2 ' + ' '.join(PUBLIC_DATASET_PATHS) + ' > dataset.tar.bz2.log',
                ):
        print(cmd)
        os.system(cmd)
    os.chdir(old_dir)

def make_public_beta_dataset():
    print('Making public dataset archive...')
    old_dir = os.getcwd()
    os.chdir(RESULTS_PATH)
    log(datetime.datetime.now().isoformat())
    log('Beta')
    for cmd in (#'tar -zcvf dataset-beta.tar.gz ' + ' '.join(PUBLIC_DATASET_BETA_PATHS) + ' > dataset-beta.tar.gz.log',
                #'zip -rq dataset-beta.zip ' + ' '.join(PUBLIC_DATASET_BETA_PATHS),
                'tar -jcvf dataset-beta.tar.bz2 ' + ' '.join(PUBLIC_DATASET_BETA_PATHS) + ' > dataset-beta.tar.bz2.log',
                ):
        print(cmd)
        os.system(cmd)
    os.chdir(old_dir)

def main():
    make_public_dataset()
    make_public_beta_dataset()
    return 0

if __name__ == '__main__':
    sys.exit(main())
