from player import Player
import time
import random
from util_bp import Stack, Queue

player = Player("Bryant")


# Loads the map into a dictionary
# room_graph = literal_eval(open(map_file, "r").read())
# world.load_graph(room_graph)


def add_to_visited_rooms(visited_rooms_graph, room):
    if room["id"] not in visited_rooms_graph:
        exits = room["exits"]
        current_exits = visited_rooms_graph[room["id"]] = {exit: "?" for exit in exits}
        player.visited_rooms_track.add(room["id"])
        return current_exits


def new_path(visited_rooms_graph, room):
    queue = Queue()
    queue.enqueue([(room["id"], None)])
    visited = set()
    while queue.size() > 0:
        path = queue.dequeue()
        vertex = path[-1]
        room = vertex[0]
        if room not in visited:
            visited.add(room)
            exits = visited_rooms_graph[room]
            for e in exits:
                if exits[e] == "?":
                    new_path = path.copy()
                    new_path.append((exits[e], e))
                    d_path = [p[1] for p in new_path[1:]]
                    travel_path = Queue()
                    travel_path.enqueue([d_path][-1])
                    return travel_path
                else:
                    new_path = list(path)
                    new_path.append((exits[e], e))
                    queue.enqueue(new_path)


def visit_rooms():
    while len(player.visited_rooms_graph) < 1:
        room = player.room
        current_exits = player.room["exits"]
        if room["id"] not in player.visited_rooms_graph:
            player.visited_rooms_graph[room["id"]] = {e: "?" for e in current_exits}
        unexplored_exits = [e for e in current_exits if player.visited_rooms_graph[player.room["id"]][e] == "?"]
        if len(unexplored_exits) > 0:
            next_move = random.choice(unexplored_exits)
        else:
            travel_path = new_path(player.visited_rooms_graph, room)
            next_move = travel_path.dequeue()
            next_move = next_move[0]

        previous_room = room
        traversal_path.append(next_move)
        player.move(next_move)
        room = player.room
        if player.room["id"] not in player.visited_rooms_track:
            add_to_visited_rooms(player.visited_rooms_graph, player.room)

        if room["id"] not in player.visited_rooms_graph:
            current_exits = player.room["exits"]
            player.visited_rooms_graph[room["id"]] = {e: "?" for e in current_exits}
        player.visited_rooms_graph[previous_room["id"]][next_move] = room["id"]
        player.visited_rooms_graph[room["id"]][opposite_directions[next_move]] = previous_room["id"]


travel_path = Queue()
traversal_path = []
directions = ["n", "e", "s", "w"]
opposite_directions = {"n": "s", "e": "w", "s": "n", "w": "e"}

# player.visited_rooms_track = set()
# visit_rooms()
# d = player.visited_rooms_graph
# import json

# json = json.dumps(d)
# f = open("player.visited_rooms_graph.json", "w")
# f.write(json)
# f.close()
