from lib import Actor, Address


class Channel(Actor):
    def init(self, label: str):
        self.label = label
        self.owner = self.sender
        self.subscribers: list[Address] = []

    def subscribe(self) -> str:
        self.subscribers.append(self.sender)

        return f"Subscriber {self.sender} added to channel {self.label}"

    def unsubscribe(self) -> str:
        self.subscribers.remove(self.sender)

        return f"Subscriber {self.sender} removed from channel {self.label}"

    def publish(self, message: str) -> str:
        for subscriber in self.subscribers:
            self.send("show_message", subscriber, message=message)

        return f"Message {message} published to channel {self.label}"
