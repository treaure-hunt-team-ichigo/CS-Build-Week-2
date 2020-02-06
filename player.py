import requests
from requests import Request
import json
import time
from decouple import config
import time
import ast


visited_rooms_graph = "files/visited_rooms_graph.json"
rooms_file = "files/rooms_graph.json"
visited_rooms_track = "files/visited_rooms_track.json"
directions = ["n", "e", "s", "w"]
opposite_directions = {"n": "s", "e": "w", "s": "n", "w": "e"}
base_url = "https://lambda-treasure-hunt.herokuapp.com/api"
auth_key = config("api_key")
headers = {"Authorization": auth_key, "Content-Type": "application/json"}


class Player:
    def __init__(self, name):
        self.name = name
        self.room = None  # Room data
        self.rooms = {}
        self.visited_rooms_track = ast.literal_eval(open(visited_rooms_track, "r").read())
        self.room_grid = []
        self.visited_rooms_graph = ast.literal_eval(open(visited_rooms_graph, "r").read())
        self.grid_size = 0
        self.room_graph = ast.literal_eval(open(rooms_file, "r").read())

        # ---------------------------PARSED DATA CLASS VARIABLES---------------------------#
        self.lc_balance = None  # Lambda Coin balance
        # self.status["cooldown"] = None  # Cooldown
        self.lc_mining = None  # Lambda Coin mining data
        self.lc_proof = None  # Lambda Coin last valid proof
        self.status = {}
        self.status["cooldown"] = 0  # Player status
        # self.init = None
        self.start = self.get_init()

    def get_status(self):
        method2 = "POST"
        endpoint = "/adv/status/"
        url2 = base_url + endpoint
        s = requests.request(method2, url2, headers=headers)
        self.status = s.json()

    def get_init(self):
        initmethod = "GET"
        initendpoint = "/adv/init/"
        url = base_url + initendpoint
        r = requests.request("GET", url, headers=headers)
        self.room = r.json()
        exits = self.room["exits"]
        try:
            self.visited_rooms_graph[self.room["room_id"]]
            self.room_graph[self.room["room_id"]]
        except KeyError:
            self.visited_rooms_graph[self.room["room_id"]] = {e: "?" for e in exits}
            self.room_graph[self.room["room_id"]] = self.room
        finally:
            self.visited_rooms_track.add(self.room["room_id"])
            self.write()

    def callapi(self, method, endpoint, payload=""):
        # print(self.status["cooldown"])
        # self.get_status()
        # sleepy = self.status["cooldown"] * 1
        sleepy = self.room["cooldown"] * 1
        print(f"sleepy {sleepy}")
        time.sleep(sleepy)
        url = base_url + endpoint
        errors = []
        # try:
        r = requests.request(method, url, data=json.dumps(payload), headers=headers)
        # print(r.__dict__)
        return r.json()
        # except:
        #     errors.append("Unable to get URL. Please make sure it's valid and try again.")
        #     return {"error": errors}

    def inits(self):
        exits = self.room["exits"]
        self.visited_rooms_graph[self.room["room_id"]] = {exit: "?" for exit in exits}
        # if self.room["room_id"] not in self.visited_rooms_track:
        self.visited_rooms_track.add(self.room["room_id"])
        # if self.room["room_id"] not in self.room_graph:
        self.room_graph[self.room["room_id"]] = self.room
        self.write()

    def write(self):
        with open(visited_rooms_graph, "w") as f:
            f.write(str(self.visited_rooms_graph))

        with open(rooms_file, "w") as f:
            f.write(str(self.room_graph))

        with open(visited_rooms_track, "w") as f:
            f.write(str(self.visited_rooms_track))

    # ---------------------------TREASURE---------------------------#
    def take(self):
        method = "POST"
        endpoint = "/adv/take/"
        data = {"name": "treasure"}
        res = self.callapi(method, endpoint, payload=data)
        # res = requests.post(self.base_url + endpoint, headers=headers, data=json.dumps(data))
        print(f"------- {res.text} TAKING TREASURE")

        # self.room = parseRoom(res.text)  # Parse room data
        # self.status['cooldown'] = self.room["cd"]  # Get cooldown

        if self.room["err"]:
            print(self.room["err"])
        else:
            print(self.room["msgs"])

    def drop(self):
        method = "POST"
        endpoint = "/adv/drop/"
        data = {"name": "treasure"}
        res = self.callapi(method, endpoint, payload=data)
        # res = requests.post(self.base_url + endpoint, headers=headers, data=json.dumps(data))
        # print(f"------- {res.text} DROPPING TREASURE")

        # self.room = parseRoom(res.text)  # Parse room data
        # self.status['cooldown'] = self.room["cd"]  # Get cooldown

        if self.room["err"]:
            print(self.room["err"])
        else:
            print(self.room["msgs"])

    def sell(self):
        method = "POST"
        endpoint = "/adv/sell/"
        data = {"name": "treasure"}
        res = self.callapi(method, endpoint, payload=data)
        # res = requests.post(self.base_url + endpoint, headers=headers, data=json.dumps(data))
        # print(f"------- {res.text} SELL TREASURE")

        # self.room = parseRoom(res.text)  # Parse room data
        # self.status['cooldown'] = self.room["cd"]  # Get cooldown

        if self.room["err"]:
            print(self.room["err"])
        else:
            print(self.room["msgs"])

    def sell_confirm(self):
        method = "POST"
        endpoint = "/adv/sell/"
        data = {"name": "treasure", "confirm": "yes"}
        res = self.callapi(method, endpoint, payload=data)
        # res = requests.post(self.base_url + endpoint, headers=headers, data=json.dumps(data))
        # print(f"------- {res.text} SELL CONFIRM TREASURE")

        # self.room = parseRoom(res.text)  # Parse room data
        # self.status['cooldown'] = self.room["cd"]  # Get cooldown

        if self.room["err"]:
            print(self.room["err"])
        else:
            print(self.room["msgs"])

    # ---------------------------MOVE---------------------------#
    def move(self, direction):
        try:
            check_map = self.visited_rooms_graph[self.room["room_id"]][direction]
            print(f"check_map: {check_map}")
            if check_map == "?":
                self.move_blind(direction)
            else:
                self.wise_move(direction, check_map)
                print("wise_move")
        except KeyError:
            print("not an known exit direction")

    def move_blind(self, direction):
        print("move_blind")
        opposite_directions = {"n": "s", "e": "w", "s": "n", "w": "e"}
        method = "POST"
        endpoint = "/adv/move/"
        data = {"direction": direction}
        previous_room = self.room
        self.room = self.callapi(method, endpoint, payload=data)
        if self.room["room_id"] not in self.visited_rooms_graph:
            exits = self.room["exits"]
            self.visited_rooms_graph[self.room["room_id"]] = {exit: "?" for exit in exits}
        if self.room["room_id"] not in self.visited_rooms_track:
            self.visited_rooms_track.add(self.room["room_id"])
        if self.room["room_id"] not in self.room_graph:
            self.room_graph[self.room["room_id"]] = self.room
        self.visited_rooms_graph[previous_room["room_id"]][direction] = self.room["room_id"]
        self.visited_rooms_graph[self.room["room_id"]][opposite_directions[direction]] = previous_room["room_id"]
        self.write()

    def wise_move(self, direction, room):
        # next_room_id = self.visited_rooms_graph[self.room["room_id"]][direction]
        print(room)
        method = "POST"
        endpoint = "/adv/move/"
        data = {"direction": direction, "next_room_id": str(room)}
        self.room = self.callapi(method, endpoint, payload=data)
        if self.room["room_id"] not in self.room_graph:
            self.room_graph[self.room["room_id"]] = self.room
        self.write()

    # ---------------------------CARRY AND RECEIVE---------------------------#
    def carry(self, item):
        endpoint = "/adv/carry/"
        data = {"name": item}
        res = requests.post(self.base_url + endpoint, headers=headers)

        self.room = parseRoom(res.text)  # Parse room data
        self.status["cooldown"] = self.room["cd"]  # Get cooldown

        if self.room["err"]:
            print(self.room["err"])
        else:
            print(self.room["msgs"])

    def receive(self):
        endpoint = "/adv/receive/"
        res = requests.post(self.base_url + endpoint, headers=headers)

        self.room = parseRoom(res.text)  # Parse room data
        self.status["cooldown"] = self.room["cd"]  # Get cooldown

        if self.room["err"]:
            print(self.room["err"])
        else:
            print(self.room["msgs"])

    # ---------------------------STATUS AND EXAMINE---------------------------#

    def examine(self):
        endpoint = "/adv/examine/"
        data = {"name": "Wishing Well"}
        res = requests.post(self.base_url + endpoint, headers=headers, data=json.dumps(data))
        print(f"------- {res.text} WISHING WELL INFO")

    # ---------------------------EQUIPMENT (WEAR AND UNDRESS)---------------------------#
    def wear(self, item):
        endpoint = "/adv/wear/"
        data = {"name": item}
        res = requests.post(self.base_url + endpoint, headers=headers, data=json.dumps(data))
        print(f"------- {res.text} WEAR")

        self.p_status = parsePlayer(res.text)  # Parse player data
        self.status["cooldown"] = self.p_status["cd"]  # Get cooldown

        if self.p_status["err"]:
            print(self.room["err"])
        else:
            print(self.room["msgs"])

    def undress(self, item):
        endpoint = "/adv/undress/"
        data = {"name": item}
        res = requests.post(self.base_url + endpoint, headers=headers, data=json.dumps(data))
        print(f"------- {res.text} UNDRESS")

        self.p_status = parsePlayer(res.text)  # Parse player data
        self.status["cooldown"] = self.p_status["cd"]  # Get cooldown

        if self.p_status["err"]:
            print(self.room["err"])
        else:
            print(self.room["msgs"])

    # ---------------------------NAME CHANGER---------------------------#
    def change_name(self, name):
        endpoint = "/adv/change_name/"
        data = {"name": name}
        res = requests.post(self.base_url + endpoint, headers=headers, data=json.dumps(data))
        print(f"------- {res.text} CHANGE NAME")

    # ---------------------------FAST MOVE---------------------------#
    def dash(self, direction, number_of_rooms, sequential_room_ids):
        endpoint = "/adv/dash/"
        data = {"direction": direction, "num_rooms": number_of_rooms, "next_room_ids": sequential_room_ids}
        res = requests.post(self.base_url + endpoint, headers=headers, data=json.dumps(data))
        print(f"------- {res.text} DASH")

        self.room = parseRoom(res.text)  # Parse room data
        self.status["cooldown"] = self.room["cd"]  # Get cooldown

    def flight(self, direction):
        endpoint = "/adv/fly/"
        data = {"direction": direction}
        res = requests.post(self.base_url + endpoint, headers=headers, data=json.dumps(data))
        print(f"------- {res.text} FLY")

        self.room = parseRoom(res.text)  # Parse room data
        self.status["cooldown"] = self.room["cd"]  # Get cooldown

    # ---------------------------TELEPORTAION---------------------------#
    def warp(self):
        endpoint = "/adv/warp/"
        res = requests.post(self.base_url + endpoint, headers=headers)
        print(f"------- {res.text} WARP")

        self.room = parseRoom(res.text)  # Parse room data
        self.status["cooldown"] = self.room["cd"]  # Get cooldown

    def recall(self):
        endpoint = "/adv/recall/"
        res = requests.post(self.base_url + endpoint, headers=headers)
        print(f"------- {res.text} RECALL")

        self.room = parseRoom(res.text)  # Parse room data
        self.status["cooldown"] = self.room["cd"]  # Get cooldown

    # ---------------------------TRANSMOGRIFY---------------------------#
    def transmogrify(self, item):
        endpoint = "/adv/transmogrify/"
        res = requests.post(self.base_url + endpoint, headers=headers)

        self.room = parseRoom(res.text)  # Parse room data
        self.status["cooldown"] = self.room["cd"]  # Get cooldown

        if self.room["err"]:
            print(self.room["err"])
        else:
            print(self.room["msgs"])

    # ---------------------------LAMBDA COINS---------------------------#
    def mine(self, proof):
        endpoint = "/bc/mine/"
        res = requests.post(self.base_url + endpoint, headers=headers)

        self.lc_mining = parseMine(res.text)  # Parse mining data
        self.status["cooldown"] = self.lc_mining["cd"]  # Get cooldown

        if self.lc_mining["err"]:
            print(self.lc_mining["err"])
        else:
            print(self.lc_mining["msgs"])

    def proof(self):
        endpoint = "/bc/last_proof/"
        res = requests.get(self.base_url + endpoint, headers=headers)

        self.lc_proof = parseProof(res.text)  # Parse last valid proof data
        self.status["cooldown"] = self.lc_proof["cd"]  # Get cooldown

    def balance(self):
        endpoint = "/bc/get_balance"
        res = requests.get(self.base_url + endpoint, headers=headers)

        self.lc_balance = parseBalance(res.text)  # Parse Lambda Coin balance data
        self.status["cooldown"] = self.lc_balance["cd"]  # Get cooldown

    def load_graph(self, room_graph):
        num_rooms = len(room_graph)
        rooms = [None] * num_rooms
        grid_size = 1
        for i in range(0, num_rooms):
            x = room_graph[i][0][0]
            grid_size = max(grid_size, room_graph[i][0][0], room_graph[i][0][1])
            self.rooms[i] = Room(f"Room {i}", f"({room_graph[i][0][0]},{room_graph[i][0][1]})", i, room_graph[i][0][0], room_graph[i][0][1])
        self.room_grid = []
        grid_size += 1
        self.grid_size = grid_size
        for i in range(0, grid_size):
            self.room_grid.append([None] * grid_size)
        for room_id in room_graph:
            room = self.rooms[room_id]
            self.room_grid[room.x][room.y] = room
            if "n" in room_graph[room_id][1]:
                self.rooms[room_id].connect_rooms("n", self.rooms[room_graph[room_id][1]["n"]])
            if "s" in room_graph[room_id][1]:
                self.rooms[room_id].connect_rooms("s", self.rooms[room_graph[room_id][1]["s"]])
            if "e" in room_graph[room_id][1]:
                self.rooms[room_id].connect_rooms("e", self.rooms[room_graph[room_id][1]["e"]])
            if "w" in room_graph[room_id][1]:
                self.rooms[room_id].connect_rooms("w", self.rooms[room_graph[room_id][1]["w"]])
        self.starting_room = self.rooms[0]


