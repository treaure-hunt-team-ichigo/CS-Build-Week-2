from player import Player
import time

phade = Player("Phade", 0)

phade.init()

print(phade.room['room_id'])

time.sleep(1)

phade.move('s')

print(phade.room['room_id'])















