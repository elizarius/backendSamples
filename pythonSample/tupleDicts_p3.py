#!/usr/bin/env python


#Tuple of dictionaries example

ROLES = (
    {'auvancedanalyst':
        {'Advanced analyst':
            'Manage and execute advanced analytics activities'}},
    {'assetadmin':
        {'Asset administrator': 'Manage assets in ESM'}}
)
#    {'securityadmin':
#        {'Security administrator': 'Manage logging events in ESM'}},
#    {'securityoperator':
#        {'Security operator': 'Execute daily operational activities'}},
#    {'sysadmin':
#        {'System administrator': 'Manage users, roles and privileges'}},
#    {'threatanalyst':
#        {'Threat analyst': 'Manage and execute basic analytics activities'}},
#    {'superuser':
#        {'Super user': 'Complete ESM access for deployment and emergency'}}


for role in ROLES:
    print (role)


print ('***************Print whole LIST\n')
print (ROLES)



print ('***************Append member\n')
pa = {'policyadmin':
        {'Policy administrator':'Manage and execute policies and security controls'}}

ROLES.append(pa)
print (ROLES)


