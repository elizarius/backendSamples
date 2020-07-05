import sys
import hashlib
import secrets
import hmac

# AELZ_01 sha256 alone is not recommended to use alone for passwords as naive algo
# Use pbkdf2 instead (salting, IV, deviation)
#
# AELZ_02:
#   - hmac is algo (sha256) + key + method to encrypt
#   - sha256 is algo based on MAC?, no keys, vulnerable to several types of attacks as
#   dictionary, rainbow
#   - pbkdf2 recommended to use instead (salting, IV, deviation, key, message). At least
#

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


def set_sha256_hash(password):
    pwhash = password.encode()
    pwhash = hashlib.sha256(pwhash)
    print ("Created sha256 hash:\n {}".format(pwhash.digest()))
    print ("Created sha256 hex hash:\n{}".format(pwhash.hexdigest()))
    return pwhash

def set_hmac_hash(password):
    shared_key =  'secret-shared-key'
    pwhash = hmac.new(shared_key.encode(), password.encode(), hashlib.sha256)
    # print ("Created hmac hash:\n {}".format(pwhash.digest()))
    print ("Created hmac hex hash:\n{}".format(pwhash.hexdigest()))
    return pwhash


if __name__ == "__main__":
    password = read_password()
    validate_password_policy(password)
    set_sha256_hash(password)
    print ('*' * 60)
    set_hmac_hash(password)
