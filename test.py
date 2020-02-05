from player import Player
import time

phade = Player("Phade", 0)

phade.init()

# print(phade.room)

# print(f'cooldown: {phade.cd}')

# time.sleep(phade.cd)

# phade.move('e')
# phade.take()
print(phade.status())


for k, v in phade.room.items():
    print(f'{k}: {v}')










