class Queue():

    def __init__(self):
        self.queue = []

    def enqueue(self, value):
        self.queue.append(value)

    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None

    def size(self):
        return len(self.queue)


def bfs(player, starting_vertex, destination_vertex, player_graph):
    q = Queue()
    q.enqueue([starting_vertex])
    visited = set()

    while q.size() > 0:
        path = q.dequeue()
        v = path[-1]
        if v not in visited:
            if v == destination_vertex:
                return path
            visited.add(v)
            for direction in player_graph[v].keys():
                if direction in ["n", "w", "e", "s"]:
                    path_copy = path.copy()
                    dd = player_graph[v][direction]
                    if dd == "?":
                        pass
                    else:
                        path_copy.append(dd)
                        q.enqueue(path_copy)
                else:
                    break


def unexplored_directions(player_graph, room):
    unexplored_directions = []
    for i in ["n", "s", "e", "w"]:
        try:
            if player_graph[room][i] == "?":
                unexplored_directions.append(i)
        except KeyError:
            pass
    return unexplored_directions


def find_unexplored_room(player_graph):
    for i in player_graph:
        ii = unexplored_directions(player_graph, i)
        if len(ii) > 0:
            return i


def find_room_direction(room, next_room):
    for i in ["n", "s", "e", "w"]:
        try:
            if room[i] == next_room:
                return i
        except KeyError:
            pass


def record_room_info(player_graph, response, direction=None, previous_room=None):
    opposite_map = {"n": "s", "s": "n", "e": "w", "w": "e"}
    r = response
    room_id = r.json()["room_id"]
    if room_id not in player_graph:
        player_graph[room_id] = {}
    player_graph[room_id]["title"] = r.json()["title"]
    player_graph[room_id]["description"] = r.json()["description"]
    player_graph[room_id]["coordinates"] = r.json()["coordinates"]
    player_graph[room_id]["messages"] = r.json()["messages"]
    player_graph[room_id]["elevation"] = r.json()["elevation"]
    player_graph[room_id]["terrain"] = r.json()["terrain"]
    if "exits" not in player_graph[room_id]:
        player_graph[room_id]["exits"] = {
            i: "?" for i in r.json()["exits"]}

    if player_graph[previous_room]["exits"][direction] == "?":
        player_graph[previous_room]["exits"][direction] = room_id
    if player_graph[room_id]["exits"][opposite_map[direction]] == "?":
        player_graph[room_id]["exits"][opposite_map[direction]
                                       ] = previous_room

    return room_id
