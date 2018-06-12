#! /usr/bin/python

# exercise13.py
# file handling exercise
# Copyright Tieturi Oy 2010

def printList(name):
    print ""
    print name + "'s todo list:"
    try:
        with open(name+".todo", "r+") as input:
            print input.read()
    except IOError:
        print "You don't have a todo list yet!"
        
def askListItem():
    item = raw_input("What do you want to add to your to-do list? ")
    return item

def addToList(name, item):
    print 'Adding "' + item + '" to ' + name + "'s list"
    
    file = open (name+".todo", 'a')
    file.write(item+'\n')
    file.close()
    
username = raw_input("What is your name? ")
choice = 0

while (choice != 3):
    print "****************************"
    print "What do you want to do?"
    print "1. Print my to-do list"
    print "2. Add item to my to-do list"
    print "3. Exit"
    print "****************************"
    choice = input("1/2/3? ")

    if (choice == 1):
        printList(username)
    elif (choice == 2):
        listitem = askListItem()
        addToList(username, listitem)



