#!/usr/bin/env python

import json

#List of dictionaries example
#https://www.quackit.com/python/reference/python_3_list_methods.cfm


# Short roles description
ROLES = [
    {'advancedanalyst':
        {'Advanced analyst':
            'Manage and execute advanced analytics activities'}},
    {'assetadmin':
        {'Asset administrator': 'Manage assets in ESM'}}
]


ROLES = [
    {'advancedanalyst':
        {'Advanced analyst':
            'Manage and execute advanced analytics activities'}},
    {'assetadmin':
        {'Asset administrator': 'Manage assets in ESM'}}
]

R1 = {'aelz': ROLES}


for role in ROLES:
    print (role)


print ('***************Print whole LIST\n')
print (ROLES)



print ('***************Append member\n')
pa = {'policyadmin':
        {'Policy administrator':'Manage and execute policies and security controls'}}

ROLES.append(pa)
print (ROLES)

# More difficult  case:  dict of  list  of dicts:
print ('***************dict -> lists -> dicts\n')



ASSETS = {}
aff_assets = \
        [ {'test asset_1': 'http://test.invalid/#assets/1'},
          {'test asset_2': 'http://test.invalid/#assets/2'} ]

ASSETS['affected_assets'] = aff_assets


print (ASSETS)

a1 = json.dumps(ASSETS)
print ('***************JSON DUMP: \n')
print (a1)


print ('***************iterating by key 2 \n')


rols = R1.get('aelz',None)
if rols:
    for asset in rols:
        for  key, value in asset.items():
            print  ('key: {}  value {}'.format(key, value))

