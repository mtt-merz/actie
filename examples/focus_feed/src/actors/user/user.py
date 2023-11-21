from lib import Actor, Address


class TopicData:
    def __init__(self, policy: int) -> None:
        self.policy = policy
        self.contents: list[dict] = []


class User(Actor):
    def __init__(self) -> None:
        self.topics: dict[str, TopicData] = {}

    def add_content(self, content: dict) -> str:
        topic = self.sender.name

        self.topics[topic].contents.append(content)

        contents = self.topics[topic].contents
        policy = self.topics[topic].policy
        if len(contents) < policy:
            return f"Topic '{topic}' no aggregation performed: 
            missing {policy - len(contents)} content(s)"

        del self.topics[topic]
        return f"Topic '{topic}' aggregation: {contents}"

    def subscribe(self, topic: str, policy: int = 1) -> str:
        if topic in self.topics:
            return f"Already subscribed to topic '{topic}'"

        self.topics[topic] = TopicData(policy)

        address = Address("topic", topic)
        self.send("add_subscriber", address, {
            "user": self.name,
        })

        return f"Subscribed to topic '{topic}'"

    def unsubscribe(self, topic: str) -> str:
        if topic not in self.topics:
            return f"Not subscribed to topic '{topic}'"

        del self.topics[topic]

        address = Address("topic", topic)
        self.send("remove_subscriber", address, {
            "user": self.name,
        })

        return f"Unsubscribed from topic '{topic}'"

    def set_policy(self, topic: str, policy: int) -> str:
        if topic not in self.topics:
            return f"Not subscribed to topic '{topic}'"

        self.topics[topic].policy = policy

        return f"Policy set for topic '{topic}' to {policy}"
