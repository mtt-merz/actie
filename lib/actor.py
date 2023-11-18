import json

from lib.wsk import OpenWhisk


class Address:
    def __init__(self, family: str, name: str) -> None:
        self.family = family
        self.name = name

    def __str__(self) -> str:
        return f"{self.family}@{self.name}"


def get_address_from_label(label: str) -> Address:
    return Address(*label.split("@"))


class Actor:
    def __init__(self) -> None:
        self.name: str
        self.is_isolated: bool
        self.wsk: OpenWhisk

    @classmethod
    def get_label(cls, name: str) -> str:
        address = Address(
            family=cls.__name__.lower(),
            name=name,
        )

        return str(address)

    def __str__(self) -> str:
        return self.get_label(self.name)

    def receive(self, msg: str) -> str:
        raw: dict = json.loads(msg)

        if "action" not in raw.keys():
            raise ValueError("Missing 'action' field in message")

        action: str = str(raw.get("action"))
        if not hasattr(self, action):
            raise NotImplementedError(f"Action '{action}' not implemented")

        if "sender" in raw.keys():
            self.sender: Address = get_address_from_label(raw["sender"])

        execute = getattr(self, action)
        result = execute(**raw.get("args", {}))

        return str(result)

    def send(self, action: str, recipient: Address,  args: dict = {}) -> None:
        if self.is_isolated:
            return

        self.wsk.invoke_actor(
            family=recipient.family,
            name=recipient.name,
            message={
                "action": action,
                "args": args,
                "sender": str(self),
            },
        )

    def reply(self, action: str, args: dict = {}) -> None:
        if self.sender is None:
            raise ValueError("Missing sender: cannot reply")

        return self.send(action, self.sender, args)
