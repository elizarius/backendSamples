#!/usr/bin/env python
import hashlib

#zz = 'Hello World'

#hash_object = hashlib.sha256(b'Hello World')

#hash_object = hashlib.sha256(zz.encode())
#hex_dig = hash_object.hexdigest()

#print(hash_object.digest())
#print(hex_dig)

#print(hashlib.algorithms_available)
#print(hashlib.algorithms_guaranteed)


print('Step 2 ************')
pwd="password"
p_object = hashlib.sha256(pwd.encode())
p_dig = p_object.hexdigest()


u_object = hashlib.sha256(pwd.encode('utf-8'))
u_dig = u_object.hexdigest()



print(p_dig)
print(p_dig[:8])

print(u_dig)
print(u_dig[:8])


