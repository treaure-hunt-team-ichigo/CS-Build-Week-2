from player import Player
import time
import random
from util_bp import Stack, Queue
import ast

player = Player("Bryant")


def new_path(visited_rooms_graph, room):
    queue = Queue()
    queue.enqueue([(room["room_id"], None)])
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
    while len(player.visited_rooms_graph) < 500:
        room = player.room
        current_exits = player.room["exits"]
        if room["room_id"] not in player.visited_rooms_graph:
            player.visited_rooms_graph[room["room_id"]] = {e: "?" for e in current_exits}
        unexplored_exits = [e for e in current_exits if player.visited_rooms_graph[player.room["room_id"]][e] == "?"]
        if len(unexplored_exits) > 0:
            next_move = random.choice(unexplored_exits)
        else:
            travel_path = new_path(player.visited_rooms_graph, room)
            next_move = travel_path.dequeue()
            next_move = next_move[0]
        print(f"visited rooms: {len(player.visited_rooms_graph)}")
        player.move(next_move)


travel_path = Queue()
directions = ["n", "e", "s", "w"]
opposite_directions = {"n": "s", "e": "w", "s": "n", "w": "e"}
visit_rooms()
