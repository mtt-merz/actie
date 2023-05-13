from os import getcwd
from os.path import join as join_paths
import json
from re import match
from typing import Type, TypeVar

from lib.wsk import OpenWhisk


class Actor:
    id = None

    def __init_subclass__(cls, **kwargs):
        if id == None:
            raise NotImplementedError('You should provide a unique id.')

        cls.name = get_actor_name(cls)
        cls.label = get_actor_label(cls, cls.id)

    def receive(self, msg: str) -> str:
        raise NotImplementedError

    def send(self, id: str,  name: str, msg: str, *args) -> None:
        pattern = r"^\w+(_\w+)*$"
        if (not match(pattern, msg)):
            raise ValueError(
                "Messages should contain lower case, alphanumeric chars or undescores, " +
                "not spaces, upper case or any other special chars.")

        with open(join_paths(getcwd(), "config.json"), "r") as f:
            config = json.loads(f.read())["wsk"]
            wsk = OpenWhisk(config["host"], config["auth"])

        wsk.invoke(name, id, msg)


A = TypeVar("A", bound=Actor)


def get_actor_name(type: Type[A]) -> str:
    return type.__name__.lower()


def get_actor_label(type: Type[A], id: str) -> str:
    return f"{get_actor_name(type)}@{id}"
