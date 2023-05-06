from os import getcwd
from os.path import join as join_paths
import json
from re import match

from actie.wsk import OpenWhisk

class Actor:
    def __init__(self, id: str) -> None:
        self.id = id

    def receive(self, msg: str) -> str:
        raise NotImplementedError

    def send(self, id: str,  name: str, msg: str, *args) -> None:
        pattern = r"^\w+(_\w+)*$"
        if (not match(pattern, msg)):
            raise ValueError(
                "Messages should contain lower case, alphanumeric chars or undescores, " +
                "not spaces, upper case or any other special chars.")


        with open(join_paths(getcwd(), "wsk_config.json"), "r") as f:
            config = json.loads(f.read())
            wsk = OpenWhisk(config["api-host"], config["auth"])
        
        wsk.invoke(name, id, msg)

