import requests
import json
import time

jason_clemons_api_key = "Token 25064e5e6056d2c785295da3e30c023b138b70db"

headers = {
    'Authorization': jason_clemons_api_key,
    'Content-Type': 'application/json'
}


#-----------------------------------SERVER RESPONSE PARSING----------------------------------------#

def parseBalance(res):                          # Parse Lambda Coin balance data
    data = json.loads(res)

    bal = {
        'cd': data['cooldown'],                 # Cooldown
        'err': data['errors'],                  # Generated error messages
        'msgs': data['messages']                # Generated messages
    }

    return bal


def parseMine(res):                             # Parse Lambda Coin mining data
    data = json.loads(res)

    mine = {
        'cd': data['cooldown'],                 # Cooldown
        # Description of player when attempting to mine
        'desc': data['description'],
        'err': data['errors'],                  # Generated error messages
        'msgs': data['messages'],               # Generated messages
        'name': data['name']                    # Player name
    }

    return mine


def parsePlayer(res):                           # Parse player inventory / status data
    data = json.loads(res)

    status = {
        'body': data['bodywear'],               # Bodywear
        'cd': data['cooldown'],                 # Cooldown
        'encumbbrance': data['encumbrance'],    # How much are you carrying?
        'err': data['errors'],                  # Generated error messages
        'feet': data['footwear'],               # Footwear
        'gold': data['gold'],                   # Player gold
        'inv': data['inventory'],               # Inventory
        'msgs': data['messages'],               # Generated messages
        'name': data['name'],                   # Player name
        'spd': data['speed'],                   # How fast do you travel?
        'status': data['status'],               # Player status
        'str': data['strength']                 # How much can you carry?
    }

    return status


def parseProof(res):                            # Parse Lambda Coin last valid proof (lvp) data
    data = json.loads(res)

    lvp = {
        'cd': data['cooldown'],                 # Cooldown
        'dl': data['difficulty'],               # Difficulty lvl
        'err': data['errors'],                  # Generated error messages
        'msgs': data['messages'],               # Generated messages
        'proof': data['proof']                  # Proof
    }

    return lvp


def parseRoom(res):                             # Parse room data
    data = json.loads(res)

    rm = {
        'cd': data['cooldown'],                 # Cooldown
        'coords': data['coordinates'],          # Room coordinates
        'description': data['description'],     # Room description
        'elevation': data['elevation'],         # Room elevation
        'err': data['errors'],                  # Generated error messages
        'exits': data['exits'],                 # Room exits
        'id': data['room_id'],                  # Room ID
        'items': data['items'],                 # Items found in room
        'itf': False,                           # Room has items: true/false
        'iCnt': None,                           # Number of items in room
        'msgs': data['messages'],               # Generated messages
        'terrain': data['terrain'],             # Room terrain
        'title': data['title']                  # Room title
    }

    rm['iCnt'] = len(rm['items'])

    if rm['iCnt'] > 0:
        rm['itf'] = True
    else:
        rm['itf'] = False

    return rm


class Player:
    def __init__(self, name, starting_room):
        self.name = name
        self.current_room = starting_room
        self.base_url = "https://lambda-treasure-hunt.herokuapp.com/api"

        #---------------------------PARSED DATA CLASS VARIABLES---------------------------#
        self.lc_balance = None                  # Lambda Coin balance
        self.cd = None                          # Cooldown
        self.lc_mining = None                   # Lambda Coin mining data
        self.lc_proof = None                    # Lambda Coin last valid proof
        self.room = None                        # Room data
        self.p_status = None                    # Player status


#---------------------------INIT---------------------------#


    def init(self):
        endpoint = "/adv/init/"
        res = requests.get(
            self.base_url + endpoint,
            headers=headers
        )

        self.room = parseRoom(res.text)             # Parse room data
        self.cd = self.room['cd']                   # Get cooldown


