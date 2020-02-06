import hashlib
import json
# from player import Player
from time import time

DIFFICULTY = 3

def proof(lvp):
    block_string = json.dumps(lvp, sort_keys=True)    
    proof = 0    
    while valid_proof(block_string, proof) is False:
        proof += 1   
    return proof

def valid_proof(block_string, proof):
    guess = f'{block_string}{proof}'.encode()
    guess_hash = hashlib.sha256(guess).hexdigest()
    
    return guess_hash[:DIFFICULTY] == '0' * DIFFICULTY

block = {
  "proof": 123456,
}

print('Finding a new proof')

new_proof = proof(block)

print(new_proof)