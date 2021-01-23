
# NOTE ****** break, continue, else  used to control flow: if statement and loos

print('\n 1***  While loop example')
counter=4
while counter > 0:
  print('counter: {}'.format(counter))
  counter -= 1

fruits = ['1orange', 'apple', 'pear', 'banana', 'kiwi', 'apple']
while fruits:
  zz =fruits.pop()
  print('removed: {}'.format(zz))
print('Empty list')


print('\n 2** For loop, iterating in list, print items in one line ')
fruits = ['1orange', 'apple', 'pear', 'banana', 'kiwi', 'apple']
for fruit in fruits:
  print (fruit, end=' ')

print('\nFruits type: {}'.format(type(fruits)))
print('Fruits  attributes: {}'.format(dir(fruits)))


print('\n\n  3***  Iterators')
print('Fruits  : {}'.format(fruits))
print('Fruits iterable ? : {}'.format(hasattr(fruits, '__iter__')))

myiter = iter(fruits)
print('Fruits iterator : {}'.format(myiter))
print('Fruits next : {}'.format(next(myiter)))
print('Fruits next : {}'.format(next(myiter)))


# 4. Enumerate function: for adding index of iterable object type.
# Might be used to avoid for loops
print('\n 4***  Enumerations')
cars = ['kia', 'audi', 'bmw']
for car in enumerate(cars):
  print(car)

for i, car in enumerate(cars):  # similar uasge as in dict.items()
  print(i, ' : ', car)

print(' '*3)
print(list(enumerate(cars)))


print('\n 5***  Iterating in dictionary')
dict = {'sape': 4139, 'guido': 127, 'jack': 4098}

for a,b in dict.items():
  print(a, ':' , b)

for key in dict.keys():
  print(key)

for val in dict.values():
  print(val)


print('\n 6***  break && else ')
fruits = ['1orange', 'apple', 'pear', 'banana', 'kiwi', 'apple']
for fruit in fruits:
  if  fruit == 'mango':
    print ('found')
    break # break the loop and not continue anymore
else:
  print ('Mango not found in loop')


print('\n 7***  continue usage')
fruits = ['1orange', 'apple', 'pear', 'banana', 'kiwi', 'apple']
for fruit in fruits:
  if  fruit != 'apple':
    continue
  print (fruit)

