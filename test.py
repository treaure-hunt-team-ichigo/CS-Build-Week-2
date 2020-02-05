from player import Player
import time

phade = Player("Phade", 0)

phade.init()

for k, v in phade.room.items():
    print(f'{k}: {v}')

time.sleep(2)

phade.move('w')
 
print(phade.room['room_id'])

print(f'COOLDOWN: {phade.cd}')

time.sleep(phade.cd)

phade.status()  

print(phade.p_status['speed'])

# f = open('test.txt', 'a')
# f.write(phade.room)
# f.close()

# f = open('test.txt', 'r')
# print(f.read()) 











