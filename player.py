import requests
import json
import time

jason_clemons_api_key = "Token 25064e5e6056d2c785295da3e30c023b138b70db"

headers = {
    'Authorization': jason_clemons_api_key,
    'Content-Type': 'application/json'
}


class Player:
    def __init__(self, name, starting_room):
        self.name = name
        self.current_room = starting_room

    def init(self):
        res = requests.get(
            'https://lambda-treasure-hunt.herokuapp.com/api/adv/init/', headers=headers
        )
        res = res.text
        data = json.loads(res)
        print(f'type of: {type(data)}')
        print(data['room_id'])


#---------------------------TREASURE---------------------------#

    def take(self):
        data = {"name": "treasure"}
        res = requests.post(
            'https://lambda-treasure-hunt.herokuapp.com/api/adv/take/', headers=headers, data=json.dumps(data)
        )
        print(f'------- {res.text} TAKING TREASURE')

    def drop(self):
        data = {"name": "treasure"}
        res = requests.post(
            'https://lambda-treasure-hunt.herokuapp.com/api/adv/drop/', headers=headers, data=json.dumps(data)
        )
        print(f'------- {res.text} DROPPING TREASURE')

    def sell(self):
        data = {"name": "treasure"}
        res = requests.post(
            'https://lambda-treasure-hunt.herokuapp.com/api/adv/sell/', headers=headers, data=json.dumps(data)
        )
        print(f'------- {res.text} SELL TREASURE')

    def sell_confirm(self):
        data = {"name": "treasure", "confirm": "yes"}
        res = requests.post(
            'https://lambda-treasure-hunt.herokuapp.com/api/adv/sell/', headers=headers, data=json.dumps(data)
        )
        print(f'------- {res.text} SELL CONFIRM TREASURE')

#---------------------------MOVE---------------------------#

    def move(self, direction):
        print("Direction", direction)
        if direction == "n":
            data = {"direction": "n"}
        if direction == "s":
            data = {"direction": "s"}
        if direction == "e":
            data = {"direction": "e"}
        if direction == "w":
            data = {"direction": "w"}
        res = requests.post(
            'https://lambda-treasure-hunt.herokuapp.com/api/adv/move/', headers=headers, data=json.dumps(data)
        )

    def wise_move(self, direction, room):
        print(f'Direction: {direction} Room: {room}')
        if direction == "n":
            data = {"direction": "n", "next_room": room}
        if direction == "s":
            data = {"direction": "s", "next_room": room}
        if direction == "e":
            data = {"direction": "e", "next_room": room}
        if direction == "w":
            data = {"direction": "w", "next_room": room}
        res = requests.post(
            'https://lambda-treasure-hunt.herokuapp.com/api/adv/move/', headers=headers, data=json.dumps(data)
        )

        next_room = json.loads(res.text)
        self.current_room = next_room
        print(f'{next_room} Here is our new room.')


phade = Player("Phade", 0)

phade.init()
