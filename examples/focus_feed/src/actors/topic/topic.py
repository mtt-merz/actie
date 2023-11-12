from lib import Actor, Address


class Topic(Actor):
    def __init__(self) -> None:
        self.contents: list[dict] = []
        self.subscribers: list[Address] = []

    def publish(self, content: dict) -> str:
        self.contents.append(content)

        for subscriber in self.subscribers:
            self.send('append', subscriber, {"content": content})

        return f'Contents published: {self.contents}'

    def subscribe(self) -> str:
        self.subscribers.append(self.sender)

        self.reply('join_topic', {"contents": self.contents})
        return f'User {self.sender.name} subscribed'
    
    def unsubscribe(self) -> str:
        self.subscribers.remove(self.sender)

        return f'User {self.sender.name} unsubscribed'