import time
from console import Console, Implementation, LogArgs
from logger import Logger



# EXPERIMENT #1:
# a user subscribe every 2 sec to a different topic, for 500 times 
# (scale the number of topics)
# 
# - logs/subscribe/BASE__2023-11-25_07-26-07.csv (1->500)
# - logs/subscribe/ACTIE__2023-11-25_10-24-34.csv

# EXPERIMENT #2:
# a different user subscribe every 2 sec to a topic, for 500 times 
# (scale the number of topics)
# 
# - logs/subscribe/BASE__2023-11-25_07-26-07.csv (500 -> 1000)
# - logs/

console = Console(
    name='subscribe',
    implementation=Implementation.actie
)

for i in range(500):
    res = console.subscribe(
        topic=f"topic",
        user=f"user{i}",
        log_args=LogArgs(
            topics=1,
            users=i,
            articles=0,
            subcriptions=i,
            persist=False
        )
    )

    print(f'{i} -> {res}')
    time.sleep(2)
