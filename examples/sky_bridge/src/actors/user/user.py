from lib import Actor


class User(Actor):
    def init(self, name: str) -> str:
        self.name = name
        self.tickets = []

    def booking_confirmed(self, flight: dict) -> str:
        self.tickets.append(flight)

        return f"User {self.name} tickets are: {self.tickets}"
    
    def show_flights(self, flights: list[dict]):
        return flights


## AGGIUNGERE SCONTO SUL PRIMO VOLO