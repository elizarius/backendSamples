#!/usr/bin/env python


#Tuple of dictionaries example

ROLES = (
    {'auvancedanalyst':
        {'Advanced analyst':
            'Manage and execute advanced analytics activities'}},
    {'assetadmin':
        {'Asset administrator': 'Manage assets in ESM'}}
)

for role in ROLES:
    print (role)


print ('***************Print whole LIST\n')
print (ROLES)



print ('***************Append member\n')
pa = {'policyadmin':
        {'Policy administrator':'Manage and execute policies and security controls'}}

ROLES.append(pa)
print (ROLES)


