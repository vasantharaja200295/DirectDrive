import hashlib

def hash(text):
    text_encoded = text.encode('utf-8')
    hashed = hashlib.sha256(text_encoded)
    return hashed.hexdigest()