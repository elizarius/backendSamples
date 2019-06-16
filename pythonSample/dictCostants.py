#!/usr/bin/env python
import json
import os


#Tuple of dictionaries example

#ESM_SYSADMIN_USER = os.getenv('ESM_SYSADMIN_USER')
#ESM_SYSADMIN_PASSWORD = os.getenv('ESM_SYSADMIN_PASSWORD')


ESM_SYSADMIN_USER = 'sasa'
ESM_SYSADMIN_PASSWORD = 'SASA'





print ('user:  {}'.format(ESM_SYSADMIN_USER))
print ('password :  {}'.format(ESM_SYSADMIN_PASSWORD))

data = {'user': ESM_SYSADMIN_USER, 'password': ESM_SYSADMIN_PASSWORD}

print ('{}'.format(data))


