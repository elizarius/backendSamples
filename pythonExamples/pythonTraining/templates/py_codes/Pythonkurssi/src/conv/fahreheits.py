#! /usr/bin/python
# -*- coding: iso-8859-1 -*-

# fahrenheits.py
# Module printing Fahrenheits within a range
# Copyright Tieturi Oy 2010

def init():
    print "Initialializer of fahrenheits module"

def print_fahrenheits(range_start, range_end, step = 10):
    for celsius in range(range_start, range_end + 10, step):
        print '%+-10d%+10.2f' % (celsius,  (1.8*celsius + 32))
        
init()