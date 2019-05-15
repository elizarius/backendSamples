#!/usr/bin/env python
import subprocess
import os

tmp_path = '/home/ealexel/samples/pythonExample'
src_pattern = 'ex1'
files = os.listdir(tmp_path)
f=open('aelz.txt','w')

for src_file in files:
    if src_pattern in src_file:
        with open(src_file,'r') as infile:
            f.write(infile.read())
