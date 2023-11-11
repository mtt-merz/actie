import json
from lib import Actor


class Operator(Actor):
    def receive(self, msg: str) -> str:
        raw = json.loads(msg)
        name = raw["name"]
        body = raw["body"]

        if name == "init":
            return self.init(body)
        elif name == "create_flight":
            return self.create_flight(body)

    def init(self, body) -> str:
        self.name = body["name"]

        return self.code
    
    def create_flight(self, body) -> str:
        msg = {
            "name": "init",
            "body": {
                "departure": body["departure"],
                "arrival": body["arrival"],
                "plane": body["plane"],
            }
        }