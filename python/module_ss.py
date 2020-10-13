#!/usr/bin/env python3


# Module names example

print('Module name {}'.format(__name__))
print (dir())

import math
print (dir())
del math

import math as mat
print (dir())
del mat

from math import pi
print (dir())
print ('PI value: {}'.format(pi))
del pi 
print (dir())
# 
# must call undefined
# print ('PI value: {}'.format(pi))

# not recommended due to space pollution
from math import *
print (dir())

