import time

import requests
from console import Console, Implementation, LogArgs
from logger import Logger

# an article is published every 1 sec for 1000 times, in a topic with 100 subscribers
# the articles are lorem ipsum generated and has a length of 1000 bytes
# each subscriber has a fixed policy of 50

# EXPERIMENT #1 -
# db usage notes |  08:29    08:51     |
# -------------------------------------|
# DISK READ:     |  0B       0B        |
# DISK WRITE:    |  1.04MB   KB     |
# memory usage:  |  29.36MB  MB   |
# data sent:     |  4.45MB   0B        |

console = Console(
    name='aggregate',
    implementation=Implementation.base
)

# for i in range(1000):
#     res = console.aggregate(
#         topic=f"topic",
#         user=f"user{i}",
#         log_args=LogArgs(
#             topics=i,
#             users=1,
#             articles=0,
#             subcriptions=1000-i,
#             persist=False
#         )
#     )

#     print(f'{i} -> {res}')
#     time.sleep(2)


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