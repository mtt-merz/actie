import time

import requests

from console import Console, Implementation, LogArgs
from logger import Logger

# a user unsubscribe every 1 sec from a different topic, for 1000 times

# EXPERIMENT #1 - log/unsubscribe/BASE__2023-11-25_07-53-54
# db usage notes |  07:53    08:14     |
# -------------------------------------|
# DISK READ:     |  0B       0B        |
# DISK WRITE:    |  696KB    942KB     |
# memory usage:  |  27.16MB  MB   |

console = Console(
    name='unsubscribe',
    implementation=Implementation.base
)

for i in range(1000):
    res = console.unsubscribe(
        topic=f"topic{i}",
        user=f"luigi",
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
