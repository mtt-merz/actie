import time

import requests
from console import Console, Implementation, LogArgs
from logger import Logger

# an article is published every 1 sec for 1000 times, in a topic with 100 subscribers
# the articles are lorem ipsum generated and has a length of 1000 bytes
# each subscriber has a fixed policy of 50

# EXPERIMENT #1 -
# db usage notes |  07:53    08:51     |
# -------------------------------------|
# DISK READ:     |  0B       0B        |
# DISK WRITE:    |  KB       KB     |
# memory usage:  |  29.36MB  MB   |

console = Console(
    name='publish',
    implementation=Implementation.base
)

for i in range(1000):
    res = console.publish(
        topic=f"topic",
        article=f"""ARTICLE:{i}\nLorem ipsum dolor sit amet, consectetur adipiscing elit. Ut vitae sollicitudin ante. Cras eu turpis in lacus pharetra molestie sed vitae libero. Quisque dignissim enim sed augue convallis feugiat. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Phasellus purus mauris, volutpat ac ex quis, vestibulum ornare ante. Nunc sit amet elit efficitur, venenatis justo et, vestibulum lacus. Morbi dui nunc, fringilla vel orci at.
        In in elit pulvinar, sodales eros nec, tincidunt sapien. Praesent in fringilla lacus. Nullam pulvinar vulputate metus et consequat. Nullam suscipit, enim in placerat luctus, lectus orci elementum massa, fringilla consectetur risus eros in elit. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Suspendisse interdum semper iaculis. Morbi tellus tortor, mollis non felis vitae, efficitur feugiat velit. Sed in venenatis augue. Phasellus purus ligula, elementum vel arcu laoreet.""",
        log_args=LogArgs(
            topics=i,
            users=1,
            articles=0,
            subcriptions=1000-i,
            persist=False
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