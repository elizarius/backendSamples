#!/usr/bin/python

#  def output_fun( low, up ,diff):
#  print "" 
#  print "Celcius   Fahrenheit"
#  for C in range (low ,up, diff):
#  print "%+-10d %+-10d" % (C,1.8*C+32) 


def input_integers():
  int_list = [] 
  print "Enter integer value or -1 to exit  ?"
    
  while True: 
   inp_value   = input("")
   if inp_value is -1:
     break 
   else:
     int_list.append(inp_value)

  return int_list 


def get_list_size(input_list ):
 ctr = 0 ;
 for c in input_list:
  ctr = ctr+1   
 return ctr 


def get_list_average(input_list ):

 lsize = get_list_size(input_list)
 if lsize is not 0:  
   return get_list_sum(input_list) / get_list_size(input_list) 
 else: 
   return 0 

def get_list_sum(input_list ):
 sm_elem = 0 ;
 for c in input_list:
   sm_elem = sm_elem + c  
 return sm_elem

def init():
 print "IO.py init function called "

init()


