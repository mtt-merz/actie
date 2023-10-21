from typing import Type, TypeVar

from lib.wsk import OpenWhiskInterface


class Actor:
    def receive(self, msg: str) -> str:
        raise NotImplementedError()

    is_isolated: bool = False

    def isolate(self) -> None:
        self.is_isolated = True

    def send(self, family: str, name: str, msg: str, *args) -> None:
        if (self.is_isolated):
            return

        self.wsk.invoke(family, name, msg)

    def set_wsk(self, wsk: OpenWhiskInterface):
        self.wsk = wsk


A = TypeVar("A", bound=Actor)


def get_actor_family(type: Type[A]) -> str:
    return type.__name__.lower()


def get_actor_label(type: Type[A], name: str) -> str:
    return f"{get_actor_family(type)}@{name}"
