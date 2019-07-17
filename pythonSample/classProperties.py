#!/usr/bin/python

# print all attributes of class

class Animal(object):
    def __init__(self):
        self.legs = 2
        self.name = 'Dog'
        self.color= 'Spotted'
        self.smell= 'Alot'
        self.age  = 10
        self.kids = 0

an = Animal()
attrs =vars(an)
print (attrs)



# Note: only works with  class and perhaps with dictionary ?

#zz1= {'a': 'b'}
#attrs1 = vars (zz1)
#print ('********************************')
#print (attrs1)

#zz = {'This is test  string '}
#attrs1 = vars (zz)
#print ('********************************')
#print (attrs)
