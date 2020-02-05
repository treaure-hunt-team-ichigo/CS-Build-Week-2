from player import Player
import time

phade = Player("Phade", 0)

phade.init()

print(phade.room)

time.sleep(1)
phade.move('e')

print(phade.room)

for k, v in phade.room.items():
    print(f'{k}: {v}')