#---------------------------TREASURE---------------------------#


    def take(self):
        endpoint = "/adv/take/"
        data = {
            "name": "treasure"
        }
        res = requests.post(
            self.base_url + endpoint,
            headers=headers,
            data=json.dumps(data)
        )
        print(f'------- {res.text} TAKING TREASURE')

        self.room = parseRoom(res.text)                 # Parse room data
        self.cd = self.room['cd']                       # Get cooldown

        if self.room['err']:
            print(self.room['err'])
        else:
            print(self.room['msgs'])

    def drop(self):
        endpoint = "/adv/drop/"
        data = {
            "name": "treasure"
        }
        res = requests.post(
            self.base_url + endpoint,
            headers=headers,
            data=json.dumps(data)
        )
        print(f'------- {res.text} DROPPING TREASURE')

        self.room = parseRoom(res.text)                 # Parse room data
        self.cd = self.room['cd']                       # Get cooldown

        if self.room['err']:
            print(self.room['err'])
        else:
            print(self.room['msgs'])

    def sell(self):
        endpoint = "/adv/sell/"
        data = {
            "name": "treasure"
        }
        res = requests.post(
            self.base_url + endpoint,
            headers=headers,
            data=json.dumps(data)
        )
        print(f'------- {res.text} SELL TREASURE')

        self.room = parseRoom(res.text)                 # Parse room data
        self.cd = self.room['cd']                       # Get cooldown

        if self.room['err']:
            print(self.room['err'])
        else:
            print(self.room['msgs'])

    def sell_confirm(self):
        endpoint = "/adv/sell/"
        data = {
            "name": "treasure",
            "confirm": "yes"
        }
        res = requests.post(
            self.base_url + endpoint,
            headers=headers,
            data=json.dumps(data)
        )
        print(f'------- {res.text} SELL CONFIRM TREASURE')

        self.room = parseRoom(res.text)                 # Parse room data
        self.cd = self.room['cd']                       # Get cooldown

        if self.room['err']:
            print(self.room['err'])
        else:
            print(self.room['msgs'])


#---------------------------MOVE---------------------------#


    def move(self, direction):
        print(f'Direction: {direction}')
        endpoint = "/adv/move/"
        data = {
            "direction": direction
        }
        res = requests.post(
            self.base_url + endpoint,
            headers=headers,
            data=json.dumps(data)
        )
        next_room = json.loads(res.text)
        # self.current_room = next_room
        # print(f'{next_room} Here is our new room.')

        self.room = parseRoom(res.text)                 # Parse room data
        self.cd = self.room['cd']                       # Get cooldown

    def wise_move(self, direction, room):
        print(f'Direction: {direction} Room: {room}')
        endpoint = "/adv/move/"
        data = {
            "direction": direction,
            "next_room": room
        }
        res = requests.post(
            self.base_url + endpoint,
            headers=headers,
            data=json.dumps(data)
        )
        next_room = json.loads(res.text)
        self.current_room = next_room
        print(f'{next_room} Here is our new room.')

        self.room = parseRoom(res.text)                 # Parse room data
        self.cd = self.room['cd']                       # Get cooldown


#---------------------------CARRY AND RECEIVE---------------------------#


    def carry(self, item):
        endpoint = '/adv/carry/'
        data = {
            'name': item
        }
        res = requests.post(
            self.base_url + endpoint,
            headers=headers,
            data=json.dumps(data)
        )

        self.room = parseRoom(res.text)                 # Parse room data
        self.cd = self.room['cd']                       # Get cooldown

        if self.room['err']:
            print(self.room['err'])
        else:
            print(self.room['msgs'])

    def receive(self):
        endpoint = '/adv/receive/'
        res = requests.post(
            self.base_url + endpoint,
            headers=headers
        )

        self.room = parseRoom(res.text)                 # Parse room data
        self.cd = self.room['cd']                       # Get cooldown

        if self.room['err']:
            print(self.room['err'])
        else:
            print(self.room['msgs'])


#---------------------------STATUS AND EXAMINE---------------------------#


    def status(self):
        endpoint = "/adv/status/"
        res = requests.post(
            self.base_url + endpoint,
            headers=headers
        )
        print(f'------- {res.text} STATUS')

        self.p_status = parsePlayer(res.text)             # Parse player data
        self.cd = self.p_status['cd']                     # Get cooldown

    def examine(self):
        endpoint = "/adv/examine/"
        data = {
            "name": "Wishing Well"
        }
        res = requests.post(
            self.base_url + endpoint,
            headers=headers,
            data=json.dumps(data)
        )
        print(f'------- {res.text} WISHING WELL INFO')


