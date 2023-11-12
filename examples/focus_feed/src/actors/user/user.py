from lib import Actor, Address


class TopicData:
    def __init__(self, policy: int) -> None:
        self.policy = policy
        self.contents: list[dict] = []


class User(Actor):
    def __init__(self) -> None:
        self.topics: dict[str, TopicData] = {}

    def append(self, content: dict) -> str:
        topic = self.sender.name

        if topic not in self.topics:
            return f'Missing topic "{topic}"'

        self.topics[topic].contents.append(content)
        result = self.__aggregate(topic)

        return f'Content appended to topic "{topic}".\n Aggregation: {result}'

    def append_multiple(self, contents: list[dict]) -> str:
        results = []
        for content in contents:
            result = self.append(content)
            results.append(result)

        return '\n'.join(results)

    def join_topic(self, topic: str, policy: int) -> str:
        if topic in self.topics:
            return f'Topic "{topic}" already joined'

        self.topics[topic] = TopicData(policy)

        address = Address('topic', topic)
        self.send('subscribe', address, {"policy": policy})

        return f'Topic "{topic}" joined'

    def leave_topic(self, topic: str) -> str:
        if topic not in self.topics:
            return f'Missing topic "{topic}"'
        
        del self.topics[topic]

        address = Address('topic', topic)
        self.send('unsubscribe', address)

        return f'Topic "{topic}" left'

    def set_topic_policy(self, topic: str, policy: int) -> str:
        if topic not in self.topics:
            raise Exception(f'Missing topic "{topic}"')

        self.topics[topic].policy = policy

        return f'Policy for topic "{topic}" set to {policy}'

    def __aggregate(self, topic: str) -> list[dict] | None:
        contents = self.topics[topic].contents
        if len(contents) < self.topics[topic].policy:
            return None

        self.topics[topic].contents = []

        return contents
