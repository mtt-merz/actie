from lib import Actor


class User(Actor):
    def __init__(self) -> None:
        self.tickets = []

    def booking_confirmed(self, flight: dict) -> str:
        self.tickets.append(flight)

        return f"User {self.name} tickets are: {self.tickets}"
