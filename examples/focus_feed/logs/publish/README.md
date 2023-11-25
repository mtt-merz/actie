# EXPERIMENT #1

publish an article always in the same topic

the articles are lorem ipsum generated and has a length of 1000 bytes
every 2 sec for 500 times
with 100 subscribers
each subscriber has a fixed policy of 50

- publish/BASE__2023-11-25_08-31-18.csv
- publish/ACTIE__2023-11-25_14-00-58.csv (1->500)(persist)
- publish/ACTIE__2023-11-25_14-53-23.csv (1->500)(no persist)

# EXPERIMENT #2

publish an article each time in a different topic

the articles are lorem ipsum generated and has a length of 1000 bytes
every 2 sec for 500 times
with 100 subscribers
each subscriber has a fixed policy of 50

- publish/BASE__2023-11-25_08-31-18.csv
- publish/ACTIE__2023-11-25_14-00-58.csv (500->1000)(persist)
- publish/ACTIE__2023-11-25_14-53-23.csv (500->1000)(no persist)