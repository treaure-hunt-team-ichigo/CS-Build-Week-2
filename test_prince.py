from player import Player
import time

player = Player("player", 0)

player.init()

time.sleep(2)

# player.move('w')

print(player.room['room_id'])
print(player.room['exits'])

player.move('n')

print(player.room)
print(player.room['exits'])
