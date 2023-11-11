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
        raw = json.loads(msg)
        if not hasattr(self, raw["name"]):
            raise NotImplementedError()

        self.sender = ActorAddress(raw["sender"])
        execute = getattr(self, raw["name"])

        return execute(**raw["body"])

    def send(self, recipient: ActorAddress, action: str, **kwargs) -> None:
        if self.is_isolated:
            return

        msg = {
            "name": action,
            "sender": self.get_address_label(),
            "body": kwargs,
        }
        self.wsk.invoke(
            recipient.family,
            recipient.name,
            json.dumps(msg),
        )

    def send_back(self, action: str, **kwargs) -> None:
        return self.send(self.sender["family"], self.sender["name"], action, kwargs)

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
