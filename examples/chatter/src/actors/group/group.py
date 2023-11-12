from lib import Actor, Address


class GroupMessage:
    def __init__(self, sender: Address, message: str):
        self.sender = sender
        self.message = message


class Group(Actor):
    def __init__(self):
        self.messages = []
        self.members = []

    def init(self, label: str, members: list[Address]) -> str:
        self.label = label
        self.members = [self.sender, *members]
        self.messages = []

        return f"Group {self.label} created"

    def add_member(self) -> str:
        self.members.append(self.sender)

        return f"Member {self.sender} added to group {self.label}"

    def remove_member(self) -> str:
        self.members.remove(self.sender)

        return f"Member {self.sender} removed from group {self.label}"

    def add_message(self, message: str) -> str:
        group_message = GroupMessage(self.sender, message)
        self.messages.append(group_message)

        for member in self.members:
            self.send("show_message", member,
                      {"message": message, "by": self.sender})

        return f"Message {message} added to group {self.label}"
