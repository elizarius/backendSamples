#!/usr/bin/env python
import os


def my_function(arg1, arg2, **kwargs):
    print "Arg1: {}".format(arg1) 
    print "Arg2: {}".format(arg2) 



my_function ('one', 'two')
my_function (arg2='one', arg1='two')

