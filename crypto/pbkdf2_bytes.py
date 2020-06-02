import sys
import hashlib
oimport secrets
from hmac import compare_digest
import binascii

def read_password():
    print('Reading password from stdin', flush=True)
    try:
        password = sys.stdin.readline().rstrip('\n')
    except OSError as e:
        sys.exit(e.strerror)
    except UnicodeDecodeError as e:
        sys.exit(e)
    except KeyboardInterrupt:
        sys.exit('')

    return password


def validate_password_policy(password):
    # use ASCII range from https://tools.ietf.org/html/rfc7564#section-9.11
    # and space (0x20)
    if not (len(password) >= 8
            and all(0x20 <= ord(ch) <= 0x7e for ch in password)):
        sys.exit("Password doesn't meet policy requirements:\n" +
                 "- Must be at least 8 characters long\n" +
                 "- Must contain only non-control ASCII characters\n")


def set_password(password):

    salt = (secrets.token_bytes(16))
    print ("Created salt:\n {}".format(salt))
    print ("Hex salt:\n {}".format(salt.hex()))
    print ("Hex salt encoded:\n {}".format(salt.hex().encode()))
    binFromHex = binascii.a2b_hex(salt.hex())
    print ("Hex -> byte string\n {}".format(binFromHex))



if __name__ == "__main__":
    password = read_password()
    validate_password_policy(password)
    set_password(password)
    print('Password set')
