#!/usr/bin/env python
import json

# https://www.educative.io/answers/what-is-the-difference-between-jsonloads-and-jsondumps
# resp.text
# resp.json()))   # actually the same as json.loads()

x =  '{ "name":"John", "age":30, "city":"New York"}'
print ("AELZ_01 string  {}".format(x))
#print(x["age"])    NOK , because string 
y = json.loads(x)
print(y["age"])

z = json.dumps(y)
print ("AELZ_02 dict  {}".format(y))
print ("AELZ_03 string  {}".format(z))

