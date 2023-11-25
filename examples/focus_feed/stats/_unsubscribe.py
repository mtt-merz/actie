import time
from console import Console, Implementation, LogArgs
from logger import Logger

# a user subscribe every 2 sec to a different topic, for 100 times

console = Console(
    name='subscribe',
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
