#!/usr/bin/python
from __future__ import with_statement
from datetime import *
from time import *
import re
import os

SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))
TIME_WORKED = os.path.join(SCRIPT_PATH, 'Time Worked.txt')

def write_begin_time():
    try:
        with open(TIME_WORKED, 'r') as f:
            lines = f.readlines()
    except Exception:
        with open(TIME_WORKED, 'w') as f:
            lines = []
    fmt = '\n'.join(['%' + i for i in 'aAbBcdHIjmMpSUwWxXyYZ%'])
    with open(TIME_WORKED, 'a') as f:
        f.write('Start: ' + datetime.now().strftime('%A, %B %d, %Y %H:%M.%S') + '\n')

def write_end_time():
    with open(TIME_WORKED, 'r') as f:
        lines = f.readlines()
    if not lines[-1].strip(): lines = lines[:-1]
    print(lines[-1][len('Start: '):].strip())
    start = datetime.strptime(lines[-1][len('Start: '):].strip(), '%A, %B %d, %Y %H:%M.%S')
    with open(TIME_WORKED, 'a') as f:
        f.write('End: ' + datetime.now().strftime('%A, %B %d, %Y %H:%M.%S') + '\n')
        f.write('Time Spent: ' + str(datetime.now() - start) + '\n\n')
    print('End: ' + datetime.now().strftime('%A, %B %d, %Y %H:%M.%S'))
    print('Time Spent: ' + str(datetime.now() - start))

def get_total_time(begin=None, end=None):
    return get_total_timef(TIME_WORKED, begin, end)

def get_total_timef(file_name=None, begin=None, end=None):
    with open(file_name, 'r') as f:
        lines = f.readlines()
    lines2 = []
    for i in range(len(lines)):
        if lines[i][:len('Time Spent: ')] == 'Time Spent: ':
            lines2.append([datetime.strptime(lines[i - 2][len('Start: '):].strip(), '%A, %B %d, %Y %H:%M.%S'),
                           datetime.strptime(lines[i - 1][len('End: '):].strip(), '%A, %B %d, %Y %H:%M.%S'),
                           lines[i][len('Time Spent: '):].strip()])
    for i in lines2:
        if 'day' in i[-1]:
            if '.' in i[-1]:
                i[-1] = [int(j) for j in i[-1].replace('days', 'day').replace(' day, ',':').replace('.',':').split(':')]
                i[-1] = timedelta(i[-1][0], i[-1][3] + 60 * (i[-1][2] + 60 * i[-1][1]), i[-1][4])
            else:
                i[-1] = [int(j) for j in i[-1].replace('days', 'day').replace(' day, ',':').replace('.',':').split(':')]
                i[-1] = timedelta(i[-1][0], i[-1][3] + 60 * (i[-1][2] + 60 * i[-1][1]), 0)
        else:
            if '.' in i[-1]:
                i[-1] = [int(j) for j in i[-1].replace('days', 'day').replace(' day, ',':').replace('.',':').split(':')]
                i[-1] = timedelta(0, i[-1][2] + 60 * (i[-1][1] + 60 * i[-1][0]), i[-1][3])
            else:
                i[-1] = [int(j) for j in i[-1].replace('days', 'day').replace(' day, ',':').replace('.',':').split(':')]
                i[-1] = timedelta(0, i[-1][2] + 60 * (i[-1][1] + 60 * i[-1][0]), 0)
    total = timedelta(0)
    for i in lines2:
        if begin == None or i[0] >= begin:
            if end == None or i[1] <= end:
                total += i[-1]
            else:
                total += end - i[0]
        else:
            if end == None or i[1] <= end:
                total += begin - i[end]
    return total
def get_total_time_files(file_list, begin=None, end=None):
    rtn = get_total_timef(file_list[0], begin, end)
    for i in file_list[1:]:
        rtn += get_total_timef(i, begin, end)
    return rtn

def split_time():
    total = get_total_time()
    with open(TIME_WORKED, 'r') as f:
        lines = f.readlines()
    lines2 = []
    for i in range(len(lines)):
        if lines[i][:len('Time Spent: ')] == 'Time Spent: ':
            lines2.append([datetime.strptime(lines[i - 2][len('Start: '):].strip(), '%A, %B %d, %Y %H:%M.%S'), datetime.strptime(lines[i - 1][len('End: '):].strip(), '%A, %B %d, %Y %H:%M.%S'), lines[i][len('Time Spent: '):].strip()])
    for i in lines2:
        if 'day' in i[-1]:
            if '.' in i[-1]:
                i[-1] = [int(j) for j in i[-1].replace('days', 'day').replace(' day, ',':').replace('.',':').split(':')]
                i[-1] = timedelta(i[-1][0], i[-1][3] + 60 * (i[-1][2] + 60 * i[-1][1]), i[-1][4])
            else:
                i[-1] = [int(j) for j in i[-1].replace('days', 'day').replace(' day, ',':').replace('.',':').split(':')]
                i[-1] = timedelta(i[-1][0], i[-1][3] + 60 * (i[-1][2] + 60 * i[-1][1]), 0)
        else:
            if '.' in i[-1]:
                i[-1] = [int(j) for j in i[-1].replace('days', 'day').replace(' day, ',':').replace('.',':').split(':')]
                i[-1] = timedelta(0, i[-1][2] + 60 * (i[-1][1] + 60 * i[-1][0]), i[-1][3])
            else:
                i[-1] = [int(j) for j in i[-1].replace('days', 'day').replace(' day, ',':').replace('.',':').split(':')]
                i[-1] = timedelta(0, i[-1][2] + 60 * (i[-1][1] + 60 * i[-1][0]), 0)
    begin = lines2[0][0]
    end = lines2[-1][1]
    with open(os.path.join(SCRIPT_PATH, 'Time Worked (From ' + begin.strftime('%Y-%m-%d (%b)') + ' to ' + end.strftime('%Y-%m-%d (%b)') + ').txt'), 'w') as f:
        for i in lines:
            f.write(i)
        f.write('\nTotal Time: ' + str(total))
    with open(TIME_WORKED, 'w') as f:
        f.write('')
