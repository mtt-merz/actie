from lib import Actor


class Counter(Actor):
    def __init__(self) -> None:
        self.value = 0

    def increment(self, value: int = 1) -> str:
        old_value = self.value
        self.value += value

        new_value = self.value
        return f'Value incremented from {old_value} to {new_value}'

    def decrement(self, value: int = 1) -> str:
        old_value = self.value
        self.value -= value

        new_value = self.value
        return f'Value decremented from {old_value} to {new_value}'
