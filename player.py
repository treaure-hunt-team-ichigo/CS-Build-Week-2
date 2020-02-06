import requests
import json
import time
from decouple import config
import time
import ast

auth_key = config("api_key")


headers = {"Authorization": auth_key, "Content-Type": "application/json"}


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


visited_rooms_graph = "files/visited_rooms_graph.json"
rooms_file = "files/rooms_graph.json"
visited_rooms_track = "files/visited_rooms_track.json"
directions = ["n", "e", "s", "w"]
opposite_directions = {"n": "s", "e": "w", "s": "n", "w": "e"}


class Player:
    def __init__(self, name):
        self.name = name
        self.current_room = None
        self.room = None  # Room data
        self.rooms = {}
        self.visited_rooms_track = None
        self.room_grid = []
        self.visited_rooms_graph = {}
        self.grid_size = 0
        self.base_url = "https://lambda-treasure-hunt.herokuapp.com/api"

        # ---------------------------PARSED DATA CLASS VARIABLES---------------------------#
        self.lc_balance = None  # Lambda Coin balance
        self.cd = None  # Cooldown
        self.lc_mining = None  # Lambda Coin mining data
        self.lc_proof = None  # Lambda Coin last valid proof

        self.p_status = None  # Player status
        self.init = self.init()

    # ---------------------------INIT---------------------------#
    def init(self):
        # load graph
        self.visited_rooms_graph = ast.literal_eval(open(visited_rooms_graph, "r").read())

        # load rooms set
        self.visited_rooms_track = ast.literal_eval(open(visited_rooms_track, "r").read())

        # rooms graph file
        self.rooms = ast.literal_eval(open(rooms_file, "r").read())

        endpoint = "/adv/init/"
        res = requests.get(self.base_url + endpoint, headers=headers)

        self.room = parseRoom(res.text)  # Parse room data
        self.current_room = parseRoom(res.text)
        self.cd = self.room["cd"]  # Get cooldown
        # rooms dict
        keys = ["coords", "description", "elevation", "err", "exits", "id", "terrain", "title"]
        self.rooms[self.room["id"]] = {k: v for (k, v) in self.room.items() if k in keys}

    def write(self):
        # visited_rooms_graph = "files/visited_rooms_graph2.json"
        # rooms_file = "files/rooms_graph.json"
        # visited_rooms_track = "files/visited_rooms_track.json"
        # g = player.visited_rooms_graph
        # j = json.dumps(g)
        # f = open(visited_rooms_graph, "w")
        # f.write(j)
        # f.close()
        with open(visited_rooms_graph, "w") as f:
            f.write(str(self.visited_rooms_graph))

        r = self.rooms
        k = json.dumps(r)
        f = open(rooms_file, "w")
        f.write(k)
        f.close()

        # with open(rooms_file, "w") as f:
        #     f.write(str(self.rooms))

        with open(visited_rooms_track, "w") as f:
            f.write(str(self.visited_rooms_track))

    # ---------------------------TREASURE---------------------------#
    def take(self):
        endpoint = "/adv/take/"
        data = {"name": "treasure"}
        res = requests.post(self.base_url + endpoint, headers=headers, data=json.dumps(data))
        print(f"------- {res.text} TAKING TREASURE")

        self.room = parseRoom(res.text)  # Parse room data
        self.cd = self.room["cd"]  # Get cooldown

        if self.room["err"]:
            print(self.room["err"])
        else:
            print(self.room["msgs"])

    def drop(self):
        endpoint = "/adv/drop/"
        data = {"name": "treasure"}
        res = requests.post(self.base_url + endpoint, headers=headers, data=json.dumps(data))
        print(f"------- {res.text} DROPPING TREASURE")

        self.room = parseRoom(res.text)  # Parse room data
        self.cd = self.room["cd"]  # Get cooldown

        if self.room["err"]:
            print(self.room["err"])
        else:
            print(self.room["msgs"])

    def sell(self):
        endpoint = "/adv/sell/"
        data = {"name": "treasure"}
        res = requests.post(self.base_url + endpoint, headers=headers, data=json.dumps(data))
        print(f"------- {res.text} SELL TREASURE")

        self.room = parseRoom(res.text)  # Parse room data
        self.cd = self.room["cd"]  # Get cooldown

        if self.room["err"]:
            print(self.room["err"])
        else:
            print(self.room["msgs"])

    def sell_confirm(self):
        endpoint = "/adv/sell/"
        data = {"name": "treasure", "confirm": "yes"}
        res = requests.post(self.base_url + endpoint, headers=headers, data=json.dumps(data))
        print(f"------- {res.text} SELL CONFIRM TREASURE")

        self.room = parseRoom(res.text)  # Parse room data
        self.cd = self.room["cd"]  # Get cooldown

        if self.room["err"]:
            print(self.room["err"])
        else:
            print(self.room["msgs"])

    # ---------------------------MOVE---------------------------#
    def move(self, direction):
        self.status()
        print(f"Cooldown: {self.cd}")
        print(f"Direction: {direction}")
        time.sleep(self.cd)
        try:
            check_map = self.visited_rooms_graph[self.room["id"]][direction]
            print(f"check_map: {check_map}")
            if check_map == "?":
                self.move_blind(direction)
                print("move_blind")
            else:
                self.wise_move(direction, check_map)
                print("wise_move")
        except KeyError:
            print("not an known exit direction")

        # self.cd = self.room["cd"]  # Get cooldown
        self.write()

    def move_blind(self, direction):
        # self.status()
        # time.sleep(self.cd)
        # check_map = self.visited_rooms_graph[self.room["id"]][next_move]
        # print("Cooldown: {self.cd}")
        # print(f"Direction: {direction}")
        endpoint = "/adv/move/"
        data = {"direction": direction}
        res = requests.post(self.base_url + endpoint, headers=headers, data=json.dumps(data))
        next_room = json.loads(res.text)
        # print(res.text)
        self.room = parseRoom(res.text)  # Parse room data
        # self.cd = self.room["cd"]  # Get cooldown
        # self.write()

    def wise_move(self, direction, room):
        # print(f"Direction: {direction} Room: {room}")
        endpoint = "/adv/move/"
        data = {"direction": direction, "next_room": room}
        res = requests.post(self.base_url + endpoint, headers=headers, data=json.dumps(data))
        # next_room = json.loads(res.text)
        # self.current_room = next_room
        # print(f"{next_room} Here is our new room.")

        self.room = parseRoom(res.text)  # Parse room data
        # self.cd = self.room["cd"]  # Get cooldown

    # ---------------------------CARRY AND RECEIVE---------------------------#
    def carry(self, item):
        endpoint = "/adv/carry/"
        data = {"name": item}
        res = requests.post(self.base_url + endpoint, headers=headers)

        self.room = parseRoom(res.text)  # Parse room data
        self.cd = self.room["cd"]  # Get cooldown

        if self.room["err"]:
            print(self.room["err"])
        else:
            print(self.room["msgs"])

    def receive(self):
        endpoint = "/adv/receive/"
        res = requests.post(self.base_url + endpoint, headers=headers)

        self.room = parseRoom(res.text)  # Parse room data
        self.cd = self.room["cd"]  # Get cooldown

        if self.room["err"]:
            print(self.room["err"])
        else:
            print(self.room["msgs"])

    # ---------------------------STATUS AND EXAMINE---------------------------#
    def status(self):
        endpoint = "/adv/status/"
        res = requests.post(self.base_url + endpoint, headers=headers)
        # print(f"------- {res.text} STATUS")

        self.p_status = parsePlayer(res.text)  # Parse player data
        self.cd = self.p_status["cd"]  # Get cooldown

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
        self.cd = self.p_status["cd"]  # Get cooldown

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
        self.cd = self.p_status["cd"]  # Get cooldown

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
        self.cd = self.room["cd"]  # Get cooldown

    def flight(self, direction):
        endpoint = "/adv/fly/"
        data = {"direction": direction}
        res = requests.post(self.base_url + endpoint, headers=headers, data=json.dumps(data))
        print(f"------- {res.text} FLY")

        self.room = parseRoom(res.text)  # Parse room data
        self.cd = self.room["cd"]  # Get cooldown

    # ---------------------------TELEPORTAION---------------------------#
    def warp(self):
        endpoint = "/adv/warp/"
        res = requests.post(self.base_url + endpoint, headers=headers)
        print(f"------- {res.text} WARP")

        self.room = parseRoom(res.text)  # Parse room data
        self.cd = self.room["cd"]  # Get cooldown

    def recall(self):
        endpoint = "/adv/recall/"
        res = requests.post(self.base_url + endpoint, headers=headers)
        print(f"------- {res.text} RECALL")

        self.room = parseRoom(res.text)  # Parse room data
        self.cd = self.room["cd"]  # Get cooldown

    # ---------------------------TRANSMOGRIFY---------------------------#
    def transmogrify(self, item):
        endpoint = "/adv/transmogrify/"
        res = requests.post(self.base_url + endpoint, headers=headers)

        self.room = parseRoom(res.text)  # Parse room data
        self.cd = self.room["cd"]  # Get cooldown

        if self.room["err"]:
            print(self.room["err"])
        else:
            print(self.room["msgs"])

    # ---------------------------LAMBDA COINS---------------------------#
    def mine(self, proof):
        endpoint = "/bc/mine/"
        res = requests.post(self.base_url + endpoint, headers=headers)

        self.lc_mining = parseMine(res.text)  # Parse mining data
        self.cd = self.lc_mining["cd"]  # Get cooldown

        if self.lc_mining["err"]:
            print(self.lc_mining["err"])
        else:
            print(self.lc_mining["msgs"])

    def proof(self):
        endpoint = "/bc/last_proof/"
        res = requests.get(self.base_url + endpoint, headers=headers)

        self.lc_proof = parseProof(res.text)  # Parse last valid proof data
        self.cd = self.lc_proof["cd"]  # Get cooldown

    def balance(self):
        endpoint = "/bc/get_balance"
        res = requests.get(self.base_url + endpoint, headers=headers)

        self.lc_balance = parseBalance(res.text)  # Parse Lambda Coin balance data
        self.cd = self.lc_balance["cd"]  # Get cooldown
