from lib import Actor, Address


class Topic(Actor):
    def __init__(self) -> None:
        self.contents: list[dict] = []
        self.subscribers: list[Address] = []

    def add_subscriber(self, user: str) -> str:
        if user in self.subscribers:
            return f"User '{user}' already subscribed"

        address = Address("user", user)
        self.subscribers.append(address)

        return f"User '{user}' subscribed"

    def remove_subscriber(self, user: str) -> str:
        if user not in self.subscribers:
            return f"User '{user}' not subscribed"

        address = Address("user", user)
        self.subscribers.remove (address)

        return f"User '{user}' unsubscribed"

    def publish(self, content: dict) -> str:
        self.contents.append(content)

        for subscriber in self.subscribers:
            self.send("append", subscriber, {
                "content": content,
            })

        return f"Content '{content}' published"
