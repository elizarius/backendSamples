#!/usr/bin/env python3
import os
import sys
import json
from pprint import pprint


dict_aa =  {
  "agentPort":161,
  "agentEngineId":"",
  "heartbeatInterval":60,
  "ahAddress":"eric-fh-alarm-handler",
  "ahPort":5005,
  "kafkaAddress":"eric-data-message-bus-kf",
  "kafkaPort":9092,
  "trapTargets":
  [
    {
      "address":"10.10.10.10",
      "port":"122",
      "user":"sasa",
      "securityLevel":"authPriv",
      "authPassphrase":"wewewewe",
      "authProtocol":"SHA1",
      "privPassphrase":"sesesese",
      "privProtocol":"AES128"
    }
  ]
}


print ('-------------------------------') 

pprint(dict_aa)
print ('-------------------------------') 

pprint(json.dumps(dict_aa))
print ('-------------------------------') 

print ('{}'.format(dict_aa))
print ('*********************') 

kki = "aeklx aaaaaa"


#print(vars(kki))
# convert to json from string 
#jsonObj = json.loads(aa)
#print ('{}'.format(aa))


