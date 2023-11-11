import json
from lib import Actor, ActorAddress


class Flight(Actor):

    def init(self, departure: str, arrival: str, plane: dict, price: float) -> str:
        self.departure = departure
        self.arrival = arrival
        self.plane = plane
        self.price = price

        self.passengers = []

        self.send("add_flight", ActorAddress("airport", self.departure),  flight={
            "departure": self.departure,
            "arrival": self.arrival,
            "plane": self.plane,
            "price": self.price,
            "status": "available",
        })

        return self.name

    def reserve(self) -> str:
        if not self.has_available_seats:
            self.reply("booking_failed", flight={
                "departure": self.departure,
                "arrival": self.arrival,
                "plane": self.plane,
            })

            return "Flight is full"

        self.passengers.append(self.sender)
        self.reply("booking_confirmed", flight={
            "departure": self.departure,
            "arrival": self.arrival,
            "plane": self.plane,
        })

        return "Booking confirmed"

    def has_available_seats(self) -> bool:
        return len(self.passengers) < self.plane["seats"]