#---------------------------EQUIPMENT (WEAR AND UNDRESS)---------------------------#


    def wear(self, item):
        endpoint = "/adv/wear/"
        data = {"name": item}
        res = requests.post(
            self.base_url + endpoint,
            headers=headers,
            data=json.dumps(data)
        )
        print(f'------- {res.text} WEAR')

        self.status = parseStatus(res.text)             # Parse player data
        self.cd = self.status['cd']                     # Get cooldown

        if self.status['err']:
            print(self.room['err'])
        else:
            print(self.room['msgs'])

    def undress(self, item):
        endpoint = "/adv/undress/"
        data = {"name": item}
        res = requests.post(
            self.base_url + endpoint,
            headers=headers,
            data=json.dumps(data)
        )
        print(f'------- {res.text} UNDRESS')

        self.status = parseStatus(res.text)             # Parse player data
        self.cd = self.status['cd']                     # Get cooldown

        if self.status['err']:
            print(self.room['err'])
        else:
            print(self.room['msgs'])


#---------------------------NAME CHANGER---------------------------#


    def change_name(self, name):
        endpoint = "/adv/change_name/"
        data = {
            "name": name
        }
        res = requests.post(
            self.base_url + endpoint,
            headers=headers,
            data=json.dumps(data)
        )
        print(f'------- {res.text} CHANGE NAME')


#---------------------------FAST MOVE---------------------------#


    def dash(self, direction, number_of_rooms, sequential_room_ids):
        endpoint = "/adv/dash/"
        data = {
            "direction": direction,
            "num_rooms": number_of_rooms,
            "next_room_ids": sequential_room_ids
        }
        res = requests.post(
            self.base_url + endpoint,
            headers=headers,
            data=json.dumps(data)
        )
        print(f'------- {res.text} DASH')

        self.room = parseRoom(res.text)                 # Parse room data
        self.cd = self.room['cd']                       # Get cooldown

    def flight(self, direction):
        endpoint = "/adv/fly/"
        data = {
            "direction": direction
        }
        res = requests.post(
            self.base_url + endpoint,
            headers=headers,
            data=json.dumps(data)
        )
        print(f'------- {res.text} FLY')

        self.room = parseRoom(res.text)                 # Parse room data
        self.cd = self.room['cd']                       # Get cooldown


#---------------------------TELEPORTAION---------------------------#


    def warp(self):
        endpoint = "/adv/warp/"
        res = requests.post(
            self.base_url + endpoint,
            headers=headers
        )
        print(f'------- {res.text} WARP')

        self.room = parseRoom(res.text)                 # Parse room data
        self.cd = self.room['cd']                       # Get cooldown

    def recall(self):
        endpoint = "/adv/recall/"
        res = requests.post(
            self.base_url + endpoint,
            headers=headers
        )
        print(f'------- {res.text} RECALL')

        self.room = parseRoom(res.text)                 # Parse room data
        self.cd = self.room['cd']                       # Get cooldown


#---------------------------TRANSMOGRIFY---------------------------#


    def transmogrify(self, item):
        endpoint = '/adv/transmogrify/'
        res = requests.post(
            self.base_url + endpoint,
            headers=headers
        )

        self.room = parseRoom(res.text)                 # Parse room data
        self.cd = self.room['cd']                       # Get cooldown

        if self.room['err']:
            print(self.room['err'])
        else:
            print(self.room['msgs'])


#---------------------------LAMBDA COINS---------------------------#


    def mine(self, proof):
        endpoint = '/bc/mine/'
        res = requests.post(
            self.base_url + endpoint,
            headers=headers
        )

        self.lc_mining = parseMine(res.text)             # Parse mining data
        self.cd = self.lc_mining['cd']                   # Get cooldown

        if self.lc_mining['err']:
            print(self.lc_mining['err'])
        else:
            print(self.lc_mining['msgs'])

    def proof(self):
        endpoint = '/bc/last_proof/'
        res = requests.get(
            self.base_url + endpoint,
            headers=headers
        )

        # Parse last valid proof data
        self.lc_proof = parseProof(res.text)
        self.cd = self.lc_proof['cd']                    # Get cooldown

    def balance(self):
        endpoint = '/bc/get_balance'
        res = requests.get(
            self.base_url + endpoint,
            headers=headers
        )

        # Parse Lambda Coin balance data
        self.lc_balance = parseBalance(res.text)
        self.cd = self.lc_balance['cd']                  # Get cooldown
