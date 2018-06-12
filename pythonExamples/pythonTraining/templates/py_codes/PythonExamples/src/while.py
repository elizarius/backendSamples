condition = True
values = list()
while condition:
   print "Give number"
   i = input()
   if i == 1 :
      condition = False
   else :
      values.append(i)
else:
    print "Else branch selected"

print values

