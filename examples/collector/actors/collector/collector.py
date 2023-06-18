import json
from lib.actor import Actor


class Collector(Actor):
    def __init__(self) -> None:
        self.data = {}

    def print_mean(self) -> None:
        data = {}
        for position, states in self.data.items():
            data[position] = sum(states) / len(states)

        self.send("MEAN", "printer", {
            "title": "Mean states",
            "data": json.dumps(data)
        })

    def print_max(self) -> None:
        data = {}
        for position, states in self.data.items():
            data[position] = max(states)

        self.send("MAX", "printer", {
            "title": "Max states",
            "data": json.dumps(data)
        })

    def receive(self, msg: str) -> str:
        try:
            data = json.loads(msg)

            position = data['position']
            state = data['state']
        except:
            return ('Wrong message format:' +
                    '\n\treceived {}'.format(msg) +
                    '\n\texpected: { "position": <POSITION>, "state": <STATE> }')

        if self.data.get(position):
            self.data[position].append(state)
        else:
            self.data[position] = [state]

        self.print_mean()
        self.print_max()

        return str(self.data)
