#!/usr/bin/env python
import os
import shutil


hash_file ="/home/ealexel/samples/pythonExample/gitversion"
s_file ="/home/ealexel/samples/pythonExample/save_gitversion"

with open(hash_file,'r') as f:
    key = f.read()
    print (key)
shutil.copyfile (hash_file, s_file)
os.remove(hash_file)
