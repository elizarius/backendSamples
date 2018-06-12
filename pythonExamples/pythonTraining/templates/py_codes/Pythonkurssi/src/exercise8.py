# -*- coding: utf-8 -*-

def query():
    return input("Give a number, -1 to finish: ")

l = list()

while True:
    value = query()
    if value == -1:
        break
    else:
        l.append(value)
print "Numbers: ", len(l)
print "Sum: ", sum(l)
print "Average: ", float(sum(l)) / len(l)