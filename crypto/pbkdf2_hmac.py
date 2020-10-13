import sys
import hashlib
import secrets
from hmac import compare_digest

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

    # random hexadecimal string
    salt = (secrets.token_hex(16))
    print ("Created salt:\n {}".format(salt))

    pwhash = password.encode()
    print ("Encoded pass:\n {}".format(pwhash))
    print ("Encoded salt:\n {}".format(salt.encode()))

    dk = hashlib.pbkdf2_hmac('sha256', pwhash, salt.encode(), 100000)
    print ("Created hash:\n {}".format(dk))
    return salt, dk.hex()

def compare_password(given_password, salt, pwhash):

    gpw = given_password.encode()
    print ("Given encoded pass:\n {}".format(gpw))
    print ("Received salt:\n {}".format(salt))
    s = salt.encode()
    print ("Encoded salt:\n {}".format(s))


    dk = hashlib.pbkdf2_hmac('sha256', gpw, s, 100000)
    dk = dk.hex()
    print ("Given hash:\n {}".format(dk))

    if not compare_digest(dk, pwhash):
        # use generic error to make it harder for an attacker
        raise DecryptionError('Wrong passphrase')


if __name__ == "__main__":
    password = read_password()
    validate_password_policy(password)
    salt, pwhash = set_password(password)
    print('Password set')
    print('Processing of given password:')
    given = read_password()
    validate_password_policy(given)
    compare_password(given, salt, pwhash)
