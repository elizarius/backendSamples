
id = 127

upperpart = '{0:08b}'.format(id)
lowerpart_min = '0000000000000000'
lowerpart_max = '1111111111111111'

first_number = int(upperpart + lowerpart_min, 2)
last_number= int(upperpart + lowerpart_max, 2)

print(first_number,last_number)