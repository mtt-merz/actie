names = [
    "subscribe_scale_users.csv",
    "subscribe_scale_topics.csv",
    "unsubscribe.csv",
    "aggregate_policy_1.csv",
    "aggregate_policy_100.csv",
    "aggregate_policy_1000.csv",
    "set_policy.csv",
    "publish_same_topic.csv",
    "publish_different_topics.csv",
]

for file_name in names:
    dataset: list = []
    with open(file_name, "r") as f:
        for line in f.read().splitlines():
            dataset.append(line.split(","))

    for line in dataset:
        del line[0]
        # temp = line[1]
        # line[1] = line[2]
        # line[2] = temp

        # line.insert(0, line.pop())

    with open(file_name, "w") as f:
        for line in dataset:
            f.write(",".join(line) + "\n")
