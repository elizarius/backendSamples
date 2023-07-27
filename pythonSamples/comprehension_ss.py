#!/usr/bin/env python

#   1. List comphehensions
#   Nested comprehensions, see training course for example
odds = [num for num in range(10) if num % 2]
print('Odds: {}'.format(odds))

#   2. zip usage
#   zip returns iterator as result , be careful
a = ("John", "Charles", "Mike")
b = ("Jenny", "Christy", "Monica")
print('Zip: {}'.format(zip(a, b)))
print('Zip to tuple: {}'.format(tuple(zip(a,b))))
print('Zip to list: {}'.format(list(zip(a,b))))
print('Zip to dict: {}'.format(dict(zip(a,b))))

# Unzip
k, v = zip(*(zip(a, b)))
print('Zip unzipped {} {}'.format(k,v))

# pprint formatted print of dictionaries, lists, matrixes etc
