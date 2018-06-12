# -*- coding: utf-8 -*-

import pickle

def query() :
    while True:  
        try:
            english = raw_input("Word in English: ")
            finnish = raw_input("Same word in Finnish: ")
        except:
            print "Come on! End with an epty line."
        else:
            break
    return english, finnish

def save(vocabulary) :
    try:
        myfile = open("./data/words", "wb")
        pickle.dump(vocabulary, myfile)
    except IOError:
        print "File handling error"
    myfile.close()

vocabulary = dict()

while True:
    english, finnish = query()
    if finnish == '' or english == '':
        break
    vocabulary[english] = finnish
save(vocabulary)

