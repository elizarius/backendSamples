#!/usr/bin/env python
#https://docs.python.org/3/tutorial/datastructures.html


# Immutable types: stings, bytes, tuples
# Mutable types: lists, bytearrays


#   1. Str type
x =23.4556
zz= str(x) + ' contact DEMO'
print('* String type:', zz)

# repetition
print('x'*40)


#   2. Bytes type
bytes_string = b'Bytes type example'
print('\n**', bytes_string)
print('** Bytes decoded bs: ', bytes_string.decode())
print('** Bytes decoded - encoded  bs: ', bytes_string.decode().encode())


#   3. Byte array type plays as strings but represents byte as each member
ints_array = bytearray((87, 114, 97, 100, 101))
print('\n*** Byte array {}'.format(ints_array))
ints_array.append(86)
print(ints_array)
ints_array.extend((85, 84, 83))
print(ints_array)
ints_array.pop()
ints_array.pop()
print(ints_array)
ints_array.pop(3)
print(ints_array)


#   4. List type: mutable / changeable
print ('\n----------   LIST -------------')
list_1 = list('create list by constructor')
print('**** List by constructor: ', list_1)

fruits = ['1orange', 'apple', 'pear', 'banana', 'kiwi', 'apple']

print('**** List by assignment: ', fruits)
print('**** List sorted : ', sorted(fruits))
fruits.sort()
print('**** List sort() : ', fruits)
print('**** List min value : ', min(fruits))
print('**** List max value : ', max(fruits))
print('**** List operations with one,range, index:\n'
    ' append,\n pop,\n extend,\n insert(ind, value),\n remove(value),\n'
    ' clear,\n sorted,\n reversed,\n count,\n index')


#   5. Tuple type: immutable / constant elements: no add, delete etc
print ('\n----------   TUPLE 1 -------------')
fruits = ('orange', 'apple', 'pear', 'banana', 'kiwi', 'apple', 'banana')
print('***** Tuple by assignment: ', fruits)

# T2, just another initialization of tuple
print ('\n----------   TUPLE 2 -------------')
tup = 12345, 54321, 'hello!'
print (tup)


print ('\n----------   SET --------------')
basket = {'apple', 'orange', 'apple', 'pear', 'orange', 'banana'}
print (basket)

print ('\n----------   DICTIONARY --------------')
dict = {'sape': 4139, 'guido': 127, 'jack': 4098}
print (dict)


# 6. Map example , apply function to each element of iterable object
#   Note: mapping , same result can be reached as comprehensions
fruits = ['1orange', 'apple', 'pear', 'banana', 'kiwi', 'apple']
fr1 = map(len, fruits)
print ('\n map of fruits returns object: {}'.format(fr1))
print ('\n map of fruits returns set: {}'.format(set(fr1)))
print ('\n map of fruits returns tuple: {}'.format(tuple(fr1))) # !!!! only set is working in python3

 
# Filter funtion is similar to map
print('Filter example: {}'.format(list(map(lambda val: len(val), fruits))))