# -----------------------------------SERVER RESPONSE PARSING----------------------------------------#


def parseBalance(res):  # Parse Lambda Coin balance data
    data = json.loads(res)

    bal = {
        "cd": data["cooldown"],  # Cooldown
        "err": data["errors"],  # Generated error messages
        "msgs": data["messages"],  # Generated messages
    }

    return bal


def parseMine(res):  # Parse Lambda Coin mining data
    data = json.loads(res)

    mine = {
        "cd": data["cooldown"],  # Cooldown
        "desc": data["description"],  # Description of player when attempting to mine
        "err": data["errors"],  # Generated error messages
        "msgs": data["messages"],  # Generated messages
        "name": data["name"],  # Player name
    }

    return mine


def parsePlayer(res):  # Parse player inventory / status data
    data = json.loads(res)

    status = {
        "body": data["bodywear"],  # Bodywear
        "cd": data["cooldown"],  # Cooldown
        "encumbbrance": data["encumbrance"],  # How much are you carrying?
        "err": data["errors"],  # Generated error messages
        "feet": data["footwear"],  # Footwear
        "gold": data["gold"],  # Player gold
        "inv": data["inventory"],  # Inventory
        "msgs": data["messages"],  # Generated messages
        "name": data["name"],  # Player name
        "spd": data["speed"],  # How fast do you travel?
        "status": data["status"],  # Player status
        "str": data["strength"],  # How much can you carry?
    }

    return status


def parseProof(res):  # Parse Lambda Coin last valid proof (lvp) data
    data = json.loads(res)

    lvp = {
        "cd": data["cooldown"],  # Cooldown
        "dl": data["difficulty"],  # Difficulty lvl
        "err": data["errors"],  # Generated error messages
        "msgs": data["messages"],  # Generated messages
        "proof": data["proof"],  # Proof
    }

    return lvp


def parseRoom(res):  # Parse room data
    data = json.loads(res)

    rm = {
        "cd": data["cooldown"],  # Cooldown
        "coords": data["coordinates"],  # Room coordinates
        "description": data["description"],  # Room description
        "elevation": data["elevation"],  # Room elevation
        "err": data["errors"],  # Generated error messages
        "exits": data["exits"],  # Room exits
        "id": data["room_id"],  # Room ID
        "items": data["items"],  # Items found in room
        "itf": False,  # Room has items: true/false
        "iCnt": None,  # Number of items in room
        "msgs": data["messages"],  # Generated messages
        "terrain": data["terrain"],  # Room terrain
        "title": data["title"],  # Room title
    }

    rm["iCnt"] = len(rm["items"])

    if rm["iCnt"] > 0:
        rm["itf"] = True
    else:
        rm["itf"] = False

    return rm
