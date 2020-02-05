import requests
import json
import time

jason_clemons_api_key = "Token 25064e5e6056d2c785295da3e30c023b138b70db"

headers = {
    'Authorization': jason_clemons_api_key,
    'Content-Type': 'application/json'
}

#-----------------------------------SERVER RESPONSE PARSING----------------------------------------#

def parseBalance(res):
    data = json.loads(res)
    
    bal = {
        'cd': data['cooldown'],                 # Cooldown 
        'err': data['errors'],                  # Generated error messages
        'msgs': data['messages']                # Generated messages
    }
    
    return bal

def parsePlayer(res): # Get player inventory / status data
    data = json.loads(res)
    
    status = {
        'body': data['bodywear'],               # Bodywear 
        'cd': data['cooldown'],                 # Cooldown
        'encumbbrance': data['encumbrance'],    # How much are you carrying?
        'err': data['errors'],                  # Generated error messages
        'feet': data['footwear'],               # Footwear
        'gold': data['gold'],                   # Player gold
        'inv': data['inventory'],               # Inventory
        'msgs': data['messages']                # Generated messages
        'name': data['name'],                   # Player name 
        'spd': data['speed'],                   # How fast do you travel?
        'status': data['status'],               # Player status
        'str': data['strength'],                # How much can you carry?
    }
    
    return status

def parseRoom(res): # Get room data
    data = json.loads(res)    
    
    rm = {
        'cd': data['cooldown'],                 # Cooldown
        'coords': data['coordinates'],          # Room coordinates
        'description': data['description'],     # Room description
        'elevation': data['elevation'],         # Room elevation
        'err': data['errors']                   # Generated error messages
        'exits': data['exits'],                 # Room exits
        'id': data['room_id'],                  # Room ID
        'items': data['items'],                 # Items in room
        'itf': False,                           # Items in room: true/false
        'iCnt': None,                           # Number of items in room
        'msgs': data['messages']                # Generated messages
        'terrain': data['terrain'],             # Room's terrain
        'title': data['title'],                 # Room title
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
        
    #---------------------------PARSED DATA VARIABLES---------------------------#            
    # Cooldown
    self.cd = None
    
    # Room data 
    self.room = None
    
    # Player status  
    self.status = None

#---------------------------INIT---------------------------#
    def init(self):
        endpoint = "/adv/init/"
        res = requests.get(
            self.base_url + endpoint,
            headers=headers
        )
        self.room = parseRoom(res.text)

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
        self.current_room = next_room
        print(f'{next_room} Here is our new room.')
        
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
        
        self.room = parseRoom(res.text)

#---------------------------STATUS AND EXAMINE---------------------------#
    def status(self):
        endpoint = "/adv/status/"
        res = requests.post(
            self.base_url + endpoint,
            headers=headers
        )
        print(f'------- {res.text} STATUS')
        
        self.status = parsePlayer(res.text)     # Parses player status data into self.status

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

    def undress(self, item):
        endpoint = "/adv/undress/"
        data = {"name": item}
        res = requests.post(
            self.base_url + endpoint,
            headers=headers,
            data=json.dumps(data)
        )
        print(f'------- {res.text} UNDRESS')

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

#---------------------------TELEPORTAION---------------------------#
    def warp(self):
        endpoint = "/adv/warp/"
        res = requests.post(
            self.base_url + endpoint,
            headers=headers
        )
        print(f'------- {res.text} WARP')

    def recall(self):
        endpoint = "/adv/recall/"
        res = requests.post(
            self.base_url + endpoint,
            headers=headers
        )
        print(f'------- {res.text} RECALL')
