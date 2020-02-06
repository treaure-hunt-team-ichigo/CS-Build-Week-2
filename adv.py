from player import Player
import json
import random
import time

player = Player('Name', 0)
player.init()
time.sleep(player.cd)
graph = dict()
mapped = []
traversal_path = []
reverse_path = []
visited_rooms = set()

def populate_graph_with_exits(room):
    ''' Populate graph with exits set to ? '''
    graph[room['room_id']] = dict()
    exits = room['exits']
    for exit in exits:
        graph[room['room_id']][exit] = '?'

def get_opposite(cardinal_direction):
    ''' Returns the opposite cardinal direction '''
    opposite = {'n': 's', 's': 'n', 'e': 'w', 'w': 'e'}
    return opposite.get(cardinal_direction)

def bfs(room):
    ''' Moves player over reverse_path. '''
    for move in reverse_path[::-1]:
        player.move(move)
        time.sleep(player.cd)
        traversal_path.append(move)
        reverse_path.pop(-1)
        if '?' in graph[player.room['room_id']].values():
            # print(f'Graph at end of BFS. {graph}')
            return

def dfs(room, cardinal_directions):
    ''' Builds the graph and adds to the traversal and reverse paths '''
    previous_room_id = player.room['room_id']
    cardinal_direction = cardinal_directions.pop(0)
    player.move(cardinal_direction)
    time.sleep(player.cd)
    in_room_id = player.room['room_id']
    in_room = player.room
    traversal_path.append(cardinal_direction)
    opposite = get_opposite(cardinal_direction)
    reverse_path.append(opposite)
    if in_room_id not in graph:
        populate_graph_with_exits(in_room)
        graph[previous_room_id][cardinal_direction] = in_room_id
        graph[in_room_id][opposite] = previous_room_id
    else:
        graph[previous_room_id][cardinal_direction] = in_room_id


def take_treasure(self):
    if len(player.room['items']) > 0:
        player.take()
        time.sleep(player.cd)

def sell_treasure(self):
    if player.room['title'] == "Shop":
        player.sell()
        time.sleep(player.cd)

def name_change(self):
    if player.room['title'] == "Pirate Ry's":
        player.status()
        time.sleep(player.cd)
        if player.p_status['gold'] > 999:
            player.change_name("Jason_Prince")
            time.sleep(player.cd)

rm_txt = open('rooms.txt', 'w+')

while len(graph) < 500:
    # print(graph)
    # print(player.room)
    rm_json = json.dumps(player.room)
    rm_txt.write(rm_json)
    take_treasure(player.room)
    sell_treasure(player.room)
    name_change(player.room)
    in_room = player.room
    if in_room['room_id'] not in graph:
        populate_graph_with_exits(in_room)
    unexplored_exits = []
    for cardinal_direction, room in graph[in_room['room_id']].items():
        if room == '?':
            unexplored_exits.append(cardinal_direction)
    if len(unexplored_exits) > 0:
        dfs(in_room, unexplored_exits)
    else:
        if len(reverse_path) > 0:
            bfs(in_room)
        else:
            exits = in_room['exits']
            choice = random.choice(exits)
            player.move(choice)
            time.sleep(player.cd)

rm_txt.close

# collect items
# sell items
# change name
# mine lambda coin
