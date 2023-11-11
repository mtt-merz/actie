import json
from lib import Actor


class Flight(Actor):
    def receive(self, msg: str) -> str:
        raw = json.loads(msg)
        name = raw["name"]
        body = raw["body"]

        if name == "init":
            return self.init(body)
        elif name == "reserve":
            return self.reserve(body)

    def init(self, body) -> str:
        self.departure = body["departure"]
        self.arrival = body["arrival"]
        self.plane = body["plane"]
        self.price = body["price"]

        self.passengers = []

        self.send(
            "airport",
            self.departure,
            {
                "name": "add_flight",
                "sender": {"family": "flight", "name": self.name},
                "body": {
                    "flight": {
                        "departure": self.departure,
                        "arrival": self.arrival,
                        "plane": self.plane,
                        "price": self.price,
                        "status": "available",
                    }
                },
            },
        )

        return self.code

    def reserve(self, body) -> str:
        sender = body["sender"]

        if not self.has_available_seats:
            self.send(
                sender["family"],
                sender["name"],
                {
                    "name": "booking_failed",
                    "body": {
                        "sender": {"family": "flight", "name": self.name},
                        "flight": {
                            "departure": self.departure,
                            "arrival": self.arrival,
                            "plane": self.plane,
                        },
                    },
                },
            )

            return "Flight is full"

        self.passengers.append(sender)
        self.send(
            sender["family"],
            sender["name"],
            {
                "name": "booking_confirmed",
                "body": {
                    "sender": {"family": "flight", "name": self.name},
                    "flight": {
                        "departure": self.departure,
                        "arrival": self.arrival,
                        "plane": self.plane,
                    },
                },
            },
        )

        return "Booking confirmed"

    def has_available_seats(self) -> bool:
        return len(self.passengers) < self.plane["seats"]
