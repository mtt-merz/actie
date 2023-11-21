from lib import Actor, Address


class User(Actor):
    def __init__(self) -> None:
        self.topics: dict[str, list[dict]] = {}

    def append(self, content: dict, policy: int) -> str:
        topic = self.sender.name

        if topic not in self.topics.keys():
            self.topics[topic] = [content]
        else:
            self.topics[topic].append(content)

        contents = self.topics[topic]
        if len(contents) < policy:
            return f"No aggregation performed: missing {policy - len(contents)} content(s)"

        del self.topics[topic]
        return f"Aggregation: {contents}"
