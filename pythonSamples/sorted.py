#!/usr/bin/env python3
import subprocess
import os

tmp_path = '/home/aelz/repa/backendSamples/python'
files = os.listdir(tmp_path)
print('Unsorted files: {}'.format(files))

print('**********************************\n')
files = sorted(os.listdir(tmp_path))
print('Sorted files: {}'.format(files))
