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


def otp_encrypt(key, msg):
    if len(key) != len(msg):
        print ('Error key and message must have same size')
        return '-1'

    enc = ''.join([chr(ord(x) ^ ord(y)) for (x, y) in zip(key, msg)])
    return enc



if __name__ == '__main__':
    #key = secrets.token_hex(16)
    key =  'very secure one time pad key used twice'
    msg1 = 'mESSAGE 111 VVSSS WWW XXXXXXXXXXXX BBBB'
    msg2 = 'mESSAGE 222 CCCCCCCCCCCCCCCCCCCCCCCCCCD'
    print ('otp hex: {}'.format(key.encode().hex()))


    encrypted = otp_encrypt(key, msg1)
    decrypted = otp_encrypt(key, encrypted)
    print ('DEC1: {}'.format(decrypted))

    enc2 = otp_encrypt(key, msg2)
    decr2 = otp_encrypt(key, enc2)
    print ('DEC2: {}'.format(decr2))

    decr3 = otp_encrypt(encrypted, enc2)
    print ('OTP hex: {}'.format(decr3.encode().hex()))
    print ('')
    print(60*'*')


    print ('msg1_hex: {}'.format(msg1.encode().hex()))
    encrypted = otp_encrypt(key.encode().hex(), msg1.encode().hex())
    decrypted = otp_encrypt(key.encode().hex(), encrypted)
    print ('DEC1 hex: {}'.format(decrypted))

    print ('msg2_hex: {}'.format(msg2.encode().hex()))
    enc2 = otp_encrypt(key.encode().hex(), msg2.encode().hex())
    decr2 = otp_encrypt(key.encode().hex(), enc2)
    print ('DEC2 hex: {}'.format(decr2))

    print ('Calculate OTP')
    print(60*'*')

    decr3 = otp_encrypt(encrypted.encode().hex(), enc2.encode().hex())
    print ('DEC3 hex: {}'.format(decr3.encode().hex()))
    #print ('DEC3 hex: {}'.format(decr3))
