#!/usr/bin/env python
import traceback


class MyException(Exception):
    def __init__(self, message=None, status_code=None):
        self.message=message
        self.status_code = status_code

  #  def __str__(self):
  #      print ('AELZ 000   IN __str__')
  #      return self.message


try:
    print ('AELZ 00 calling exception')
    raise MyException('aelz exception', status_code =300)

except MyException as e:
    print ("AELZ 1  IN exception: {}".format(e))
    print ("AELZ 2  IN exception: {}".format(str(e)))
    print ("AELZ 3 message: {}".format(e.message))
    if e.status_code:
        print ("AELZ 4 status_code: {}".format(e.status_code))

else:
    ### Reached  this branch if there are no any exceptions
    print ("Reached ELSE stmt ")

finally:
    ### Reached ALWAYS this branch
    print ("Reached FINAL stmt ")

