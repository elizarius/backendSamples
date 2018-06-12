#! /usr/bin/python
# namespace example
# Copyright Tieturi Oy 2010

x = 5
y = 2

def foo():
    x = 3

def bar():
    global y
    y = 3

foo()
bar()

print x, y
