import requests
import json
import time

jason_prince_api_key = "Token ece07b1e0e2fc9e8a6c86ae269422e9afb9de66d"

headers = {
    'Authorization': jason_prince_api_key,
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
        print(res.text)

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


jason = Player("Jason", 0)

jason.sell()
