from sys import argv


s1 = '/tmp/zzz'
s2 = s1+'.aelz'
s3=''

print ('%s    %s ' % (s1, s2))
s3 = s3 +'/'
print ('%s' % (s3))


tenant = 'tenant123'
print (tenant)

tenant=tenant.capitalize()
tenant= tenant[:6]+'Id:'+tenant[6:]
msg  = '{}'.format(tenant)
print (tenant)
print (msg)


# print apostrof
print ('*** Printing apostrofs *****')
print (" *** 'HAHHA INAPS' ")



