#!/usr/bin/env python

import hmac, base64, struct, hashlib, time, sys


def get_hotp_token(secret, intervals_no):
    secret = secret.replace('1', 'I').replace('0', 'O')
    key = base64.b32decode(secret, True)
    if (len(key) < 10):
        raise ValueError('Key too short!')
    msg = struct.pack(">Q", intervals_no)
    h = hmac.new(key, msg, hashlib.sha1).digest()
    o = ord(h[19]) & 15
    h = (struct.unpack(">I", h[o:o+4])[0] & 0x7fffffff) % 1000000
    return h


def get_totp_token(secret):
    return get_hotp_token(secret, intervals_no=int(time.time())//30)


if __name__ == "__main__":
    secret = sys.argv[1]
    for i in range(1, 10):
        print('{} {:06d}'.format(i, get_hotp_token(secret,i)))
    print('TimeBased: {:06d}'.format(get_totp_token(secret)))
