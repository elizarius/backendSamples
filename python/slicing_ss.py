#!/usr/bin/env python3
#https://docs.python.org/3/tutorial/datastructures.html

print ('\n----------   LIST -------------')
fruits = ['1orange', 'apple', 'pear', 'banana', 'kiwi', 'apple']
print('**** Orig list: ', fruits)
print('**** Access by negative index[-2] from end: ', fruits[-2])
print('**** Subslicing [0:2]: ', fruits[0:2])
print('**** Subslicing [:2]: ', fruits[:2])
print('**** Subslicing until end[2:]: ', fruits[2:])
print('**** Subslicing by step [::2] --> 1,3,5: ', fruits[::2])

# Create a reference 
fruits_ref = fruits
print('**** By reference [2:]: ', fruits_ref[2:])
fruits_copy = fruits[:]
fruits_copy.pop()
print('**** By copy  [2:]: ', fruits_copy[2:])
print('**** Subslicing orig [2:]: ', fruits[2:])
