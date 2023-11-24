import time
from console import Console, Implementation
from logger import Logger

# a user subscribe every 2 sec to a different topic, for 100 times

console = Console(
    id=2,
    implementation=Implementation.FUNCTIONS
)

for i in range(1000):
    res = console.subscribe(
        topic=f"topic{i}",
        user=f"luigi"
    )
    print(f'Subscribe {i} -> {res}')
