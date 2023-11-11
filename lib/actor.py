import json
from typing import Type, TypeVar

from lib.wsk import OpenWhiskInterface


class ActorAddress:
    def __init__(self, family: str, name: str) -> None:
        self.family = family
        self.name = name

        self.label = f"{self.family}@{self.name}"

    def __init__(self, string: str) -> None:
        family, name = string.split("@")
        self.family = family
        self.name = name


class Actor:
    def get_address_label(self):
        ActorAddress = ActorAddress(
            family=self.__class__.__name__.lower(),
            name=self.name,
        ).label

    def receive(self, msg: str) -> str:
        raw: dict = json.loads(msg)

        if "action" not in raw.keys():
            raise ValueError("Missing 'action' field in message")

        action: str = raw.get("action")
        if not hasattr(self, action):
            raise NotImplementedError(f"Action '{action}' not implemented")

        if "sender" in raw.keys():
            self.sender: ActorAddress = ActorAddress(raw.get["sender"])

        execute = getattr(self, action)
        result = execute(**raw.get("args", {}))

        return str(result)

    def send(self, action: str, recipient: ActorAddress,  **kwargs) -> None:
        if self.is_isolated:
            return

        msg = {
            "action": action,
            "sender": self.get_address_label(),
            "args": kwargs,
        }
        self.wsk.invoke(
            recipient.family,
            recipient.name,
            json.dumps(msg),
        )

    def reply(self, action: str, **kwargs) -> None:
        if self.sender is None:
            raise ValueError("Missing sender: cannot reply")

        return self.send(self.sender, action, kwargs)

    is_isolated: bool = False

    def isolate(self) -> None:
        self.is_isolated = True

    def set_wsk(self, wsk: OpenWhiskInterface):
        self.wsk = wsk


A = TypeVar("A", bound=Actor)


def get_actor_family(type: Type[A]) -> str:
    return type.__name__.lower()


def get_actor_label(type: Type[A], name: str) -> str:
    return f"{get_actor_family(type)}@{name}"
