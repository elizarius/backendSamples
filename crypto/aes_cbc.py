# AES CBC with Cryptodome usage

import sys
import secrets
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad


if __name__ == '__main__':
    #key = 'sasa bababab'
    key = secrets.token_bytes(16)
    iv = secrets.token_bytes(16)

    print ('key:            {}'.format(key))

    aes = AES.new(key, AES.MODE_CBC, iv)
    msg = 'This is message to be encoded'
    padded = pad(msg.encode(), 16, style='pkcs7')
    cipher = aes.encrypt(padded)
    print ('encoded message: {}'.format(cipher))
    print ('encoded hex: {} \n'.format(cipher.hex()))

    print('Decrypting')
    aes = AES.new(key, AES.MODE_CBC, iv)
    decr = aes.decrypt(cipher)
    unpadded = unpad(decr, 16, style='pkcs7' )
    print ('decrypted message:  {}'.format(unpadded))
    print ('decrypted asci msg: {}'.format(unpadded.decode()))
    print('\n{}'.format(60*'*'))

    print('Decrypt for hexadecimal strings')
    cbc_key = '140b41b22a29beb4061bda66b6747e14'
    byted_key =  bytes.fromhex(cbc_key)
    print ('byted_key:          {} {}'.format(len(byted_key) , byted_key))
    cbc_cipher = '4ca00ff4c898d61e1edbf1800618fb2828a226d160dad07883d04e008a7897ee2e4b7465d5290d0c0e6c6822236e1daafb94ffe0c5da05d9476be028ad7c1d81'
 
    byted_cipher =  bytes.fromhex(cbc_cipher)

    aes = AES.new(byted_key, AES.MODE_CBC)
    decr = aes.decrypt(byted_cipher)
    unpadded = unpad(decr, 16, style='pkcs7' )
    print ('decrypted message:  {}'.format(unpadded))
    print ('decrypted no IV  :  {}'.format(unpadded[16:]))
    print ('decoded no IV    :  {}'.format(unpadded[16:].decode('ascii')))
    print('\n{}'.format(60*'*'))

    cbc_cipher = '5b68629feb8606f9a6667670b75b38a5b4832d0f26e1ab7da33249de7d4afc48e713ac646ace36e872ad5fb8a512428a6e21364b0c374df45503473c5242a253'
    byted_cipher =  bytes.fromhex(cbc_cipher)

    aes = AES.new(byted_key, AES.MODE_CBC)
    decr = aes.decrypt(byted_cipher)
    unpadded = unpad(decr, 16, style='pkcs7' )
    print ('decrypted message:  {}'.format(unpadded))
    print ('decrypted no IV  :  {}'.format(unpadded[16:]))
    print ('decoded no IV    :  {}'.format(unpadded[16:].decode('ascii')))

    print('\n{}'.format(60*'*'))

    # Does not work example, require hex object to be converted to bytes, see above
    # cbc_key = '140b41b22a29beb4061bda66b6747e14'
    # cbc_cipher = '4ca00ff4c898d61e1edbf1800618fb2828a226d160dad07883d04e008a7897ee2e4b7465d5290d0c0e6c6822236e1daafb94ffe0c5da05d9476be028ad7c1d81'
    # aes = AES.new(cbc_key.encode(), AES.MODE_CBC)
    # decr = aes.decrypt(cbc_cipher.encode())
    # unpadded = unpad(decr, 16, style='pkcs7' )
    # print ('decrypted message:  {}'.format(unpadded))
    # print('\n{}'.format(60*'*'))
