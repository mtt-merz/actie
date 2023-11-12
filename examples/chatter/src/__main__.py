import json
import os
import random
from threading import Thread
import time

from lib import OpenWhisk


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

wsk: OpenWhisk

for i in range(n):
    name = random.choice(list(invocations_counter))
    invocations_counter[name] += 1

    msg = {
        "action": "increment",
        "args": {"value": 2}
    }
    t = Thread(target=wsk.invoke, args=['counter', name, json.dumps(msg)])
    t.start()

    threads.append(t)

# Wait for thread execution
for t in threads:
    t.join()

# Print expected results
for i in invocations_counter.items():
    print('Actor@{} invoked {} times'.format(i[0], i[1]))

print('\nInvocations count: {}'.format(n))
