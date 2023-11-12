import json
from lib import Actor


class Airport(Actor):
    def __init__(self) -> None:
        self.flights = []

    def add_flight(self, flight: dict) -> str:

        self.flights.append(flight)

    def get_flights(self) -> str:
        self.reply("get_flights",
                   departures=json.dump(self.flights))

        return self.flights

    def find_flights(self, destination: str) -> str:
        flights = [
            flight for flight in self.flights
            if flight["arrival"] == destination
        ]

        self.reply("show_flights", flights=json.dump(flights))

        return flights
