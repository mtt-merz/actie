import json
import os
import random
from threading import Thread

from lib import OpenWhisk

wsk: OpenWhisk

# planes owned by sky_bridge
planes = [
    {
        "model": "Boeing 757",
        "seats": 200
    },
    {
        "model": "Airbus A321",
        "seats": 220
    },
    {
        "model": "Airbus A220",
        "seats": 145
    }
]

# create users (simulate login)
for nickname in ["Annie", "Bob", "Cathy", "David", "Eve", "Frank"]:
    msg = {
        "action": "init",
        "args": {"nickname": nickname}
    }
    wsk.invoke('user', nickname, json.dumps(msg))

# create operators
for code in ["op_0", "op_1", "op_2"]:
    msg = {
        "action": "init",
        "args": {"name": code}
    }
    wsk.invoke('operator', code, json.dumps(msg))

fligths = [
    {
        "departure": "Milan",
        "arrival": "Rome",
        "plane": {
            "model": "Boeing 747",
            "seats": 200
        },
        "price": 100
    },
    {
        "departure": "Berlin",
        "arrival": "Paris",
        "plane": {
            "model": "Tupolev Tu-144",
        }
    }
]

# Multiple purposes:
#   (1) declare the available actor instances
#   (2) count instance invocations
invocations_counter = {
    'ASDFG': 0,
    'QWERT': 0,
    'POIUY': 0,
    'LKJHG': 0,
    'MNBVC': 0,
    'ZXCVB': 0
}

# 30 is the max number of concurrent invocations
# 60 is the max number of invocations each minute
n = 30

# Invoke n times the 'increment' operation on a random actor
# To test the concurrency, each invokation is sent on a new thread
threads = []


for i in range(n):
    nickname = random.choice(list(invocations_counter))
    invocations_counter[nickname] += 1

    msg = {
        "action": "increment",
        "args": {"value": 2}
    }
    t = Thread(target=wsk.invoke, args=['counter', nickname, json.dumps(msg)])
    t.start()

    threads.append(t)

# Wait for thread execution
for t in threads:
    t.join()

# Print expected results
for i in invocations_counter.items():
    print('Actor@{} invoked {} times'.format(i[0], i[1]))

print('\nInvocations count: {}'.format(n))
