import json
from lib import Actor


class Airport(Actor):
    def __init__(self) -> None:
        self.departures = []
        self.arrivals = []


    def receive(self, msg: str) -> str:
        raw = json.loads(msg)
        name = raw["name"]
        body = raw["body"]

        if name == "init":
            return self.init(body)
        elif name == "add_flight":
            return self.reserve(body)
        elif name == "get_departing_flights":
            return self.get_flights(body)
        elif name == "get_arriving_flights":
            return self.get_flights(body)
        elif name == "find_flights":
            return self.find_flights(body)

    def add_flight(self, body) -> str:
        flight = body["flight"]

        if flight["departure"] == self.name:
            self.departures.append(flight)

        if flight["arrival"] == self.name:
            self.arrivals.append(flight)

    def get_departing_flights(self, body) -> str:
        msg = {
            "name": "get_departing_flights",
            "body": {
                "sender": {"family": "airport", "name": self.name},
                "departures": json.dump(self.departures),
            },
        }

        sender = body["sender"]
        self.send(sender["family"], sender["name"], msg)

        return self.departures

    def get_arriving_flights(self, body) -> str:
        msg = {
            "name": "get_arriving_flights",
            "body": {
                "sender": {"family": "airport", "name": self.name},
                "arrivals": json.dump(self.arrivals),
            },
        }

        sender = body["sender"]
        self.send(sender["family"], sender["name"], msg)

        return self.arrivals

    def find_flights(self, body) -> str:
        arrival = body["arrival"]
        if arrival == None:
            return self.get_departing_flights(body)

        flights = []
        for flight in self.departures:
            if flight["arrival"] == arrival:
                flights.append(flight)

        msg = {
            "name": "find_flights",
            "body": {
                "sender": {"family": "airport", "name": self.name},
                "flights": json.dump(flights),
            },
        }

        sender = body["sender"]
        self.send(sender["family"], sender["name"], msg)

        return flights
