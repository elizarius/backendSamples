#!/usr/bin/env python

pwd = "12345678999"
BACKUP_BASE_KEY = "Ax34()7*90+-&@!<"
print "PWD is:  %s" % pwd
key = pwd[:8] + pwd[:8] + BACKUP_BASE_KEY
print "key is:  %s" %   key
field_backup_key = key[:16]
print "fbk is:  %s" %   field_backup_key



zz = "1234"
key = zz[:8] + zz[:8]
print "zz_key is:  %s" %   key
