#!/usr/bin/env python
import os
import sys
import json

class ActivityResponse:
        subscriber = {
                'imsi': '252525',
                'msdn': '363636'
        }
        network = {
                'mcc': 12345,
                'countryName': 'Finland',
                'mnc': 55,
                'networkName': 'any_operator',
        }
        connectivity = {
                'ipCanType': 'strange_type',
                'ipv4': '20.20.20.2',
                'ipv6': '2001:db8:a0b:12f0::1'
        }
        roaming = 'outbound'
        kpi = {
                'time': '23:12:2016:18:55:40',
                'name': 'Fraud_first_KPI',
                'uplink': 100,
                'downlink': 200,
                'total': 400,
                'relative': 500
    }



acResp = ActivityResponse()
zz = json.dumps(acResp.subscriber)
#zz = json.dumps(acResp)


print "****Working with subscriber dictionary of Response class***"
print ''
print "all dictionary ", acResp.subscriber
print "['imsi'] ", acResp.subscriber['imsi']
print "get():    ", acResp.subscriber.get('imsi')
print "keys():   ", acResp.subscriber.keys()
print "values(): ", acResp.subscriber.values()
print "len(): ", len(acResp.subscriber)
print ''

#print "1: ", acResp.subscriber


print "**** Working with kpi dictionary of Response class"
print "1.2 ", acResp.kpi.get('total')

print "AELZ_O2: ", json.dumps(acResp.subscriber)
print "AELZ_O3: ", zz
