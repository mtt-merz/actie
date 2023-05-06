import json
import os
import random
from threading import Thread
import time

from actie import OpenWhisk


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

# Record starting time, for logging purposes
start_time = time.time()

# 30 is the max number of concurrent invocations
# 60 is the max number of invocations each minute
n = 10

# Invoke n times the 'increment' operation on a random actor
# To test the concurrency, each invokation is sent on a new thread
threads = []

with open(os.path.join(os.getcwd(), "wsk_config.json"), "r") as f:
    config = json.loads(f.read())
    wsk = OpenWhisk(config["api-host"], config["auth"])

for i in range(n):
    id = random.choice(list(invocations_counter))
    invocations_counter[id] += 1

    t = Thread(target=wsk.invoke, args=['counter', id, 'increment'])
    t.start()

    threads.append(t)

# Wait for thread execution
for t in threads:
    t.join()

# Print expected results
for i in invocations_counter.items():
    print('Actor@{} invoked {} times'.format(i[0], i[1]))

print('\nInvocations count: {}'.format(n))
print('Execution time: ~{} seconds'.format(int(time.time() - start_time)))
