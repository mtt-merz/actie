from lib import Actor


class __Actor__(Actor):
    def __init__(self, name: str) -> None:
        self.id = name

    def receive(self, msg: str) -> str:
        return super().receive(msg)
