from lib import Actor, Address


class Topic(Actor):
    def __init__(self) -> None:
        self.contents: list[dict] = []
        self.subscribers: dict[Address, int] = {}

    def subscribe(self, user: str, policy: int) -> str:
        address = Address("user", user)
        self.subscribers[address] = policy

        return f"User {user} subscribed"

    def unsubscribe(self, user: str) -> str:
        address = Address("user", user)
        del self.subscribers[address]

        return f"User {user} unsubscribed"

    def publish(self, content: dict) -> str:
        self.contents.append(content)

        for subscriber in self.subscribers.keys():
            self.send("append", subscriber, {
                "content": content,
                "policy": self.subscribers[subscriber]
            })

        return f"Content published: {content}"
