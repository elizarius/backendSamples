#!/usr/bin/env python
import os
import sys
import json

class Activity:
    glob =10
    def __init__(self, a1, a2):
        self.i = a1
        self.z = a2


ac1 = Activity(11,21)
ac2 = Activity(100,100)
print "AELZ_O1: ", ac1.i, ac2.i
print "AELZ_O2: ", ac1.z, ac2.z
print "AELZ_O3: AC static data ", ac1.glob , ac2.glob
ac2.glob =100000
print "AELZ_O4: AC static data ", ac1.glob , ac2.glob
