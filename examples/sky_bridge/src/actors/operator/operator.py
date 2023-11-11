import json
from lib import Actor, ActorAddress


class Operator(Actor):
    def init(self, name: str) -> str:
        self.name = name

        return f"Operator {self.name} initialized"

    def create_flight(self, code: str, departure: str, arrival: str, plane: dict) -> str:
        self.send("init", ActorAddress("flight", code),
                  departure=departure, arrival=arrival, plane=plane)
        
        return f"Flight {code} created"
