from lib import Actor, Address


class Topic(Actor):
    def __init__(self) -> None:
        self.contents: list[dict] = []
        self.subscribers: list[Address] = []

    def publish(self, content: dict) -> str:
        self.contents.append(content)

        for subscriber in self.subscribers:
            self.send('append', subscriber, {"content": content})

        return f'Content published: {content}'

    def subscribe(self, user: str, policy: int) -> str:
        address = Address('user', user)
        self.subscribers.append(address)

        self.send("append_topic", address,
                  {"policy": policy, "contents": self.contents})

        return f'User {user} subscribed'

    def unsubscribe(self, user: str) -> str:
        address = Address('user', user)
        self.subscribers.remove(address)

        return f'User {user} unsubscribed'
