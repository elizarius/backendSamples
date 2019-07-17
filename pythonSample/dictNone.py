#!/usr/bin/env python

def create_error_msg(msg, detail=None):
    error_msg = {'message': msg}
    if detail:
         error_msg['detail'] = detail
    return error_msg

def form_dict(inp_dict):
    out_dict  = {'one': inp_dict['one']}
    out_dict['two']  = inp_dict.get('two', 'AELZnotFOund')

    return out_dict




print (create_error_msg('Aelz msg'))
print (create_error_msg('Aelz msg', 'with  hueva tucha details'))
print (form_dict({'one':'1'}))




d1 ={'aelz1': 'aelz11111'}


out1 = d1.get('aelz1',0)

if out1:
    print ("KEY FOUND")
else:
    print ("KEY NOT  FOUND")






