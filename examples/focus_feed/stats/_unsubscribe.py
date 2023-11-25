import time

import requests

from console import Console, Implementation, LogArgs
from logger import Logger


# EXPERIMENT #1
# a user unsubscribe every 2 sec from a different topic, for 1000 times
#
# - log/unsubscribe/BASE__2023-11-25_07-53-54.csv
# - log/unsubscribe/ACTIE__2023-11-25_12-14-22.csv (persist)
# - log/unsubscribe/ACTIE__2023-11-25_12-53-58.csv (no persist)

console = Console(
    name='unsubscribe',
    implementation=Implementation.actie
)

for i in range(500):
    res = console.unsubscribe(
        topic=f"topic{i}",
        user=f"user",
        log_args=LogArgs(
            topics=500,
            users=1,
            articles=0,
            subcriptions=500 - i,
            persist=False
        )
    )

    print(f'{i} -> {res}')
    time.sleep(2)
