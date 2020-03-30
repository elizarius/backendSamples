#!/usr/bin/env python
import json


data = {"redirectUris":
        ["http:://kuku.com",
            "http:://zz.com"],
        "aelz": "aelz_01",
        "ZOPA":1234567
       
}


#for role in ROLES:
#    #print (role)
#    for a,b in role.items():
#        print('id : %s ' % a)
#        #print('Name : %s ' % b)
#        print('name: %s ' % b.keys()[0])
#        print('description: %s ' % b.values()[0])
        #data.append ({'id': a, 'name': b.fromkeys()})

print ('******************\n')
print (data)
print ('******************\n')


for key in data:
    print ('{} :: {}'.format(key, data[key]))
print ('---------------------------\n')


for a,b in data.items():
    print('key : {} value: {}'.format(a, b)) 

