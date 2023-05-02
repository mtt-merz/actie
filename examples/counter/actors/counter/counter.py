from actie import Actor


class Counter(Actor):
    def __init__(self) -> None:
        self.value = 0

    def onMessage(self, msg: str) -> str:
        old_value = self.value

        if msg == 'increment':
            self.value += 1

        elif msg == 'decrement':
            self.value -= 1

        new_value = self.value
        return 'Value updated from {} to {}'.format(old_value, new_value)