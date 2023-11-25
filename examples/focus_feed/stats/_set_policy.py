import time

import requests
from console import Console, Implementation, LogArgs
from logger import Logger


# EXPERIMENT #1
# Set the user policy for 500 times, to an increasing number
# 
# - set_policy/BASE__2023-11-25_09-18-18.csv
# - set_policy/ACTIE__2023-11-25_13-17-09.csv (no persist)
# - set_policy/ACTIE__2023-11-25_13-33-50.csv (persist)

console = Console(
    name='set_policy',
    implementation=Implementation.actie
)

for i in range(500):
    res = console.set_policy(
        user=f"luigi",
        topic=f"topic",
        policy=i,
        log_args=LogArgs(
            topics=1,
            users=1,
            articles=0,
            subcriptions=1,
            persist=True
        )
    )

    print(f'{i} -> {res}')
    time.sleep(1)


# script to add subscriptions
# for i in range(1):
#     res = requests.post(
#         url=f"http://192.168.1.102:3000/subscriptions",
#         json={
#             "topic": "topic",
#             "user_name": "luigi",
#             "user_policy": 1,
#             "last_published": 0
#         }
#     )

#     print(res.content)