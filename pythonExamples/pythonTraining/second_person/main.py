#!/usr/bin/python

import time
from  person  import *


print "Person class "
p=Person("Anssi",30, "Purotie 8")
p.printInfo()

print ""
print "Changing age 30 --> 18, wait little bit "
p.setAge(18)
time.sleep(2)

print ""
print p.getName(), " is younger now , his age is : " , p.getAge()



print ""
e=Employee("Pekka", "Manager")
e.setSalary(10000)
e.printInfo()
print ""
