#!/usr/bin/env python
import os
import sys
import json


def basic_ecm_data():
    return dict(
        name='ECM-1',
        address='http://131.160.90.44:8080/',
        tenant='ECM',
        vdc='TestVDC',
        username='ecmadmin',
        password='password1'
    )




aelz =[]
print ("AELZ list length: {} ".format(len(aelz)))

ecm_data = basic_ecm_data()
print ("Dictionary data:{} ".format(ecm_data.items()))
print ("VDC:{}".format(ecm_data['vdc']))

ecm_data['vdc'] = json.dumps(ecm_data['vdc'])
print ("Dictionary data:{} ".format(ecm_data.items()))

vdc_list = ['vdc_1','vdc_2']
#vdc_list = ['vdc_1']
ecm_data['vdc'] = json.dumps(vdc_list)

print ("VDCs: {} ".format(ecm_data.items()))
print ("VDCs: length {} ".format(len(vdc_list)))


print ("")
print ("*********************************")
print ("")

vdcs = json.loads(ecm_data['vdc'])

print ("AELZ_01 vdcs {}".format(vdcs))
for vdc in vdcs:
    print ("AELZ_02 vdc {}".format(vdc))


