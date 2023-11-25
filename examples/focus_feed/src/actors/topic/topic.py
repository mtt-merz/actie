from lib import Actor, Address


class Topic(Actor):
    def __init__(self) -> None:
        self.articles: list[str] = []
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
        self.subscribers.remove(address)

        return f"User '{user}' unsubscribed"

    def publish(self, article: str) -> str:
        self.articles.append(article)

        # for subscriber in self.subscribers:
        subscriber = Address("user", "user")
        self.send("append", subscriber, {
            "article": article,
        })

        return f"Article '{article}' published"
