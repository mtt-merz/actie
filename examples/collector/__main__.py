from datetime import datetime
import json
import random
from threading import Thread
import time

from lib import OpenWhisk

# The system is composed by a certain number of sensors, mocked as threads,
# that periodically sends messages to a collector.
#
# Each sensor repeats the following routine:
#  - sleep for a variable time, lower than a threshold
#  - send a message to the collector (position + current state)
#  - sleep again till reaching the threshold
#
# By default OpenWhisk allows a maximum of 60 invocations per minute:
# we suggest a network of 10 sensors and a threshold time of 10 seconds.

sensors_count = 10
period = 10

# with open(os.path.join(os.getcwd(), "config.json"), "r") as f:
#     config = json.loads(f.read())["wsk"]
#     wsk = OpenWhisk(config["host"], config["auth"])

def start_sensor(index: int,
                 period=period, wsk=wsk,
                 random=random, time=time, datetime=datetime) -> None:
    while True:
        random_sleep_time = random.random() * period
        time.sleep(random_sleep_time)

        wsk.invoke('collector', id='collector_0',
                   message=json.dumps({
                       "position": index,
                       "state": random.randint(0, 100),
                   }))

        print(f'[{datetime.now()}] Message sent by {index}')

        time.sleep(period - random_sleep_time)


threads = []

# Start threads
for index in range(sensors_count):
    t = Thread(target=start_sensor, args=[index])
    t.start()

    threads.append(t)

# Wait for thread execution
for t in threads:
    t.join()
