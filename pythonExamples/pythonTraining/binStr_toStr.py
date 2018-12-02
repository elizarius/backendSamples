#!/usr/bin/env python
import hashlib


## sample , AELZ_01 using hashes library 

hash_object = hashlib.sha256(b'Hello World')
hex_dig = hash_object.hexdigest()
print(hash_object.digest())
#print(hash_object.digest().decode('utf-8'))


