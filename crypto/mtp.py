# One time pad exercise, that used twice

import sys
import secrets


def strxor(a, b):     # xor two strings of different lengths
    if len(a) > len(b):
       return ''.join([chr(ord(x) ^ ord(y)) for (x, y) in zip(a[:len(b)], b)])
    else:
       return ''.join([chr(ord(x) ^ ord(y)) for (x, y) in zip(a, b[:len(a)])])

def encrypt(key, msg):
    c = strxor(key, msg)
    return c



if __name__ == '__main__':
    #key = secrets.token_hex(16)
    key =  'very secure one time pad key used twice'
    msg1 = 'mESSAGE 111 VVSSS WWW XXXXXXXXXXXX BBBB'
    msg2 = 'mESSAGE 222 CCCCCCCCCCCCCCCCCCCCCCCCCCD'

    space = ' '
    a = 'a'
    b = 'b'
    A = 'A'

    print ('space XOR a : {}'.format(ord(space) ^ ord(a)))
    print ('space XOR a : {}'.format(chr(ord(space) ^ ord(a))))

    print ('space XOR A : {}'.format(ord(space) ^ ord(A)))
    print ('space XOR A : {}'.format(chr(ord(space) ^ ord(A))))


    print ('space XOR b : {}'.format(ord(space) ^ ord(b)))
    print ('space XOR b : {}'.format(chr(ord(space) ^ ord(b))))


    print ('space XOR space : {}'.format(ord(space) ^ ord(space)))
    print ('space XOR space : {}'.format(chr(ord(space) ^ ord(space))))



