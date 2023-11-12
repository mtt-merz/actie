from lib import Actor, Address

class User(Actor):
    def __init__(self):
        self.chats = []
        self.groups = []
        self.channels = []

    def init(self, firstName: str, lastName: str) -> str:
        self.name = firstName
        self.surname = lastName

        return f"User {self.name} {self.surname} created"

    def send_message(self, message: str, recipient: Address) -> str:
        if recipient in self.chats:
            self.send("show_message", recipient, message=message)
            return f"Message {message} sent to {recipient}"
        elif recipient in self.groups:
            self.send("show_message", recipient, message=message)
            return f"Message {message} sent to {recipient}"
        elif recipient in self.channels:
            self.send("show_message", recipient, message=message)
            return f"Message {message} sent to {recipient}"
        else:
            return f"User {recipient} not found"