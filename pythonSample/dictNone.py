#!/usr/bin/env python

#def create_error_msg(msg, detail=None):
#    if detail:
#        error_msg = {'message': msg, 'detail': detail}
#    else:
#        error_msg = {'message': msg}
#    return error_msg


def create_error_msg(msg, detail=None):
    error_msg = {'message': msg}
    if detail:
         error_msg['detail'] = detail
    return error_msg




print (create_error_msg('Aelz msg'))
print (create_error_msg('Aelz msg',
                        'with  hueva tucha details'))


