#!/usr/bin/python

print "What is your names , 0 to end  ?"

zz=True
while zz: 
  name =raw_input(" ")
  if name == "0":
   zz=False
   break 
  else: 
   for c in name:
     print c
  print "-----"
  print "Type name again"
