from lib import Actor


class Counter(Actor):
    def __init__(self, name: str) -> None:
        self.id = name
        self.value = 0

    def receive(self, msg: str) -> str:
        old_value = self.value

        if msg == 'increment':
            self.value += 1
            if (self.value < 5):
                self.send(self.name, self.id, msg)

        elif msg == 'decrement':
            self.value -= 1

        new_value = self.value
        return 'Value updated from {} to {}'.format(old_value, new_value)