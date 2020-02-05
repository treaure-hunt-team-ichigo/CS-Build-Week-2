import hashlib
import json
from time import time

def hash(block):
    string_object = json.dumps(block, sort_keys=True).encode()
    raw_hash = hashlib.sha256(string_object)
    hex_hash = raw_hash.hexdigest()
    
    return hex_hash

