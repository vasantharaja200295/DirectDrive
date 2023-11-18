import hashlib

def hash(text):
    hashed = hashlib.sha256(text)
    return hashed