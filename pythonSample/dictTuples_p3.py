#!/usr/bin/env python
import json


#Tuple of dictionaries example


# Short roles description
ROLES = (
    {'advancedanalyst':
        {'Advanced analyst':
            'Manage and execute advanced analytics activities'}},
    {'assetadmin':
        {'Asset administrator': 'Manage assets in ESM'}},
    {'policyadmin':
        {'Policy administrator':
            'Manage and execute policies and security controls'}},
    {'securityadmin':
        {'Security administrator': 'Manage logging events in ESM'}},
    {'securityoperator':
        {'Security operator': 'Execute daily operational activities'}},
    {'sysadmin':
        {'System administrator': 'Manage users, roles and privileges'}},
    {'threatanalyst':
        {'Threat analyst': 'Manage and execute basic analytics activities'}},
    {'superuser':
        {'Super user': 'Complete ESM access for deployment and emergency'}}
)

data = []
for role in ROLES:
    print (role)
    for a,b in role.items():
        print('id : %s ' % a)
        print('Name : %s ' % b)
        for c, d in b.items():
            print (c)
            print (d)
            data.append ({'id': a, 'name': c, 'description':d})

        #print('listed name: %s ' % list(b))
        #print('description: %s ' % list(b)[1])

    print ('******************')
print (data)

#[
#    {"id": "foo", "name": "Foo", "description": "..."},
#...
#]

