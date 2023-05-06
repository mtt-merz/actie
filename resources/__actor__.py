from lib import Actor

class __Actor__(Actor):
    def receive(self, msg: str) -> str:
        return super().receive(msg)