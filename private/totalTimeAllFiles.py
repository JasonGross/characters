#!/usr/bin/python
from TimeWorked import *
import os
files = [i for i in os.listdir(os.getcwd()) if 'Time Worked' in i]
print get_total_time_files(files)
raw_input()
