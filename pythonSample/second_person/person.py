#!/usr/bin/python

class Person:
      name = ""
      age = 0 
      address = "TUSULA"
      
      def __init__(self, aName ,aAge , aAddress):
         self.name = aName 
         self.age = aAge 
         self.address = aAddress

      def printInfo(self):
        print "Name   :" , self.name 
        print "Age    :" , self.age
        print "Address:",  self.address  
   

      def setAge(self, aAge):
       if aAge < 0 :
          self.age = 0 
       else : 
          self.age = aAge 


      def getAge(self):
       return self.age  

      def getName(self):
       return self.name



class Employee(Person):
      title   = ""
      salary  = 0 
      bus_phone = ""
      
      def __init__(self, aName , aTitle ):
         self.name = aName 
         self.title = aTitle

      def printInfo(self):
        Person.printInfo(self)
        print "title    :" , self.title
        print "Salary   :",  self.salary  
        print "Phone    :",  self.bus_phone

      def setSalary(self, aSal):
       if aSal < 0 :
          self.salary = 0 
       else : 
          self.salary = aSal 


      def getSalary(self):
       return self.salary  











 







 
