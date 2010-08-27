#!/usr/bin/python
import os
from alphabetspaths import *
if __name__ == '__main__':
    print('RewriteEngine on')
    for alphabet in sorted(os.listdir(ACCEPTED_IMAGES_PATH)):
        first, second, third, fourth = (alphabet + 'a')[:4]
        print('RewriteRule ^results/accepted-images/(..)%(first)s(..)%(second)s(..)%(third)s(..)%(fourth)s([0-9][0-9])([^\.]+)\.png /~jgross/alphabets/results/accepted-images/%(alphabet)s/%(alphabet)s_$5_$1$2$3$4$6.png' % locals())

