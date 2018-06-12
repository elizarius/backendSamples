#!/usr/bin/python

#  def output_fun( low, up ,diff):
#  print "" 
#  print "Celcius   Fahrenheit"
#  for C in range (low ,up, diff):
#  print "%+-10d %+-10d" % (C,1.8*C+32) 


import sys
import traceback 

def input_integers():
  int_list = [] 
  print "Enter integer value or -1 to exit  ?"
 
  try :    

   while True: 
    inp_value   = input("")
    if inp_value is -1:
      break 
    else:
     int_list.append(inp_value)

  except Exception :
    print "Something wrong with input "
    exc_type , exc_value , exc_traceback =sys.exc_info()
  #  traceback.print_tb(exc_traceback)
    traceback.print_exception(exc_type, exc_value, exc_traceback)
    return int_list
   

  return int_list 


def get_list_size(input_list ):
 ctr = 0 ;
 for c in input_list:
  ctr = ctr+1   
 return ctr 


def get_list_average(input_list ):

 lsize = get_list_size(input_list)
 try : 
   return get_list_sum(input_list) / get_list_size(input_list)

 
 except ZeroDivisionError :
   print "division by 0!!!! "
   return 0    
 
 except Exception , e :
   print "General exception "
  
 else : 
  print "Something very wrong"
 

 
def get_list_sum(input_list ):
 sm_elem = 0 ;
 for c in input_list:
   sm_elem = sm_elem + c  
 return sm_elem

def init():
 print "IO.py init function called "

init()


