#!/usr/bin/env python
#https://docs.python.org/3/tutorial/datastructures.html

import math
print (dir())

print('PI = {}'.format(math.pi))
print('E  = {}'.format(math.e))

del math
from math import *

print (dir())

import math
x = float('nan')
print('x= {} not an number = {}'.format(x, math.isnan(x)))

z  = 25
print('z= {} not an number = {}'.format(z, math.isnan(z)))

