import hashlib
import os

def hash(text):
    text_encoded = text.encode('utf-8')
    hashed = hashlib.sha256(text_encoded)
    return hashed.hexdigest()

def getFileName(path):
    return os.path.basename(path)

def contains_file(lst, file_name):
    file_dict = {d.get('name'): True for d in lst}
    return file_name in file_dict