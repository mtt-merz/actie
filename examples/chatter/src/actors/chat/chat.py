from lib import Actor, Address


class ChatMessage:
    def __init__(self, sender: Address, message: str):
        self.sender = sender
        self.message = message


class Chat(Actor):
    def __init__(self):
        self.messages = []

    def init(self, recipient: Address) -> str:
        self.members = [self.sender, recipient]

        return f"Chat with {recipient} created"

    def send_message(self, message: str) -> str:
        chat_message = ChatMessage(self.sender, message)
        self.messages.append(chat_message)

        if self.members[0] == self.sender:
            recipient = self.members[1]
        else:
            recipient = self.members[0]

        self.send("show_message", recipient,
                  {"message": message, "by": self.sender})
        
        return f"Message {message} sent to {recipient}"
