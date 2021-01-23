#!/usr/bin/env python
import json


data = {"redirectUris":
        ["http:://kuku.com",
            "http:://zz.com"],
        "aelz": "aelz_01",
        "ZOPA":1234567

}


print ('******************\n')
print (data)
print ('******************\n')


for key in data:
    print ('{} :: {}'.format(key, data[key]))
print ('---------------------------\n')


for a,b in data.items():
    print('key : {} value: {}'.format(a, b))

