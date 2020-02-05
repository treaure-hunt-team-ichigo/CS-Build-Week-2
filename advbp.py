from player import Player
from world import World

import random
from ast import literal_eval
import sys

sys.path.append("./graph")
from util import Stack, Queue


# Load world
world = World()

map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
# world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []
directions = ["n", "e", "s", "w"]
opposite_directions = {"n": "s", "e": "w", "s": "n", "w": "e"}

# graph the rooms visited and their exits
visited_rooms_graph = {}
# all the room Id's that have been visited
visited_rooms_track = set()

# add the current room to the visited rooms graph
# create directions objects "n:?,s:?"
# add to visited rooms set
def add_to_visited_rooms(visited_rooms_graph, current_room):
    if current_room.id not in visited_rooms_graph:
        exits = current_room.get_exits()
        current_exits = visited_rooms_graph[current_room.id] = {exit: "?" for exit in exits}
        visited_rooms_track.add(current_room.id)
        return current_exits


def new_path(visited_rooms_graph, current_room):
    queue = Queue()
    queue.enqueue([(current_room.id, None)])
    visited = set()
    while queue.size() > 0:
        path = queue.dequeue()
        # print("current_path", path)
        vertex = path[-1]
        # print("current_room", vertex)
        room = vertex[0]
        # print("current_room_id:", room)
        if room not in visited:
            # print(vertex)
            visited.add(room)
            # loop through exits
            exits = visited_rooms_graph[room]
            # print("exits:", exits)
            for e in exits:
                # if unvisited exit, return path
                if exits[e] == "?":
                    new_path = path.copy()
                    # print("exits[e]", exits[e])
                    new_path.append((exits[e], e))
                    # print("new_path", new_path)
                    d_path = [p[1] for p in new_path[1:]]
                    # print("d_path", d_path)
                    travel_path = Queue()
                    travel_path.enqueue([d_path][-1])
                    # for d in d_path:
                    #     travel_path.enqueue([d])
                    # travel_path = queue.enqueue(d_path)
                    print("travel_path", travel_path.queue)
                    return travel_path
                else:
                    new_path = list(path)
                    new_path.append((exits[e], e))
                    queue.enqueue(new_path)


# setup queue for traversal
travel_path = Queue()
# loop through the rooms until all visited
# def visit_rooms(visited_rooms_graph,room_graph)
while len(visited_rooms_graph) < len(room_graph):
    current_room = player.current_room
    current_exits = current_room.get_exits()
    if current_room.id not in visited_rooms_graph:
        # add room to graph and set if not already there
        visited_rooms_graph[current_room.id] = {e: "?" for e in current_exits}
    # find new/unexplored exits
    unexplored_exits = [e for e in current_exits if visited_rooms_graph[player.current_room.id][e] == "?"]

    # if there are unexplored exits add it to the q
    if len(unexplored_exits) > 0:
        next_move = random.choice(unexplored_exits)
    # if all exits are explored, find a new room
    else:
        travel_path = new_path(visited_rooms_graph, current_room)
        next_move = travel_path.dequeue()
        next_move = next_move[0]

    # go to next room
    previous_room = current_room
    traversal_path.append(next_move)
    player.travel(next_move)
    current_room = player.current_room
    if player.current_room.id not in visited_rooms_track:
        # add room to graph and set if not already there
        add_to_visited_rooms(visited_rooms_graph, player.current_room)

    if current_room.id not in visited_rooms_graph:
        current_exits = current_room.get_exits()
        visited_rooms_graph[current_room.id] = {e: "?" for e in current_exits}
    # set the direction in graph
    visited_rooms_graph[previous_room.id][next_move] = current_room.id
    # print("line120", visited_rooms_graph[current_room.id])
    visited_rooms_graph[current_room.id][opposite_directions[next_move]] = previous_room.id

    # connections = current_room.connect_rooms(next_move, previous_room.id)

# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")


#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
