#!/usr/bin/python
import os
from alphabetspaths import *
if __name__ == '__main__':
    print('RewriteEngine on')
    for alphabet in sorted(os.listdir(ACCEPTED_IMAGES_PATH)):
        first, second, third = alphabet[:3]
        print('RewriteRule ^results/accepted-images/(..)%(first)s(..)%(second)s(..)%(third)s([0-9][0-9])([^\.]+)\.png /~jgross/alphabets/results/accepted-images/%(alphabet)s/%(alphabet)s_$4_$1$2$3$5.png' % locals())

