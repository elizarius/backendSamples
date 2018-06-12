#!/usr/bin/env python
import subprocess
import os

tmp_path = '/home/ealexel/samples/pythonExample'
src_pattern = 'ex1'
files = os.listdir(tmp_path)
print "Unsorted files: {} ".format(files)

print "**********************************"
print " "
files = sorted(os.listdir(tmp_path))
print "Sorted files: {} ".format(files)
