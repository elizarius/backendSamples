#!/usr/bin/env python
#import os
#import sys
import json

vdc_list = ['vdc_1','vdc_2']
ha = 'xaxaxaxa'
json_data = json.dumps(vdc_list)

print ("AELZ_01 vdcs {}".format(vdc_list))
print ("AELZ_01 j_data {}".format(json_data))

print ("AELZ_03 ha {}".format(ha))
print ("AELZ_03 j_ha {}".format(json.dumps(ha)))




print ("")
print ("*********************************")
print ("")


print ("AELZ_04 l_data {}".format(json.loads(json_data)))
print ("AELZ_05 l_ha {}".format(json.loads(json.dumps(ha))))

#vdcs = json.loads(ecm_data['vdc'])

#print ("AELZ_01 vdcs {}".format(vdcs))
#for vdc in vdcs:
#    print ("AELZ_02 vdc {}".format(vdc))


