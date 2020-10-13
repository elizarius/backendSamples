#!/usr/bin/env python
#https://docs.python.org/3/tutorial/datastructures.html

#   Mapping types: range, set, dictionary

#   1. Range type
a_range = range(3)
b_range = range(5,-1,-1)


print('* Range type: ', a_range)
print('* Range to list: ', list(a_range))

for i in a_range:
    print(i)
print('*'*10)

print('* Range with interval: ', list(range(4,12)))
print('* Range with negative ind: ', list(range(5,-1,-1)))

#   2. Set type unique mapping of mutable elements
#      frozenset is immutable set (no update operation )
print('\n----------   SET --------------')
basket = {'apple', 'orange', 'apple', 'banana', 'orange', 'banana', 'pear'}
print('* Set type: ', basket)
set_n = {1,6,10}
combined = basket.union(set_n)
print('** Union  Set: ', combined)
print'** Union  Set combined: ', sorted(combined)
print('** Set operations:\n'
    ' |,\n inrersection,\n simmetric_intersection,\n difference....\n')

# set_b  = set_a            reference
# set_b  = set_a.copy()     reference


#   3. Dictionaly type
print ('\n----------   DICTIONARY --------------')
dict = {'sape': 4139, 'guido': 127, 'jack': 4098}
print ('*** Dictionary type: {}'.format(dict))
print ('*** Dic keys: {}'.format(dict.keys()))
print ('*** Dic values: {}'.format(dict.values()))
print ('*** Dic items: {}'.format(dict.items()))

# zip is used to pack key / value f.i to creat new dictionary new dictionary 


