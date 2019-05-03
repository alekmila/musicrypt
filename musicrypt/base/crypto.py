# https://nitratine.net/blog/post/encryption-and-decryption-in-python/

import base64
import os

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def key_from_password(password_provided):
    password = password_provided.encode() # Convert to type bytes
    salt = b'salt_' # CHANGE THIS - recommend using a key from os.urandom(16), must be of type bytes
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(password)) # Can only use kdf once
    return key


def encrypt(xs, password):
    '''file bytes -> encrypted bytes'''
    key = key_from_password(password)
    f = Fernet(key)
    return f.encrypt(xs)


def decrypt(xs, password):
    '''encrypted bytes -> file bytes'''
    key = key_from_password(password)
    f = Fernet(key)
    return f.decrypt(xs)

