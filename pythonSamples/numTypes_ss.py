#!/usr/bin/env python
#https://docs.python.org/3/tutorial/datastructures.html

#   1.  None keyword
aelz  = None
if aelz:
    print ("aelz exist")
else:
    print ("aelz does not exist")


#   2.  Int type operations

print('\n')
x = 5
print('x = {}, type = {}'.format(x, type(x)))

y = 0xA
print('y = {}, type = {}'.format(hex(y), type(y)))

z = x/y
print('Division x/y = {}, type = {}'.format((z), type(z)))

# whole division
z = x//y
print('Division x//y = {}, type = {}'.format((z), type(z)))


z = x%y
print('Rest x%y = {}, type = {}'.format((z), type(z)))

z = x<<1
print('Left shift  x<<1 = {}, type = {}'.format((z), type(z)))

z = ~x
print('Inversion  (-n-1) ~x = {}, type = {}'.format((z), type(z)))


#   2.  Float type
x = 1.5
print('\b x = {}, type = {}'.format(x, type(x)))

zz= x.as_integer_ratio()
print('zz  as integer ratio 3/2=1.5:  {}'.format(zz))

# Bitwise operators cannot be used for float types
