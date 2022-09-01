import binascii
import hashlib
import os


def hash_password(password: str) -> str:
    salt = b'__hash__' + hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pHash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'),
                                salt, 100000)
    pHash = binascii.hexlify(pHash)
    return (salt + pHash).decode('ascii')


def is_hash(pw: str) -> bool:
    return pw.startswith('__hash__') and len(pw) == 200


def verify_password(stored_password: str, provided_password: str) -> bool:
    salt = stored_password[:72]
    stored_password = stored_password[72:]
    pHash = hashlib.pbkdf2_hmac('sha512',
                                provided_password.encode('utf-8'),
                                salt.encode('ascii'),
                                100000)
    pHash = binascii.hexlify(pHash).decode('ascii')
    return pHash == stored_password
