#!/usr/bin/env python
import os
import shutil
import subprocess

fl ='math_ss.py'

''' Read text file line by line'''
with open(fl) as text_file:
    for line in text_file:
        print(line)

''' Using read object '''
with open(fl) as text_file:
    zz = text_file.read()
    print(zz)

''' Using read lines --> lines into list '''
with open(fl) as text_file:
    zz =text_file.readlines()
    print(zz)


'''
Write file: w, a options
r read
rb, wb  binary files
'''
with open('aelz.txt', mode ='r' ) as text_file:
    print('\n\n {}'.format(text_file.read()))

