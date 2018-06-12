# -*- coding: utf-8 -*-

import pickle

try:
    myfile = open("./data/words", "rb")
    vocabulary = pickle.load(myfile)
except IOError:
    print "File handling error"
myfile.close()

print vocabulary

while True:
    word = raw_input("Word in English ")
    try:
        ref = vocabulary[word]
    except KeyError:
        print "The word", word, "not found"
    else:
        print ref
