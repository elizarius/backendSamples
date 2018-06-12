#!/usr/bin/python

import io

ints_list=io.input_integers()
print "List : Number of  elements :" ,  io.get_list_size(ints_list)
print "List : Average value       :" ,  io.get_list_average(ints_list)
print "List : Sum of elements     :" ,  io.get_list_sum (ints_list)


