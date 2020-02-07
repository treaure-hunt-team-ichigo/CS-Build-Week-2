from player import Player
import hashlib
import mine 
import time

player = Player('Name', 0)
player.init()
time.sleep(player.cd)

player.proof()
time.sleep(player.cd)

lvp = player.lc_proof['proof']
difficulty = player.lc_proof['difficulty']

new_proof = mine.proof(lvp, difficulty)

player.mine(new_proof)

time.sleep(player.cd)

player.balance()

print(player.lc_balance)
