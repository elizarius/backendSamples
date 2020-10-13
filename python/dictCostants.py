#!/usr/bin/env python
import json
import os

# dictionary of constants


ESM_SYSADMIN_USER = 'sasa'
ESM_SYSADMIN_PASSWORD = 'SASA'

print ('user:  {}'.format(ESM_SYSADMIN_USER))
print ('password :  {}'.format(ESM_SYSADMIN_PASSWORD))

data = {'user': ESM_SYSADMIN_USER, 'password': ESM_SYSADMIN_PASSWORD}

print ('{}'.format(data))


