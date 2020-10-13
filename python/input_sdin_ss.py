#!/usr/bin/env python3

# input form command line stdin example, raw_input() for python2 only 
# example multiple same symbols print
print('*'*10)
 
print ("How old are you?")
age = input()
print ("How tall are you?")
height = input()
print ("How much do you weigh?")
weight = input()

print ("So, you're {} old, {} tall and {} heavy.".format(age, height, weight))

print ("\n************** COMPACT VERSION *******")
age = input("How old are you? ")
height = input("How tall are you? ")
weight = input("How much do you weigh? ")

print ("SSSO, you're {} old, {} tall and {} heavy.".format(age, height, weight))