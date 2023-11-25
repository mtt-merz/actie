import time
from console import Console, Implementation, LogArgs
from logger import Logger

# a user subscribe every 1 sec to a different topic, for 1000 times

# EXPERIMENT #1 - logs/subscribe/BASE__2023-11-25_07-26-07.csv
# db usage notes |  07:20    07:51     |
# -------------------------------------|  
# DISK READ:     |  0B       0B        |
# DISK WRITE:    |  418KB    696KB     |
# memory usage:  |  27.05MB  29.36MB   |

console = Console(
    name='subscribe',
    implementation=Implementation.base
)

for i in range(1000):
    res = console.subscribe(
        topic=f"topic{i}",
        user=f"luigi",
        log_args=LogArgs(
            topics=i,
            users=1,
            articles=0,
            subcriptions=i,
            persist=False
        )
    )

    print(f'{i} -> {res}')
    time.sleep(1)
