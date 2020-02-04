import requests
import json
import time

jason_clemons_api_key = "Token 25064e5e6056d2c785295da3e30c023b138b70db"

headers = {
    'Authorization': jason_clemons_api_key,
    'Content-Type': 'application/json'
}


def parseRoom(res):
    data = json.loads(res)
    rm = {
        'id': data['room_id'],
        'coords': data['coordinates'],
        'exits': data['exits'],
        'elevation': data['elevation'],
        'terrain': data['terrain'],
        'cd': data['cooldown'],
        'description': data['description'],
        'title': data['title'],
        'items': data['items'],
    }
    
    print(rm)
    return rm


class Player:
    def __init__(self, name, starting_room):
        self.name = name
        self.current_room = starting_room
        self.base_url = "https://lambda-treasure-hunt.herokuapp.com/api"

#---------------------------INIT---------------------------#
    def init(self):
        endpoint = "/adv/init/"
        res = requests.get(
            self.base_url + endpoint,
            headers=headers
        )
        parseRoom(res.text)
     


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
        data = {"name": "treasure"}
        res = requests.post(
            self.base_url + endpoint,
            headers=headers,
            data=json.dumps(data)
        )
        print(f'------- {res.text} SELL TREASURE')

    def sell_confirm(self):
        endpoint = "/adv/sell/"
        data = {"name": "treasure", "confirm": "yes"}
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
        data = {"direction": direction}
        res = requests.post(
            self.base_url + endpoint,
            headers=headers,
            data=json.dumps(data)
        )
        next_room = json.loads(res.text)
        self.current_room = next_room
        print(f'{next_room} Here is our new room.')

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

#---------------------------STATUS AND EXAMINE---------------------------#
    def status(self):
        endpoint = "/adv/status/"
        res = requests.post(self.base_url + endpoint, headers=headers)
        print(f'------- {res.text} STATUS')

    def examine(self):
        endpoint = "/adv/examine/"
        data = {"name": "Wishing Well"}
        res = requests.post(
            self.base_url + endpoint,
            headers=headers,
            data=json.dumps(data)
        )
        print(f'------- {res.text} WISHING WELL INFO')

#---------------------------EQUIPMENT (WEAR AND UNDRESS)---------------------------#
    def wear(self, item):
        data = {"name": item}
        res = requests.post(
            'https://lambda-treasure-hunt.herokuapp.com/api/adv/wear/', headers=headers, data=json.dumps(data)
        )
        print(f'------- {res.text} WEAR')

    def undress(self, item):
        data = {"name": item}
        res = requests.post(
            'https://lambda-treasure-hunt.herokuapp.com/api/adv/undress/', headers=headers, data=json.dumps(data)
        )
        print(f'------- {res.text} UNDRESS')

#---------------------------NAME CHANGER---------------------------#
    def change_name(self, name):
        data = {"name": name}
        res = requests.post(
            'https://lambda-treasure-hunt.herokuapp.com/api/adv/change_name/', headers=headers, data=json.dumps(data)
        )
        print(f'------- {res.text} CHANGE NAME')

#---------------------------FAST MOVE---------------------------#
#     def dash(self, direction, number_of_rooms, sequential_room_ids):
#         data = {"direction":"n", "num_rooms":"5", "next_room_ids":"10,19,20,63,72"
# }


phade = Player("Phade", 0)

phade.init()
