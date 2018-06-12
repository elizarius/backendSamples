#!/usr/bin/python
import math

def callc_hypo ( c1, c2):
 hypo = math.sqrt(math.pow(c1,2)+math.pow(c2,2))
 print "Hyphotenuse value = ", hypo


def input_fun():
 print "Enter Cathetuses in format  [x y ]?"
 x = input("Cathetus X  ")
 y = input("Cathetus Y  ")
 return x,y 

def init():
 print "IO.py init function called "

init()


