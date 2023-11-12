from lib import Actor, Address


class TopicData:
    def __init__(self, policy: int, contents: list[dict]) -> None:
        self.policy = policy
        self.contents = contents


class User(Actor):
    def __init__(self) -> None:
        self.topics: dict[str, TopicData] = {}

    def append(self, content: dict) -> str:
        topic = self.sender.name
        self.topics[topic].contents.append(content)

        contents = self.topics[topic].contents
        if len(contents) < self.topics[topic].policy:
            return f'Content appended to topic "{topic}"'

        self.topics[topic].contents = []

        return f'Content appended to topic "{topic}".\n Aggregation: {contents}'

    def add_topic(self, policy: int, contents: list[dict]) -> str:
        topic = self.sender.name
        self.topics[topic] = TopicData(policy, contents)

        return f'Topic "{topic}" joined'

    def remove_topic(self) -> str:
        topic = self.sender.name
        del self.topics[topic]

        return f'Topic "{topic}" left'
