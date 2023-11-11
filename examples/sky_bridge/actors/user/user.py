from lib import Actor


class User(Actor):
    def __init__(self) -> None:
        self.name = "Giangiovanni"
        self.tickets = []

    def receive(self, msg: str) -> str:
        name = msg["name"]
        body = msg["body"]

        if name == "booking-confirmed":
            self.tickets.append(body)

        return f"User {self.name} tickets are: {self.tickets}"
