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

def format_used_memory(used_memory):
    gb_threshold = 1 * 1024 * 1024 * 1024  # 1 GB in bytes
    used_memory_mb = used_memory / (1024 * 1024)
    if used_memory < gb_threshold:
        formatted_used_memory = round(used_memory_mb, 2)
        unit = "MB"
    else:
        formatted_used_memory = round(used_memory / gb_threshold, 2)
        unit = "GB"

    return str(formatted_used_memory)+" "+unit

def calculate_percentage(used_memory, total_memory):
    percentage = (used_memory / total_memory) * 100
    return round(percentage, 2)