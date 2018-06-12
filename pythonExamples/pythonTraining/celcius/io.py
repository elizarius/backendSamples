#!/usr/bin/python

def output_fun( low, up ,diff):
 print "" 
 print "Celcius   Fahrenheit"
 for C in range (low ,up, diff):
  print "%+-10d %+-10d" % (C,1.8*C+32) 


def input_fun():
 print "Type : enter degree in Celcius in format [lower upper range ]?"
 lower = input("Lower value  ")
 upper = input("Upper value  ")
 delta = input("Range ")
 return lower, upper , delta 

def init():
 print "IO.py init function called "

init()


