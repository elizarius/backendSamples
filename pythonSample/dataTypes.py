#!/usr/bin/env python
#https://docs.python.org/3/tutorial/datastructures.html


aelz  = None

if aelz:
    print ("aelz exist")
else:
    print ("aelz does not exist")


print ('----------   LIST -------------')
fruits = ['orange', 'apple', 'pear', 'banana', 'kiwi', 'apple', 'banana']
print (fruits)


print ('----------   TUPLE 1 -------------')
fruits = ('orange', 'apple', 'pear', 'banana', 'kiwi', 'apple', 'banana')
print (fruits)


print ('deleted orange, banana')
## delete operation is not supported  for tuples
#del fruits[0]
#del fruits[5]

print (' ')
print ('----------   TUPLE 2 -------------')
tup = 12345, 54321, 'hello!'
print (tup)

print (' ')
print ('----------   SET --------------')
basket = {'apple', 'orange', 'apple', 'pear', 'orange', 'banana'}
print (basket)

print (' ')
print ('----------   DICTIONARY --------------')
#
dict = {'sape': 4139, 'guido': 127, 'jack': 4098}
print (dict)
