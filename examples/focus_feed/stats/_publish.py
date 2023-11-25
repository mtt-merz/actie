import time

import requests
from console import Console, Implementation, LogArgs
from logger import Logger


# EXPERIMENT #1
# publish an article every 2 sec for 500 times, in a topic with 100 subscribers
# the articles are lorem ipsum generated and has a length of 1000 bytes
# each subscriber has a fixed policy of 50
#
# - publish/BASE__2023-11-25_08-31-18.csv
# - publish/ACTIE__2023-11-25_14-00-58.csv (1->500)(persist)
# - publish/.csv (no persist)

# EXPERIMENT #2
# publish an article every 2 sec for 500 times, each time in a different topic!! 
# with 100 subscribers
# the articles are lorem ipsum generated and has a length of 1000 bytes
# each subscriber has a fixed policy of 50
#
# - publish/BASE__2023-11-25_08-31-18.csv
# - publish/ACTIE__2023-11-25_14-00-58.csv (500->1000)(persist)
# - publish/.csv (no persist)

console = Console(
    name='publish',
    implementation=Implementation.actie
)

for i in range(91, 500):
    res = console.publish(
        topic=f"topic",
        article=f"""ARTICLE:{i}\nLorem ipsum dolor sit amet, consectetur adipiscing elit. Ut vitae sollicitudin ante. Cras eu turpis in lacus pharetra molestie sed vitae libero. Quisque dignissim enim sed augue convallis feugiat. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Phasellus purus mauris, volutpat ac ex quis, vestibulum ornare ante. Nunc sit amet elit efficitur, venenatis justo et, vestibulum lacus. Morbi dui nunc, fringilla vel orci at.
        In in elit pulvinar, sodales eros nec, tincidunt sapien. Praesent in fringilla lacus. Nullam pulvinar vulputate metus et consequat. Nullam suscipit, enim in placerat luctus, lectus orci elementum massa, fringilla consectetur risus eros in elit. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Suspendisse interdum semper iaculis. Morbi tellus tortor, mollis non felis vitae, efficitur feugiat velit. Sed in venenatis augue. Phasellus purus ligula, elementum vel arcu laoreet.""",
        log_args=LogArgs(
            topics=1,
            users=1,
            articles=0,
            subcriptions=1,
            persist=False
        )
    )

    print(f'{i} -> {res}')
    time.sleep(2)


for i in range(500):
    res = console.publish(
        topic=f"topic{i}",
        article=f"""ARTICLE:\nLorem ipsum dolor sit amet, consectetur adipiscing elit. Ut vitae sollicitudin ante. Cras eu turpis in lacus pharetra molestie sed vitae libero. Quisque dignissim enim sed augue convallis feugiat. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Phasellus purus mauris, volutpat ac ex quis, vestibulum ornare ante. Nunc sit amet elit efficitur, venenatis justo et, vestibulum lacus. Morbi dui nunc, fringilla vel orci at.
        In in elit pulvinar, sodales eros nec, tincidunt sapien. Praesent in fringilla lacus. Nullam pulvinar vulputate metus et consequat. Nullam suscipit, enim in placerat luctus, lectus orci elementum massa, fringilla consectetur risus eros in elit. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Suspendisse interdum semper iaculis. Morbi tellus tortor, mollis non felis vitae, efficitur feugiat velit. Sed in venenatis augue. Phasellus purus ligula, elementum vel arcu laoreet.""",
        log_args=LogArgs(
            topics=1,
            users=1,
            articles=0,
            subcriptions=1,
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
