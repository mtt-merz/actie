import json
from lib import Actor


class Airport(Actor):
    def __init__(self) -> None:
        self.departures = []
        self.arrivals = []

    def add_flight(self, flight: dict) -> str:
        if flight["departure"] == self.name:
            self.departures.append(flight)

        if flight["arrival"] == self.name:
            self.arrivals.append(flight)

    def get_departing_flights(self) -> str:
        self.reply("get_departing_flights",
                   departures=json.dump(self.departures))

        return self.departures

    def get_arriving_flights(self, body) -> str:
        self.reply("get_arriving_flights",
                   arrivals=json.dump(self.arrivals))

        return self.arrivals

    def find_flights(self, destination: str | None) -> str:
        if destination == None:
            return self.get_departing_flights()

        flights = []
        for flight in self.departures:
            if flight["arrival"] == destination:
                flights.append(flight)

        self.reply("find_flights", flights=json.dump(flights))

        return flights
