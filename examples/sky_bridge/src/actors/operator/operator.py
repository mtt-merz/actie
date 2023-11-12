import json
from lib import Actor, Address


class Operator(Actor):
    def init(self, code: str) -> str:
        self.name = code

        return f"Operator {self.name} initialized"

    def create_flight(self, code: str, departure: str, arrival: str, plane: dict) -> str:
        self.send("init", Address("flight", code),
                  departure=departure, arrival=arrival, plane=plane)

        self.send("add_flight", Address("airport", departure),
                  flight={
                      "code": code,
                      "departure": departure,
                      "arrival": arrival,
                  })
        
        return f"Flight {code} created"
