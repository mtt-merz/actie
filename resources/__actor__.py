from lib import Actor


class __Actor__(Actor):
    def __init__(self, id: str) -> None:
        self.id = id

    def receive(self, msg: str) -> str:
        return super().receive(msg)
