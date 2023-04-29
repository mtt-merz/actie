# actie/actor.py

import re
import subprocess


class Actor:
    def __init__(self, id: str) -> None:
        self.id = id

    def receive(self, msg: str) -> str:
        raise NotImplementedError

    def send(self, msg: str, *args) -> None:
        pattern = r"^\w+(_\w+)*$"
        if (not re.match(pattern, msg)):
            raise ValueError(
                "Messages should contain lower case, alphanumeric chars or undescores, " +
                "not spaces, upper case or any other special chars.")

        subprocess.run([
            "wsk", "action", "invoke", self.__class__.__name__,
            "--result",
            "--param", "actor_id", self.id,
            "--param", "actor_type", self.__class__.__name__,
            "--param", "message", msg
        ], check=True)
