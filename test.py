from player import Player
import time

phade = Player("Phade", 0)

phade.init()

# print(phade.room)

# print(f'cooldown: {phade.cd}')

# time.sleep(phade.cd)
print(phade.room)
time.sleep(2)

phade.move('w')

time.sleep(5)
# phade.take()
# print(phade.status())

# phade.status()

# for k, v in phade.p_status.items():
#     print(f'{k}: {v}')
print(phade.room)

print(phade.room['room_id'])

time.sleep(phade.cd)

phade.status()  

print(phade.p_status)

print(phade.p_status['inventory'])










