#!/usr/bin/env python
import json


#Short roles description
TENANT_ROLES_DESCRIPTION = {
    'Assetadmin':       'Manage assets in ESM',
    'Policyadmin':      'Manage and execute policies and security controls',
    'Securityoperator': 'Execute daily operational activities',
    'Sysadmin':         'Manage users, roles and privileges',
    'Threatanalyst':    'Manage and execute basic analytics activities',
    'Superuser':        'Complete ESM access for deployment and emergency'
}



print '----------   DICT  -------------'
print  TENANT_ROLES_DESCRIPTION 
print ''
print '-------------------------------'
data = json.dumps(TENANT_ROLES_DESCRIPTION )
print  data


#print ''
#print '-------------------------------'
#data = json.loads(TENANT_ROLES_DESCRIPTION )
#print  data
