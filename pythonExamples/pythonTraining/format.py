#!/usr/bin/python

print "Type : enter degree in Celcius : ?"
C =input(" ")
F = 1.8*C+32
print "Celcius Fahrenheit"
print "%+-10d  %+-10d" % (C,F)
print "---------"
print ""


for C in range (-100, 110, 10):
 print "%+-10d %+-10d" % (C,1.8*C+32)


