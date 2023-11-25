import time

import requests
from console import Console, Implementation, LogArgs
from logger import Logger

# aggregate with different user policies:
#1 policy = 1000
#2 policy = 100
#3 policy = 1
# for each experiment, repeat the calculation 100 times

# EXPERIMENT #1
# aggregate with user policy=1000
# 
# - aggregate/BASE__2023-11-25_09-54-18.csv
# - aggregate/ACTIE__2023-11-25_16-10-50.csv (persist)
# - aggregate/ACTIE__2023-11-25_16-03-54.csv (no persist)

# EXPERIMENT #2
# aggregate with user policy=100
# 
# - aggregate/BASE__2023-11-25_09-59-31.csv
# - aggregate/ACTIE__2023-11-25_16-15-25.csv (persist)
# - aggregate/ACTIE__2023-11-25_16-18-35.csv (no persist)

# EXPERIMENT #3 
# aggregate with user policy=1
#
# - aggregate/BASE__2023-11-25_10-04-03.csv
# - aggregate/ACTIE__2023-11-25_16-24-01.csv (persist)
# - aggregate/ACTIE__2023-11-25_16-21-28.csv (no persist)

console = Console(
    name='aggregate',
    implementation=Implementation.actie
)

for i in range(100):
    res = console.aggregate(
        topic=f"topic",
        user=f"user",
        log_args=LogArgs(
            topics=1,
            users=1,
            articles=1,
            subcriptions=1,
            persist=True
        )
    )

    print(f'{i} -> {res}')
    time.sleep(1)


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