import time

import requests
from console import Console, Implementation, LogArgs
from logger import Logger

# aggregate with different user policies:
#1 policy = 1
#2 policy = 10
#3 policy = 100
#4 policy = 1000
# for each experiment, repeat the calculation 20 times

# EXPERIMENT #1 - aggregate/

console = Console(
    name='aggregate',
    implementation=Implementation.base
)

for i in range(1000):
    res = console.aggregate(
        topic=f"topic",
        user=f"user{i}",
        log_args=LogArgs(
            topics=i,
            users=1,
            articles=0,
            subcriptions=1000-i,
            persist=False
        )
    )

    print(f'{i} -> {res}')
    time.sleep(2)


# script to add subscriptions
# for i in range(100):
#     res = requests.post(
#         url=f"http://192.168.1.102:3000/subscriptions",
#         json={
#             "topic": "topic",
#             "user_name": f"user{i}",
#             "user_policy": 50,
#             "last_published": 0
#         }
#     )

#     print(res.content)