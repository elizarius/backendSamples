# AES CTR with Cryptodome usage

import sys
import secrets
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad


if __name__ == '__main__':
    key = secrets.token_bytes(16)
    print ('key:            {}'.format(key))

    aes = AES.new(key, AES.MODE_CTR)
    msg = 'This is message to be encoded'
    cipher_text = aes.encrypt(msg.encode())
    nonce = aes.nonce

    print ('encoded message: {}'.format(cipher_text))
    print ('cipher nonce:    {}'.format(nonce))
    print ('encoded hex: {} \n'.format(cipher_text.hex()))

    print('Decrypting')
    aes = AES.new(key, AES.MODE_CTR, nonce=nonce)
    decr = aes.decrypt(cipher_text)
    print ('decrypted message:  {}'.format(decr))
    print ('decrypted asci msg: {}'.format(decr.decode()))
    print('\n{}'.format(60*'*'))

    print('Decrypt for hexadecimal strings')
    ctr_key = '36f18357be4dbd77f050515c73fcf9f2'
    byted_key =  bytes.fromhex(ctr_key)
    print ('byted_key:          {} {}'.format(len(byted_key) , byted_key))
    ctr_cipher = '69dda8455c7dd4254bf353b773304eec0ec7702330098ce7f7520d1cbbb20fc388d1b0adb5054dbd7370849dbf0b88d393f252e764f1f5f7ad97ef79d59ce29f5f51eeca32eabedd9afa9329'
    byted_cipher =  bytes.fromhex(ctr_cipher)
    nonce = b'nonce'
    aes = AES.new(byted_key, AES.MODE_CTR, nonce=nonce, initial_value = 0) 
    decr = aes.decrypt(byted_cipher)
    print ('decrypted message:  {}'.format(decr))

    # Note 1: need to know nonce in init value from encryption to get correct result 
    # Note 2: it is possible to use counter parameter instead of nonce / iv combination
    # but again decryptor have to know counter value

