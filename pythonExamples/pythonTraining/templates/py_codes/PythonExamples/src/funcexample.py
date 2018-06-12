#! /usr/bin/python
# return value example
# Copyright Tieturi Oy 2010


def sum(a,b):
    return a+b, "Python rules!", 75

print sum(12,3)
print sum("Kalle", "Ville")

e,f,g = sum(7,10)
print e
print f
print g

