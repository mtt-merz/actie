from lib import Actor


class Counter(Actor):
    def __init__(self) -> None:
        self.value = 0

    def increment(self) -> str:
        old_value = self.value
        self.value += 1
        # if (self.value < 5):
        #     self.send(self.family, self.name, msg)
        
        new_value = self.value
        return f'Value incremented from {old_value} to {new_value}'

    def decrement(self) -> str:
        old_value = self.value
        self.value -= 1

        new_value = self.value
        return f'Value decremented from {old_value} to {new_value}'