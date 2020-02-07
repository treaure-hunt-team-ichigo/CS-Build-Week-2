import json
import hashlib
import time
from player import Player



def proof_of_work(last_block, difficulty):
    bl_string = json.dumps(last_block, sort_keys=True)
    proof = 0
    while valid_proof(bl_string, proof, difficulty) is False:
        proof += 1
    return proof

def valid_proof(bl_string, proof, difficulty):
    guess = f"{bl_string}{proof}".encode()
    guess_hash = hashlib.sha256(guess).hexdigest()
    return guess_hash[:difficulty] == "0" * difficulty


player = Player('Name', 0)
player.init()
time.sleep(player.cd)

print('getting last valid proof')
player.proof()
time.sleep(player.cd)

lvp = player.lc_proof['proof']
dif = player.lc_proof['difficulty']
proof = proof_of_work(lvp, dif)
print('found proof: ', proof)

print('submitting proof')
player.mine(proof)
time.sleep(player.cd)

print('checking balance')    
player.balance()
time.sleep(player.cd)
bal = player.lc_balance['messages']
print(bal)


    
    
