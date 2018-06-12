#!/usr/bin/env python

def average(arr):
    sum = 0
    count = 0
    for value, number in arr.iteritems():
        sum += value * number
        count += number
    return sum / float(count)

def distribution(arr):
    for value, number in arr.iteritems():
        print "%6i: %-i" %(value, number)

# main()
arr = dict()
print "Give numbers, -1 quits"
while True:
    value = input("Luku: ")
    if value == -1:
        break        
    if value in arr:
        arr[value] = arr[value] + 1
    else:
        arr[value] = 1

print "\n================================\n"

print "Average: ", average(arr)
print "Distribution of values:"
distribution(arr)


