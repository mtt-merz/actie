from re import match
from typing import Type, TypeVar

from lib.wsk import OpenWhiskInterface


class Actor:
    def receive(self, msg: str) -> str:
        raise NotImplementedError()

    is_isolated: bool = False

    def isolate(self) -> None:
        self.is_isolated = True

    def send(self, id: str,  name: str, msg: str, *args) -> None:
        if (self.is_isolated):
            return

        # pattern = r"^\w+(_\w+)*$"
        # if (not match(pattern, msg)):
        #     raise ValueError(
        #         "Messages should contain lower case, alphanumeric chars or undescores, " +
        #         "not spaces, upper case or any other special chars.")

        self.wsk.invoke(name, id, msg)

    def set_wsk(self, wsk: OpenWhiskInterface):
        self.wsk = wsk


A = TypeVar("A", bound=Actor)


def get_actor_name(type: Type[A]) -> str:
    return type.__name__.lower()


def get_actor_label(type: Type[A], id: str) -> str:
    return f"{get_actor_name(type)}@{id}"
