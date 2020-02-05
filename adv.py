from player import Player
# from room import Room
# from world import World

import random
import time
from ast import literal_eval

from utils import bfs, unexplored_directions, find_unexplored_room, find_room_direction, record_room_info

# Load world
# world = World()

# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
# map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
# room_graph = literal_eval(open(map_file, "r").read())
# world.load_graph(room_graph)

# world.print_rooms()

# TODO: player = Player(world.starting_room)
player = Player("Player One", 0)
player.init()
cool_down = player.cd
# time.sleep(cool_down)
# player graph dictionary in world
# TODO: player_graph = {world.starting_room.id: {}}
player_graph = {0: {}}

# defines opposite
opposite_map = {"n": "s", "e": "w", "w": "e", "s": "n"}

traversal_path = []
visited_rooms_list = [0, ]

# player's room location
# TODO: exits = player.current_room.get_exits()
exits = player.room['exits']

# when player moves room in a specific direction
# TODO: player_graph[player.current_room.id] = {i: "?" for i in exits}
player_graph[player.room['room_id']] = {i: "?" for i in exits}

# visiting every room on map at least once
while len(player_graph) < 500:

    direction = None

    # TODO: ud = unexplored_directions(player_graph, player.current_room.id)
    ud = unexplored_directions(player_graph, player.room['room_id'])

    # TODO: if len(player.current_room.get_exits()) == 1:
    if len(player.room['exits']) == 1:
        # pops the direction, removes it and returns it
        # TODO: direction = player.current_room.get_exits().pop()
        direction = player.room['exits'].pop()

    elif len(ud) > 1:
        # returns unexplored direction
        direction = ud.pop()

    # visit unexplored rooms
    elif len(ud) == 0:
        nr = find_unexplored_room(player_graph)
        # TODO: path = bfs(player, player.current_room.id, nr, player_graph)
        path = bfs(player, player.room['room_id'], nr, player_graph)
        path = path[1:]
        while len(path) > 0:
            next_room = path.pop(0)
            direction = find_room_direction(
                # TODO: player_graph[player.current_room.id], next_room)
                player_graph[player.room['room_id']], next_room)
            if len(path) > 0:
                # TODO: previous_room = player.current_room.id
                previous_room = player.room['room_id']
                # TODO: player.travel(direction)
                player.move(direction)
                time.sleep(cool_down)
                traversal_path.append(direction)
                # TODO: visited_rooms_list.append(player.current_room.id)
                visited_rooms_list.append(player.room['room_id'])

    if direction is None:
        # TODO: for key, value in player_graph[player.current_room.id].items():
        for key, value in player_graph[player.room['room_id']].items():
            if (key in ["n", "s", "e", "w"]) and (value == "?"):
                direction = key
                break

    # TODO: previous_room = player.current_room.id
    previous_room = player.room['id']
    # TODO: player.travel(direction)
    print(f'***DIRECTION*** {direction}')
    player.move(direction)
    time.sleep(cool_down)
    traversal_path.append(direction)
    # TODO: visited_rooms_list.append(player.current_room.id)
    visited_rooms_list.append(player.room['room_id'])

    # TODO: player_graph[previous_room][direction] = player.current_room.id
    player_graph[previous_room][direction] = player.room['room_id']
    # TODO: new_exits = player.current_room.get_exits()
    new_exits = player.room['exits']

    # TODO: if player.current_room.id not in player_graph.keys():
    if player.room['room_id'] not in player_graph.keys():
        # TODO: player_graph[player.current_room.id] = {i: "?" for i in new_exits}
        player_graph[player.room['room_id']] = {i: "?" for i in new_exits}

    try:
        # TODO: player_graph[player.current_room.id][opposite_map[direction]
        player_graph[player.room['room_id']
                     ][opposite_map[direction]] = previous_room
    except:
        pass


# FILL THIS IN


# print(visited_rooms_list)

# NOT USED
# TRAVERSAL TEST
# visited_rooms = set()
# player.current_room = world.starting_room
# visited_rooms.add(player.current_room.id)
# for move in traversal_path:
#     player.travel(move)
#     visited_rooms.add(player.current_room.id)
# not_visited_rooms = [i for i in list(
#     room_graph.keys()) if i not in visited_rooms]
# if len(visited_rooms) == len(room_graph):
#     print(
#         f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited"
#     )
# else:
#     print("TESTS FAILED: INCOMPLETE TRAVERSAL")
#     print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")

#     print(sorted(not_visited_rooms))
#     print(len(traversal_path))
#     o = open("path.txt", "w")
#     o.write(", ".join([str(i) for i in visited_rooms_list]))
#     o.close()

#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     else:
#         print("I did not understand that command.")
