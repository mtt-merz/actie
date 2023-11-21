from lib import Actor, Address


class TopicData:
    def __init__(self, policy: int, contents: list[dict]) -> None:
        self.policy = policy
        self.contents = contents


class User(Actor):
    def __init__(self) -> None:
        self.topics: dict[str, TopicData] = {}

    def append(self, content: dict, policy: int) -> str:
        topic = self.sender.name

        if topic not in self.topics.keys():
            self.topics[topic] = TopicData(policy, [content])
        else:
            self.topics[topic].contents.append(content)

        return self.__aggregate(topic)

    def __aggregate(self, topic: str) -> str:
        contents = self.topics[topic].contents
        if len(contents) < self.topics[topic].policy:
            return f"No aggregation performed: missing {self.topics[topic].policy - len(contents)} content(s)"

        self.topics[topic].contents = []

        return f"Aggregation: {contents}"
