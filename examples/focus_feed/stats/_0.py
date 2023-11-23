import time
from console import Console, Implementation
from logger import Logger

# a user subscribe every 2 sec to a different topic, for 100 times

console = Console(
    id=0,
    implementation=Implementation.ACTORS
)

for i in range(100):
    res = console.subscribe(
        topic=f"topic{i}",
        user=f"luigi"
    )
    print(f'Subscribe {i} -> {res}')

    time.sleep(2)
