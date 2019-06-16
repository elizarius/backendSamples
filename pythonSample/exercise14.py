#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
import sys
import re

arg = sys.argv

if len(arg) > 1:
    print arg
else:
    print "No characters"
    sys.exit()

#date
model = r"(([012]\d)|(3[01]))"
#month
model += r"((0[1-9])|(1[0-2]))"
#year and the rest
model += r"[0-9]{2}[-+A][0-9]{3}([0-9A-FHJ-N]|[PR-Y])"

pattern = re.compile(model)
# match
response = pattern.match(arg[1])

if response is not None:
    print response.group()
else:
    print "'%s' was not a right ID" %(arg[1])

