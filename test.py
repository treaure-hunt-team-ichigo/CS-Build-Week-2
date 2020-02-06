from player import Player
import json
import time

test_list = []
json_d = None

phade = Player("Phade", 0)

phade.init()

test_list.append(phade.room)

time.sleep(1)

phade.status()

test_list.append(phade.p_status)

print(test_list)

json_d = json.dumps(test_list)

f = open('test.txt', 'w+')
f.write(json_d)
f.close















