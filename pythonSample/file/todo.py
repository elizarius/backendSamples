#!/usr/bin/python


def printList(name):
    # This hasn't yet been implemented!
    print name
    # Read the file username.todo for the todo-list of the user!
    f=open(name+".todo" , "r")
    print f.read()
    f.close()
   
    

def askListItem():
    item = raw_input("What do you want to add to your to-do list? ")
    return item

def addToList(name, item):
    # This hasn't yet been implemented!
    print name
    print item
    # Append the item to the username.todo file!
    f=open(name+".todo", "a")
    f.write(item+"\n" )
    f.close()


    
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



