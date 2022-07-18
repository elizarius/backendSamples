#!/usr/bin/env python3

# Create  destination string fro original dtring  with partition method
orig = 'Threat indicator (ID 1) was created. Threat detection logic "kJwEtvbk" matched 1 log lines on 1 asset(s)'
print ('\n\n {}'.format(orig))
stripped = orig.partition('log lines on')
print (stripped)

#dest = stripped[0] + stripped[1]
#print =(dest)
asset_name = ' Asset: sasa_asset '
asset_id = '(ID {})'.format(25)

dest = stripped[0] + stripped[1] + asset_name + asset_id
print (dest)

# non_exist = orig.partition('kuku')
# print (non_exist)
# print ('\n\nAELZ stripped http: {}'.format(es_url.partition('://')[2].partition(':')[0]))



